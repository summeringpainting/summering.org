from flask import Flask, render_template, Response
import requests


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/audio_stream.mp3")
def Audio_Stream():
    headers = {'Transfer-Encoding': 'chunked'}
    r = requests.get("http://ais-edge69-nyc04.cdnstream.com/2263_128.mp3", headers=headers, stream=True)
    return Response(r.iter_content(chunk_size=1024), mimetype='audio/mp3', direct_passthrough=True)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)

