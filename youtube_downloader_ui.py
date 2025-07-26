# File: youtube_downloader_colab.py

# Google Colab YouTube Downloader App with UI
# See README.md for instructions

# Install required packages
!pip install -q yt-dlp
!apt-get install -y -qq ffmpeg

# Imports
import os
import ipywidgets as widgets
from IPython.display import display, clear_output
from google.colab import files
import time

# Global phase tracker
current_phase = "init"

# --- UI Widgets ---
yt_url = widgets.Text(description='YouTube URL:', layout=widgets.Layout(width='100%'))
quality = widgets.Dropdown(options=['1440p', '1080p', '720p', '480p'], value='1080p', description='Quality:')
file_format = widgets.Dropdown(options=['mp4', 'mp3'], value='mp4', description='Format:')
cookie_upload = widgets.FileUpload(accept='.txt', multiple=False, description='Upload cookies.txt')

progress_bar = widgets.FloatProgress(value=0.0, min=0.0, max=100.0, description='Progress:',
                                     bar_style='info', layout=widgets.Layout(width='100%'))
progress_label = widgets.Label(value="")
progress_output = widgets.Output()


download_button = widgets.Button(description='Download Video', button_style='success')

# --- Progress Hook ---
def hook_print(d):
    global current_phase
    if d['status'] == 'downloading':
        try:
            percent = float(d.get('_percent_str', '0%').strip('%'))
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', d.get('total_bytes_estimate', 0))
            speed = d.get('_speed_str', 'N/A').strip()
            eta = d.get('_eta_str', 'N/A').strip()

            label = "📥 Downloading"
            if current_phase == "video": label = "🎥 Video"
            elif current_phase == "audio": label = "🔊 Audio"

            progress_bar.value = percent
            progress_label.value = f"{label}... {percent:.1f}% | {downloaded / 1e6:.2f}MB of {total / 1e6:.2f}MB @ {speed}, ETA: {eta}"
        except: pass
    elif d['status'] == 'finished':
        progress_bar.value = 100
        progress_label.value = f"✅ {current_phase.capitalize()} download complete."


# --- Merge Simulation ---
def simulate_merging_bar():
    global current_phase
    current_phase = "merging"
    progress_label.value = "🛠️ Merging audio and video..."
    for i in range(101):
        progress_bar.value = i
        time.sleep(0.02)
    progress_label.value = "✅ Merge complete. Preparing download..."


# --- Main Download Handler ---
def run_download(b):
    with progress_output:
        clear_output()
        progress_bar.value = 0
        progress_label.value = ""
        print("⏳ Preparing download...")

        url = yt_url.value.strip()
        fmt = file_format.value
        res = quality.value.replace('p', '')

        if not url:
            print("❌ Please enter a YouTube URL.")
            return

        if cookie_upload.value:
            with open("cookies.txt", "wb") as f:
                f.write(list(cookie_upload.value.values())[0]['content'])

        import yt_dlp

        try:
            ydl_info_opts = {'quiet': True}
            if os.path.exists("cookies.txt"):
                ydl_info_opts['cookiefile'] = 'cookies.txt'

            with yt_dlp.YoutubeDL(ydl_info_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
        except Exception as e:
            print(f"❌ Failed to fetch video info: {str(e)}")
            return

        title = info_dict.get('title', 'video').replace(" ", "_").replace("/", "_")
        output_name = f"{title}.%(ext)s"

        global current_phase

        if fmt == 'mp3':
            current_phase = "audio"
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_name,
                'ffmpeg_location': '/usr/bin/ffmpeg',
                'progress_hooks': [hook_print],
                'quiet': True,
                'no_warnings': True,
                'noprogress': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }
        else:
            ydl_opts = {
                'format': f'bestvideo[height<={res}]+bestaudio/best',
                'outtmpl': output_name,
                'ffmpeg_location': '/usr/bin/ffmpeg',
                'progress_hooks': [hook_print],
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
                'noprogress': True
            }

        if os.path.exists("cookies.txt"):
            ydl_opts['cookiefile'] = "cookies.txt"

        current_phase = "video"
        print(f"🎥 Downloading video in {res}p...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if fmt == 'mp4':
            simulate_merging_bar()

        print("✅ Download complete. Generating file link...")
        serve_download(fmt, title)


# --- File Download Helper ---
def serve_download(fmt, base_name):
    for file in os.listdir():
        if file.endswith(f'.{fmt}'):
            print(f"⬇️ Click below to download: {file}")
            files.download(file)
            break


# --- Bind Events ---
download_button.on_click(run_download)

# --- Display UI ---
display(widgets.VBox([
    yt_url,
    widgets.HBox([quality, file_format]),
    cookie_upload,
    download_button,
    progress_bar,
    progress_label,
    progress_output
]))