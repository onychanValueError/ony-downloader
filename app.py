from flask import Flask, request, jsonify
from pytubefix import YouTube
import os
import re

app = Flask(__name__)

def sanitize_filename(filename):
    """Menghapus karakter yang tidak diperbolehkan dalam nama file."""
    return re.sub(r'[^A-Za-z0-9 ]+', '', filename).strip()

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    download_type = data.get("type")  # "video" atau "audio"

    try:
        yt = YouTube(url)
        title = sanitize_filename(yt.title)

        if download_type == "video":
            stream = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()
            return jsonify({"status": "success", "title": title, "download_url": stream.url})

        elif download_type == "audio":
            stream = yt.streams.filter(only_audio=True).first()
            return jsonify({"status": "success", "title": title, "download_url": stream.url})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
