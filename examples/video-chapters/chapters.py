#!/usr/bin/env python3
"""Read Bilibili video chapters via HTTP or the Kimi browser daemon."""
import argparse
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class ChapterError(Exception):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ChapterError(message)


def read_json(request):
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def daemon(address, action, args):
    payload = json.dumps({'session': 'bilibili', 'action': action, 'args': args})
    result = read_json(Request(address.rstrip('/') + '/command',
                               data=payload.encode('utf-8'),
                               headers={'Content-Type': 'application/json'}))
    if not result.get('ok'):
        error = result.get('error', {})
        raise ChapterError(f"Kimi {error.get('code')}: {error.get('message')}")
    return result['data']


def setup_browser(address, bvid):
    url = f'https://www.bilibili.com/video/{bvid}/'
    try:
        daemon(address, 'find_tab', {'url': url})
    except ChapterError as exc:
        if 'no tab matching' not in str(exc).lower():
            raise
        daemon(address, 'navigate', {'url': url, 'newTab': True,
                                     'group_title': 'B站视频章节接口分析'})
    else:
        daemon(address, 'navigate', {'url': url})


def api(args, path, params, fields):
    url = 'https://api.bilibili.com' + path + '?' + urlencode(params)
    if args.transport == 'http':
        body = read_json(Request(url, headers={
            'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.bilibili.com/'}))
    else:
        # Whitelist fields before crossing the browser boundary; no cookies,
        # login_mid, ip_info or signed media URLs are exported.
        code = '''(async()=>{
          const r=await fetch(URL,{credentials:CREDENTIALS});
          if(!r.ok) throw new Error('HTTP '+r.status);
          const b=await r.json(); const d=b.data||{};
          return JSON.stringify({code:b.code,message:b.message,
            data:Object.fromEntries(FIELDS.filter(k=>k in d).map(k=>[k,d[k]]))});
        })()'''.replace('URL', json.dumps(url)).replace(
            'CREDENTIALS', json.dumps(args.credentials)).replace('FIELDS', json.dumps(fields))
        result = daemon(args.daemon_url, 'evaluate', {'code': code})
        value = result.get('value')
        if not isinstance(value, str):
            raise ChapterError('Browser evaluate did not return JSON text')
        body = json.loads(value)
    if not isinstance(body, dict) or body.get('code') != 0:
        raise ChapterError(f"API failed: {body.get('code')} {body.get('message')}"
                           if isinstance(body, dict) else 'Invalid API response')
    if not isinstance(body.get('data'), dict):
        raise ChapterError('Missing API data object')
    return body['data']


def validate_points(points, duration):
    if not isinstance(points, list):
        raise ChapterError('Missing or invalid view_points array')
    def number(value):
        return type(value) in (int, float) and math.isfinite(value)
    if not number(duration) or duration <= 0:
        raise ChapterError('Invalid page duration')
    previous = -1
    for point in points:
        if not isinstance(point, dict) or not isinstance(point.get('content'), str):
            raise ChapterError('Invalid chapter object or title')
        start, end = point.get('from'), point.get('to')
        if not number(start) or not number(end) or not 0 <= start <= end <= duration:
            raise ChapterError('Invalid chapter time range')
        if start < previous:
            raise ChapterError('Chapters are not sorted by start time')
        previous = start
    return points


def run(args):
    if not re.fullmatch(r'BV[0-9A-Za-z]{10}', args.bvid):
        raise ChapterError('Expected a BV identifier, e.g. BV1vL411G7N7')
    if args.page < 1:
        raise ChapterError('--page must be positive')
    if args.transport == 'http' and args.credentials != 'omit':
        raise ChapterError('--credentials include requires --transport kimi')
    if args.transport == 'kimi':
        setup_browser(args.daemon_url, args.bvid)
    video = api(args, '/x/web-interface/view', {'bvid': args.bvid},
                ['aid', 'bvid', 'title', 'pages'])
    if video.get('bvid') != args.bvid or type(video.get('aid')) is not int:
        raise ChapterError('Video identity mismatch')
    pages = video.get('pages')
    if not isinstance(pages, list):
        raise ChapterError('Missing pages array')
    page = next((p for p in pages if isinstance(p, dict) and p.get('page') == args.page), None)
    if page is None or type(page.get('cid')) is not int:
        raise ChapterError('Requested page is absent or has invalid cid')
    player = api(args, '/x/player/wbi/v2', {'aid': video['aid'], 'cid': page['cid']},
                 ['aid', 'bvid', 'cid', 'view_points'])
    if any(player.get(k) != v for k, v in
           {'aid': video['aid'], 'bvid': args.bvid, 'cid': page['cid']}.items()):
        raise ChapterError('Player identity mismatch')
    points = validate_points(player.get('view_points'), page.get('duration'))
    return {'bvid': args.bvid, 'aid': video['aid'], 'cid': page['cid'],
            'title': video.get('title'), 'page': args.page, 'duration': page['duration'],
            'view_points': points}


def main():
    parser = Parser(description=__doc__)
    parser.add_argument('bvid')
    parser.add_argument('--page', type=int, default=1)
    parser.add_argument('--transport', choices=['http', 'kimi'], default='http')
    parser.add_argument('--daemon-url', default='http://127.0.0.1:10086')
    parser.add_argument('--credentials', choices=['omit', 'include'], default='omit')
    parser.add_argument('--output', type=Path, help='Save the same JSON envelope to a file')
    try:
        args = parser.parse_args()
        result = {'ok': True, 'data': run(args)}
        output = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(output + '\n', encoding='utf-8')
        print(output)
        return 0
    except Exception as exc:
        print(json.dumps({'ok': False, 'error': {
            'code': type(exc).__name__, 'message': str(exc)}}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
