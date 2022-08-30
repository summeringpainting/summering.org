from turtle import dot
from flask import Flask, render_template, Response
import requests
import os
import eyed3
from dotenv import load_dotenv, find_dotenv
from bs4 import BeautifulSoup

app = Flask(__name__)

load_dotenv(find_dotenv())
print(os.getenv("STATS_DOMAIN"))


@app.route('/')
def home():
    statsurl = os.getenv("STATS_DOMAIN")
    s = requests.get(statsurl).text
    soup = BeautifulSoup(s, 'html.parser')
    stats = []
    md = {}
    for row in soup.find_all('tr'):
        stats.append(row.get_text())
    #file = stats[8].split(" - ")[1] + ".mp3"
    #tag = eyed3.load(os.getenv("MUSIC_DIR") + file)
    # print(tag.tag.album)
    return render_template("index.html", stats=stats, md=md)


@app.route("/audio_stream.mp3")
def Audio_Stream():
    streamurl = os.getenv("RADIO_DOMAIN")
    headers = {'Accept-Ranges': 'bytes'}
    r = requests.get(streamurl, headers=headers, stream=True)
    song = Response(r.iter_content(chunk_size=1024),
                    mimetype='audio/mp3', direct_passthrough=True)
    return song


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
