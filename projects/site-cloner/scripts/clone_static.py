"""
静态网站捕获脚本 (v1.1.0)
当 HTTrack/wget 不可用时的备选方案。
v1.1.0 增强：CSS/字体/图片全量路径修正 + @font-face 字体文件下载
"""

import os
import re
import sys
import json
import time
import hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse, urldefrag
from collections import deque
from io import BytesIO

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("需要安装依赖: pip install requests beautifulsoup4")
    sys.exit(1)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
REQUEST_DELAY = 0.5
MAX_DEPTH = 3
MAX_PAGES = 200

RESOURCE_EXTENSIONS = {
    '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp',
    '.woff', '.woff2', '.ttf', '.eot', '.otf', '.mp4', '.webm',
    '.pdf', '.zip', '.json', '.xml', '.txt', '.map'
}

FONT_EXTS = {'.woff', '.woff2', '.ttf', '.eot', '.otf'}


def normalize_url(url):
    url, _ = urldefrag(url)
    return url.rstrip('/')


def is_same_domain(url, base_domain):
    parsed = urlparse(url)
    return parsed.netloc == base_domain or parsed.netloc.endswith('.' + base_domain)


def is_resource_url(url):
    path = urlparse(url).path.lower()
    return any(path.endswith(ext) for ext in RESOURCE_EXTENSIONS)


def is_page_url(url):
    if is_resource_url(url):
        return False
    path = urlparse(url).path
    if not path or path == '/':
        return True
    if '.' in os.path.basename(path):
        ext = os.path.splitext(path)[1].lower()
        if ext in {'.html', '.htm', '.php', '.asp', '.aspx', '.jsp'}:
            return True
        if ext and ext not in RESOURCE_EXTENSIONS:
            return False
    return True


def get_output_path(url, base_url, output_dir, category='pages'):
    parsed_base = urlparse(base_url)
    parsed_url = urlparse(url)
    path = parsed_url.path
    if not path or path == '/':
        path = '/index.html'
    elif path.endswith('/'):
        path += 'index.html'
    elif '.' not in os.path.basename(path) and category == 'pages':
        path += '/index.html'
    if path.startswith('/'):
        path = path[1:]
    return Path(output_dir) / category / path


def download_resource(url, output_path, session):
    if output_path.exists():
        return True
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        resp = session.get(url, headers={'User-Agent': USER_AGENT}, timeout=30)
        resp.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(resp.content)
        return True
    except Exception as e:
        print(f"  [错误] 下载失败 {url}: {e}")
        return False


def extract_all_urls(html, base_url):
    """★ v1.1.0: 从 HTML/CSS 中提取所有资源 URL（含 @font-face）"""
    soup = BeautifulSoup(html, 'html.parser')
    urls = set()

    # HTML 标签属性
    for tag in soup.find_all(['a', 'link', 'script', 'img', 'source', 'video', 'audio', 'iframe']):
        for attr in ['href', 'src', 'srcset', 'data-src', 'poster']:
            val = tag.get(attr)
            if val:
                # srcset 可能含多个 URL
                for part in val.split(','):
                    url = part.strip().split(' ')[0]
                    if url:
                        full_url = urljoin(base_url, url)
                        urls.add(normalize_url(full_url))

    # CSS url() 引用（含 @font-face / background-image）
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            for match in re.finditer(r'url\(["\']?([^"\')\s]+)["\']?\)', style_tag.string):
                full_url = urljoin(base_url, match.group(1))
                urls.add(normalize_url(full_url))

    # inline style
    for tag in soup.find_all(style=True):
        for match in re.finditer(r'url\(["\']?([^"\')\s]+)["\']?\)', tag['style']):
            full_url = urljoin(base_url, match.group(1))
            urls.add(normalize_url(full_url))

    # @import in style tags
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            for match in re.finditer(r'@import\s+["\']([^"\']+)["\']', style_tag.string):
                full_url = urljoin(base_url, match.group(1))
                urls.add(normalize_url(full_url))

    return urls


def extract_css_variables(html):
    """★ v1.1.0: 从 HTML 的 style 标签中提取 CSS 变量"""
    variables = {}
    for match in re.finditer(r'--([\w-]+)\s*:\s*([^;]+);', html):
        variables[f'--{match.group(1)}'] = match.group(2).strip()
    return variables


def extract_font_face_rules(html):
    """★ v1.1.0: 提取 @font-face 规则及其字体 URL"""
    font_info = []
    pattern = re.compile(
        r'@font-face\s*\{([^}]+)\}',
        re.DOTALL | re.IGNORECASE
    )
    url_pattern = re.compile(r'url\(["\']?([^"\')\s]+)["\']?\)')

    for match in pattern.finditer(html):
        block = match.group(1)
        font_entry = {'css': match.group(0)}
        family_match = re.search(r'font-family\s*:\s*["\']?([^"\'};]+)["\']?', block)
        if family_match:
            font_entry['family'] = family_match.group(1).strip()
        urls = url_pattern.findall(block)
        font_entry['urls'] = urls
        font_info.append(font_entry)

    return font_info


def extract_keyframes(html):
    """★ v1.1.0: 提取 @keyframes 名称"""
    names = set()
    for match in re.finditer(r'@(?:-webkit-)?keyframes\s+([^{\s]+)', html, re.IGNORECASE):
        names.add(match.group(1))
    return list(names)


def fix_all_links(html, base_url, base_domain):
    """★ v1.1.0: 完整替换所有资源链接为相对路径"""
    soup = BeautifulSoup(html, 'html.parser')

    # HTML 标签
    for tag in soup.find_all(['a', 'link', 'script', 'img', 'source', 'video', 'audio']):
        for attr in ['href', 'src', 'data-src', 'poster']:
            url = tag.get(attr)
            if url and not url.startswith(('data:', 'blob:', 'javascript:', 'mailto:', 'tel:', '#')):
                full_url = urljoin(base_url, url)
                parsed = urlparse(full_url)
                if is_same_domain(full_url, base_domain):
                    new_path = parsed.path
                    if new_path.startswith('/'):
                        new_path = new_path[1:]
                    # 资源文件移到对应目录
                    ext = os.path.splitext(new_path)[1].lower()
                    if ext in FONT_EXTS:
                        new_path = 'fonts/' + os.path.basename(new_path)
                    elif ext in {'.css'}:
                        new_path = 'css/' + os.path.basename(new_path)
                    elif ext in {'.js'}:
                        new_path = 'js/' + os.path.basename(new_path)
                    elif ext in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp'}:
                        new_path = 'images/' + os.path.basename(new_path)
                    tag[attr] = '/' + new_path

    # CSS url()
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            def replace_css_url(match):
                url = match.group(1)
                if url.startswith(('data:', 'blob:')):
                    return match.group(0)
                full_url = urljoin(base_url, url)
                parsed = urlparse(full_url)
                if is_same_domain(full_url, base_domain):
                    path = parsed.path
                    ext = os.path.splitext(path)[1].lower()
                    if ext in FONT_EXTS:
                        return f"url('/fonts/{os.path.basename(path)}')"
                    elif ext in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp'}:
                        return f"url('/images/{os.path.basename(path)}')"
                    return f"url('/{path.lstrip('/')}')"
                return match.group(0)
            style_tag.string = re.sub(
                r'url\(["\']?([^"\')\s]+)["\']?\)',
                replace_css_url,
                style_tag.string
            )

    # inline styles
    for tag in soup.find_all(style=True):
        def replace_inline_url(match):
            url = match.group(1)
            if url.startswith(('data:', 'blob:')):
                return match.group(0)
            full_url = urljoin(base_url, url)
            parsed = urlparse(full_url)
            if is_same_domain(full_url, base_domain):
                path = parsed.path
                ext = os.path.splitext(path)[1].lower()
                if ext in FONT_EXTS:
                    return f"url('/fonts/{os.path.basename(path)}')"
                elif ext in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp'}:
                    return f"url('/images/{os.path.basename(path)}')"
                return f"url('/{path.lstrip('/')}')"
            return match.group(0)
        tag['style'] = re.sub(
            r'url\(["\']?([^"\')\s]+)["\']?\)',
            replace_inline_url,
            tag['style']
        )

    return str(soup)


def extract_design_info(html):
    """★ v1.1.0: 从静态 HTML 提取设计信息"""
    return {
        'css_variables': extract_css_variables(html),
        'font_faces': extract_font_face_rules(html),
        'keyframes': extract_keyframes(html)
    }


def clone_static(url, output_dir, max_depth=MAX_DEPTH, max_pages=MAX_PAGES):
    """主函数：克隆静态网站"""
    parsed = urlparse(url)
    base_domain = parsed.netloc
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frontend_dir = output_dir / 'frontend'
    frontend_dir.mkdir(exist_ok=True)

    for subdir in ['pages', 'css', 'js', 'images', 'fonts']:
        (frontend_dir / subdir).mkdir(exist_ok=True)

    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})

    visited = set()
    queue = deque([(url, 0)])
    stats = {
        'pages': 0, 'css': 0, 'js': 0, 'images': 0, 'fonts': 0, 'others': 0, 'errors': 0
    }
    all_design_info = {}
    all_font_urls = set()

    print(f"开始克隆: {url}")
    print(f"输出目录: {output_dir}")
    print(f"最大深度: {max_depth}, 最大页面数: {max_pages}")
    print("-" * 60)

    while queue and stats['pages'] < max_pages:
        current_url, depth = queue.popleft()
        normalized = normalize_url(current_url)
        if normalized in visited:
            continue
        visited.add(normalized)

        page_num = stats['pages'] + 1
        print(f"[页面 {page_num}] 深度={depth} {current_url}")

        try:
            resp = session.get(current_url, headers={'User-Agent': USER_AGENT}, timeout=30)
            resp.raise_for_status()
            html = resp.text
        except Exception as e:
            print(f"  [错误] {e}")
            stats['errors'] += 1
            continue

        # ★ v1.1.0: 提取所有资源 URL（含 @font-face CSS内 url()）
        urls = extract_all_urls(html, current_url)
        resources = []
        child_pages = []

        for link in urls:
            parsed_link = urlparse(link)
            if is_same_domain(link, base_domain):
                if is_resource_url(link):
                    resources.append(link)
                elif is_page_url(link) and depth < max_depth:
                    child_pages.append(link)

        # 下载资源
        for res_url in resources:
            ext = os.path.splitext(urlparse(res_url).path)[1].lower()
            if ext in FONT_EXTS:
                subdir = 'fonts'
            elif ext == '.css':
                subdir = 'css'
            elif ext == '.js':
                subdir = 'js'
            elif ext in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp'}:
                subdir = 'images'
            else:
                subdir = 'others'

            res_path = frontend_dir / subdir / os.path.basename(urlparse(res_url).path)
            if download_resource(res_url, res_path, session):
                if subdir == 'fonts':
                    stats['fonts'] += 1
                    all_font_urls.add(res_url)
                elif subdir == 'css':
                    stats['css'] += 1
                elif subdir == 'js':
                    stats['js'] += 1
                elif subdir == 'images':
                    stats['images'] += 1
                else:
                    stats['others'] += 1

        # ★ v1.1.0: 提取设计信息
        page_slug = normalized.replace(base_url, '').replace('/', '_').strip('_') or 'index'
        page_slug = re.sub(r'[<>:"/\\|?*#]', '_', page_slug)[:60]
        all_design_info[page_slug] = extract_design_info(html)

        # ★ v1.1.0: 路径修正
        fixed_html = fix_all_links(html, current_url, base_domain)

        # 保存页面
        page_path = frontend_dir / 'pages' / f"{page_slug}.html"
        page_path.parent.mkdir(parents=True, exist_ok=True)
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(fixed_html)

        stats['pages'] += 1

        # 加入子页面
        for child_url in child_pages:
            normalized_child = normalize_url(child_url)
            if normalized_child not in visited:
                queue.append((child_url, depth + 1))

        time.sleep(REQUEST_DELAY)

    # ★ v1.1.0: 保存设计信息
    design_file = output_dir / 'design_info.json'
    design_output = {
        'pages': all_design_info,
        'font_urls': list(all_font_urls),
        'total_css_variables': sum(len(info['css_variables']) for info in all_design_info.values()),
        'total_font_faces': sum(len(info['font_faces']) for info in all_design_info.values()),
        'total_keyframes': sum(len(info['keyframes']) for info in all_design_info.values()),
    }
    with open(design_file, 'w', encoding='utf-8') as f:
        json.dump(design_output, f, ensure_ascii=False, indent=2)

    # ★ v1.1.0: 生成 design-tokens.css
    all_vars = {}
    for info in all_design_info.values():
        all_vars.update(info['css_variables'])
    if all_vars:
        tokens_css = ":root {\n"
        for name, val in list(all_vars.items())[:50]:
            tokens_css += f"  {name}: {val};\n"
        tokens_css += "}\n"
        (frontend_dir / 'css').mkdir(parents=True, exist_ok=True)
        with open(frontend_dir / 'css' / 'design-tokens.css', 'w', encoding='utf-8') as f:
            f.write(tokens_css)

    # ★ v1.1.0: 生成 animations.css
    animations_css = ""
    for page_slug, info in all_design_info.items():
        for kf_name in info.get('keyframes', []):
            animations_css += f"/* {page_slug} — {kf_name} */\n"
    if animations_css:
        with open(frontend_dir / 'css' / 'animations.css', 'w', encoding='utf-8') as f:
            f.write(animations_css)

    # 输出统计
    print("-" * 60)
    print(f"完成！")
    print(f"  页面: {stats['pages']}  CSS: {stats['css']}  JS: {stats['js']}")
    print(f"  图片: {stats['images']}  字体: {stats['fonts']}  其他: {stats['others']}")
    print(f"  错误: {stats['errors']}")
    print(f"  CSS变量: {design_output['total_css_variables']}")
    print(f"  @font-face: {design_output['total_font_faces']}")
    print(f"  @keyframes: {design_output['total_keyframes']}")

    stats['base_url'] = url
    stats.update(design_output)
    stats_file = output_dir / 'clone_stats.json'
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    return stats


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python clone_static.py <URL> <输出目录> [最大深度] [最大页面数]")
        print("示例: python clone_static.py https://example.com ./output 3 100")
        sys.exit(1)

    target_url = sys.argv[1]
    out_dir = sys.argv[2]
    depth = int(sys.argv[3]) if len(sys.argv) > 3 else MAX_DEPTH
    pages = int(sys.argv[4]) if len(sys.argv) > 4 else MAX_PAGES

    clone_static(target_url, out_dir, depth, pages)
