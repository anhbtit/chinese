# Chinese Pinyin & Flashcards

Trang tĩnh (HTML/CSS/JS thuần, không cần build) gồm bảng âm tiết pinyin có phát âm (trang chính) và trang
tạo flashcard từ file Excel (Chinese, Pinyin, Part of Speech, Meaning), kèm sẵn bộ 500 từ HSK1. Ngôn ngữ mặc định: English.

## Cấu trúc

```
index.html            trang chính: bảng âm tiết pinyin (assets/pinyin.{js,css}, assets/pinyin-data.js)
audio/pinyin/         mp3 âm tiết pinyin (Chen Wang, CC BY-SA)
tools/build_pinyin_data.py  tạo assets/pinyin-data.js + audio/pinyin/ từ repo zispace/hanyu-pinyin-audio
flashcard.html        trang flashcard
assets/style.css      giao diện chung
assets/app.js         logic flashcard (thẻ, cài đặt, nhập Excel, phát âm)
assets/hsk1-data.js   bộ 500 từ HSK1 có sẵn
audio/{m,f}/{w,x}/    mp3 phát âm giọng nam/nữ (tuỳ chọn, tạo bằng tools/google_tts.py)
tools/google_tts.py   tạo audio bằng Google Cloud Text-to-Speech
reference/            tài liệu gốc (không đưa lên git)
```

## Chạy thử trên máy

```
python3 -m http.server 8000   # rồi mở http://localhost:8000
```
(Mở thẳng `index.html` bằng file:// cũng chạy được.)

## Nhập từ Excel

⚙︎ Cài đặt → **Nhập từ Excel** → chọn file `.xlsx` với các cột:
`Chinese | Pinyin | Part of Speech | Meaning` (dòng tiêu đề tự bỏ qua).
Bộ thẻ nhập vào lưu trong localStorage của trình duyệt, không tải lên server.

## Bảng âm tiết pinyin

`index.html` (nút **🗂 Flashcards** để sang trang flashcard, nút **拼 Pinyin** để quay lại): bấm một âm tiết
để nghe và xem đủ các thanh. Audio trong `audio/pinyin/` là bản ghi của Chen Wang
([hugolpz/audio-cmn](https://github.com/hugolpz/audio-cmn), CC BY-SA), lấy từ
[zispace/hanyu-pinyin-audio](https://github.com/zispace/hanyu-pinyin-audio).
Cập nhật dữ liệu + audio: `python3 tools/build_pinyin_data.py` (thêm `--force` để tải lại audio).

## Tạo audio (tuỳ chọn)

```
export GOOGLE_TTS_API_KEY=...   # API key của project đã bật Cloud Text-to-Speech API
python3 tools/google_tts.py --dry-run   # xem trước, không gọi API
python3 tools/google_tts.py
```
Script tạo cả giọng nam (`cmn-CN-Wavenet-B`) và nữ (`cmn-CN-Wavenet-A`); đổi bằng `--voice-male` / `--voice-female`, hoặc `--gender m|f` để chỉ tạo một giọng. Trên trang, mỗi lần bấm loa (hoặc phím S/E) đọc luân phiên nam → nữ → nam… Kết quả nằm trong `audio/` – commit thư mục này để trang dùng giọng Google. Không commit key.

## Đưa lên GitHub Pages

Settings → Pages → Source: **Deploy from a branch** → Branch `main` / `/ (root)`.
Trang có tại `https://<user>.github.io/<repo>/`.
