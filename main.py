from flask import Flask, render_template, Response
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv, find_dotenv
import eyed3
import eyed3.plugins.art
import subprocess
from PIL import Image
import PIL
# from fnmatch import fnmatch
# from ..id3.frames import ImageFrame


load_dotenv(find_dotenv())

app = Flask(__name__)


@app.route('/')
def home():
    """Root with radio. Use bs4 to scrape data off icecast page."""
    statsurl = os.getenv("STATS_DOMAIN")
    s = requests.get(statsurl).text
    soup = BeautifulSoup(s, 'html.parser')
    stats = []
    for row in soup.find_all('tr'):
        stats.append(row.get_text())
    file = stats[9].split(":")[1]
    file = f'{file}.mp3'
    file = file.replace(' ', r'\ ')
    file = file.replace("'", r"\'")
    test = subprocess.run(['find', '/home/steve/Music/', '-name', f'{file}',
                           '-print'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    test = test.strip()
    print(test)
    print(file)
    try:
        tag = eyed3.load("test")
        print("Title:", tag.tag.title)
        print("Artist:", tag.tag.artist)
        print("Album:", tag.tag.album)
        print("Album artist:", tag.tag.album_artist)
        print("Genre:", tag.tag.genre.name)

        print(tag)
        # print(eyed3.plugins.art.ArtFile(test))
        return render_template("index.html", stats=stats)
    except (FileNotFoundError, OSError):
        return render_template("index.html", stats=stats)


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

