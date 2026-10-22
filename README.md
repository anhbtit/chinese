# Flashcard

Trang tạo flashcard từ file Excel (Chinese, Pinyin, Part of Speech, Meaning) – HTML/CSS/JS thuần, không cần build. Kèm sẵn bộ 500 từ HSK1 để học ngay.

## Cấu trúc

```
index.html            trang chính
assets/style.css      giao diện
assets/app.js         logic (thẻ, cài đặt, nhập Excel, phát âm)
assets/hsk1-data.js   bộ 500 từ HSK1 có sẵn
audio/                mp3 phát âm (tuỳ chọn, tạo bằng tools/azure_tts.py)
tools/azure_tts.py    tạo audio bằng Azure Speech
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

## Tạo audio (tuỳ chọn)

```
export AZURE_SPEECH_KEY=...   AZURE_SPEECH_REGION=southeastasia
python3 tools/azure_tts.py
```
Kết quả nằm trong `audio/` – commit thư mục này để trang dùng giọng Azure. Không commit key.

## Đưa lên GitHub Pages

Settings → Pages → Source: **Deploy from a branch** → Branch `main` / `/ (root)`.
Trang có tại `https://<user>.github.io/<repo>/`.
