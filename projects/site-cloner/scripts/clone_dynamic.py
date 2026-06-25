"""
动态 SPA 捕获脚本 (v1.2.0)
使用 Playwright 启动浏览器，拦截所有网络请求，保存渲染后的 HTML 和 API 响应。
v1.1.0: CSS 计算样式提取 + 字体完整捕获 + 交互行为记录 + 设计Token抽取
v1.2.0: 版本同步
"""

import os
import sys
import json
import time
import re
import hashlib
import subprocess
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag


def normalize_url(url):
    url, _ = urldefrag(url)
    return url.rstrip('/')


def ensure_playwright():
    try:
        from playwright.sync_api import sync_playwright
        return True
    except ImportError:
        print("Playwright 未安装。正在安装...")
        os.system(f"{sys.executable} -m pip install playwright")
        os.system(f"{sys.executable} -m playwright install chromium")
        return True


def get_output_path(url, base_url, output_dir):
    parsed_base = urlparse(base_url)
    parsed_url = urlparse(url)
    if parsed_url.netloc and parsed_url.netloc != parsed_base.netloc:
        return None
    path = parsed_url.path
    if not path or path == '/':
        path = '/index.html'
    elif path.endswith('/'):
        path += 'index.html'
    elif '.' not in os.path.basename(path):
        path += '/index.html'
    if path.startswith('/'):
        path = path[1:]
    return Path(output_dir) / path


def extract_css_snapshot(page):
    """★ v1.1.0: CSS 完整提取"""
    return page.evaluate('''() => {
        const snapshot = {
            styleTags: Array.from(document.querySelectorAll('style')).map(s => s.textContent),
            stylesheets: Array.from(document.styleSheets).map(s => s.href).filter(Boolean),
            customProperties: {},
            keyframes: [],
            fontFaces: [],
            mediaQueries: [],
            allCssRules: []
        };

        // CSS 自定义属性
        const rootStyles = getComputedStyle(document.documentElement);
        for (let i = 0; i < rootStyles.length; i++) {
            const name = rootStyles[i];
            if (name.startsWith('--')) {
                snapshot.customProperties[name] = rootStyles.getPropertyValue(name).trim();
            }
        }

        // @keyframes / @font-face / @media
        for (let sheet of document.styleSheets) {
            try {
                for (let rule of sheet.cssRules) {
                    if (rule.type === CSSRule.KEYFRAMES_RULE) {
                        snapshot.keyframes.push({ name: rule.name, css: rule.cssText });
                    } else if (rule.type === CSSRule.FONT_FACE_RULE) {
                        snapshot.fontFaces.push({ family: rule.style.fontFamily, src: rule.style.src, css: rule.cssText });
                    } else if (rule.type === CSSRule.MEDIA_RULE) {
                        snapshot.mediaQueries.push({ condition: rule.conditionText, css: rule.cssText });
                    } else if (rule.cssText) {
                        snapshot.allCssRules.push(rule.cssText);
                    }
                }
            } catch(e) {}
        }

        return JSON.parse(JSON.stringify(snapshot));
    }''')


def extract_font_capture(page):
    """★ v1.1.0: 字体完整捕获"""
    return page.evaluate('''() => {
        const capture = {
            usedFonts: [],
            googleFonts: [],
            fontFileUrls: [],
            fontStyles: {}
        };

        // 页面使用的所有字体族
        const fontSet = new Set();
        const allEls = document.querySelectorAll('*');
        for (let i = 0; i < Math.min(allEls.length, 500); i++) {
            const family = getComputedStyle(allEls[i]).fontFamily;
            if (family) fontSet.add(family);
        }
        capture.usedFonts = Array.from(fontSet);

        // Google Fonts 链接
        capture.googleFonts = Array.from(document.querySelectorAll(
            'link[href*="fonts.googleapis.com"], link[href*="fonts.gstatic.com"]'
        )).map(l => l.href);

        // @font-face 字体文件 URL（从 CSS 内联 style 和外部 sheet 两处提取）
        const fontUrls = new Set();
        for (let sheet of document.styleSheets) {
            try {
                for (let rule of sheet.cssRules) {
                    if (rule.type === CSSRule.FONT_FACE_RULE) {
                        const src = rule.style.src;
                        const matches = src.matchAll(/url\\(["']?([^"')]+)["']?\\)/g);
                        for (let m of matches) fontUrls.add(m[1]);
                    }
                }
            } catch(e) {}
        }
        capture.fontFileUrls = Array.from(fontUrls);

        // 字体渲染样式快照（前 50 个不同字号/字重的元素）
        const seen = new Set();
        for (let i = 0; i < Math.min(allEls.length, 200); i++) {
            const el = allEls[i];
            const style = getComputedStyle(el);
            const key = style.fontFamily + '|' + style.fontSize + '|' + style.fontWeight;
            if (!seen.has(key)) {
                seen.add(key);
                capture.fontStyles[key] = {
                    family: style.fontFamily,
                    size: style.fontSize,
                    weight: style.fontWeight,
                    style: style.fontStyle,
                    lineHeight: style.lineHeight,
                    letterSpacing: style.letterSpacing
                };
            }
        }

        return JSON.parse(JSON.stringify(capture));
    }''')


def extract_interaction_capture(page):
    """★ v1.1.0: 交互行为完整记录"""
    return page.evaluate('''() => {
        const capture = {
            formValidations: [],
            animations: [],
            eventHandlers: [],
            pseudoStyles: { hover: [], focus: [], active: [] }
        };

        // 表单校验逻辑
        capture.formValidations = Array.from(document.querySelectorAll('form')).map(form => ({
            action: form.action,
            method: form.method,
            id: form.id,
            className: form.className,
            inputs: Array.from(form.querySelectorAll('input, select, textarea, button[type="submit"]')).map(el => ({
                name: el.name,
                type: el.type || el.tagName.toLowerCase(),
                required: el.required || false,
                placeholder: el.placeholder || '',
                pattern: el.pattern || '',
                min: el.min || '',
                max: el.max || '',
                minLength: el.minLength || null,
                maxLength: el.maxLength || null,
                id: el.id,
                className: el.className
            }))
        }));

        // 按钮交互元素
        const interactiveEls = Array.from(document.querySelectorAll(
            'button, [role="button"], .btn, [class*="btn"], [class*="button"], a[href]'
        )).slice(0, 200);
        for (let el of interactiveEls) {
            const style = getComputedStyle(el);
            const hasTransition = style.transition !== 'all 0s ease 0s';
            const hasTransform = style.transform !== 'none';
            if (hasTransition || hasTransform) {
                capture.animations.push({
                    selector: el.tagName + (el.id ? '#' + el.id : '') +
                              (el.className ? '.' + el.className.split(' ').slice(0,3).join('.') : ''),
                    tag: el.tagName,
                    text: (el.textContent || '').trim().slice(0, 30),
                    transition: style.transition,
                    transform: style.transform,
                    animation: style.animation,
                    cursor: style.cursor
                });
            }
        }

        // 有动效的元素（transition 非默认 + animation 非默认）
        const animatedEls = Array.from(document.querySelectorAll('*')).slice(0, 500);
        for (let el of animatedEls) {
            const style = getComputedStyle(el);
            if (style.animation && style.animation !== 'none 0s ease 0s 1 normal none running') {
                capture.animations.push({
                    selector: el.tagName + (el.id ? '#' + el.id : '') + (el.className ? '.' + el.className.split(' ').slice(0,3).join('.') : ''),
                    animation: style.animation,
                    animationDelay: style.animationDelay,
                    animationDuration: style.animationDuration,
                    animationIterationCount: style.animationIterationCount
                });
            }
        }

        // 内联事件处理器
        const handlerEls = document.querySelectorAll('[onclick], [onsubmit], [onchange], [oninput], [onfocus], [onblur], [onmouseenter], [onmouseleave], [onkeydown], [onkeyup], [onmouseover], [onmouseout]');
        capture.eventHandlers = Array.from(handlerEls).map(el => ({
            tag: el.tagName,
            id: el.id,
            className: el.className,
            events: Array.from(el.attributes)
                .filter(a => a.name.startsWith('on'))
                .map(a => ({ name: a.name.slice(2), handler: a.value.slice(0, 100) }))
        })).filter(e => e.events.length > 0);

        return JSON.parse(JSON.stringify(capture));
    }''')


def extract_design_tokens(page):
    """★ v1.1.0: 设计 Token 提取"""
    return page.evaluate('''() => {
        const tokens = {
            colors: [],
            typography: {},
            spacing: {},
            shadows: [],
            borderRadiuses: [],
            gradients: []
        };

        // 颜色体系（限制扫描 1000 个元素）
        const colorSet = new Set();
        const gradientSet = new Set();
        document.querySelectorAll('*').forEach((el, idx) => {
            if (idx > 1000) return;
            const style = getComputedStyle(el);
            ['color', 'backgroundColor', 'borderColor', 'borderTopColor', 'borderBottomColor',
             'outlineColor', 'caretColor', 'columnRuleColor', 'textDecorationColor'].forEach(prop => {
                const val = style[prop];
                if (val && val !== 'rgba(0, 0, 0, 0)' && val !== 'transparent'
                    && !val.startsWith('rgb(0, 0, 0') && val !== 'rgb(0, 0, 0)') {
                    colorSet.add(val);
                }
            });
            // 渐变
            const bg = style.backgroundImage;
            if (bg && bg.includes('gradient')) gradientSet.add(bg);
        });
        tokens.colors = Array.from(colorSet).slice(0, 200);
        tokens.gradients = Array.from(gradientSet).slice(0, 50);

        // 排版层级
        const typos = {};
        document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, a, li, div, button, label, input').forEach((el, idx) => {
            if (idx > 800) return;
            const style = getComputedStyle(el);
            const key = style.fontFamily + '|' + style.fontSize + '|' + style.fontWeight;
            if (!typos[key]) {
                typos[key] = {
                    family: style.fontFamily,
                    size: style.fontSize,
                    weight: style.fontWeight,
                    lineHeight: style.lineHeight,
                    letterSpacing: style.letterSpacing,
                    textTransform: style.textTransform,
                    sample: el.textContent?.trim().slice(0, 40) || ''
                };
            }
        });
        tokens.typography = typos;

        // 间距
        const gapSet = new Set();
        document.querySelectorAll('section, .section, [class*="section"], main > div, .container, .wrapper, nav, header, footer').forEach(el => {
            const style = getComputedStyle(el);
            gapSet.add(style.paddingTop); gapSet.add(style.paddingBottom);
            gapSet.add(style.marginBottom); gapSet.add(style.marginTop);
        });
        tokens.spacing = { commonGaps: Array.from(gapSet).filter(g => g !== '0px').slice(0, 30) };

        // 阴影
        const shadowSet = new Set();
        document.querySelectorAll('*').forEach((el, idx) => {
            if (idx > 1000) return;
            const shadow = getComputedStyle(el).boxShadow;
            if (shadow && shadow !== 'none') shadowSet.add(shadow);
        });
        tokens.shadows = Array.from(shadowSet).slice(0, 30);

        // 圆角
        const radiusSet = new Set();
        document.querySelectorAll('*').forEach((el, idx) => {
            if (idx > 1000) return;
            const radius = getComputedStyle(el).borderRadius;
            if (radius && radius !== '0px' && !radius.includes('0px /')) radiusSet.add(radius);
        });
        tokens.borderRadiuses = Array.from(radiusSet).slice(0, 20);

        return JSON.parse(JSON.stringify(tokens));
    }''')


def capture_rendered_html(page):
    """捕获渲染后完整 HTML，含注入的 style 标签"""
    return page.evaluate('''() => {
        const clone = document.documentElement.cloneNode(true);
        return '<!DOCTYPE html>\\n' + clone.outerHTML;
    }''')


def download_assets(page, output_dir, base_domain, base_url):
    """下载页面静态资源（CSS/JS/图片/字体）"""
    assets_dir = Path(output_dir) / 'assets'
    assets_dir.mkdir(parents=True, exist_ok=True)

    assets = page.evaluate('''() => {
        const urls = { css: [], js: [], img: [], font: [], other: [] };

        // CSS
        document.querySelectorAll('link[rel="stylesheet"]').forEach(l => urls.css.push(l.href));
        document.styleSheets;

        // JS
        document.querySelectorAll('script[src]').forEach(s => urls.js.push(s.src));

        // 图片
        document.querySelectorAll('img[src]').forEach(i => urls.img.push(i.src));
        document.querySelectorAll('[style*="background-image"]').forEach(el => {
            const m = el.style.backgroundImage.match(/url\\(["']?([^"')]+)["']?\\)/);
            if (m) urls.img.push(m[1]);
        });
        document.querySelectorAll('source[srcset]').forEach(s => urls.img.push(s.srcset));
        document.querySelectorAll('video[poster]').forEach(v => urls.img.push(v.poster));

        // 字体
        document.querySelectorAll('link[href*="font"]').forEach(l => urls.font.push(l.href));
        document.querySelectorAll('link[href*="woff"], link[href*="woff2"], link[href*="ttf"]').forEach(l => urls.font.push(l.href));

        return JSON.parse(JSON.stringify(urls));
    }''')

    # 从 @font-face CSS 规则中额外提取字体 URL
    font_urls = page.evaluate('''() => {
        const urls = [];
        for (let sheet of document.styleSheets) {
            try {
                for (let rule of sheet.cssRules) {
                    if (rule.type === CSSRule.FONT_FACE_RULE) {
                        const src = rule.style.src;
                        const matches = src.matchAll(/url\\(["']?([^"')]+)["']?\\)/g);
                        for (let m of matches) urls.push(m[1]);
                    }
                }
            } catch(e) {}
        }
        return urls;
    }''')
    assets['font'].extend(font_urls)
    assets['font'] = list(set(assets['font']))

    downloaded = {'css': 0, 'js': 0, 'img': 0, 'font': 0}

    for category, urls in assets.items():
        cat_dir = assets_dir / category
        cat_dir.mkdir(exist_ok=True)
        for url in urls:
            try:
                filename = os.path.basename(urlparse(url).path) or hashlib.md5(url.encode()).hexdigest()[:8]
                if not any(filename.lower().endswith(ext) for ext in [
                    '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
                    '.webp', '.woff', '.woff2', '.ttf', '.eot', '.otf', '.json', '.xml',
                    '.mp4', '.webm', '.map'
                ]):
                    if category == 'css': filename += '.css'
                    elif category == 'js': filename += '.js'
                filepath = cat_dir / filename
                if filepath.exists():
                    downloaded[category] += 1
                    continue
                subprocess.run(['curl', '-s', '-L', '-o', str(filepath), url], timeout=30)
                if filepath.exists() and filepath.stat().st_size > 0:
                    downloaded[category] += 1
            except Exception:
                pass

    return downloaded


def detect_framework(html):
    """检测前端框架"""
    if '__NEXT_DATA__' in html or 'next' in html.lower():
        return 'Next.js'
    if 'window.__NUXT__' in html or 'nuxt' in html.lower():
        return 'Nuxt.js'
    if 'react' in html.lower() or 'data-reactroot' in html.lower():
        return 'React'
    if 'vue' in html.lower() or 'data-v-' in html:
        return 'Vue'
    if 'ng-version' in html:
        return 'Angular'
    if 'wp-content' in html or 'WordPress' in html:
        return 'WordPress'
    return 'Unknown'


def clone_dynamic(url, output_dir, capture_screenshots=False, max_pages=50):
    """主函数：使用 Playwright 捕获动态网站"""
    from playwright.sync_api import sync_playwright

    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    base_domain = parsed.netloc

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    frontend_dir = output_dir / 'frontend'
    frontend_dir.mkdir(exist_ok=True)
    pages_dir = frontend_dir / 'pages'
    pages_dir.mkdir(exist_ok=True)

    api_dir = output_dir / 'api_responses'
    api_dir.mkdir(exist_ok=True)
    css_dir = output_dir / 'css_snapshot'
    css_dir.mkdir(exist_ok=True)
    tokens_dir = output_dir / 'design_tokens'
    tokens_dir.mkdir(exist_ok=True)
    fonts_dir = output_dir / 'font_capture'
    fonts_dir.mkdir(exist_ok=True)
    interaction_dir = output_dir / 'interaction_data'
    interaction_dir.mkdir(exist_ok=True)

    if capture_screenshots:
        screenshots_dir = output_dir / 'screenshots'
        screenshots_dir.mkdir(exist_ok=True)

    api_calls = []
    visited_pages = set()
    pages_to_visit = [url]
    captured_stylesheets = []
    all_css_snapshots = {}
    all_font_captures = {}
    all_design_tokens = {}
    all_interactions = {}
    framework = None

    print(f"启动浏览器捕获: {url}")
    print(f"输出目录: {output_dir}")
    print("-" * 70)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1440, 'height': 900},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        )

        def on_response(response):
            content_type = response.headers.get('content-type', '').lower()
            if 'application/json' in content_type or 'api' in response.url.lower():
                try:
                    body = response.text()
                    api_calls.append({
                        'url': response.url,
                        'method': response.request.method,
                        'status': response.status,
                        'request_headers': dict(response.request.headers),
                        'response_headers': dict(response.headers),
                        'body': json.loads(body) if body else None,
                        'timestamp': time.time()
                    })
                except Exception:
                    api_calls.append({
                        'url': response.url, 'method': response.request.method,
                        'status': response.status, 'error': '无法解析响应体'
                    })

            # 收集样式表 URL
            if 'css' in content_type or response.url.endswith('.css'):
                captured_stylesheets.append(response.url)

        try:
            page = context.new_page()
            page.on('response', on_response)

            # 尝试先设置视口为桌面
            page.set_viewport_size({'width': 1920, 'height': 1080})

            while pages_to_visit and len(visited_pages) < max_pages:
                current_url = pages_to_visit.pop(0)
                normalized = normalize_url(current_url)
                if normalized in visited_pages:
                    continue
                visited_pages.add(normalized)
                page_num = len(visited_pages)

                page_slug = normalized.replace(base_url, '').replace('/', '_').strip('_') or 'index'
                page_slug = re.sub(r'[<>:"/\\|?*#]', '_', page_slug)[:60]
                print(f"[页面 {page_num}] {page_slug} | {current_url}")

                try:
                    page.goto(current_url, wait_until='networkidle', timeout=45000)
                    page.wait_for_timeout(1500)

                    # 滚动到底部触发懒加载
                    page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                    page.wait_for_timeout(1000)
                    page.evaluate('window.scrollTo(0, 0)')
                    page.wait_for_timeout(500)

                except Exception as e:
                    print(f"  [错误] {e}")
                    continue

                # ★ 框架检测（首次页面）
                if framework is None:
                    html_preview = page.content()
                    framework = detect_framework(html_preview)
                    print(f"  [检测] 框架: {framework}")

                # ★ v1.1.0: CSS 完整提取
                css_snapshot = extract_css_snapshot(page)
                all_css_snapshots[page_slug] = css_snapshot
                print(f"  [CSS] 变量: {len(css_snapshot.get('customProperties', {}))} "
                      f"关键帧: {len(css_snapshot.get('keyframes', []))} "
                      f"@font-face: {len(css_snapshot.get('fontFaces', []))}")

                # ★ v1.1.0: 字体捕获
                font_capture = extract_font_capture(page)
                all_font_captures[page_slug] = font_capture
                print(f"  [字体] 使用: {len(font_capture.get('usedFonts', []))} "
                      f"Google: {len(font_capture.get('googleFonts', []))} "
                      f"文件URL: {len(font_capture.get('fontFileUrls', []))}")

                # ★ v1.1.0: 交互行为记录
                interaction = extract_interaction_capture(page)
                all_interactions[page_slug] = interaction
                print(f"  [交互] 表单: {len(interaction.get('formValidations', []))} "
                      f"动效元素: {len(interaction.get('animations', []))} "
                      f"事件处理器: {len(interaction.get('eventHandlers', []))}")

                # ★ v1.1.0: 设计Token提取
                tokens = extract_design_tokens(page)
                all_design_tokens[page_slug] = tokens
                print(f"  [Token] 颜色: {len(tokens.get('colors', []))} "
                      f"阴影: {len(tokens.get('shadows', []))} "
                      f"圆角: {len(tokens.get('borderRadiuses', []))}")

                # 保存渲染后 HTML
                html_content = capture_rendered_html(page)
                html_path = pages_dir / f"{page_slug}.html"
                html_path.parent.mkdir(parents=True, exist_ok=True)
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                # 截图
                if capture_screenshots:
                    ss_path = screenshots_dir / f"{page_slug}.png"
                    page.screenshot(path=str(ss_path), full_page=True)

                # 提取页面链接
                links = page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('a[href]'))
                        .map(a => a.href)
                        .filter(h => {
                            try {
                                const u = new URL(h, window.location.origin);
                                return u.origin === window.location.origin &&
                                       !h.includes('mailto:') && !h.includes('tel:') &&
                                       !h.includes('javascript:') && !h.includes('#');
                            } catch { return false; }
                        });
                }''')
                for link in links:
                    norm_link = normalize_url(link)
                    if norm_link not in visited_pages:
                        pages_to_visit.append(link)

                # 下载静态资源（CSS/JS/图片/字体）
                downloaded = download_assets(page, frontend_dir, base_domain, base_url)
                if page_num == 1:
                    print(f"  [资源] CSS:{downloaded['css']} JS:{downloaded['js']} "
                          f"图片:{downloaded['img']} 字体:{downloaded['font']}")

                time.sleep(0.8)

        finally:
            browser.close()

    # 保存所有提取数据
    print("-" * 70)
    print("保存提取数据...")

    # API 响应
    api_file = api_dir / 'all_api_calls.json'
    with open(api_file, 'w', encoding='utf-8') as f:
        json.dump(api_calls, f, ensure_ascii=False, indent=2)

    # CSS 快照
    css_file = css_dir / 'css_snapshot.json'
    with open(css_file, 'w', encoding='utf-8') as f:
        json.dump(all_css_snapshots, f, ensure_ascii=False, indent=2)

    # 字体捕获
    font_file = fonts_dir / 'font_capture.json'
    with open(font_file, 'w', encoding='utf-8') as f:
        json.dump(all_font_captures, f, ensure_ascii=False, indent=2)

    # 交互数据
    interaction_file = interaction_dir / 'interaction_data.json'
    with open(interaction_file, 'w', encoding='utf-8') as f:
        json.dump(all_interactions, f, ensure_ascii=False, indent=2)

    # 设计 Token
    tokens_file = tokens_dir / 'design_tokens.json'
    with open(tokens_file, 'w', encoding='utf-8') as f:
        json.dump(all_design_tokens, f, ensure_ascii=False, indent=2)

    # ★ 生成 design-tokens.css
    if all_design_tokens:
        first_page = list(all_design_tokens.values())[0]
        tokens_css = ":root {\n"
        if 'colors' in first_page and first_page['colors']:
            for i, c in enumerate(first_page['colors'][:30]):
                tokens_css += f"  --color-{i}: {c};\n"
        tokens_css += "}\n"
        tokens_css_path = frontend_dir / 'css' / 'design-tokens.css'
        tokens_css_path.parent.mkdir(parents=True, exist_ok=True)
        with open(tokens_css_path, 'w', encoding='utf-8') as f:
            f.write(tokens_css)

    # ★ 生成 animations.css（关键帧）
    animations_css = ""
    for page_slug, snapshot in all_css_snapshots.items():
        for kf in snapshot.get('keyframes', []):
            animations_css += f"/* {page_slug} — {kf.get('name', '')} */\n"
            animations_css += f"{kf.get('css', '')}\n\n"
    if animations_css:
        anim_path = frontend_dir / 'css' / 'animations.css'
        anim_path.parent.mkdir(parents=True, exist_ok=True)
        with open(anim_path, 'w', encoding='utf-8') as f:
            f.write(animations_css)

    # 下载字体文件
    print("下载字体文件...")
    all_font_urls = set()
    for capture in all_font_captures.values():
        for url in capture.get('fontFileUrls', []):
            all_font_urls.add(url)
    fonts_output_dir = frontend_dir / 'fonts'
    fonts_output_dir.mkdir(parents=True, exist_ok=True)
    font_count = 0
    for font_url in all_font_urls:
        try:
            filename = os.path.basename(urlparse(font_url).path) or f"font_{font_count}.woff2"
            filepath = fonts_output_dir / filename
            if not filepath.exists():
                subprocess.run(['curl', '-s', '-L', '-o', str(filepath), font_url], timeout=30)
            if filepath.exists() and filepath.stat().st_size > 0:
                font_count += 1
        except Exception:
            pass
    print(f"  字体文件: {font_count} 个")

    # 统计输出
    stats = {
        'base_url': url,
        'framework': framework,
        'pages_captured': len(visited_pages),
        'api_endpoints': len(api_calls),
        'css_variables': sum(len(s.get('customProperties', {})) for s in all_css_snapshots.values()),
        'keyframes': sum(len(s.get('keyframes', [])) for s in all_css_snapshots.values()),
        'font_faces': sum(len(s.get('fontFaces', [])) for s in all_css_snapshots.values()),
        'font_files_downloaded': font_count,
        'forms_captured': sum(len(i.get('formValidations', [])) for i in all_interactions.values()),
        'animations_captured': sum(len(i.get('animations', [])) for i in all_interactions.values()),
        'colors_extracted': sum(len(t.get('colors', [])) for t in all_design_tokens.values()),
        'shadows_extracted': sum(len(t.get('shadows', [])) for t in all_design_tokens.values()),
        'border_radiuses_extracted': sum(len(t.get('borderRadiuses', [])) for t in all_design_tokens.values()),
        'gradients_extracted': sum(len(t.get('gradients', [])) for t in all_design_tokens.values())
    }

    print("-" * 70)
    print("完成! 捕获统计:")
    for key, val in stats.items():
        if key != 'base_url':
            print(f"  {key}: {val}")

    stats_file = output_dir / 'clone_stats.json'
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    return stats


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python clone_dynamic.py <URL> <输出目录> [--screenshots] [--max-pages N]")
        print("示例: python clone_dynamic.py https://example.com ./output --screenshots --max-pages 30")
        sys.exit(1)

    ensure_playwright()

    target_url = sys.argv[1]
    out_dir = sys.argv[2]
    screenshots = '--screenshots' in sys.argv
    max_p = 50
    if '--max-pages' in sys.argv:
        idx = sys.argv.index('--max-pages')
        if idx + 1 < len(sys.argv):
            max_p = int(sys.argv[idx + 1])

    clone_dynamic(target_url, out_dir, capture_screenshots=screenshots, max_pages=max_p)
