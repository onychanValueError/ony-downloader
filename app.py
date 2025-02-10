from flask import Flask, request, jsonify
from pytubefix import YouTube
import os
import re

app = Flask(__name__)

# Fungsi untuk membersihkan nama file dari karakter tidak valid
def sanitize_filename(filename):
    return re.sub(r'[^A-Za-z0-9 ]+', '', filename).strip()

# Endpoint utama untuk mengecek apakah API berjalan
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "YouTube Downloader API is running!"}), 200

# Endpoint untuk mendownload video/audio
@app.route("/download", methods=["POST"])
def download():
    try:
        data = request.json
        if not data or "url" not in data or "type" not in data:
            return jsonify({"error": "Invalid request"}), 400

        url = data["url"]
        download_type = data["type"].lower()

        yt = YouTube(url)
        title = sanitize_filename(yt.title)

        if download_type == "video":
            stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
            filename = f"{title}.mp4"
        elif download_type == "audio":
            stream = yt.streams.filter(only_audio=True).first()
            filename = f"{title}.mp3"
        else:
            return jsonify({"error": "Invalid download type. Use 'video' or 'audio'"}), 400

        # Simpan file di folder sementara
        temp_path = stream.download()
        new_path = os.path.join(os.getcwd(), filename)

        # Ganti nama file ke format yang benar
        os.rename(temp_path, new_path)

        return jsonify({
            "message": f"Download completed!",
            "title": yt.title,
            "filename": filename,
            "download_url": f"/downloaded/{filename}"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Menjalankan server Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
