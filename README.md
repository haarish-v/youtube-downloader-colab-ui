# 🎬 Google Colab YouTube Downloader App with UI

An interactive YouTube downloader app built in Google Colab using `yt-dlp`, with a user-friendly interface for choosing resolution, format, and uploading cookies for restricted downloads.

## ✅ Features
- UI with YouTube URL input
- Resolution selection: 480p, 720p, 1080p, 1440p
- Format selection: MP4 / MP3
- Upload `cookies.txt` for authenticated downloads
- Real-time download progress bar and status display
- FFmpeg-powered merging and audio extraction
- Auto-download option after processing

## 🚀 How to Use

1. **Open Google Colab** and upload the notebook or copy-paste the code.
2. **Install required packages** (done automatically by the notebook).
3. **Input your YouTube video URL**.
4. **Select resolution and format**.
5. **(Optional)** Upload `cookies.txt` if needed.
6. **Click “Download Video”**.
7. **Wait for the file link to appear** and download it.

## 🍪 How to Get `cookies.txt` (for age-restricted/private videos)

1. Install a browser extension:
   - [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/oeopbcgkkoapgobdbedcemjljbihmemj) (Chrome)
   - [cookies.txt Export](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) (Firefox)

2. Go to [youtube.com](https://www.youtube.com), login, and export cookies using the extension.

3. Upload the `cookies.txt` file in the Colab UI.

## 🧹 Cleanup

To avoid confusion on repeated downloads, delete previous video files using the Colab file browser.

## 📄 License

This project is licensed under the MIT License.

---

### Screenshot
![screenshot](https://via.placeholder.com/800x400?text=Colab+Downloader+UI)

---

### 🙌 Credits
- Built with `yt-dlp`, `ipywidgets`, `ffmpeg`, and ❤️
