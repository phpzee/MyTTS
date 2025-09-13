from flask import Flask, render_template, request, send_file
from gtts import gTTS
from pathlib import Path
import os, time

app = Flask(__name__)

# Save folder
BASE_FOLDER = Path.home() / "voice-clone-tts" / "mp3Files"
os.makedirs(BASE_FOLDER, exist_ok=True)

# Hindi speakers (gTTS supports language + TLD trick for voice variations)
HINDI_SPEAKERS = {
    "Standard Hindi": {"lang": "hi", "tld": "co.in"},
    "Female-ish Hindi": {"lang": "hi", "tld": "com"},
    "Hindi UK Accent": {"lang": "hi", "tld": "co.uk"},
    "Hindi Canadian": {"lang": "hi", "tld": "ca"},
    "Hindi Australian": {"lang": "hi", "tld": "com.au"},
    "Hindi US Accent": {"lang": "hi", "tld": "us"},
    "Hindi Indian Regional": {"lang": "hi", "tld": "in"},
    "Hindi Standard 2": {"lang": "hi", "tld": "co.in"},
    "Hindi Female 2": {"lang": "hi", "tld": "co.in"},
    "Hindi Neutral": {"lang": "hi", "tld": "com"}
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text")
        speaker = request.form.get("speaker")
        if not text.strip():
            return render_template("app.html", error="Please enter some text!", success=None, speakers=HINDI_SPEAKERS)
        try:
            lang = HINDI_SPEAKERS[speaker]["lang"]
            tld = HINDI_SPEAKERS[speaker]["tld"]

            filename = f"tts_{int(time.time())}.mp3"
            file_path = BASE_FOLDER / filename

            tts = gTTS(text=text, lang=lang, tld=tld)
            tts.save(file_path)

            return render_template("app.html",
                                   success=f"MP3 ready: {filename}",
                                   filename=filename,
                                   speakers=HINDI_SPEAKERS)
        except Exception as e:
            return render_template("app.html", error=f"TTS error: {e}", success=None, speakers=HINDI_SPEAKERS)

    return render_template("app.html", error=None, success=None, speakers=HINDI_SPEAKERS)

@app.route("/play/<filename>")
def play_file(filename):
    file_path = BASE_FOLDER / filename
    return send_file(file_path, mimetype="audio/mpeg")

@app.route("/download/<filename>")
def download_file(filename):
    file_path = BASE_FOLDER / filename
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    print("Access the app at http://<your_PC_IP>:5000 on your mobile (same WiFi)")
    app.run(host="0.0.0.0", port=5000, debug=True)
