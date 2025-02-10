from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

# Folder untuk menyimpan file yang diunduh
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_media(url, format_type):
    """Fungsi untuk mengunduh video/audio dari YouTube menggunakan yt-dlp."""
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
    }

    if format_type == "mp3":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    elif format_type == "mp4":
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best'
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if format_type == "mp3":
                filename = filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")
            return {"success": True, "filename": filename}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route("/")
def home():
    return "Ony Downloader API is running!"

@app.route("/download", methods=["POST"])
def download():
    """API endpoint untuk mendownload video atau audio."""
    data = request.json
    url = data.get("url")
    format_type = data.get("type", "mp4")  # Default ke MP4 jika tidak ada input

    if not url:
        return jsonify({"error": "URL tidak boleh kosong"}), 400

    result = download_media(url, format_type)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
