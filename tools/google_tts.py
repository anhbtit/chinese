#!/usr/bin/env python3
"""Generate pronunciation mp3 files for the HSK1 flashcards with Google Cloud Text-to-Speech.

- Words: read with the exact pinyin on the card (SSML <phoneme alphabet="pinyin">), so polyphonic
  characters such as 地 de/dì, 还 hái/huán and neutral tones 吧/呢/了… match the card. Words whose
  pinyin cannot be forced (or that Google rejects) are read as plain Chinese text.
- Example sentences: read as whole sentences (enough context for TTS to pick the right reading).

Requires the GOOGLE_TTS_API_KEY environment variable (an API key for a project with the
"Cloud Text-to-Speech API" enabled).

Usage:
  python3 tools/google_tts.py --dry-run           # check pinyin splitting, no Google calls
  python3 tools/google_tts.py                     # generate missing files
  python3 tools/google_tts.py --only 67,76 --force  # regenerate a few words
  python3 tools/google_tts.py --list-voices       # list the voices that exist
  python3 tools/google_tts.py --voice-male <name> --voice-female <name>   # change voices
  python3 tools/google_tts.py --gender m          # male voice only
Both a male and a female voice are generated; the page alternates male / female on each press.
Output: audio/{m,f}/w/<No>.mp3 (words), audio/{m,f}/x/<No>.mp3 (examples), audio/index.js (file list for the page).
"""
import argparse
import base64
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from xml.sax.saxutils import escape, unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'assets', 'hsk1-data.js')
OUT = os.path.join(ROOT, 'audio')
API = 'https://texttospeech.googleapis.com/v1/text:synthesize'

# ---------- pinyin -> numbered-tone pinyin ----------
TONED = {}
for base, marks in {'a': 'āáǎà', 'e': 'ēéěè', 'i': 'īíǐì', 'o': 'ōóǒò', 'u': 'ūúǔù', 'ü': 'ǖǘǚǜ'}.items():
    for t, ch in enumerate(marks, 1):
        TONED[ch] = (base, t)

INITIALS = 'b p m f d t n l g k h j q x zh ch sh r z c s'.split()
FINALS = ('a o e ai ei ao ou an en ang eng ong i ia ie iao iu ian in iang ing iong '
          'u ua uo uai ui uan un uang ü üe üan ün ue').split()
SYLLABLES = {i + f for i in INITIALS for f in FINALS}
SYLLABLES |= {'y' + f for f in 'a o e ao ou an ang i in ing ong u ue uan un'.split()}
SYLLABLES |= {'w' + f for f in 'a o ai ei an en ang eng u'.split()}
SYLLABLES |= set('a o e ai ei ao ou an en ang eng er'.split())
MAXLEN = max(map(len, SYLLABLES))


def split_chunk(chunk):
    """'diànyǐngyuàn' -> [('dian',4),('ying',3),('yuan',4)]; erhua (…r) is only allowed at the end."""
    base, tones = '', []
    for ch in chunk:
        if ch in TONED:
            b, t = TONED[ch]
            base += b
            tones.append(t)
        else:
            base += ch
            tones.append(0)

    results = []

    def walk(i, acc):
        if i == len(base):
            results.append(acc)
            return
        for j in range(min(len(base), i + MAXLEN + 1), i, -1):
            s = base[i:j]
            tone = max(tones[i:j]) or 5
            if s in SYLLABLES:
                walk(j, acc + [(s, tone, False)])
            elif j == len(base) and s.endswith('r') and s[:-1] in SYLLABLES and s != 'er':
                walk(j, acc + [(s[:-1], tone, True)])

    walk(0, [])
    return results


def to_pinyin_ph(hz, py):
    """Return a ph string like 'ni3 hao3' for SSML <phoneme alphabet="pinyin">, or None when unsure
    (the characters are then read normally). Erhua words (…r) also return None since the syntax is unclear."""
    n_hz = len(re.findall(r'[一-鿿〇]', hz))
    p = unicodedata.normalize('NFC', py.lower())
    p = re.sub(r"//|-|'|’", ' ', p)
    p = p.replace('·', ' ·')  # '·' before a syllable usually means neutral tone (出来 chū//·lái -> chūlai)
    p = re.sub(r'[^a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü· ]', ' ', p)
    chunks = [c for c in p.split() if c.strip('·')]
    if not chunks:
        return None
    options = []
    for c in chunks:
        segs = split_chunk(c.strip('·'))
        if c.startswith('·'):
            segs = [[(s[0][0], 5, s[0][2])] + s[1:] for s in segs]
        options.append(segs)
    if any(not o for o in options):
        return None

    def count(seg):
        return sum(2 if er else 1 for _, _, er in seg)

    # pick a split for each chunk so the total syllable count matches the number of characters
    best = None

    def combine(k, acc, total):
        nonlocal best
        if best is not None:
            return
        if k == len(options):
            if total == n_hz:
                best = acc
            return
        for seg in options[k]:
            combine(k + 1, acc + seg, total + count(seg))

    combine(0, [], 0)
    if best is None:
        return None
    if any(er for _, _, er in best):
        return None
    out = []
    for s, t, _ in best:
        s = s.replace('üe', 've').replace('ü', 'v')
        out.append(f'{s}{t}')
    return ' '.join(out)


def word_parts(hz, py):
    """Split variants: '爸爸 ｜ 爸' / 'bàba ｜ bà' -> [('爸爸','bàba'), ('爸','bà')]; '第(第二)' -> 第, 第二."""
    hzs = [x.strip() for x in hz.split('｜')]
    pys = [x.strip() for x in py.split('｜')]
    if len(hzs) != len(pys):
        return [(re.sub(r'[()（）｜\s]', '', hz), None)]
    parts = []
    for h, p in zip(hzs, pys):
        alts = re.split(r'(?<!/)/(?!/)', p)  # single '/' = two readings; '//' marks a separable verb
        if len(alts) > 1:  # 谁 shéi/shuí -> read both
            parts += [(h, alt) for alt in alts]
            continue
        m, mp = re.fullmatch(r'(.+?)\((.+)\)', h), re.fullmatch(r'(.+?)\s+\((.+)\)', p)
        if m and mp:  # 们(朋友们) / men (péngyoumen)
            parts += [(m.group(1), mp.group(1)), (m.group(2), mp.group(2))]
        else:          # 有(一)些 / yǒu(yì)xiē -> read as one
            parts.append((re.sub(r'[()（）]', '', h), re.sub(r'[()（）]', ' ', p)))
    return parts


def word_ssml_body(hz, py):
    pieces, plain = [], []
    for h, p in word_parts(hz, py):
        ph = to_pinyin_ph(h, p) if p else None
        if ph:
            pieces.append(f'<phoneme alphabet="pinyin" ph="{ph}">{escape(h)}</phoneme>')
        else:
            pieces.append(escape(h))
            plain.append(h)
    return '<break time="400ms"/>'.join(pieces), plain


def ssml(body):
    return f'<speak>{body}</speak>'


# ---------- Google Cloud TTS ----------
def synth(key, xml, voice, rate, retries=6):
    if 'Chirp' in voice:   # Chirp3-HD does not accept SSML: send plain text (pinyin can no longer be forced)
        text = re.sub(r'<[^>]+>', '', xml.replace('<break time="400ms"/>', '， '))
        inp = {'text': unescape(text)}
    else:
        inp = {'ssml': xml}
    payload = {
        'input': inp,
        'voice': {'languageCode': 'cmn-CN', 'name': voice},
        'audioConfig': {'audioEncoding': 'MP3', 'speakingRate': rate, 'sampleRateHertz': 24000},
    }
    req = urllib.request.Request(API, data=json.dumps(payload).encode('utf-8'), method='POST', headers={
        'X-Goog-Api-Key': key,
        'Content-Type': 'application/json; charset=utf-8',
    })
    delay = 2
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                audio = json.load(r).get('audioContent')
                if not audio:
                    raise RuntimeError('Google trả về file rỗng')
                return base64.b64decode(audio)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                wait = int(e.headers.get('Retry-After') or delay)
                print(f'    Google {e.code}, chờ {wait}s rồi thử lại…')
                time.sleep(wait)
                delay = min(delay * 2, 60)
                continue
            body = e.read().decode('utf-8', 'replace')[:300]
            raise RuntimeError(f'HTTP {e.code}: {body}') from None
        except urllib.error.URLError as e:
            if attempt < retries - 1:
                time.sleep(delay)
                delay = min(delay * 2, 60)
                continue
            raise RuntimeError(f'Lỗi mạng: {e.reason}') from None


def load_vocab():
    js = open(PAGE, encoding='utf-8').read()
    m = re.search(r'^const HSK1_VOCAB = (.*);$', js, re.M)
    if not m:
        sys.exit(f'Không tìm thấy dữ liệu HSK1_VOCAB trong {PAGE}')
    return json.loads(m.group(1))


GENDERS = {'f': 'nữ', 'm': 'nam'}


def write_index(voices):
    def ids(g, sub):
        d = os.path.join(OUT, g, sub)
        if not os.path.isdir(d):
            return []
        return sorted(int(f[:-4]) for f in os.listdir(d) if f.endswith('.mp3') and f[:-4].isdigit()
                      and os.path.getsize(os.path.join(d, f)) > 0)
    data = {g: {'voice': voices[g], 'w': ids(g, 'w'), 'x': ids(g, 'x')} for g in GENDERS}
    with open(os.path.join(OUT, 'index.js'), 'w', encoding='utf-8') as f:
        f.write('window.HSK_AUDIO = ' + json.dumps(data) + ';\n')
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--voice-female', default='cmn-CN-Wavenet-A', help='giọng nữ (mặc định: cmn-CN-Wavenet-A)')
    ap.add_argument('--voice-male', default='cmn-CN-Wavenet-B', help='giọng nam (mặc định: cmn-CN-Wavenet-B)')
    ap.add_argument('--gender', choices=['both', 'f', 'm'], default='both', help='tạo giọng nào (mặc định: both)')
    ap.add_argument('--word-rate', type=float, default=0.85, help='tốc độ đọc từ, 1.0 = bình thường (mặc định 0.85)')
    ap.add_argument('--example-rate', type=float, default=0.95, help='tốc độ đọc câu ví dụ (mặc định 0.95)')
    ap.add_argument('--only', help='chỉ tạo các STT này, vd: 1,5,67')
    ap.add_argument('--force', action='store_true', help='tạo lại cả file đã có')
    ap.add_argument('--no-examples', action='store_true', help='bỏ qua câu ví dụ')
    ap.add_argument('--list-voices', action='store_true', help='in danh sách giọng cmn-CN của Google rồi thoát')
    ap.add_argument('--dry-run', action='store_true', help='chỉ in SSML/kiểm tra pinyin, không gọi Google')
    args = ap.parse_args()
    voices = {'f': args.voice_female, 'm': args.voice_male}
    genders = list(GENDERS) if args.gender == 'both' else [args.gender]

    if args.list_voices:
        key = os.environ.get('GOOGLE_TTS_API_KEY') or sys.exit('Thiếu biến môi trường GOOGLE_TTS_API_KEY.')
        req = urllib.request.Request(API.replace('text:synthesize', 'voices?languageCode=cmn-CN'),
                                     headers={'X-Goog-Api-Key': key})
        with urllib.request.urlopen(req, timeout=30) as r:
            for v in sorted(json.load(r).get('voices', []), key=lambda v: v['name']):
                print(f"{v['name']:<28} {v['ssmlGender']}")
        return

    vocab = load_vocab()
    if args.only:
        only = {int(x) for x in args.only.split(',') if x.strip()}
        vocab = [v for v in vocab if v['id'] in only]

    # job: (gender, kind, id, ssml, plain, rate, vocab item)
    jobs = []
    for g in genders:
        for v in vocab:
            body, plain = word_ssml_body(v['hz'], v['py'])
            jobs.append((g, 'w', v['id'], ssml(body), plain, args.word_rate, v))
            if not args.no_examples and v.get('x'):
                jobs.append((g, 'x', v['id'], ssml(escape(v['x'][0])), [], args.example_rate, v))

    if args.dry_run:
        n_plain = 0
        for g, kind, i, xml, plain, _, v in jobs:
            if kind == 'w' and g == genders[0]:
                flag = '  <-- đọc chữ Hán thường (không ép pinyin)' if plain else ''
                n_plain += bool(plain)
                print(f'{i:>3} {v["hz"]:<12} {v["py"]:<22} {xml[7:-8]}{flag}')
        chars = sum(len(j[3]) for j in jobs)
        print(f'\n{len(jobs)} file sẽ tạo ({" + ".join(f"{GENDERS[g]}: {voices[g]}" for g in genders)}; '
              f'~{chars} ký tự SSML); {n_plain} từ không ép được pinyin.')
        return

    key = os.environ.get('GOOGLE_TTS_API_KEY')
    if not key:
        sys.exit('Thiếu biến môi trường GOOGLE_TTS_API_KEY.')

    for g in genders:
        os.makedirs(os.path.join(OUT, g, 'w'), exist_ok=True)
        os.makedirs(os.path.join(OUT, g, 'x'), exist_ok=True)
    done = skipped = failed = 0
    for n, (g, kind, i, xml, plain, rate, v) in enumerate(jobs, 1):
        path = os.path.join(OUT, g, kind, f'{i}.mp3')
        if not args.force and os.path.exists(path) and os.path.getsize(path) > 0:
            skipped += 1
            continue
        label = v['hz'] if kind == 'w' else v['x'][0]
        print(f'[{n}/{len(jobs)}] {g} {kind} #{i} {label}')
        try:
            try:
                data = synth(key, xml, voices[g], rate)
            except RuntimeError as e:
                if 'does not exist' in str(e):
                    sys.exit(f'Giọng "{voices[g]}" không hợp lệ: chạy --list-voices để xem tên đúng.\n{e}')
                if kind == 'w' and 'HTTP 400' in str(e) and '<phoneme' in xml:
                    print('    Google không nhận pinyin, đọc chữ Hán thường.')
                    plain_xml = ssml(escape(re.sub(r'[()（）｜\s]', '', v['hz'])))
                    data = synth(key, plain_xml, voices[g], rate)
                else:
                    raise
            with open(path, 'wb') as f:
                f.write(data)
            done += 1
        except RuntimeError as e:
            failed += 1
            print(f'    LỖI: {e}')
            if 'HTTP 401' in str(e) or 'HTTP 403' in str(e):
                sys.exit('API key không hợp lệ hoặc chưa bật Cloud Text-to-Speech API, dừng lại.')
        time.sleep(0.1)

    idx = write_index(voices)
    summary = ', '.join(f'{GENDERS[g]}: {len(idx[g]["w"])} từ + {len(idx[g]["x"])} ví dụ' for g in GENDERS)
    print(f'\nXong: tạo {done}, bỏ qua {skipped} (đã có), lỗi {failed}. Hiện có {summary}.')


if __name__ == '__main__':
    main()
