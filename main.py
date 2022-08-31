from flask import Flask, render_template, Response
import requests
from bs4 import BeautifulSoup
import os
import json
from dotenv import load_dotenv, find_dotenv
import eyed3
import eyed3.plugins.art
import subprocess
import base64


load_dotenv(find_dotenv())

app = Flask(__name__)


@app.route('/api/cover')
def get_cover():
    data = {}
    with open('/tmp/FRONT_COVER.jpg', mode='rb') as file:
        img = file.read()
    data['img'] = base64.encodebytes(img).decode('utf-8')
    os.system("rm /tmp/FRONT_COVER.jpg")
    return new Response(json.dumps(data), status=200, mimetype="application/json")


@app.route('/api/getmetadata')
def getmetadata():
    """Root with radio. Use bs4 to scrape data off icecast page."""
    statsurl = os.getenv("STATS_DOMAIN")
    s = requests.get(statsurl).text
    soup = BeautifulSoup(s, 'html.parser')
    stats = []
    md = {}
    for row in soup.find_all('tr'):
        stats.append(row.get_text())
    file = stats[9].split(":")[1]
    file = f'{file}.mp3'
    file = file.replace(' ', r'\ ')
    file = file.replace("'", r"\'")
    test = subprocess.run(['find', os.getenv("MUSIC_DIR"), '-name', f'{file}',
                           '-print'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    test = test.strip()
    os.system(f"eyeD3 --write-images=/tmp {test}")
    print(test)
    print(file)
    try:
        tag = eyed3.load(test)
        md["title"] = tag.tag.title
        md["artist"] = tag.tag.artist
        md["album"] = tag.tag.album
        md["album_artist"] = tag.tag.album_artist
        md["genre"] = tag.tag.genre.name
        md["album_cover"] = im1
        print("Title:", tag.tag.title)
        print("Artist:", tag.tag.artist)
        print("Album:", tag.tag.album)
        print("Album artist:", tag.tag.album_artist)
        print("Genre:", tag.tag.genre.name)
        print(tag)
        return Response(json.dumps(md, indent = 4), status=200, mimetype='application/json')
    except (FileNotFoundError, OSError):
        print("ERROR >> eyed3 couldn't even find your music file :|")
        return Response("{'res':'Great! You broke it (eyed3 couldnt find music file)'}", status=404, mimetype='application/json')



@app.route('/')
def home():
    """Home."""
    return render_template("index.html")


@app.route("/audio_stream.mp3")
def Audio_Stream():
    """Grab the stream from icecast radio."""
    streamurl = os.getenv("RADIO_DOMAIN")
    headers = {'Accept-Ranges': 'bytes'}
    r = requests.get(streamurl, headers=headers, stream=True)
    song = Response(r.iter_content(chunk_size=1024),
                    mimetype='audio/mp3',
                    direct_passthrough=True)
    return song


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)

