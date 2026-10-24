# Chinese Pinyin & Flashcards

**English** · [Tiếng Việt](README.vi.md)

A static site (plain HTML/CSS/JS, no build step) with two pages:

- **Pinyin syllable table** (home page) – click a syllable to hear it and see all its tones.
- **Flashcards** – study the bundled 500-word HSK1 deck or create decks from an Excel file
  (Chinese, Pinyin, Part of Speech, Meaning).

The interface is available in English (default) and Vietnamese.

## Structure

```
index.html            home page: pinyin syllable table (assets/pinyin.{js,css}, assets/pinyin-data.js)
audio/pinyin/         pinyin syllable mp3s (Chen Wang, CC BY-SA)
tools/build_pinyin_data.py  builds assets/pinyin-data.js + audio/pinyin/ from zispace/hanyu-pinyin-audio
flashcard.html        flashcard page
assets/style.css      shared styles
assets/app.js         flashcard logic (cards, settings, Excel import, pronunciation)
assets/hsk1-data.js   bundled 500-word HSK1 deck
audio/{m,f}/{w,x}/    male/female pronunciation mp3s for the HSK1 deck (made with tools/google_tts.py)
tools/google_tts.py   generates audio with Google Cloud Text-to-Speech
reference/            source documents (not committed)
```

## Run locally

```
python3 -m http.server 8000   # then open http://localhost:8000
```
(Opening `index.html` directly via file:// also works.)

## Pinyin syllable table

`index.html` – use **🗂 Flashcards** to go to the flashcard page and **拼 Pinyin** to come back.
Click a syllable to play it; the dialog lists every tone, has **Play all tones**, and accepts keys `1`–`4` and `Esc`.

To refresh the table data and audio:

```
python3 tools/build_pinyin_data.py           # download missing files only
python3 tools/build_pinyin_data.py --force   # download all audio again
```

## Import from Excel

⚙︎ Settings → **📥 Import Excel** → pick an `.xlsx` file with the columns
`Chinese | Pinyin | Part of Speech | Meaning` (a header row is skipped automatically).
Imported decks are stored in the browser's localStorage and never uploaded.

## Generate HSK1 audio (optional)

```
export GOOGLE_TTS_API_KEY=...   # API key for a project with the Cloud Text-to-Speech API enabled
python3 tools/google_tts.py --dry-run   # preview, no API calls
python3 tools/google_tts.py
```

The script creates both a male (`cmn-CN-Wavenet-B`) and a female (`cmn-CN-Wavenet-A`) voice; change them with
`--voice-male` / `--voice-female`, or use `--gender m|f` for a single voice. On the page each press of the speaker
button (or the S/E keys) alternates male → female → male… Commit the `audio/` folder so the site uses these files.
Never commit the API key.

## Deploy to GitHub Pages

Settings → Pages → Source: **Deploy from a branch** → Branch `main` / `/ (root)`.
The site is then served at `https://<user>.github.io/<repo>/`.

## Credits

- Pinyin syllable recordings in `audio/pinyin/`: **Chen Wang**, from
  [hugolpz/audio-cmn](https://github.com/hugolpz/audio-cmn), licensed
  [CC BY-SA](https://github.com/hugolpz/audio-cmn#license). Files are used unmodified (tones 1–4 only),
  obtained via [zispace/hanyu-pinyin-audio](https://github.com/zispace/hanyu-pinyin-audio).
