#!/usr/bin/env python3
"""Offline render probe: measures what static text scanning cannot.

Uses the locally installed Playwright + its bundled Chromium over file://, so it
needs no network and no dev server. It answers the questions that only computed
style and geometry can answer: contrast, touch-target size, horizontal overflow,
heading jumps, focus indication, missing alt/label.

Usage:
    python scripts/render_probe.py <file.html> [...] [--json] [--widths 320,375,768]
                                  [--strict]
Exit: 0 clean, 1 hard findings, 2 bad invocation / browser unavailable / nothing
to probe. An unfinished load is a warning (offline environment), never a design defect,
and is never silently skipped.
"""

import argparse
import json
import sys
from pathlib import Path

KNOWN = {"--json", "--strict", "--widths", "--timeout"}
JS_CONTRAST = r"""
() => {
  const lum = (r,g,b) => {
    const f = c => { c /= 255; return c <= 0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); };
    return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b);
  };
  const parse = (s) => {
    const m = (s||'').match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(parseFloat);
    const a = p.length > 3 ? p[3] : 1;
    return {r:p[0], g:p[1], b:p[2], a:a};
  };
  const bgOf = (el) => {
    let c = el, gradient = false;
    while (c && c !== document.documentElement) {
      const st = getComputedStyle(c);
      if (/linear-gradient|radial-gradient|conic-gradient|url\(/i.test(st.backgroundImage)) gradient = true;
      const col = parse(st.backgroundColor);
      if (col && col.a > 0.85) return {col: col, gradient: gradient};
      c = c.parentElement;
    }
    return {col: {r:255,g:255,b:255,a:1}, gradient: gradient};
  };
  const sel = [];
  document.querySelectorAll('body *').forEach(el => {
    const own = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) return;
    const st = getComputedStyle(el);
    if (st.visibility === 'hidden' || st.display === 'none' || parseFloat(st.opacity) < 0.1) return;
    const rect = el.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) return;
    const fg = parse(st.color) || {r:0,g:0,b:0,a:1};
    const B = bgOf(el);
    if (B.gradient) return;   // backdrop is an image/gradient: unmeasurable, never guessed
    const bg = B.col;
    const mix = (f, b) => {
      const a = f.a;
      return {r: f.r*a + b.r*(1-a), g: f.g*a + b.g*(1-a), b: f.b*a + b.b*(1-a)};
    };
    const F = mix(fg, bg);
    const L1 = lum(F.r,F.g,F.b), L2 = lum(bg.r,bg.g,bg.b);
    const ratio = (Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);
    const size = parseFloat(st.fontSize);
    const weight = parseInt(st.fontWeight, 10) || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    sel.push({tag: el.tagName.toLowerCase(), cls: el.className && String(el.className).slice(0,40),
              ratio: Math.round(ratio*100)/100, need: large ? 3.0 : 4.5,
              size: size, text: el.textContent.trim().slice(0,28)});
  });
  return sel.filter(x => x.ratio < x.need);
}
"""

JS_GEOMETRY = r"""
() => {
  const out = {overflow: null, headings: [], touch: [], noAlt: [], noLabel: [], focus: []};
  const de = document.scrollingElement || document.documentElement;
  if (de.scrollWidth > window.innerWidth + 1) {
    out.overflow = {scrollWidth: de.scrollWidth, viewport: window.innerWidth};
  }
  let prev = 0;
  document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => {
    const lvl = parseInt(h.tagName[1], 10);
    if (prev && lvl > prev + 1) out.headings.push({from: 'h'+prev, to: h.tagName.toLowerCase(),
                                                   text: h.textContent.trim().slice(0,24)});
    prev = lvl;
  });
  document.querySelectorAll('a,button,input,select,textarea,[role=button]').forEach(el => {
    const st = getComputedStyle(el);
    if (st.display === 'inline' && el.tagName === 'A') return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    if (r.width < 44 || r.height < 44) out.touch.push({tag: el.tagName.toLowerCase(),
        w: Math.round(r.width), h: Math.round(r.height),
        text: (el.textContent || el.value || el.getAttribute('aria-label') || '').trim().slice(0,20)});
  });
  document.querySelectorAll('img').forEach(im => {
    if (im.getAttribute('alt') === null) out.noAlt.push({src: (im.currentSrc||im.src||'').slice(-40)});
  });
  document.querySelectorAll('input,select,textarea').forEach(el => {
    const id = el.getAttribute('id');
    const lab = id && document.querySelector('label[for="'+id+'"]');
    if (!lab && !el.getAttribute('aria-label') && !el.getAttribute('aria-labelledby')
        && !el.closest('label') && !el.title) {
      out.noLabel.push({tag: el.tagName.toLowerCase(), type: el.getAttribute('type') || '',
                        name: el.getAttribute('name') || ''});
    }
  });
  return out;
}
"""

JS_FOCUS = r"""
() => {
  const rows = [];
  document.querySelectorAll('a,button,input,select,textarea,[tabindex]:not([tabindex="-1"])').forEach(el => {
    const before = getComputedStyle(el);
    const b = [before.outlineStyle, before.outlineWidth, before.boxShadow].join('|');
    el.focus();
    const after = getComputedStyle(el);
    const a = [after.outlineStyle, after.outlineWidth, after.boxShadow].join('|');
    if (a === b && after.outlineStyle === 'none' && after.boxShadow === 'none') {
      rows.push({tag: el.tagName.toLowerCase(),
                 text: (el.textContent || '').trim().slice(0, 20)});
    }
    el.blur();
  });
  return rows;
}
"""


class ProbeError(Exception):
    pass


def load_playwright():
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
        return sync_playwright
    except Exception as exc:
        raise ProbeError("需要本机 Playwright（当前不可用）：%s" % exc)


def probe_file(path, widths, timeout_ms):
    sync_playwright = load_playwright()
    findings = []
    url = path.resolve().as_uri()
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch()
        except Exception as exc:
            raise ProbeError("Chromium 启动失败：%s" % exc)
        try:
            for width in widths:
                page = browser.new_page(viewport={"width": width, "height": 900})
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
                    page.wait_for_timeout(300)  # let inline layout settle
                except Exception as exc:
                    # an unfinished load here means remote assets are unreachable offline;
                    # that is an environment gap, not a design defect — never a hard FAIL
                    findings.append(mk(path, "load-timeout-offline", "warn",
                                       "%s（离线环境外链未加载完，几何结论不完整）" % str(exc)[:60],
                                       "-", "需联网复测"))
                    page.close()
                    continue
                geo = page.evaluate(JS_GEOMETRY)
                if geo["overflow"]:
                    findings.append(mk(path, "h-scroll-at-%dpx" % width, "hard",
                                       "scrollWidth=%s viewport=%s" % (geo["overflow"]["scrollWidth"],
                                                                       geo["overflow"]["viewport"]),
                                       "<= viewport", "横向滚动（V33/V36）"))
                for h in geo["headings"]:
                    findings.append(mk(path, "heading-jump", "warn",
                                       "%s -> %s（%s）" % (h["from"], h["to"], h["text"]),
                                       "逐级", "标题层级跳号"))
                for t in geo["touch"]:
                    findings.append(mk(path, "touch-target-small", "warn",
                                       "%s %dx%d（%s）" % (t["tag"], t["w"], t["h"], t["text"]),
                                       "44x44", "触摸目标小于 44x44"))
                for a in geo["noAlt"]:
                    findings.append(mk(path, "img-missing-alt", "hard", a["src"], "有 alt",
                                       "img 缺 alt"))
                for l in geo["noLabel"]:
                    findings.append(mk(path, "input-missing-label", "hard",
                                       "%s type=%s name=%s" % (l["tag"], l["type"], l["name"]),
                                       "有标签", "表单控件无可关联标签"))
                if width == widths[0]:
                    for c in page.evaluate(JS_CONTRAST):
                        findings.append(mk(path, "text-contrast-below-threshold", "hard",
                                           "%s.%s ratio=%.2f need=%.1f（%s）" % (
                                               c["tag"], c["cls"], c["ratio"], c["need"], c["text"]),
                                           "%.1f" % c["need"], "文字对比度不达标（WCAG 2.x 相对亮度）"))
                    for f in page.evaluate(JS_FOCUS):
                        findings.append(mk(path, "focus-indication-missing", "warn",
                                           "%s（%s）" % (f["tag"], f["text"]), "-",
                                           "聚焦后 outline/阴影无变化（headless 下 :focus-visible 可能与真实键盘不同）"))
                page.close()
        finally:
            browser.close()
    return findings


def mk(path, rule, severity, measured, threshold, message):
    return {"file": str(path), "rule": rule, "severity": severity,
            "measured": measured, "threshold": threshold, "message": message}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    for a in argv:
        if a.startswith("-") and a.split("=")[0] not in KNOWN:
            sys.stderr.write("ERROR  未知参数 %r（可用：%s）\n" % (a, ", ".join(sorted(KNOWN))))
            return 2
    ap = argparse.ArgumentParser(prog="render_probe.py", add_help=False, allow_abbrev=False)
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--widths", default="375,1440")
    ap.add_argument("--timeout", type=int, default=15000)
    ns = ap.parse_args(argv)

    try:
        widths = [int(w) for w in ns.widths.split(",") if w.strip()]
        if not widths:
            raise ValueError("empty widths")
        files = []
        for a in ns.paths:
            p = Path(a)
            if p.is_dir():
                files += [f for f in sorted(p.rglob("*.html")) if "node_modules" not in f.parts]
            elif p.is_file():
                files.append(p)
            else:
                raise ProbeError("no such path: %s" % a)
        if not files:
            raise ProbeError("没有可渲染的 html —— 空扫描不等于通过")
    except (ProbeError, ValueError) as exc:
        sys.stderr.write("ERROR  %s\n" % exc)
        return 2

    try:
        all_findings = []
        for f in files:
            all_findings += probe_file(f, widths, ns.timeout)
    except ProbeError as exc:
        sys.stderr.write("ERROR  %s\n" % exc)
        return 2

    seen = set()
    deduped = []
    for x in sorted(all_findings, key=lambda y: (y["file"], y["rule"], y["measured"])):
        key = (x["file"], x["rule"], x["measured"])
        if key in seen:
            continue  # the same defect seen at two viewports is one defect
        seen.add(key)
        deduped.append(x)
    all_findings = deduped
    hard = [x for x in all_findings if x["severity"] == "hard"]
    warn = [x for x in all_findings if x["severity"] == "warn"]

    if ns.json:
        print(json.dumps({"probed": len(files), "widths": widths,
                          "hard": hard, "warn": warn}, ensure_ascii=False, indent=2))
    else:
        for x in hard:
            print("FAIL  %-32s %s  %s (measured %s / threshold %s)"
                  % (x["rule"], Path(x["file"]).name, x["message"], x["measured"], x["threshold"]))
        for x in warn:
            print("WARN  %-32s %s  %s (%s)" % (x["rule"], Path(x["file"]).name, x["message"], x["measured"]))
        print("-" * 72)
        print("probed=%d widths=%s hard=%d warn=%d" % (len(files), widths, len(hard), len(warn)))
        print("RESULT: FAIL" if hard or (ns.strict and warn) else "RESULT: PASS")
    return 1 if (hard or (ns.strict and warn)) else 0


if __name__ == "__main__":
    sys.exit(main())
