#!/usr/bin/env python3
"""Tạo file mp3 phát âm cho flashcard HSK1 bằng Google Cloud Text-to-Speech.

- Từ vựng: đọc theo đúng pinyin trên thẻ (SSML <phoneme alphabet="pinyin">), nên chữ đa âm
  như 地 de/dì, 还 hái/huán, thanh nhẹ 吧/呢/了… đọc đúng như thẻ. Từ nào không ép được pinyin
  (hoặc Google từ chối) thì đọc chữ Hán thường.
- Câu ví dụ: đọc nguyên câu (ngữ cảnh đủ để TTS chọn đúng âm).

Cần biến môi trường GOOGLE_TTS_API_KEY (API key của project đã bật "Cloud Text-to-Speech API").
Giọng WaveNet/Neural2 miễn phí 1 triệu ký tự/tháng; bộ HSK1 chỉ dùng vài chục nghìn ký tự.

Cách dùng:
  python3 tools/google_tts.py --dry-run           # kiểm tra tách pinyin, không gọi Google
  python3 tools/google_tts.py                     # tạo các file còn thiếu
  python3 tools/google_tts.py --only 67,76 --force  # tạo lại vài từ
  python3 tools/google_tts.py --list-voices       # xem giọng có thật
  python3 tools/google_tts.py --voice <tên giọng>  # đổi giọng
Kết quả: audio/w/<STT>.mp3 (từ), audio/x/<STT>.mp3 (câu ví dụ), audio/index.js (danh sách cho trang).
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
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'assets', 'hsk1-data.js')
OUT = os.path.join(ROOT, 'audio')
API = 'https://texttospeech.googleapis.com/v1/text:synthesize'

# ---------- pinyin -> pinyin có số thanh ----------
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
    """'diànyǐngyuàn' -> [('dian',4),('ying',3),('yuan',4)]; chỉ cho phép nhi hoá (…r) ở cuối."""
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
    """Trả về chuỗi ph kiểu 'ni3 hao3' cho SSML <phoneme alphabet="pinyin">, hoặc None nếu không chắc chắn
    (khi đó đọc chữ Hán bình thường). Từ có nhi hoá (…r) cũng trả None vì chưa rõ cú pháp."""
    n_hz = len(re.findall(r'[一-鿿〇]', hz))
    p = unicodedata.normalize('NFC', py.lower())
    p = re.sub(r"//|-|'|’", ' ', p)
    p = p.replace('·', ' ·')  # '·' trước âm tiết = thường đọc thanh nhẹ (出来 chū//·lái -> chūlai)
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

    # chọn cách tách mỗi đoạn sao cho tổng số âm tiết khớp số chữ Hán
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
    """Tách biến thể: '爸爸 ｜ 爸' / 'bàba ｜ bà' -> [('爸爸','bàba'), ('爸','bà')]; '第(第二)' -> 第, 第二."""
    hzs = [x.strip() for x in hz.split('｜')]
    pys = [x.strip() for x in py.split('｜')]
    if len(hzs) != len(pys):
        return [(re.sub(r'[()（）｜\s]', '', hz), None)]
    parts = []
    for h, p in zip(hzs, pys):
        alts = re.split(r'(?<!/)/(?!/)', p)  # '/' đơn = hai cách đọc; '//' là dấu từ ly hợp
        if len(alts) > 1:  # 谁 shéi/shuí -> đọc cả hai cách
            parts += [(h, alt) for alt in alts]
            continue
        m, mp = re.fullmatch(r'(.+?)\((.+)\)', h), re.fullmatch(r'(.+?)\s+\((.+)\)', p)
        if m and mp:  # 们(朋友们) / men (péngyoumen)
            parts += [(m.group(1), mp.group(1)), (m.group(2), mp.group(2))]
        else:          # 有(一)些 / yǒu(yì)xiē -> đọc liền
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
    payload = {
        'input': {'ssml': xml},
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


def write_index(voice):
    def ids(sub):
        d = os.path.join(OUT, sub)
        if not os.path.isdir(d):
            return []
        return sorted(int(f[:-4]) for f in os.listdir(d) if f.endswith('.mp3') and f[:-4].isdigit()
                      and os.path.getsize(os.path.join(d, f)) > 0)
    data = {'voice': voice, 'w': ids('w'), 'x': ids('x')}
    with open(os.path.join(OUT, 'index.js'), 'w', encoding='utf-8') as f:
        f.write('window.HSK_AUDIO = ' + json.dumps(data) + ';\n')
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--voice', default='cmn-CN-Wavenet-A', help='giọng Google (mặc định: cmn-CN-Wavenet-A, nữ)')
    ap.add_argument('--word-rate', type=float, default=0.85, help='tốc độ đọc từ, 1.0 = bình thường (mặc định 0.85)')
    ap.add_argument('--example-rate', type=float, default=0.95, help='tốc độ đọc câu ví dụ (mặc định 0.95)')
    ap.add_argument('--only', help='chỉ tạo các STT này, vd: 1,5,67')
    ap.add_argument('--force', action='store_true', help='tạo lại cả file đã có')
    ap.add_argument('--no-examples', action='store_true', help='bỏ qua câu ví dụ')
    ap.add_argument('--list-voices', action='store_true', help='in danh sách giọng cmn-CN của Google rồi thoát')
    ap.add_argument('--dry-run', action='store_true', help='chỉ in SSML/kiểm tra pinyin, không gọi Google')
    args = ap.parse_args()

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

    jobs = []
    for v in vocab:
        body, plain = word_ssml_body(v['hz'], v['py'])
        jobs.append(('w', v['id'], ssml(body), plain, args.word_rate, v))
        if not args.no_examples and v.get('x'):
            jobs.append(('x', v['id'], ssml(escape(v['x'][0])), [], args.example_rate, v))

    if args.dry_run:
        n_plain = 0
        for kind, i, xml, plain, _, v in jobs:
            if kind == 'w':
                flag = '  <-- đọc chữ Hán thường (không ép pinyin)' if plain else ''
                n_plain += bool(plain)
                print(f'{i:>3} {v["hz"]:<12} {v["py"]:<22} {xml[7:-8]}{flag}')
        chars = sum(len(j[2]) for j in jobs)
        print(f'\n{len(jobs)} file sẽ tạo (~{chars} ký tự SSML); {n_plain} từ không ép được pinyin.')
        return

    key = os.environ.get('GOOGLE_TTS_API_KEY')
    if not key:
        sys.exit('Thiếu biến môi trường GOOGLE_TTS_API_KEY.')

    os.makedirs(os.path.join(OUT, 'w'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'x'), exist_ok=True)
    done = skipped = failed = 0
    for n, (kind, i, xml, plain, rate, v) in enumerate(jobs, 1):
        path = os.path.join(OUT, kind, f'{i}.mp3')
        if not args.force and os.path.exists(path) and os.path.getsize(path) > 0:
            skipped += 1
            continue
        label = v['hz'] if kind == 'w' else v['x'][0]
        print(f'[{n}/{len(jobs)}] {kind} #{i} {label}')
        try:
            try:
                data = synth(key, xml, args.voice, rate)
            except RuntimeError as e:
                if 'does not exist' in str(e) or 'voice' in str(e).lower() and 'HTTP 400' in str(e):
                    sys.exit(f'Giọng "{args.voice}" không hợp lệ: chạy --list-voices để xem tên đúng.\n{e}')
                if kind == 'w' and 'HTTP 400' in str(e) and '<phoneme' in xml:
                    print('    Google không nhận pinyin, đọc chữ Hán thường.')
                    plain_xml = ssml(escape(re.sub(r'[()（）｜\s]', '', v['hz'])))
                    data = synth(key, plain_xml, args.voice, rate)
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

    idx = write_index(args.voice)
    print(f'\nXong: tạo {done}, bỏ qua {skipped} (đã có), lỗi {failed}. '
          f'Hiện có {len(idx["w"])} file từ, {len(idx["x"])} file ví dụ.')


if __name__ == '__main__':
    main()
