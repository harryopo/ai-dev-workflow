#!/usr/bin/env python3
"""Static anti-slop scanner for generated UI code (stdlib only).

Rules live in rules/slop-table.json; this file is a generic runner plus the
named measurements. Design contract, learned the hard way:

* comments are masked before matching, so the skill's own examples and the
  fixture's explanatory comments can never count as violations;
* anything unmeasurable (var(), calc(), relative units) is SKIPPED, never guessed;
* a scan that examined zero files exits 2 — an empty scan is not a clean verdict;
* every finding carries the measured number and the threshold, not a vibe.

Usage:
    python scripts/slop_scan.py <file-or-dir> [...] [--json] [--strict]
                               [--allow RULE_ID=reason] [--rules PATH]
Exit: 0 clean, 1 findings, 2 bad invocation / nothing to scan.
"""

import argparse
import json
import re
import sys
from pathlib import Path

GENERIC_FONTS = {"sans-serif", "serif", "monospace", "system-ui", "ui-monospace",
                 "-apple-system", "blinkmacsystemfont", "segoe ui", "inherit", "initial"}
DEMO_HINT = re.compile(r"(?i)\b(demo|example|bad-?|before|after|anti-?pattern|slop-?|preview|showcase)\b")
CSS_URL = re.compile(r"(?i)url\((?!\s*['\"]?data:)")
IGNORE_TOKEN = "slop-scan-ignore"


class ScanError(Exception):
    pass


# ---------------------------------------------------------------- parsing ----

def _blank_keep_lines(match):
    """Blank a comment body but keep its newlines, or every later line number shifts."""
    return re.sub(r"[^\n]", " ", match.group())


def mask_comments(lines, lang):
    """Blank out comment bodies, keeping line count and column offsets."""
    out = list(lines)
    if lang == "css":
        joined = "\n".join(out)
        joined = re.sub(r"/\*.*?\*/", _blank_keep_lines, joined, flags=re.S)
        out = joined.split("\n")
    else:
        joined = "\n".join(out)
        joined = re.sub(r"/\*.*?\*/", _blank_keep_lines, joined, flags=re.S)
        joined = re.sub(r"<!--.*?-->", _blank_keep_lines, joined, flags=re.S)
        joined = re.sub(r"(?m)^\s*//.*$", _blank_keep_lines, joined)
        out = joined.split("\n")
    return out


def read_lines(path):
    return path.read_bytes().decode("utf-8", errors="replace").split("\n")


def split_views(lines, is_css_file):
    """Return (css_lines, html_lines) as [(original_line_no, text)]."""
    css, html = [], []
    in_style = False
    for i, text in enumerate(lines, 1):
        low = text.lower()
        if not in_style and re.search(r"(?i)<style\b", low):
            in_style = True
        if in_style:
            body = re.sub(r"(?i)^\s*.*?<style[^>]*>", "", text)
            body = re.sub(r"(?i)</style>.*$", "", body)
            css.append((i, body))
            if re.search(r"(?i)</style>", low):
                in_style = False
            continue
        stripped = re.sub(r"(?i)<script\b.*?</script>", " ", text)
        stripped = re.sub(r"(?i)<style\b.*?</style>", " ", stripped)
        html.append((i, stripped))
    if is_css_file:
        css, html = list(enumerate(lines, 1)), []
    return css, html


def css_blocks(css_pairs):
    """Group declarations into selector blocks with the block's starting line.

    Multi-line declarations are joined so patterns like `background:\n  linear-gradient`
    still match — per-line matching alone silently misses them.
    """
    blocks, cur_sel, cur_start, cur_body = [], None, None, []
    for lineno, raw in css_pairs:
        parts = re.split(r"[{};]", raw)
        rest = raw
        while True:
            if cur_sel is None:
                m = re.match(r"\s*([^{}]+?)\s*\{\s*(.*)$", rest, flags=re.S)
                if m:
                    cur_sel, rest = m.group(1), m.group(2)
                    cur_start = lineno
                elif rest.strip().startswith("@"):
                    blocks.append((lineno, rest.strip(), None))
                    rest = ""
                else:
                    rest = ""
            else:
                if "}" in rest:
                    head, _, tail = rest.partition("}")
                    cur_body.append(head)
                    blocks.append((cur_start, cur_sel, " ".join(cur_body).strip()))
                    cur_sel, cur_body, rest = None, [], tail
                else:
                    cur_body.append(rest)
                    rest = ""
            if not rest:
                break
    if cur_sel is not None:
        blocks.append((cur_start, cur_sel, " ".join(cur_body).strip()))
    return [(n, s, b) for (n, s, b) in blocks if s is not None or b]


# ------------------------------------------------------------- measuring ----

def _decl(block, prop):
    m = re.search(r"(?i)(?:^|[;\s])%s\s*:\s*([^;]+)" % re.escape(prop), block or "")
    return m.group(1).strip() if m else None


def _unmeasurable(value):
    return value is None or "var(" in value or "calc(" in value or "attr(" in value


def distinct_font_families(blocks, threshold):
    fams = {}
    for lineno, sel, body in blocks:
        value = _decl(body, "font-family") if body else None
        if value is None and sel and sel.startswith("--"):
            value = _decl(sel + ";" + (body or ""), "font-family")
        if _unmeasurable(value):
            continue
        first = value.split(",")[0].strip().strip("\"'").lower()
        if first and first not in GENERIC_FONTS:
            fams.setdefault(first, lineno)
    if len(fams) > threshold:
        line_no = min(fams.values())
        return [("distinct=%d families: %s" % (len(fams), ", ".join(sorted(fams))), line_no)]
    return []


def bare_hex_outside_root(blocks, threshold):
    count = 0
    sample = None
    for lineno, sel, body in blocks:
        if sel and sel.strip() == ":root":
            continue
        for m in re.finditer(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b",
                             (sel or "") + " " + (body or "")):
            count += 1
            sample = sample or (lineno, m.group())
    if count > threshold:
        return [(":%d %s ... 共 %d 个" % (sample[0], sample[1], count), sample[0])]
    return []


def spacing_not_multiple_of_4(blocks, threshold):
    bad = []
    for lineno, sel, body in blocks:
        for prop in ("padding", "margin", "gap", "row-gap", "column-gap"):
            value = _decl(body or "", prop)
            if _unmeasurable(value):
                continue
            for m in re.finditer(r"(?<![\d.])(\d+(?:\.\d+)?)px", value):
                px = float(m.group(1))
                if px and px % 4 != 0:
                    bad.append((":%d %s: %s -> %spx 非 4 倍数" % (lineno, prop, value, m.group(1)), lineno))
    return bad if len(bad) > threshold else []


def reduced_motion_missing(css_text, blocks, threshold):
    has_motion = bool(re.search(r"(?i)@keyframes|transition\s*:|animation\s*:", css_text))
    if has_motion and "prefers-reduced-motion" not in css_text:
        return [("css 有动效但全文件缺 prefers-reduced-motion", 1)]
    return []


def italic_on_heading_rule(blocks, threshold):
    out = []
    for lineno, sel, body in blocks:
        if not sel or not re.search(r"(?i)(?:^|[\s,>+~])h[1-6]\b", sel):
            continue
        if re.search(r"(?i)font-style\s*:\s*italic", body or ""):
            out.append(("selector %s 用 italic" % sel.strip()[:40], lineno))
    return out


def transition_on_layout_props(blocks, threshold):
    out = []
    for lineno, sel, body in blocks:
        value = _decl(body or "", "transition")
        if _unmeasurable(value):
            continue
        props = re.findall(r"(?i)\b(width|height|margin|padding|top|left|right|bottom|font-size)\b", value)
        if props:
            out.append(("selector %s 过渡了 %s" % ((sel or "").strip()[:32], ",".join(sorted(set(props)))), lineno))
    return out


def backdrop_filter_count(css_text, blocks, threshold):
    n = len(re.findall(r"(?i)backdrop-filter\s*:", css_text))
    return [("出现 %d 次" % n, 1)] if n > threshold else []


def prose_max_width_out_of_range(blocks, threshold):
    out = []
    key = re.compile(r"(?i)prose|article|body|\btext\b|measure|lede|content|copy|post")
    for lineno, sel, body in blocks:
        if not sel or not key.search(sel):
            continue
        value = _decl(body or "", "max-width")
        if _unmeasurable(value) or "ch" not in value:
            continue
        m = re.search(r"(\d+(?:\.\d+)?)ch", value)
        if not m:
            continue
        ch = float(m.group(1))
        if not (45 <= ch <= 75):
            out.append(("selector %s max-width=%sch（应 45-75ch）" % (sel.strip()[:32], m.group(1)), lineno))
    return out


INTERACTIVE_BASE = re.compile(
    r"(?i)(?:^|[\s,>])(button|a)\b|\b(?:btn|button|cta|link|tab|chip|pill|submit|input|select|textarea)\b")


def interactive_states_incomplete(blocks, threshold):
    """Require a visible keyboard focus style on things that are actually controls.

    Scope is limited to control-looking selectors: demanding :disabled on a content
    block is not a real defect and just trains people to ignore the gate.
    """
    seen = {}
    for lineno, sel, body in blocks:
        if not sel or sel.strip().startswith("@"):
            continue
        if not re.search(r"::?(?:hover|focus-visible|focus|active)", sel):
            continue
        base = re.split(r"::?(?:hover|focus-visible|focus|active)", sel)[0].strip()
        if not base or not INTERACTIVE_BASE.search(base):
            continue
        info = seen.setdefault(base, {"states": set(), "line": lineno})
        for s in ("hover", "focus-visible", "focus", "active"):
            if re.search(r"::?" + s + r"\b", sel):
                info["states"].add(s)
    out = []
    for base, info in sorted(seen.items()):
        if not ({"focus-visible", "focus"} & info["states"]):
            out.append(("控件 %s 有 hover 但缺 :focus-visible 焦点样式" % base[:40], info["line"]))
    return out


def svg_without_accessible_name(html_text, threshold):
    """Flag svg whose own tag, ancestors, and ancestor text give it no name.

    Window heuristics were tried first and wrong both ways: text from a later
    sibling section waived a bare decorative svg, while an icon inside a labelled
    button was flagged. So ancestry is parsed with html.parser and text is counted
    per ancestor, excluding text inside the svg itself.
    """
    from html.parser import HTMLParser

    VOID = {"br", "img", "input", "hr", "meta", "link", "source", "area", "base", "col"}

    class Walk(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self, convert_charrefs=True)
            self.stack = []          # [{tag, attrs, text, line}]
            self.records = []
            self.in_svg = 0
            self.svg_depth = 0

        def handle_starttag(self, tag, attrs):
            d = dict(attrs)
            if tag == "svg":
                self.records.append({
                    "line": self.getpos()[0],
                    "attrs": d,
                    "parents": [dict(p) for p in self.stack],
                })
                self.in_svg += 1
                self.stack.append({"tag": tag, "attrs": d, "text": 0, "line": self.getpos()[0]})
                return
            if tag in VOID:
                return
            self.stack.append({"tag": tag, "attrs": d, "text": 0, "line": self.getpos()[0]})

        def handle_endtag(self, tag):
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i]["tag"] == tag:
                    if tag == "svg":
                        self.in_svg = max(0, self.in_svg - 1)
                    del self.stack[i:]
                    return

        def handle_data(self, data):
            if self.in_svg:
                return
            if data.strip():
                for frame in self.stack:
                    frame["text"] += len(data.strip())

    w = Walk()
    try:
        w.feed(html_text)
        w.close()
    except Exception:
        return []  # unparseable markup is not evidence of a violation

    out = []
    for rec in w.records:
        attrs = rec["attrs"]
        joined = " ".join('%s="%s"' % (k, v) for k, v in attrs.items() if v is not None)
        if re.search(r"(?i)aria-hidden\s*=\s*[\"']?true", joined):
            continue
        if re.search(r"(?i)aria-(?:label|labelledby)\s*=|role\s*=\s*[\"']img[\"']", joined):
            continue
        named_ancestor = any(
            re.search(r"(?i)aria-(?:label|labelledby)\s*=",
                      " ".join('%s="%s"' % (k, v) for k, v in p["attrs"].items() if v is not None))
            for p in rec["parents"])
        if named_ancestor:
            continue
        # only the icon's own container counts as label context; text anywhere under
        # <body> would waive every svg on the page
        local = [p for p in rec["parents"] if p["tag"] not in ("html", "body")]
        if any(p["text"] for p in local):
            continue
        out.append(("svg 自身无 aria-hidden/可访问名，祖先既无 aria-label 也无文字", rec["line"]))
    return out


def video_autoplay_not_muted(html_text, threshold):
    out = []
    for m in re.finditer(r"(?is)<video\b[^>]*>", html_text):
        tag = m.group()
        if re.search(r"(?i)\bautoplay\b", tag) and not re.search(r"(?i)\bmuted\b", tag):
            out.append(("<video autoplay 未 muted>", html_text[:m.start()].count("\n") + 1))
    return out


def hero_img_lazy_loaded(html_text, threshold):
    imgs = list(re.finditer(r"(?is)<img\b[^>]*>", html_text))
    out = []
    for idx, m in enumerate(imgs):
        tag = m.group()
        if not re.search(r"(?i)loading\s*=\s*[\"']lazy[\"']", tag):
            continue
        is_hero = re.search(r"(?i)(?:class|id|src|alt)\s*=\s*[\"'][^\"']*(?:hero|cover|banner)", tag)
        if is_hero or idx == 0:
            why = "首屏第一张图" if (idx == 0 and not is_hero) else "hero/cover 图"
            out.append(("%s 用了 loading=lazy" % why, html_text[:m.start()].count("\n") + 1))
    return out


def numbered_eyebrow_count(html_text, threshold):
    n = len(re.findall(r">\s*\d{1,2}\s*/\s*[A-Z][A-Z0-9 &_-]{2,24}<", html_text))
    return [("检测到 %d 个 01 / XXX 式 eyebrow" % n, 1)] if n > threshold else []


BANNED_FONTS = ("inter", "roboto", "open sans", "poppins", "lato")
DISPLAY_CTX = re.compile(r"(?i)(?:^|[\s,>+~])h[1-6]\b|display|heading|hero|title")


def banned_display_font_used(blocks, threshold):
    out = []
    for lineno, sel, body in blocks:
        value = _decl(body or "", "font-family")
        where = " ".join(x for x in (sel, body) if x)
        if value is None and sel and sel.strip().startswith("--"):
            value = sel.split(":", 1)[1] if ":" in sel else None
            where = sel
        if _unmeasurable(value):
            continue
        first = value.split(",")[0].strip().strip("\"'").lower()
        if first in BANNED_FONTS and DISPLAY_CTX.search(where):
            out.append(("selector %s 的 display 字体 = %s" % ((sel or "").strip()[:36], first), lineno))
    return out


def bare_1fr_track(blocks, threshold):
    out, seen = [], set()
    for lineno, sel, body in blocks:
        value = _decl(body or "", "grid-template-columns")
        if _unmeasurable(value):
            continue
        stripped = re.sub(r"(?i)minmax\([^)]*\)", " ", value)
        if re.search(r"(?<![\w-])1fr\b", stripped):
            key = (sel or "").strip()
            if key in seen:
                continue  # the same grid repeated across media queries is one defect
            seen.add(key)
            out.append(("grid-template-columns: %s 含裸 1fr 轨道" % value.strip()[:44], lineno))
    return out


MEASURES = {
    "distinct_font_families": lambda ctx, r: distinct_font_families(ctx["blocks"], r["threshold"]),
    "bare_hex_outside_root": lambda ctx, r: bare_hex_outside_root(ctx["blocks"], r["threshold"]),
    "spacing_not_multiple_of_4": lambda ctx, r: spacing_not_multiple_of_4(ctx["blocks"], r["threshold"]),
    "reduced_motion_missing": lambda ctx, r: reduced_motion_missing(ctx["css_text"], ctx["blocks"], r["threshold"]),
    "italic_on_heading_rule": lambda ctx, r: italic_on_heading_rule(ctx["blocks"], r["threshold"]),
    "transition_on_layout_props": lambda ctx, r: transition_on_layout_props(ctx["blocks"], r["threshold"]),
    "backdrop_filter_count": lambda ctx, r: backdrop_filter_count(ctx["css_text"], ctx["blocks"], r["threshold"]),
    "prose_max_width_out_of_range": lambda ctx, r: prose_max_width_out_of_range(ctx["blocks"], r["threshold"]),
    "interactive_states_incomplete": lambda ctx, r: interactive_states_incomplete(ctx["blocks"], r["threshold"]),
    "svg_without_accessible_name": lambda ctx, r: svg_without_accessible_name(ctx["html_text"], r["threshold"]),
    "video_autoplay_not_muted": lambda ctx, r: video_autoplay_not_muted(ctx["html_text"], r["threshold"]),
    "hero_img_lazy_loaded": lambda ctx, r: hero_img_lazy_loaded(ctx["html_text"], r["threshold"]),
    "numbered_eyebrow_count": lambda ctx, r: numbered_eyebrow_count(ctx["html_text"], r["threshold"]),
    "banned_display_font_used": lambda ctx, r: banned_display_font_used(ctx["blocks"], r["threshold"]),
    "bare_1fr_track": lambda ctx, r: bare_1fr_track(ctx["blocks"], r["threshold"]),
}


# ---------------------------------------------------------------- scanning ----

def load_rules(path):
    data = json.loads(path.read_bytes().decode("utf-8"))
    ids = [r["id"] for r in data["rules"]]
    if len(ids) != len(set(ids)):
        raise ScanError("duplicate rule id in %s" % path)
    for rule in data["rules"]:
        if rule["kind"] == "regex":
            re.compile(rule["pattern"])
        elif rule["kind"] == "measure":
            if rule["fn"] not in MEASURES:
                raise ScanError("unknown measure fn %r in rule %r" % (rule["fn"], rule["id"]))
        else:
            raise ScanError("unknown rule kind %r in %s" % (rule["kind"], rule["id"]))
    return data


def collect_ignores(lines):
    """Parse `slop-scan-ignore <id>[,<id>]: reason` directives.

    A bare ignore without a stated reason is itself reported — an escape hatch
    nobody has to justify becomes the way rules die.
    """
    ignore = {}
    bad = []
    for i, text in enumerate(lines, 1):
        if IGNORE_TOKEN not in text:
            continue
        m = re.search(re.escape(IGNORE_TOKEN) + r"\s+([\w-]+(?:\s*,\s*[\w-]+)*)\s*:\s*(.+)", text)
        if m:
            for rid in re.split(r"\s*,\s*", m.group(1)):
                ignore.setdefault(i, set()).add(rid)
                ignore.setdefault(i - 1, set()).add(rid)
        else:
            bad.append(i)
    return ignore, bad


def scan_file(path, rules_data, cli_allow):
    lines = read_lines(path)
    is_css = path.suffix.lower() == ".css"
    raw_masked = mask_comments(lines, "css" if is_css else "html")
    ignore, bad_ignore = collect_ignores(lines)

    rules = rules_data["rules"]
    ids = {r["id"] for r in rules}
    findings = []

    for lineno in bad_ignore:
        findings.append(mk(path, lineno, "ignore-without-reason", "hard",
                          "豁免必须写明规则号与理由", "-",
                          "%s <rule-id>: <理由>" % IGNORE_TOKEN, "slop_scan 契约"))

    for lineno, text in enumerate(raw_masked, 1):
        if not text.strip() or DEMO_HINT.search(text):
            continue
        for rule in rules:
            if rule["kind"] != "regex":
                continue
            if rule["scope"] == "css" and is_css is False and not in_css_region(lineno, lines):
                continue
            if rule["scope"] == "html" and is_css:
                continue
            m = re.search(rule["pattern"], text, re.IGNORECASE)
            if m and rule["id"] not in ignore.get(lineno, set()):
                findings.append(mk(path, lineno, rule["id"], rule["severity"],
                                   m.group()[:70], "-", rule["message"], rule["source"]))

    blocks, css_text, html_text = build_views(raw_masked, lines, is_css)
    ctx = {"blocks": blocks, "css_text": css_text, "html_text": html_text}
    for rule in rules:
        if rule["kind"] != "measure":
            continue
        for measured, lineno in MEASURES[rule["fn"]](ctx, rule):
            if rule["id"] in ignore.get(lineno, set()) or rule["id"] in ignore.get(1, set()):
                continue
            findings.append(mk(path, lineno, rule["id"], rule["severity"],
                               measured, rule["threshold"], rule["message"], rule["source"]))

    for f in findings:
        if cli_allow.get(f["rule"]):
            f["severity"] = "allowed"
            f["waiver"] = cli_allow[f["rule"]]
    return [f for f in findings if f["severity"] != "allowed"], len(rules)


_CSS_CACHE = {}


def in_css_region(lineno, lines):
    key = id(lines)
    regions = _CSS_CACHE.get(key)
    if regions is None:
        css_pairs, _ = split_views(lines, False)
        regions = {n for n, _ in css_pairs}
        _CSS_CACHE[key] = regions
    return lineno in regions


def css_line_text(lineno, lines):
    if lines[lineno - 1].lstrip().startswith(("<style", "</style")):
        return None
    return lines[lineno - 1]


def build_views(masked_lines, raw_lines, is_css):
    """Return (blocks, css_text, html_text).

    html_text keeps one line per source line, blanking css regions, so findings
    report the real line number instead of a position inside a stripped view.
    """
    css_pairs, html_pairs = split_views(masked_lines, is_css)
    blocks = css_blocks(css_pairs) if (css_pairs or is_css) else []
    if is_css:
        blocks = css_blocks(list(enumerate(masked_lines, 1)))
    css_text = "\n".join(t for _, t in css_pairs)
    css_lines = {n for n, _ in css_pairs}
    aligned = ["" if n in css_lines else masked_lines[n - 1] for n in range(1, len(masked_lines) + 1)]
    html_text = "\n".join(aligned)
    return blocks, css_text, html_text


def mk(path, line, rule, severity, measured, threshold, message, source):
    return {"file": str(path), "line": line, "rule": rule, "severity": severity,
            "measured": measured, "threshold": threshold, "message": message,
            "source": source}


# -------------------------------------------------------------------- cli ----

def gather(args):
    files = []
    for a in args.paths:
        p = Path(a)
        if p.is_dir():
            files += [f for f in sorted(p.rglob("*"))
                      if f.is_file() and f.suffix.lower() in (".html", ".htm", ".css")
                      and "node_modules" not in f.parts]
        elif p.is_file():
            files.append(p)
        else:
            raise ScanError("no such path: %s" % a)
    uniq = []
    for f in files:
        if f.suffix.lower() in (".md",):
            continue
        uniq.append(f)
    return uniq


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    known = {"--json", "--strict", "--allow", "--rules", "-h", "--help"}
    for a in argv:
        if a.startswith("-") and a not in known:
            # argparse would happily accept '--stric' as an abbreviation of
            # '--strict'; a mistyped gate flag must not silently keep scanning
            sys.stderr.write("ERROR  未知参数 %r（可用：%s）\n" % (a, ", ".join(sorted(known))))
            return 2

    ap = argparse.ArgumentParser(prog="slop_scan.py", add_help=False, allow_abbrev=False)
    ap.add_argument("-h", "--help", action="help")
    ap.add_argument("paths", nargs="*", help="html/css files or directories")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true", help="warn 也计入失败")
    ap.add_argument("--allow", action="append", default=[], metavar="RULE=REASON",
                    help="行外豁免，必须给理由")
    ap.add_argument("--rules", default=None, help="判定表路径，默认取 skill 的 rules/slop-table.json")
    ns = ap.parse_args(argv)

    try:
        for w in ns.allow:
            if "=" not in w or not w.split("=", 1)[1].strip():
                raise ScanError("--allow 需要 RULE=理由 形式：%r" % w)
        table = Path(ns.rules) if ns.rules else Path(__file__).resolve().parent.parent / "rules" / "slop-table.json"
        rules_data = load_rules(table)
        files = gather(ns)
        if not files:
            raise ScanError("没有可扫描的 html/css 文件——空扫描不等于通过")
    except ScanError as exc:
        sys.stderr.write("ERROR  %s\n" % exc)
        return 2
    except (OSError, ValueError, re.error) as exc:
        sys.stderr.write("ERROR  判定表或输入不可读: %s\n" % exc)
        return 2

    cli_allow = {w.split("=", 1)[0].strip(): w.split("=", 1)[1].strip() for w in ns.allow}
    all_findings = []
    for f in files:
        try:
            got, _ = scan_file(f, rules_data, cli_allow)
        except (OSError, ValueError) as exc:
            sys.stderr.write("ERROR  读不了 %s: %s\n" % (f, exc))
            return 2
        all_findings += got

    all_findings.sort(key=lambda x: (x["file"], x["line"], x["rule"]))
    hard = [x for x in all_findings if x["severity"] == "hard"]
    warn = [x for x in all_findings if x["severity"] == "warn"]

    if ns.json:
        print(json.dumps({"scanned": len(files), "rules": len(rules_data["rules"]),
                          "hard": hard, "warn": warn}, ensure_ascii=False, indent=2))
    else:
        for x in hard:
            print("FAIL  %-40s %s:%s  %s (measured %s / threshold %s) [%s]"
                  % (x["rule"], Path(x["file"]).name, x["line"], x["message"],
                     x["measured"], x["threshold"], x["source"]))
        for x in warn:
            print("WARN  %-40s %s:%s  %s (%s)"
                  % (x["rule"], Path(x["file"]).name, x["line"], x["message"], x["measured"]))
        print("-" * 72)
        print("scanned=%d rules=%d hard=%d warn=%d"
              % (len(files), len(rules_data["rules"]), len(hard), len(warn)))
        print("RESULT: FAIL" if hard or (ns.strict and warn) else "RESULT: PASS")
    return 1 if (hard or (ns.strict and warn)) else 0


if __name__ == "__main__":
    sys.exit(main())
