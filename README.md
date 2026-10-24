# Flashcard

Trang tạo flashcard từ file Excel (Chinese, Pinyin, Part of Speech, Meaning) – HTML/CSS/JS thuần, không cần build. Kèm sẵn bộ 500 từ HSK1 để học ngay.

## Cấu trúc

```
index.html            trang chính
assets/style.css      giao diện
assets/app.js         logic (thẻ, cài đặt, nhập Excel, phát âm)
assets/hsk1-data.js   bộ 500 từ HSK1 có sẵn
audio/{m,f}/{w,x}/    mp3 phát âm giọng nam/nữ (tuỳ chọn, tạo bằng tools/google_tts.py)
tools/google_tts.py   tạo audio bằng Google Cloud Text-to-Speech
pinyin.html           bảng âm tiết pinyin có phát âm (assets/pinyin.{js,css}, assets/pinyin-data.js)
tools/build_pinyin_data.py  tạo assets/pinyin-data.js từ repo zispace/hanyu-pinyin-audio
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

`pinyin.html` (nút **拼 Pinyin** trên trang chính): bấm một âm tiết để nghe và xem đủ các thanh.
Audio là bản ghi của Chen Wang ([hugolpz/audio-cmn](https://github.com/hugolpz/audio-cmn), CC BY-SA),
tải trực tiếp từ [zispace/hanyu-pinyin-audio](https://github.com/zispace/hanyu-pinyin-audio) qua jsDelivr,
không copy vào repo. Cập nhật dữ liệu bảng: `python3 tools/build_pinyin_data.py`.

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
