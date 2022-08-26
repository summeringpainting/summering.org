from flask import Flask, render_template
import requests


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/audio_stream")
def Audio_Stream():
    r = requests.get("http://localhost:8000/radio.mp3", stream=True)
    return Response(r.iter_content(chunk_size=1024), mimetype='audio/mpeg')

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)

