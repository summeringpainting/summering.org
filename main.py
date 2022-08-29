from flask import Flask, render_template, Response
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def home():
    statsurl = "http://10.0.0.125:8000/status.xsl"
    s = requests.get(statsurl).text
    soup = BeautifulSoup(s, 'html.parser')
    stats = []
    for row in soup.find_all('tr'):
        stats.append(row.get_text())
    return render_template("index.html", stats=stats)


@app.route("/audio_stream.mp3")
def Audio_Stream():
    streamurl = "http://10.0.0.125:8000/radio.mp3"
    headers = {'Accept-Ranges': 'bytes'}
    r = requests.get(streamurl, headers=headers, stream=True)
    song = Response(r.iter_content(chunk_size=1024), mimetype='audio/mp3', direct_passthrough=True)
    return song



if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)

