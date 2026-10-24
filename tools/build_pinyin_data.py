#!/usr/bin/env python3
"""Generate assets/pinyin-data.js and audio/pinyin/ for the pinyin syllable table page (index.html).

Reads the file list of the zispace/hanyu-pinyin-audio repo (data branch) via the GitHub API:
- A syllable is included if it has playable audio (see below), or audio in at least MIN_SOURCES
  sources in the repo (filters out odd file names found in only 1–2 sources); those are shown muted.
- Audio played on the page comes ONLY from the github-hugolpz/audio folder – recordings by Chen Wang
  (hugolpz/audio-cmn project, CC BY-SA). The other sources in the repo have no clear license,
  so they are not used for playback.
The playable mp3 files are downloaded (via jsDelivr) into audio/pinyin/ so the page has no
runtime dependency on that repo. Existing files are kept; pass --force to download them again.

Usage: python3 tools/build_pinyin_data.py [--force]
"""
import argparse
import json
import os
import re
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'pinyin-data.js')
TREE = 'https://api.github.com/repos/zispace/hanyu-pinyin-audio/git/trees/data?recursive=1'
PLAY_DIR = 'github-hugolpz/audio'
MIN_SOURCES = 3
CDN_BASE = 'https://cdn.jsdelivr.net/gh/zispace/hanyu-pinyin-audio@data/' + PLAY_DIR + '/'
AUDIO_DIR = os.path.join(ROOT, 'audio', 'pinyin')
AUDIO_BASE = 'audio/pinyin/'   # relative to the site root (index.html)

INITIALS = ['', 'b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'j', 'q', 'x',
            'zh', 'ch', 'sh', 'r', 'z', 'c', 's']
# (final key, column label, spelling after an initial)
FINALS = [
    ('a', 'a', 'a'), ('ai', 'ai', 'ai'), ('an', 'an', 'an'), ('ang', 'ang', 'ang'), ('ao', 'ao', 'ao'),
    ('e', 'e', 'e'), ('ê', 'ê', 'ê'), ('ei', 'ei', 'ei'), ('en', 'en', 'en'), ('eng', 'eng', 'eng'),
    ('er', 'er', 'er'), ('i', 'i', 'i'), ('-i1', '-i[ʅ]', 'i'), ('-i2', '-i[ɿ]', 'i'),
    ('ia', 'ia', 'ia'), ('ian', 'ian', 'ian'), ('iang', 'iang', 'iang'), ('iao', 'iao', 'iao'),
    ('ie', 'ie', 'ie'), ('in', 'in', 'in'), ('ing', 'ing', 'ing'), ('iong', 'iong', 'iong'),
    ('iou', 'iu', 'iu'), ('o', 'o', 'o'), ('ong', 'ong', 'ong'), ('ou', 'ou', 'ou'),
    ('u', 'u', 'u'), ('ua', 'ua', 'ua'), ('uai', 'uai', 'uai'), ('uan', 'uan', 'uan'),
    ('uang', 'uang', 'uang'), ('uei', 'ui', 'ui'), ('uen', 'un', 'un'), ('ueng', 'ueng', 'ueng'),
    ('uo', 'uo', 'uo'), ('ü', 'ü', 'ü'), ('üan', 'üan', 'üan'), ('üe', 'üe', 'üe'), ('ün', 'ün', 'ün'),
]
ZERO = {  # spelling without an initial
    'i': 'yi', 'ia': 'ya', 'ian': 'yan', 'iang': 'yang', 'iao': 'yao', 'ie': 'ye', 'in': 'yin',
    'ing': 'ying', 'iong': 'yong', 'iou': 'you', 'u': 'wu', 'ua': 'wa', 'uai': 'wai', 'uan': 'wan',
    'uang': 'wang', 'uei': 'wei', 'uen': 'wen', 'ueng': 'weng', 'uo': 'wo', 'ü': 'yu', 'üan': 'yuan',
    'üe': 'yue', 'ün': 'yun', '-i1': None, '-i2': None, 'ong': None,
}


def spell(ini, key, written):
    if ini == '':
        return ZERO.get(key, written)
    if key in ('er', 'ê', 'ueng'):
        return None
    if key == '-i1':
        return ini + 'i' if ini in ('zh', 'ch', 'sh', 'r') else None
    if key == '-i2':
        return ini + 'i' if ini in ('z', 'c', 's') else None
    if key == 'i' and ini in ('zh', 'ch', 'sh', 'r', 'z', 'c', 's'):
        return None
    if ini in ('j', 'q', 'x'):
        if key.startswith('ü'):
            return ini + written.replace('ü', 'u')
        if key.startswith('u'):
            return None
    return ini + written


def audio_key(s):
    return s.replace('ü', 'v')


def download(name, force):
    path = os.path.join(AUDIO_DIR, name)
    if not force and os.path.exists(path) and os.path.getsize(path) > 0:
        return 'kept'
    req = urllib.request.Request(CDN_BASE + name, headers={'User-Agent': 'pinyin-table'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            if not data:
                raise OSError('empty file')
            with open(path, 'wb') as f:
                f.write(data)
            return 'new'
        except OSError as e:
            err = e
    return f'error: {err}'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--force', action='store_true', help='download audio files again even if present')
    args = ap.parse_args()

    with urllib.request.urlopen(urllib.request.Request(TREE, headers={'User-Agent': 'pinyin-table'}), timeout=60) as r:
        tree = json.load(r)['tree']
    sources, tones = defaultdict(set), defaultdict(set)
    for item in tree:
        if item['type'] != 'blob':
            continue
        d, _, f = item['path'].rpartition('/')
        m = re.fullmatch(r'([a-zü]+)([1-5])\.(mp3|wav)', f)
        if not m or d.startswith('misc'):
            continue
        k = m.group(1).replace('ü', 'v')
        sources[k].add(d)
        if d == PLAY_DIR and m.group(2) != '5':   # the *5.mp3 files there are not Mandarin recordings
            tones[k].add(int(m.group(2)))

    rows = []
    n_cells = n_play = 0
    for ini in INITIALS:
        row = []
        for key, _, written in FINALS:
            s = spell(ini, key, written)
            k = s and audio_key(s)
            if not s or (k not in tones and len(sources.get(k, ())) < MIN_SOURCES):
                row.append(None)
                continue
            t = sorted(tones.get(k, ()))
            row.append([s, t] if t else [s])
            n_cells += 1
            n_play += bool(t)
        rows.append(row)

    # download the playable files and drop stale ones
    os.makedirs(AUDIO_DIR, exist_ok=True)
    wanted = {f'{k}{t}.mp3' for k, ts in tones.items() for t in ts
              if any(c and audio_key(c[0]) == k for row in rows for c in row)}
    with ThreadPoolExecutor(8) as pool:
        results = dict(zip(sorted(wanted), pool.map(lambda n: download(n, args.force), sorted(wanted))))
    errors = {n: r for n, r in results.items() if r.startswith('error')}
    for name in os.listdir(AUDIO_DIR):
        if name.endswith('.mp3') and name not in wanted:
            os.remove(os.path.join(AUDIO_DIR, name))
    for n, r in sorted(errors.items()):
        print(f'  {n}: {r}')
    if errors:
        raise SystemExit(f'{len(errors)} file(s) failed to download – run the script again to retry.')
    print(f'audio/pinyin: {len(wanted)} files ({sum(r == "new" for r in results.values())} newly downloaded)')

    data = {
        'audioBase': AUDIO_BASE,
        'initials': INITIALS,
        'finals': [[key, label] for key, label, _ in FINALS],
        'rows': rows,
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('// Generated by tools/build_pinyin_data.py – do not edit by hand.\n')
        f.write('const PINYIN_DATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print(f'{n_cells} syllables, {n_play} with playable audio -> {os.path.relpath(OUT, ROOT)}')


if __name__ == '__main__':
    main()
