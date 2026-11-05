#!/usr/bin/env python3
"""Run fetch_feed.main() every couple of minutes for most of a GitHub Actions job,
pushing gpt100/feed.json to the `feed` branch whenever it changes.

Usage: feed_loop.py <worktree-dir-of-feed-branch>
"""
import os, shutil, subprocess, sys, time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_feed  # noqa: E402

WT = sys.argv[1]
TARGET = os.path.join(WT, 'feed.json')
RACE_OVER = datetime(2026, 11, 8, 0, 30, tzinfo=timezone.utc).timestamp()   # Sun 11:30 am AEDT, after the 10 am cut-off
INTERVAL = 120
JOB_SECONDS = 5 * 3600 + 35 * 60   # stay under the 6 hour job limit


def git(*args, check=True):
    return subprocess.run(['git', '-C', WT] + list(args), check=check, capture_output=True, text=True)


def push():
    git('add', 'feed.json')
    if git('diff', '--cached', '--quiet', check=False).returncode == 0:
        return False
    msg = 'feed ' + datetime.now(timezone.utc).strftime('%H:%M')
    # keep the branch to a single commit; its history is worthless
    if git('rev-parse', '--verify', 'HEAD', check=False).returncode == 0:
        git('commit', '-q', '--amend', '-m', msg)
    else:
        git('commit', '-q', '-m', msg)
    for attempt in range(3):
        r = git('push', '-q', '--force', 'origin', 'HEAD:feed', check=False)
        if r.returncode == 0:
            return True
        print('push failed:', r.stderr.strip()[:200])
        time.sleep(10)
    return False


def main():
    # work on the feed branch's copy so history accumulates there
    if os.path.exists(TARGET):
        shutil.copy(TARGET, fetch_feed.FEED)
    end = min(time.time() + JOB_SECONDS, RACE_OVER)
    while time.time() < end:
        try:
            fetch_feed.main()
            shutil.copy(fetch_feed.FEED, TARGET)
            if push():
                print('pushed', datetime.now(timezone.utc).strftime('%H:%M:%S'), flush=True)
        except SystemExit:
            pass
        except Exception as e:
            print('loop error:', e, flush=True)
        time.sleep(INTERVAL)
    print('loop finished; race over' if time.time() >= RACE_OVER else 'loop finished; chaining', flush=True)
    sys.exit(2 if time.time() >= RACE_OVER else 0)


if __name__ == '__main__':
    main()
