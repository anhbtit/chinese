let VOCAB = HSK1_VOCAB;

const STR = {
  en: {
    deck: 'Deck', importXlsx: '📥 Import Excel', delDeck: '🗑 Delete deck',
    importHint: 'Excel (.xlsx) columns: 1 Chinese · 2 Pinyin · 3 Part of Speech · 4 Meaning. A header row is skipped automatically.',
    importOk: (n, name) => `Imported ${n} cards into “${name}”.`,
    importEmpty: 'No rows with Chinese text found in the first sheet.',
    importBad: 'Could not read this file. Please use a .xlsx file (Excel 2007+).',
    importFull: 'Browser storage is full – deck was not saved.',
    confirmDel: name => `Delete deck “${name}”?`,
    audioCustom: 'Imported deck: using the browser voice for pronunciation.',
    pinyin: 'Pinyin', pinyinTitle: 'Pinyin syllable table with audio',
    shuffle: 'Shuffle', shuffleTitle: 'Reshuffle the deck', settings: 'Settings',
    order: 'Next order', random: 'Random', seq: 'By number',
    noRepeat: 'No repeats', noRepeatDesc: 'On: go through every card before reshuffling. Off: each Next picks a fully random card (may repeat).',
    range: 'Word range (No.)', front: 'Card front', frontHz: 'Chinese', frontMeaning: 'Meaning', frontAll: 'Everything',
    speed: 'Playback speed',
    showPinyin: 'Show pinyin on front', showExample: 'Show example sentence', example: 'Example', listenEx: 'Play the example', autoSpeak: 'Auto-play audio on new card', audioSrc: 'Pronunciation source', audioBrowser: 'Browser voice',
    audioStatus: (c, n) => `Google audio found – male: ${c.m.w}/${n} words, ${c.m.x}/${n} examples · female: ${c.f.w}/${n} words, ${c.f.x}/${n} examples. Each press alternates male / female; missing files fall back to the browser voice.`,
    audioNone: 'No Google audio yet (run tools/google_tts.py). Using the browser voice for now.',
    theme: 'Theme', themeAuto: 'Auto', themeLight: 'Light', themeDark: 'Dark', apply: 'Apply & restart',
    flipHint: 'Click to flip', flip: 'Flip card', prev: 'Prev', next: 'Next', listen: 'Play pronunciation',
    tapFlip: 'Tap to flip', tapHz: 'Tap to see the Chinese', phrase: 'phrase',
    seen: (a, b) => `Seen ${a}/${b}`, rangeLbl: (a, b) => `No. ${a}–${b}`,
    modeSeq: 'By number', modeRandNR: 'Random, no repeats', modeRand: 'Random',
    keys: '<kbd>←</kbd> prev · <kbd>→</kbd> next · <kbd>Space</kbd> flip · <kbd>S</kbd> speak · <kbd>E</kbd> example · swipe left/right on mobile',
  },
  vi: {
    deck: 'Bộ thẻ', importXlsx: '📥 Nhập từ Excel', delDeck: '🗑 Xoá bộ thẻ',
    importHint: 'File Excel (.xlsx) gồm các cột: 1 Chinese · 2 Pinyin · 3 Part of Speech · 4 Meaning. Dòng tiêu đề sẽ tự bỏ qua.',
    importOk: (n, name) => `Đã nhập ${n} thẻ vào “${name}”.`,
    importEmpty: 'Không tìm thấy dòng nào có chữ Hán ở sheet đầu tiên.',
    importBad: 'Không đọc được file này. Hãy dùng file .xlsx (Excel 2007 trở lên).',
    importFull: 'Bộ nhớ trình duyệt đã đầy – chưa lưu được bộ thẻ.',
    confirmDel: name => `Xoá bộ thẻ “${name}”?`,
    audioCustom: 'Bộ thẻ nhập từ Excel: dùng giọng trình duyệt để phát âm.',
    pinyin: 'Pinyin', pinyinTitle: 'Bảng âm tiết pinyin có phát âm',
    shuffle: 'Xáo', shuffleTitle: 'Xáo lại bộ thẻ', settings: 'Cài đặt',
    order: 'Thứ tự khi Next', random: 'Ngẫu nhiên', seq: 'Theo STT',
    noRepeat: 'Không lặp lại', noRepeatDesc: 'Bật: đi hết các thẻ rồi mới xáo lại. Tắt: mỗi lần Next chọn ngẫu nhiên hoàn toàn (có thể trùng).',
    range: 'Phạm vi STT', front: 'Mặt trước', frontHz: 'Tiếng Trung', frontMeaning: 'Nghĩa', frontAll: 'Hiện hết',
    speed: 'Tốc độ phát âm',
    showPinyin: 'Hiện pinyin ở mặt trước', showExample: 'Hiện câu ví dụ', example: 'Ví dụ', listenEx: 'Nghe câu ví dụ', autoSpeak: 'Tự đọc khi lật sang thẻ mới', audioSrc: 'Nguồn phát âm', audioBrowser: 'Giọng trình duyệt',
    audioStatus: (c, n) => `Đã có audio Google – nam: ${c.m.w}/${n} từ, ${c.m.x}/${n} câu ví dụ · nữ: ${c.f.w}/${n} từ, ${c.f.x}/${n} câu ví dụ. Mỗi lần bấm đọc luân phiên nam / nữ; thiếu file nào thì dùng giọng trình duyệt.`,
    audioNone: 'Chưa có audio Google (chạy tools/google_tts.py). Tạm thời dùng giọng trình duyệt.',
    theme: 'Giao diện', themeAuto: 'Tự động', themeLight: 'Sáng', themeDark: 'Tối', apply: 'Áp dụng & bắt đầu lại',
    flipHint: 'Bấm để lật thẻ', flip: 'Lật thẻ', prev: 'Trước', next: 'Tiếp', listen: 'Nghe phát âm',
    tapFlip: 'Bấm để lật thẻ', tapHz: 'Bấm để xem chữ Hán', phrase: 'cụm từ',
    seen: (a, b) => `Đã xem ${a}/${b}`, rangeLbl: (a, b) => `STT ${a}–${b}`,
    modeSeq: 'Theo STT', modeRandNR: 'Ngẫu nhiên, không lặp', modeRand: 'Ngẫu nhiên',
    keys: '<kbd>←</kbd> trước · <kbd>→</kbd> tiếp · <kbd>Space</kbd> lật · <kbd>S</kbd> đọc · <kbd>E</kbd> ví dụ · vuốt trái/phải trên điện thoại',
  },
};
const POS_EN = {
  'danh từ': 'noun', 'động từ': 'verb', 'tính từ': 'adjective', 'đại từ': 'pronoun', 'phó từ': 'adverb',
  'lượng từ': 'measure word', 'số từ': 'numeral', 'trợ từ': 'particle', 'giới từ': 'preposition',
  'liên từ': 'conjunction', 'hậu tố': 'suffix', 'tiền tố': 'prefix',
};

const DEFAULTS = { lang: 'en', order: 'random', noRepeat: true, from: 1, to: VOCAB.length, front: 'hz', speed: 1, deck: 'hsk1', pinyin: false, example: true, autoSpeak: false, audio: 'google', theme: 'auto' };
const STORE_KEY = 'hsk1-flashcard-settings';
let cfg = { ...DEFAULTS };
try { Object.assign(cfg, JSON.parse(localStorage.getItem(STORE_KEY) || '{}')); } catch (e) {}
if (cfg.audio === 'azure') cfg.audio = 'google';   // old setting from the Azure version

// ----- Decks: built-in HSK1 + decks imported from Excel (stored in localStorage) -----
const HSK1_ID = 'hsk1';
const DECKS_KEY = 'flashcard-custom-decks';
let customDecks = {};
try { customDecks = JSON.parse(localStorage.getItem(DECKS_KEY) || '{}') || {}; } catch (e) {}
function saveDecks() { try { localStorage.setItem(DECKS_KEY, JSON.stringify(customDecks)); return true; } catch (e) { return false; } }
if (cfg.deck !== HSK1_ID && customDecks[cfg.deck]) VOCAB = customDecks[cfg.deck].vocab;
else { if (cfg.deck !== HSK1_ID) { cfg.from = 1; cfg.to = HSK1_VOCAB.length; } cfg.deck = HSK1_ID; }
const isBuiltin = () => cfg.deck === HSK1_ID;

// History of viewed cards: next appends, prev steps back; next after stepping back replays the history.
let pool = [];      // VOCAB indexes within the range
let queue = [];     // shuffled queue (no-repeat mode)
let history = [];
let pos = -1;
let seen = new Set();

const $ = id => document.getElementById(id);
const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function save() { try { localStorage.setItem(STORE_KEY, JSON.stringify(cfg)); } catch (e) {} }

// Progress is stored by card number (not index) so it still matches if the data order changes.
const progressKey = id => id === HSK1_ID ? 'hsk1-flashcard-progress' : 'flashcard-progress-' + id;
const HISTORY_MAX = 2000;
const deckSig = () => [cfg.order, cfg.noRepeat, cfg.from, cfg.to].join('|');

function saveProgress() {
  if (history.length > HISTORY_MAX) {
    const cut = history.length - HISTORY_MAX;
    history = history.slice(cut); pos = Math.max(0, pos - cut);
  }
  const ids = a => a.map(i => VOCAB[i].id);
  try {
    localStorage.setItem(progressKey(cfg.deck), JSON.stringify({
      deck: deckSig(), history: ids(history), pos, queue: ids(queue), seen: ids([...seen]),
    }));
  } catch (e) {}
}

function loadProgress() {
  let p;
  try { p = JSON.parse(localStorage.getItem(progressKey(cfg.deck)) || 'null'); } catch (e) { return false; }
  buildPool();
  if (!p || p.deck !== deckSig() || !Array.isArray(p.history)) return false;
  const inPool = new Map(pool.map(i => [VOCAB[i].id, i]));
  const idx = a => (Array.isArray(a) ? a : []).map(id => inPool.get(id)).filter(i => i !== undefined);
  history = idx(p.history);
  if (!history.length) return false;
  queue = idx(p.queue);
  seen = new Set(idx(p.seen));
  pos = Math.min(Math.max(0, p.pos | 0), history.length - 1);
  render();
  return true;
}

function shuffle(a) {
  for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
  return a;
}

function buildPool() {
  let a = Math.max(1, Math.min(cfg.from, cfg.to)), b = Math.min(VOCAB.length, Math.max(cfg.from, cfg.to));
  cfg.from = a; cfg.to = b;
  pool = VOCAB.map((v, i) => i).filter(i => VOCAB[i].id >= a && VOCAB[i].id <= b);
}

function restart() {
  buildPool();
  queue = []; history = []; pos = -1; seen = new Set();
  next();
}

function pickNext() {
  const cur = history[pos];
  if (cfg.order === 'seq') {
    if (cur === undefined) return pool[0];
    const k = pool.indexOf(cur);
    return pool[(k + 1) % pool.length];
  }
  if (cfg.noRepeat) {
    if (!queue.length) {
      queue = shuffle(pool.slice());
      // avoid repeating the card just seen when a new round is shuffled
      if (queue.length > 1 && queue[queue.length - 1] === cur) [queue[0], queue[queue.length - 1]] = [queue[queue.length - 1], queue[0]];
    }
    return queue.pop();
  }
  if (pool.length === 1) return pool[0];
  let r;
  do { r = pool[Math.floor(Math.random() * pool.length)]; } while (r === cur);
  return r;
}

function next() {
  if (!pool.length) return;
  if (pos < history.length - 1) pos++;
  else { history.push(pickNext()); pos = history.length - 1; }
  render();
}

function prev() {
  if (pos > 0) { pos--; render(); }
}

const T = () => STR[cfg.lang] || STR.en;

// Part of speech + meaning in the current language: [[pos, meaning], ...]
function senses(v) {
  if (cfg.lang === 'vi') return v.s;
  return v.s.map(([p], i) => [POS_EN[p] || p, v.e[i]]);
}

function sensesHTML(v) {
  return senses(v).map(([p, m]) => {
    const parts = m.split(/\s\/\s/).map(x => `<span class="sub">${esc(x)}</span>`).join('');
    return `<li><span class="pos ${p ? '' : 'empty'}">${p ? esc(p) : T().phrase}</span><span class="mean">${parts}</span></li>`;
  }).join('');
}

// Highlight the current word in the example sentence (longest variant found in the sentence)
function markWord(sentence, hz) {
  const cands = hz.split('｜').flatMap(x => [x.replace(/\(.*?\)/g, ''), (x.match(/\((.*?)\)/) || [])[1]])
    .map(x => (x || '').trim()).filter(Boolean).sort((a, b) => b.length - a.length);
  const w = cands.find(c => sentence.includes(c));
  if (!w) return esc(sentence);
  const i = sentence.indexOf(w);
  return esc(sentence.slice(0, i)) + `<mark>${esc(w)}</mark>` + esc(sentence.slice(i + w.length));
}

function exampleHTML(v) {
  if (!cfg.example || !v.x) return '';
  const [hz, py, vi, en] = v.x;
  return `<div class="example">
      <div class="ex-label">${T().example}<button class="ex-speak" data-speak-ex title="${T().listenEx}">🔊</button></div>
      <div class="ex-hz hz-font">${markWord(hz, v.hz)}</div>
      <div class="ex-py">${esc(py)}</div>
      <div class="ex-tr">${esc(cfg.lang === 'vi' ? vi : en)}</div>
    </div>`;
}

function render() {
  const v = VOCAB[history[pos]];
  seen.add(history[pos]);
  const card = $('card');
  card.classList.remove('flipped');
  const hzClass = v.hz.replace(/\s/g, '').length > 4 ? 'big-hz long' : 'big-hz';
  const t = T();
  const speakBtn = `<button class="speak" data-speak title="${t.listen}">🔊</button>`;
  const num = `<span class="num">#${v.id}</span>`;
  const all = `
    <div class="back-head">
      <div class="back-hz hz-font">${esc(v.hz)}</div>
      <div class="back-py">${esc(v.py)}</div>
    </div>
    <ul class="senses">${sensesHTML(v)}</ul>
    ${exampleHTML(v)}`;

  let front;
  if (cfg.front === 'vi') {
    front = `${num}<div class="front-vi">${senses(v).map(([p, m]) => `<div style="margin:6px 0">${p ? `<span class="pos-inline">${esc(p)}</span>` : ''}${esc(m)}</div>`).join('')}</div>
      <span class="hint">${t.tapHz}</span>`;
  } else if (cfg.front === 'all') {
    front = `${num}${speakBtn}${all}`;
  } else {
    front = `${num}${speakBtn}<div class="${hzClass} hz-font">${esc(v.hz)}</div>
      ${cfg.pinyin ? `<div class="front-py">${esc(v.py)}</div>` : ''}
      <span class="hint">${t.tapFlip}</span>`;
  }
  $('front').innerHTML = front;
  $('front').style.justifyContent = cfg.front === 'all' ? 'flex-start' : '';
  $('back').innerHTML = `${num}${speakBtn}${all}`;

  $('stPos').textContent = t.seen(seen.size, pool.length) + (pool.length < VOCAB.length ? ` · ${t.rangeLbl(cfg.from, cfg.to)}` : '');
  $('stMode').textContent = cfg.order === 'seq' ? t.modeSeq : (cfg.noRepeat ? t.modeRandNR : t.modeRand);
  $('stBar').style.width = (seen.size / pool.length * 100) + '%';
  $('btnPrev').disabled = pos <= 0;
  saveProgress();
  if (cfg.autoSpeak) speak();
}

function flip() { $('card').classList.toggle('flipped'); }

let zhVoice = null;
let zhVoices = { m: null, f: null };
function loadVoice() {
  const vs = speechSynthesis.getVoices();
  const zh = vs.filter(v => /^zh/i.test(v.lang));
  const pick = a => a.find(v => /zh[-_]CN/i.test(v.lang)) || a[0] || null;
  zhVoice = pick(zh);
  // pick browser voices by gender when the name gives it away; otherwise share one voice and shift pitch
  const isMale = v => /(^|[^a-z])male([^a-z]|$)|yunxi|yunjian|yunyang|kangkang|liwei|li-mu|zhiwei/i.test(v.name) && !/female/i.test(v.name);
  const isFemale = v => /female|xiaoxiao|xiaoyi|tingting|huihui|yaoyao|meijia|lili|ting-ting/i.test(v.name);
  zhVoices = { m: pick(zh.filter(isMale)), f: pick(zh.filter(isFemale)) };
}
if ('speechSynthesis' in window) { loadVoice(); speechSynthesis.onvoiceschanged = loadVoice; }
function speakTTS(text, g) {
  if (!('speechSynthesis' in window)) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'zh-CN'; u.rate = .8 * cfg.speed;
  const own = g && zhVoices[g];
  if (own) u.voice = own;
  else {
    if (zhVoice) u.voice = zhVoice;
    if (g) u.pitch = g === 'm' ? .6 : 1.25;   // no gendered voice: tell male/female apart by pitch
  }
  speechSynthesis.speak(u);
}

// mp3 files generated by tools/google_tts.py: audio/<m|f>/w/<No>.mp3 (word), audio/<m|f>/x/<No>.mp3 (example).
// audio/index.js declares window.HSK_AUDIO = {m: {w: [No...], x: [No...]}, f: {...}} listing the available files.
// Each press alternates the male (m) / female (f) voice.
const audioFiles = { m: { w: new Set(), x: new Set() }, f: { w: new Set(), x: new Set() } };
let nextGender = 'm';
const player = new Audio();
function loadAudioIndex() {
  const s = document.createElement('script');
  s.src = 'audio/index.js';
  s.onload = () => {
    const a = window.HSK_AUDIO || {};
    for (const g of ['m', 'f']) audioFiles[g] = { w: new Set((a[g] || {}).w || []), x: new Set((a[g] || {}).x || []) };
    updateAudioStatus();
  };
  s.onerror = updateAudioStatus;
  document.head.appendChild(s);
}
function updateAudioStatus() {
  const t = T(), c = {};
  for (const g of ['m', 'f']) c[g] = { w: audioFiles[g].w.size, x: audioFiles[g].x.size };
  if (!isBuiltin()) { $('audioStatus').textContent = t.audioCustom; return; }
  const any = c.m.w + c.m.x + c.f.w + c.f.x > 0;
  $('audioStatus').textContent = any ? t.audioStatus(c, VOCAB.length) : t.audioNone;
}

// kind: 'w' = word, 'x' = example sentence
function speak(kind = 'w') {
  if (pos < 0) return;
  const v = VOCAB[history[pos]];
  if (kind === 'x' && !v.x) return;
  const text = kind === 'x' ? v.x[0] : v.hz.split('｜')[0].replace(/\(.*?\)/g, '').trim();
  const g = nextGender;                        // alternate: 1st male, 2nd female, 3rd male…
  nextGender = g === 'm' ? 'f' : 'm';
  // if this voice's file is missing, use the other voice's file before falling back to the browser voice
  const src = [g, g === 'm' ? 'f' : 'm'].find(x => audioFiles[x][kind].has(v.id));
  if (cfg.audio === 'google' && isBuiltin() && src) {
    if ('speechSynthesis' in window) speechSynthesis.cancel();
    player.pause();
    player.src = `audio/${src}/${kind}/${v.id}.mp3`;
    player.defaultPlaybackRate = player.playbackRate = cfg.speed;   // set defaultPlaybackRate too, since changing src resets playbackRate
    player.play().catch(err => { if (err.name !== 'AbortError') speakTTS(text, g); });
    return;
  }
  player.pause();
  speakTTS(text, g);
}

// ----- settings UI -----
function setSeg(id, val) { document.querySelectorAll(`#${id} button`).forEach(b => b.classList.toggle('on', b.dataset.v === val)); }
function segVal(id) { return document.querySelector(`#${id} button.on`).dataset.v; }
function applyTheme() {
  if (cfg.theme === 'auto') document.documentElement.removeAttribute('data-theme');
  else document.documentElement.setAttribute('data-theme', cfg.theme);
}
function applyLang() {
  const t = T();
  document.documentElement.lang = cfg.lang;
  document.querySelectorAll('[data-i18n]').forEach(el => { el.textContent = t[el.dataset.i18n]; });
  document.querySelectorAll('[data-i18n-html]').forEach(el => { el.innerHTML = t[el.dataset.i18nHtml]; });
  document.querySelectorAll('[data-i18n-title]').forEach(el => { el.title = t[el.dataset.i18nTitle]; });
  setSeg('segLang', cfg.lang);
  updateAudioStatus();
}
$('segLang').addEventListener('click', e => {
  if (e.target.tagName !== 'BUTTON' || e.target.dataset.v === cfg.lang) return;
  cfg.lang = e.target.dataset.v; save(); applyLang();
  if (pos >= 0) {
    const flipped = $('card').classList.contains('flipped');
    render();
    $('card').classList.toggle('flipped', flipped);
  }
});
function fillSettings() {
  setSeg('segOrder', cfg.order); setSeg('segFront', cfg.front); setSeg('segTheme', cfg.theme); setSeg('segAudio', cfg.audio); setSeg('segSpeed', String(cfg.speed));
  updateAudioStatus();
  $('optNoRepeat').checked = cfg.noRepeat; $('optPinyin').checked = cfg.pinyin; $('optExample').checked = cfg.example; $('optAutoSpeak').checked = cfg.autoSpeak;
  $('rFrom').value = cfg.from; $('rTo').value = cfg.to;
  $('optNoRepeat').closest('.row').style.display = cfg.order === 'random' ? '' : 'none';
}
['segOrder', 'segFront', 'segTheme', 'segAudio'].forEach(id => {
  $(id).addEventListener('click', e => {
    if (e.target.tagName !== 'BUTTON') return;
    setSeg(id, e.target.dataset.v);
    if (id === 'segOrder') $('optNoRepeat').closest('.row').style.display = e.target.dataset.v === 'random' ? '' : 'none';
    if (id === 'segTheme') { cfg.theme = e.target.dataset.v; applyTheme(); save(); }
    if (id === 'segFront') { cfg.front = e.target.dataset.v; save(); render(); }
    if (id === 'segAudio') { cfg.audio = e.target.dataset.v; save(); }
  });
});
$('optPinyin').addEventListener('change', e => { cfg.pinyin = e.target.checked; save(); render(); });
$('segSpeed').addEventListener('click', e => {
  if (e.target.tagName !== 'BUTTON') return;
  cfg.speed = parseFloat(e.target.dataset.v); setSeg('segSpeed', e.target.dataset.v); save();
  player.defaultPlaybackRate = player.playbackRate = cfg.speed;
});
$('optAutoSpeak').addEventListener('change', e => { cfg.autoSpeak = e.target.checked; save(); });
$('optExample').addEventListener('change', e => {
  cfg.example = e.target.checked; save();
  const flipped = $('card').classList.contains('flipped');
  render();
  $('card').classList.toggle('flipped', flipped);
});
$('btnApply').addEventListener('click', () => {
  cfg.order = segVal('segOrder');
  cfg.noRepeat = $('optNoRepeat').checked;
  cfg.from = parseInt($('rFrom').value, 10) || 1;
  cfg.to = parseInt($('rTo').value, 10) || VOCAB.length;
  save(); restart(); fillSettings();
  setPanel(false);
});
// Open/close settings; while open, hide the study area (progress, card, navigation)
function setPanel(open) {
  $('panel').classList.toggle('open', open);
  $('study').hidden = open;
  $('btnSettings').setAttribute('aria-pressed', String(open));
  if (open) fillSettings();
}
$('btnSettings').addEventListener('click', () => {
  setPanel(!$('panel').classList.contains('open'));
});
$('btnShuffle').addEventListener('click', restart);

// ----- navigation -----
$('btnNext').addEventListener('click', next);
$('btnPrev').addEventListener('click', prev);
$('btnFlip').addEventListener('click', flip);
$('scene').addEventListener('click', e => {
  if (e.target.closest('[data-speak]')) { e.stopPropagation(); speak(); return; }
  if (e.target.closest('[data-speak-ex]')) { e.stopPropagation(); speak('x'); return; }
  if (swiped) return;
  flip();
});
document.addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || $('panel').classList.contains('open')) return;
  if (e.key === 'ArrowRight') { next(); e.preventDefault(); }
  else if (e.key === 'ArrowLeft') { prev(); e.preventDefault(); }
  else if (e.key === ' ' || e.key === 'Enter' || e.key === 'ArrowUp' || e.key === 'ArrowDown') { flip(); e.preventDefault(); }
  else if (e.key === 's' || e.key === 'S') speak();
  else if (e.key === 'e' || e.key === 'E') speak('x');
});
let tx = 0, ty = 0, swiped = false;
$('scene').addEventListener('touchstart', e => { tx = e.touches[0].clientX; ty = e.touches[0].clientY; swiped = false; }, { passive: true });
$('scene').addEventListener('touchend', e => {
  const dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
  if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) {
    swiped = true; dx < 0 ? next() : prev();
    setTimeout(() => { swiped = false; }, 400);
  }
});

// ----- Excel (.xlsx) flashcard import – parsed in-browser, no external library, works offline -----
async function unzip(buf) {
  const dv = new DataView(buf), u8 = new Uint8Array(buf), dec = new TextDecoder();
  let eocd = -1;
  for (let i = buf.byteLength - 22; i >= Math.max(0, buf.byteLength - 65557); i--) {
    if (dv.getUint32(i, true) === 0x06054b50) { eocd = i; break; }
  }
  if (eocd < 0) throw new Error('not a zip');
  const n = dv.getUint16(eocd + 10, true);
  let p = dv.getUint32(eocd + 16, true);
  const files = {};
  for (let k = 0; k < n && dv.getUint32(p, true) === 0x02014b50; k++) {
    const nlen = dv.getUint16(p + 28, true), elen = dv.getUint16(p + 30, true), clen = dv.getUint16(p + 32, true);
    files[dec.decode(u8.subarray(p + 46, p + 46 + nlen))] = {
      method: dv.getUint16(p + 10, true), size: dv.getUint32(p + 20, true), off: dv.getUint32(p + 42, true),
    };
    p += 46 + nlen + elen + clen;
  }
  return async name => {
    const f = files[name];
    if (!f) return null;
    const start = f.off + 30 + dv.getUint16(f.off + 26, true) + dv.getUint16(f.off + 28, true);
    const data = u8.subarray(start, start + f.size);
    if (f.method === 0) return dec.decode(data);
    if (f.method !== 8) throw new Error('unsupported zip method');
    return new Response(new Blob([data]).stream().pipeThrough(new DecompressionStream('deflate-raw'))).text();
  };
}

const xmlDoc = txt => new DOMParser().parseFromString(txt, 'application/xml');
const xmlAll = (node, tag) => Array.from(node.getElementsByTagNameNS('*', tag));

// Return the rows of the first sheet as an array of string arrays
async function readXlsxRows(file) {
  const read = await unzip(await file.arrayBuffer());
  const wb = await read('xl/workbook.xml');
  if (!wb) throw new Error('not an xlsx');
  let path = 'xl/worksheets/sheet1.xml';
  const sheet = xmlAll(xmlDoc(wb), 'sheet')[0];
  const rid = sheet && (sheet.getAttribute('r:id') || sheet.getAttributeNS('http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'id'));
  const rels = await read('xl/_rels/workbook.xml.rels');
  if (rid && rels) {
    const rel = xmlAll(xmlDoc(rels), 'Relationship').find(r => r.getAttribute('Id') === rid);
    if (rel) { const t = rel.getAttribute('Target'); path = t.startsWith('/') ? t.slice(1) : 'xl/' + t; }
  }
  const sheetXml = await read(path);
  if (!sheetXml) throw new Error('sheet not found');

  // shared strings (skip phonetic <rPh> runs)
  const textOf = si => xmlAll(si, 't').filter(t => !t.parentNode.localName.startsWith('rPh')).map(t => t.textContent).join('');
  const sstXml = await read('xl/sharedStrings.xml');
  const shared = sstXml ? xmlAll(xmlDoc(sstXml), 'si').map(textOf) : [];

  const colIdx = ref => { let n = 0; for (const ch of ref.replace(/[^A-Za-z]/g, '').toUpperCase()) n = n * 26 + ch.charCodeAt(0) - 64; return n - 1; };
  return xmlAll(xmlDoc(sheetXml), 'row').map(row => {
    const arr = [];
    xmlAll(row, 'c').forEach(c => {
      const ref = c.getAttribute('r'), idx = ref ? colIdx(ref) : arr.length, t = c.getAttribute('t');
      const v = xmlAll(c, 'v')[0];
      let val = '';
      if (t === 'inlineStr') val = xmlAll(c, 'is')[0] ? textOf(xmlAll(c, 'is')[0]) : '';
      else if (v) val = t === 's' ? (shared[+v.textContent] || '') : v.textContent;
      arr[idx] = val;
    });
    return Array.from(arr, x => x ?? '');
  });
}

// Map parts of speech (English / abbreviations) to the Vietnamese names used by the HSK1 deck; keep unknown ones as is.
const POS_CANON = (() => {
  const m = {};
  Object.entries(POS_EN).forEach(([vi, en]) => { m[en] = vi; m[vi] = vi; });
  Object.entries({
    n: 'danh từ', v: 'động từ', vt: 'động từ', vi: 'động từ', adj: 'tính từ', a: 'tính từ', adv: 'phó từ', pron: 'đại từ', pr: 'đại từ',
    mw: 'lượng từ', m: 'lượng từ', classifier: 'lượng từ', measure: 'lượng từ', num: 'số từ', numeral: 'số từ',
    part: 'trợ từ', prep: 'giới từ', conj: 'liên từ',
  }).forEach(([k, vi]) => { m[k] = vi; });
  return m;
})();
const canonPos = p => POS_CANON[p.toLowerCase().replace(/\.$/, '').trim()] || p;

// Columns: 1 Chinese · 2 Pinyin · 3 Part of Speech · 4 Meaning. Rows with the same characters + pinyin merge into one multi-sense card.
function rowsToVocab(rows) {
  const cell = (r, i) => String(r[i] ?? '').replace(/\s*[\r\n]+\s*/g, ' / ').trim();
  const hasHan = s => /[\u3400-\u9fff\uf900-\ufaff]/.test(s);
  const start = rows.length && !hasHan(cell(rows[0], 0)) ? 1 : 0;   // skip the header row
  const vocab = [], byKey = new Map();
  rows.slice(start).forEach(r => {
    const hz = cell(r, 0), py = cell(r, 1), pos = canonPos(cell(r, 2)), mean = cell(r, 3);
    if (!hz) return;
    const key = hz + '\0' + py, w = byKey.get(key);
    if (w) {
      if (!w.s.some(([p, m]) => p === pos && m === mean)) { w.s.push([pos, mean]); w.e.push(mean); }
    } else {
      const nw = { id: vocab.length + 1, hz, py, s: [[pos, mean]], e: [mean] };
      vocab.push(nw); byKey.set(key, nw);
    }
  });
  return vocab;
}

function showImportMsg(text, kind) {
  const el = $('importMsg');
  el.textContent = text || ''; el.hidden = !text; el.className = 'msg ' + (kind || '');
}

async function importFile(file) {
  const t = T();
  try {
    const vocab = rowsToVocab(await readXlsxRows(file));
    if (!vocab.length) return showImportMsg(t.importEmpty, 'err');
    const name = file.name.replace(/\.[^.]+$/, '');
    // re-importing a file with the same name replaces the deck (and clears progress, since numbers may change)
    let id = Object.keys(customDecks).find(k => customDecks[k].name === name);
    const old = id && customDecks[id];
    if (!id) id = 'c' + Date.now().toString(36);
    customDecks[id] = { name, vocab };
    if (!saveDecks()) {
      if (old) customDecks[id] = old; else delete customDecks[id];
      return showImportMsg(t.importFull, 'err');
    }
    try { localStorage.removeItem(progressKey(id)); } catch (e) {}
    switchDeck(id);
    showImportMsg(t.importOk(vocab.length, name), 'ok');
    setPanel(true);
  } catch (err) {
    console.error(err);
    showImportMsg(t.importBad, 'err');
  }
}

function refreshDeckUI() {
  const name = isBuiltin() ? 'HSK1' : customDecks[cfg.deck].name;
  $('deckName').textContent = name;
  document.title = 'Flashcard ' + name;
  $('selDeck').innerHTML = [[HSK1_ID, 'HSK1', HSK1_VOCAB.length], ...Object.entries(customDecks).map(([id, d]) => [id, d.name, d.vocab.length])]
    .map(([id, n, c]) => `<option value="${esc(id)}"${id === cfg.deck ? ' selected' : ''}>${esc(n)} (${c})</option>`).join('');
  $('btnDelDeck').style.display = isBuiltin() ? 'none' : '';
  $('rFrom').max = $('rTo').max = VOCAB.length;
  updateAudioStatus();
}

function switchDeck(id) {
  cfg.deck = id;
  VOCAB = isBuiltin() ? HSK1_VOCAB : customDecks[id].vocab;
  cfg.from = 1; cfg.to = VOCAB.length;
  save(); refreshDeckUI(); fillSettings();
  if (!loadProgress()) restart();
}

$('selDeck').addEventListener('change', e => {
  showImportMsg('');
  switchDeck(e.target.value);
  setPanel(false);
});
$('btnImport').addEventListener('click', () => $('fileXlsx').click());
$('fileXlsx').addEventListener('change', e => {
  const f = e.target.files[0];
  e.target.value = '';   // allow picking the same file again
  if (f) importFile(f);
});
$('btnDelDeck').addEventListener('click', () => {
  if (isBuiltin() || !confirm(T().confirmDel(customDecks[cfg.deck].name))) return;
  const id = cfg.deck;
  delete customDecks[id]; saveDecks();
  try { localStorage.removeItem(progressKey(id)); } catch (e) {}
  showImportMsg('');
  switchDeck(HSK1_ID);
});

applyTheme();
applyLang();
refreshDeckUI();
loadAudioIndex();
if (!loadProgress()) restart();
