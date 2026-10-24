# Chinese Pinyin & Flashcards

[English](README.md) · **Tiếng Việt**

Trang tĩnh (HTML/CSS/JS thuần, không cần build) gồm hai trang:

- **Bảng âm tiết pinyin** (trang chính): bấm một âm tiết để nghe và xem đủ các thanh.
- **Flashcard**: học bộ 500 từ HSK1 có sẵn hoặc tạo bộ thẻ từ file Excel
  (Chinese, Pinyin, Part of Speech, Meaning).

Giao diện có tiếng Anh (mặc định) và tiếng Việt.

## Cấu trúc

```
index.html            trang chính: bảng âm tiết pinyin (assets/pinyin.{js,css}, assets/pinyin-data.js)
audio/pinyin/         mp3 âm tiết pinyin (Chen Wang, CC BY-SA)
tools/build_pinyin_data.py  tạo assets/pinyin-data.js + audio/pinyin/ từ repo zispace/hanyu-pinyin-audio
flashcard.html        trang flashcard
assets/style.css      giao diện chung
assets/app.js         logic flashcard (thẻ, cài đặt, nhập Excel, phát âm)
assets/hsk1-data.js   bộ 500 từ HSK1 có sẵn
audio/{m,f}/{w,x}/    mp3 phát âm giọng nam/nữ cho bộ HSK1 (tạo bằng tools/google_tts.py)
tools/google_tts.py   tạo audio bằng Google Cloud Text-to-Speech
reference/            tài liệu gốc (không đưa lên git)
```

## Chạy thử trên máy

```
python3 -m http.server 8000   # rồi mở http://localhost:8000
```
(Mở thẳng `index.html` bằng file:// cũng chạy được.)

## Bảng âm tiết pinyin

`index.html`: nút **🗂 Flashcards** để sang trang flashcard, nút **拼 Pinyin** để quay lại.
Bấm một âm tiết để nghe; hộp chi tiết liệt kê đủ các thanh, có nút **Nghe tất cả các thanh**, phím `1`–`4` và `Esc`.

Cập nhật dữ liệu bảng và audio:

```
python3 tools/build_pinyin_data.py           # chỉ tải file còn thiếu
python3 tools/build_pinyin_data.py --force   # tải lại toàn bộ audio
```

## Nhập từ Excel

⚙︎ Cài đặt → **📥 Nhập từ Excel** → chọn file `.xlsx` với các cột
`Chinese | Pinyin | Part of Speech | Meaning` (dòng tiêu đề tự bỏ qua).
Bộ thẻ nhập vào lưu trong localStorage của trình duyệt, không tải lên server.

## Tạo audio cho bộ HSK1 (tuỳ chọn)

```
export GOOGLE_TTS_API_KEY=...   # API key của project đã bật Cloud Text-to-Speech API
python3 tools/google_tts.py --dry-run   # xem trước, không gọi API
python3 tools/google_tts.py
```

Script tạo cả giọng nam (`cmn-CN-Wavenet-B`) và nữ (`cmn-CN-Wavenet-A`); đổi bằng `--voice-male` / `--voice-female`,
hoặc `--gender m|f` để chỉ tạo một giọng. Trên trang, mỗi lần bấm loa (hoặc phím S/E) đọc luân phiên nam → nữ → nam…
Commit thư mục `audio/` để trang dùng các file này. Không commit API key.

## Đưa lên GitHub Pages

Settings → Pages → Source: **Deploy from a branch** → Branch `main` / `/ (root)`.
Trang có tại `https://<user>.github.io/<repo>/`.

## Ghi nguồn

- Bản ghi âm tiết pinyin trong `audio/pinyin/`: **Chen Wang**, từ
  [hugolpz/audio-cmn](https://github.com/hugolpz/audio-cmn), giấy phép
  [CC BY-SA](https://github.com/hugolpz/audio-cmn#license). File giữ nguyên, không chỉnh sửa (chỉ lấy thanh 1–4),
  lấy qua [zispace/hanyu-pinyin-audio](https://github.com/zispace/hanyu-pinyin-audio).
