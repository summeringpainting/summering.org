from flask import Flask, render_template, Response
import requests


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/audio_stream.opus")
def Audio_Stream():
    headers = {'Accept-Ranges': 'bytes'}
    r = requests.get("http://10.0.0.125:8000/radio.opus", headers=headers, stream=True)
    return Response(r.iter_content(chunk_size=1024), mimetype='audio/mp3', direct_passthrough=True)



if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)

