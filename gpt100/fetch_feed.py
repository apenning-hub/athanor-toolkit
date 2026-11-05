#!/usr/bin/env python3
"""Pull the GPT100 tracker feed for bib 187 (Sam Rosenzweig) and write gpt100/feed.json.

The event's GPS feed (tulospalvelu.fi) only allows its own website to read it from a browser,
so this runs on a schedule in GitHub Actions and publishes a small JSON the page can fetch directly.
"""
import json, os, re, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone

BASE = 'https://www.tulospalvelu.fi/gps/20261106gpt100/'
SAM = 'au187'
EPOCH = 1136073600  # tracker timestamps count seconds from 2006-01-01 UTC
HERE = os.path.dirname(os.path.abspath(__file__))
FEED = os.path.join(HERE, 'feed.json')
UA = {'User-Agent': 'Mozilla/5.0 (gpt100 feed bot; github actions)'}
LINE = re.compile(r'^([A-Za-z0-9]+)\.(\d+)_(-?\d+)_(-?\d+)((?:_[A-Z]-?\d*)*)\.?')


def get(url, headers=None, timeout=60):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, dict(r.headers), r.read()


def load_feed():
    try:
        with open(FEED) as f:
            return json.load(f)
    except Exception:
        return {'sam': [], 'field': {}, 'names': {}, 'lastLine': None, 'offset': 0, 'generated': None}


def parse(text, feed, drop_first=False):
    lines = text.split('\n')
    if drop_first and lines:
        lines = lines[1:]
    seen = {tuple(p[:1]) for p in feed['sam']}  # timestamps already stored
    added = 0
    last_complete = None
    for i, ln in enumerate(lines):
        if len(ln) < 12:
            continue
        m = LINE.match(ln)
        if not m:
            continue
        if i < len(lines) - 1 or text.endswith('\n') or ln.endswith('.'):
            last_complete = ln
        tid = m.group(1)
        t = int(m.group(2)) + EPOCH
        lon = int(m.group(3)) / 5e4
        lat = int(m.group(4)) / 1e5
        bat = spd = None
        for f in (m.group(5) or '').split('_'):
            if f.startswith('B'):
                bat = int(f[1:]) if f[1:].lstrip('-').isdigit() else None
            elif f.startswith('S'):
                spd = int(f[1:]) / 10 if f[1:].lstrip('-').isdigit() else None
        if tid == SAM:
            if (t,) not in seen:
                feed['sam'].append([t, round(lat, 5), round(lon, 5), spd, bat])
                seen.add((t,))
                added += 1
        else:
            cur = feed['field'].get(tid)
            if not cur or t > cur[0]:
                feed['field'][tid] = [t, round(lat, 5), round(lon, 5)]
    if last_complete:
        feed['lastLine'] = last_complete[:29]
    feed['sam'].sort(key=lambda p: p[0])
    return added


def main():
    feed = load_feed()
    if not feed.get('names'):
        try:
            _, _, body = get(BASE + 'init.txt')
            for l in body.decode('utf-8', 'replace').split('\n'):
                if l.startswith('COMPETITOR:'):
                    p = l[11:].split('|')
                    if len(p) > 3:
                        feed['names'][p[0]] = p[3]
        except Exception as e:
            print('init.txt failed:', e)
    offset = int(feed.get('offset') or 0)
    status, headers, body = None, {}, b''
    try:
        if offset > 0:
            status, headers, body = get(BASE + 'data.php?offset=%d' % offset)
        else:
            # cold start: just the tail of the file
            try:
                status, headers, body = get(BASE + 'data.lst', {'Range': 'bytes=-900000'})
            except urllib.error.HTTPError as e:
                if e.code == 416:
                    status, headers, body = get(BASE + 'data.lst')
                else:
                    raise
    except Exception as e:
        print('feed fetch failed:', e)
        sys.exit(0)  # keep the previous feed.json; try again next run
    text = body.decode('utf-8', 'replace')
    partial = status == 206
    size = headers.get('X-GPS-Server-Filesize') or headers.get('x-gps-server-filesize')
    if not size and headers.get('Content-Range'):
        m = re.search(r'/(\d+)\s*$', headers['Content-Range'])
        if m:
            size = m.group(1)
    if offset > 0 and len(text) > 3_000_000 and size and int(size) < offset:
        # the server restarted its file: start again from the tail of what we got
        text = text[-900000:]
        partial = True
    added = parse(text, feed, drop_first=partial)
    if size and size.isdigit():
        feed['offset'] = int(size)
    elif offset > 0:
        feed['offset'] = offset + len(body)
    else:
        feed['offset'] = 0
    # keep the field to the last 3 hours so the file stays small
    cutoff = time.time() - 3 * 3600
    feed['field'] = {k: v for k, v in feed['field'].items() if v[0] >= cutoff}
    feed['generated'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
    feed['generatedMs'] = int(time.time() * 1000)
    with open(FEED, 'w') as f:
        json.dump(feed, f, separators=(',', ':'))
    print('status', status, 'bytes', len(body), 'added', added, 'sam points', len(feed['sam']), 'offset', feed['offset'])


if __name__ == '__main__':
    main()
