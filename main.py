from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.clock import Clock
from pytubefix import YouTube
import os
import re

BASE_FOLDER = os.path.join(os.path.expanduser("~"), "Ony Downloader")
VIDEO_FOLDER = os.path.join(BASE_FOLDER, "Video")
AUDIO_FOLDER = os.path.join(BASE_FOLDER, "Audio")

os.makedirs(VIDEO_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

def sanitize_filename(filename):
    return re.sub(r'[\\/:*?"<>|]', '', filename)

def download_video(url, update_progress):
    try:
        yt = YouTube(url, on_progress_callback=update_progress)
        video_title = sanitize_filename(yt.title)
        stream = yt.streams.get_highest_resolution()
        filename = f"{video_title}.mp4"
        filepath = os.path.join(VIDEO_FOLDER, filename)
        stream.download(output_path=VIDEO_FOLDER, filename=filename)
        return f"Video berhasil diunduh: {filepath}"
    except Exception as e:
        return f"Error: {e}"

def download_audio(url, update_progress):
    try:
        yt = YouTube(url, on_progress_callback=update_progress)
        audio_title = sanitize_filename(yt.title)
        stream = yt.streams.filter(only_audio=True).first()
        filename = f"{audio_title}.mp3"
        filepath = os.path.join(AUDIO_FOLDER, filename)
        temp_file = stream.download(output_path=AUDIO_FOLDER)
        os.rename(temp_file, filepath)
        return f"Audio berhasil diunduh: {filepath}"
    except Exception as e:
        return f"Error: {e}"

KV = '''
ScreenManager:
    MenuScreen:
    DownloadScreen:

<MenuScreen>:
    name: "menu"
    MDLabel:
        text: "ONY DOWNLOADER"
        halign: "center"
        font_style: "H4"
        pos_hint: {"center_y": 0.85}

    MDLabel:
        text: "Tolong bantu saya berkembang, jika ada bug atau error WA ke saya ya... 081515650449"
        halign: "center"
        font_style: "Caption"
        pos_hint: {"center_y": 0.75}
        theme_text_color: "Secondary"

    MDTextField:
        id: url_input
        hint_text: "Masukkan URL YouTube"
        pos_hint: {"center_x": 0.5, "center_y": 0.6}
        size_hint_x: 0.8

    MDRaisedButton:
        text: "Download Video"
        pos_hint: {"center_x": 0.5, "center_y": 0.45}
        on_release:
            root.manager.current = "download"
            app.download_youtube("video")

    MDRaisedButton:
        text: "Download Audio"
        pos_hint: {"center_x": 0.5, "center_y": 0.35}
        on_release:
            root.manager.current = "download"
            app.download_youtube("audio")

<DownloadScreen>:
    name: "download"
    MDLabel:
        id: status_label
        text: "Sedang mengunduh..."
        halign: "center"
        font_style: "H5"
        pos_hint: {"center_y": 0.6}

    MDProgressBar:
        id: progress_bar
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint_x: 0.8
        max: 100
        value: 0

    Image:
        source: "loading.gif"
        anim_delay: 0.05
        pos_hint: {"center_x": 0.5, "center_y": 0.7}

    MDRaisedButton:
        text: "Kembali ke Menu"
        pos_hint: {"center_x": 0.5, "center_y": 0.3}
        on_release: root.manager.current = "menu"
'''

class MenuScreen(Screen):
    pass

class DownloadScreen(Screen):
    pass

class OnyDownloaderApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def update_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = int((bytes_downloaded / total_size) * 100)
        self.root.get_screen("download").ids.progress_bar.value = percentage
        self.root.get_screen("download").ids.status_label.text = f"Mengunduh... {percentage}%"

    def download_youtube(self, file_type):
        screen = self.root.get_screen("menu")
        url = screen.ids.url_input.text.strip()
        status_screen = self.root.get_screen("download")
        status_screen.ids.progress_bar.value = 0
        status_screen.ids.status_label.text = "Sedang mengunduh..."

        if not url:
            status_screen.ids.status_label.text = "URL tidak boleh kosong!"
            return

        if file_type == "video":
            result = download_video(url, self.update_progress)
        else:
            result = download_audio(url, self.update_progress)

        status_screen.ids.status_label.text = result

if __name__ == "__main__":
    OnyDownloaderApp().run()
