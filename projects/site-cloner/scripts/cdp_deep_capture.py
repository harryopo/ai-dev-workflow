"""
CDP DevTools 深度抓取脚本 (v1.2.0)
使用 Chrome DevTools Protocol Network 域完整捕获请求/响应体/WebSocket帧。
当 Playwright 高层 API 无法获取 POST body/WS 帧时使用。
"""

import json
import sys
import time
import os
from pathlib import Path
from urllib.parse import urlparse


def capture_with_cdp(target_url, output_dir, max_duration_seconds=60):
    """
    使用 Playwright CDP Session 进行深度网络抓取。
    
    捕获内容：
    - 所有请求头（包括 Authorization/Cookie）
    - 所有 POST/PUT 请求体（Network.getRequestPostData）
    - 所有响应体（Network.getResponseBody，含二进制 base64）
    - WebSocket 帧（Network.webSocketFrameReceived/Sent）
    - 请求时序（timing）
    - 重定向链
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright 未安装。安装命令: pip install playwright && playwright install chromium")
        return None

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    network_calls = []
    websocket_frames = []
    request_bodies = {}
    redirect_chains = {}

    print(f"CDP 深度抓取: {target_url}")
    print(f"输出目录: {output_dir}")
    print("-" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        # 创建 CDP Session
        cdp = page.context.new_cdp_session(page)

        # 启用 Network 域
        cdp.send('Network.enable', {
            'maxTotalBufferSize': 100000000,
            'maxResourceBufferSize': 50000000
        })

        # 监听网络事件
        def on_request_will_be_sent(params):
            request_id = params['requestId']
            request = params['request']
            redirect = params.get('redirectResponse')

            call_info = {
                'requestId': request_id,
                'url': request['url'],
                'method': request['method'],
                'headers': request.get('headers', {}),
                'postData': request.get('postData'),
                'hasPostData': request.get('hasPostData', False),
                'timestamp': params.get('timestamp'),
                'type': params.get('type', ''),
                'initiator': params.get('initiator', {}),
                'isRedirect': bool(redirect)
            }

            if redirect:
                call_info['redirectResponse'] = {
                    'status': redirect.get('status'),
                    'headers': redirect.get('headers', {}),
                    'url': redirect.get('url')
                }
                redirect_chains[request_id] = redirect.get('url')

            network_calls.append(call_info)

            # 如果有 POST 数据，尝试获取
            if request.get('hasPostData') and not request.get('postData'):
                try:
                    post_data_result = cdp.send('Network.getRequestPostData', {
                        'requestId': request_id
                    })
                    call_info['postData'] = post_data_result.get('postData', '')
                except Exception:
                    pass

        def on_response_received(params):
            request_id = params['requestId']
            response = params['response']

            # 找到对应的请求并更新
            for call in network_calls:
                if call['requestId'] == request_id:
                    call['responseStatus'] = response.get('status')
                    call['responseHeaders'] = response.get('headers', {})
                    call['mimeType'] = response.get('mimeType', '')
                    call['fromCache'] = response.get('fromDiskCache') or response.get('fromMemoryCache', False)
                    call['remoteIPAddress'] = response.get('remoteIPAddress', '')
                    call['connectionId'] = response.get('connectionId')
                    call['timing'] = response.get('timing', {})
                    break

        def on_loading_finished(params):
            request_id = params['requestId']
            encoded_length = params.get('encodedDataLength', 0)

            # 找到对应的请求
            for call in network_calls:
                if call['requestId'] == request_id:
                    call['encodedDataLength'] = encoded_length
                    break

            # 获取响应体（仅对 API 调用）
            target_call = None
            for call in network_calls:
                if call['requestId'] == request_id:
                    target_call = call
                    break

            if target_call and (
                'application/json' in target_call.get('mimeType', '') or
                'api' in target_call.get('url', '').lower() or
                target_call.get('method') == 'POST'
            ):
                try:
                    body_result = cdp.send('Network.getResponseBody', {
                        'requestId': request_id
                    })
                    body = body_result.get('body', '')
                    base64 = body_result.get('base64Encoded', False)
                    target_call['responseBody'] = body
                    target_call['responseBodyBase64'] = base64
                except Exception:
                    target_call['responseBodyError'] = '无法获取响应体'

        def on_ws_created(params):
            ws_info = {
                'requestId': params['requestId'],
                'url': params['url'],
                'type': 'websocket_created',
                'timestamp': time.time()
            }
            websocket_frames.append(ws_info)

        def on_ws_frame(params):
            ws_info = {
                'requestId': params['requestId'],
                'type': 'websocket_frame',
                'response': params.get('response', {}),
                'timestamp': params.get('timestamp'),
                'payloadData': params.get('response', {}).get('payloadData', '')[:5000]  # 限制长度
            }
            websocket_frames.append(ws_info)

        # 注册 CDP 事件监听
        cdp.on('Network.requestWillBeSent', on_request_will_be_sent)
        cdp.on('Network.responseReceived', on_response_received)
        cdp.on('Network.loadingFinished', on_loading_finished)
        cdp.on('Network.webSocketCreated', on_ws_created)
        cdp.on('Network.webSocketFrameReceived', on_ws_frame)

        # 导航到目标页面
        try:
            page.goto(target_url, wait_until='networkidle', timeout=45000)
            page.wait_for_timeout(2000)

            # 滚动触发懒加载
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            page.wait_for_timeout(1000)
            page.evaluate('window.scrollTo(0, 0)')

            # 等待额外请求
            wait_start = time.time()
            while time.time() - wait_start < max_duration_seconds:
                page.wait_for_timeout(2000)
                # 如果 3 秒内没有新请求，退出
                current_count = len(network_calls)
                page.wait_for_timeout(3000)
                if len(network_calls) == current_count:
                    break

        except Exception as e:
            print(f"  页面加载/等待异常: {e}")

        browser.close()

    # 保存结果
    print("-" * 60)
    print(f"捕获完成!")

    # 统计
    api_calls = [c for c in network_calls if
                 'application/json' in c.get('mimeType', '') or
                 'api' in c.get('url', '').lower()]

    stats = {
        'total_requests': len(network_calls),
        'api_requests': len(api_calls),
        'websocket_frames': len(websocket_frames),
        'requests_with_post_body': sum(1 for c in network_calls if c.get('postData')),
        'requests_with_response_body': sum(1 for c in network_calls if c.get('responseBody')),
        'redirects': len(redirect_chains)
    }

    print(f"  总请求数: {stats['total_requests']}")
    print(f"  API请求: {stats['api_requests']}")
    print(f"  WebSocket帧: {stats['websocket_frames']}")
    print(f"  POST请求体: {stats['requests_with_post_body']}")
    print(f"  响应体: {stats['requests_with_response_body']}")
    print(f"  重定向: {stats['redirects']}")

    # 保存网络调用
    with open(output_dir / 'cdp_network_calls.json', 'w', encoding='utf-8') as f:
        json.dump(network_calls, f, ensure_ascii=False, indent=2)

    # 保存 WebSocket 帧
    if websocket_frames:
        with open(output_dir / 'cdp_websocket_frames.json', 'w', encoding='utf-8') as f:
            json.dump(websocket_frames, f, ensure_ascii=False, indent=2)

    # 保存统计数据
    with open(output_dir / 'cdp_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    return {'network_calls': network_calls, 'ws_frames': websocket_frames, 'stats': stats}


def extract_api_endpoints_from_cdp(cdp_data, base_url=""):
    """从 CDP 捕获的数据中提取 API 端点（类似 analyze_apis.py）"""
    network_calls = cdp_data.get('network_calls', [])

    endpoints = {}
    for call in network_calls:
        if 'application/json' not in call.get('mimeType', '') and 'api' not in call.get('url', '').lower():
            continue

        parsed = urlparse(call['url'])
        path = parsed.path
        # 规范化
        parts = [p if not p.isdigit() else ':id' for p in path.split('/') if p]
        endpoint = '/' + '/'.join(parts) if parts else '/'

        if endpoint not in endpoints:
            endpoints[endpoint] = {
                'endpoint': endpoint,
                'methods': set(),
                'has_auth': False,
                'sample_request': None,
                'sample_response': None,
                'post_bodies': [],
                'response_bodies': []
            }

        ep = endpoints[endpoint]
        ep['methods'].add(call['method'])

        if call.get('headers', {}).get('authorization') or call.get('headers', {}).get('x-auth-token'):
            ep['has_auth'] = True

        if call.get('postData') and not ep.get('sample_request'):
            ep['sample_request'] = call['postData'][:2000]
            ep['post_bodies'].append(call['postData'])

        if call.get('responseBody') and not ep.get('sample_response'):
            ep['sample_response'] = call['responseBody'][:5000]
            ep['response_bodies'].append(call['responseBody'])

    # 转换 set 为 list
    for ep in endpoints.values():
        ep['methods'] = list(ep['methods'])

    return list(endpoints.values())


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python cdp_deep_capture.py <URL> <输出目录> [最大等待秒数]")
        print("示例: python cdp_deep_capture.py https://example.com ./cdp_output 30")
        sys.exit(1)

    target_url = sys.argv[1]
    out_dir = sys.argv[2]
    max_wait = int(sys.argv[3]) if len(sys.argv) > 3 else 60

    result = capture_with_cdp(target_url, out_dir, max_wait)

    if result:
        endpoints = extract_api_endpoints_from_cdp(result, target_url)
        print(f"\n提取的 API 端点: {len(endpoints)} 个")
        for ep in endpoints:
            print(f"  [{', '.join(ep['methods'])}] {ep['endpoint']}")

        with open(Path(out_dir) / 'cdp_api_endpoints.json', 'w', encoding='utf-8') as f:
            json.dump(endpoints, f, ensure_ascii=False, indent=2)
