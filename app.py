from flask import Flask, request, jsonify
from pytubefix import YouTube
import os
import re

app = Flask(__name__)

# Fungsi untuk membersihkan nama file agar valid
def sanitize_filename(filename):
    return re.sub(r'[^A-Za-z0-9 ]+', '', filename).strip()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "YouTube Downloader API is running!"})

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    type_ = data.get("type")

    if not url or not type_:
        return jsonify({"error": "Missing url or type"}), 400

    try:
        yt = YouTube(url)
        title = sanitize_filename(yt.title)

        if type_ == "video":
            stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
            filename = f"{title}.mp4"
        elif type_ == "audio":
            stream = yt.streams.filter(only_audio=True).first()
            filename = f"{title}.mp3"
        else:
            return jsonify({"error": "Invalid type. Use 'video' or 'audio'"}), 400

        # Unduh file
        filepath = stream.download()
        os.rename(filepath, filename)  # Rename file sesuai format

        return jsonify({"message": "Download successful", "file": filename})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Gunakan port dari Render
    app.run(host="0.0.0.0", port=port, debug=True)
