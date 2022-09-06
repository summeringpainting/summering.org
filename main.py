from flask import Flask, render_template, Response, redirect
import requests
from bs4 import BeautifulSoup
import os
import json
from dotenv import load_dotenv, find_dotenv
import eyed3
import eyed3.plugins
import subprocess
import base64
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from wtforms import StringField, SubmitField, validators
from flask_ckeditor import CKEditor, CKEditorField
from flask_bootstrap import Bootstrap
import sys
import yagmail


load_dotenv(find_dotenv())

app = Flask(__name__)


# Create random secret key
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
ckeditor = CKEditor(app)
Bootstrap(app)

NoAlbumCoverb64 = ""

class contactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(
        label='Email', validators=[DataRequired(), Email(granular_message=True)])
    message = CKEditorField('')
    submit = SubmitField(label="Send")


@app.route('/api/cover')
def get_cover():
    """Root with radio. Use bs4 to scrape data off icecast page."""
    print("1")
    statsurl = os.getenv("STATS_DOMAIN")
    print("2")
    s = requests.get(statsurl).text
    print("3")
    soup = BeautifulSoup(s, 'html.parser')
    print("4")
    stats = []
    print("5")
    for row in soup.find_all('tr'):
        stats.append(row.get_text())
    print("6")
    file = stats[9].split(":")[1]
    file = f'{file}.mp3'
    file = file.replace(' ', r'\ ')
    file = file.replace("'", r"\'")
    file = file.replace("&", r"\&")
    print(f"FILE IS: {file}")
    test = subprocess.run(['find', os.getenv("MUSIC_DIR"), '-name', f'{file}',
                           '-print'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    test = test.strip()
    test = test.replace('(', r'\(')
    test = test.replace(')', r'\)')
    test = test.replace(' ', r'\ ')
    test = test.replace("'", r"\'")
    test = test.replace(r"&", r"\&")
    print(test)
    print(f"tester is {test}")
    os.system(f"eyeD3 --write-images=/tmp {test}")
    data = {}
    try:
        with open('/tmp/FRONT_COVER.jpg', mode='rb') as file:
            img = file.read()
        data['img'] = base64.encodebytes(img).decode('utf-8')
        os.system("rm /tmp/FRONT_COVER.jpg")
        return Response(json.dumps(data), status=200)
    except FileNotFoundError:
        print("Not Found")
        with open('static/images/No Album Cover.png', mode='rb') as file:
            img = file.read()
        data['img'] = base64.encodebytes(img).decode('utf-8')
        return Response(json.dumps(data), status=200)


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
    try:
        tag = eyed3.load(test)
        md["title"] = tag.tag.title
        md["artist"] = tag.tag.artist
        md["album"] = tag.tag.album
        md["album_artist"] = tag.tag.album_artist
        md["genre"] = tag.tag.genre.name

        # print("Title:", tag.tag.title)
        # print("Artist:", tag.tag.artist)
        # print("Album:", tag.tag.album)
        # print("Album artist:", tag.tag.album_artist)
        # print("Genre:", tag.tag.genre.name)
        # print(tag)
        return Response(json.dumps(md, indent=4),
                        status=200, mimetype='application/json')
    except (FileNotFoundError, OSError):
        print("ERROR >> eyed3 couldn't even find your music file :|")
        return Response("{res:'Great You broke it (eyed3 couldnt find music file)'}",
                        status=404, mimetype='application/json')


@app.route('/', methods=["GET", "POST"])
def home():
    """Home."""
    return render_template("index.html")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    """Contact Form with WTF."""
    cform = contactForm()
    if cform.validate_on_submit():
        user = 'clownworldremix@gmail.com'
        app_password = 'tbqqxfasxkvcchik' # a token for gmail
        to = ['summeringpainting@gmail.com', 'satosummering@outlook.com']

        subject = f"Name:{cform.name.data}, E-mail:{cform.email.data},"
        content = [f"message:{cform.message.data}"]

        with yagmail.SMTP(user, app_password) as yag:
            yag.send(to, subject, content)
            print('Sent email successfully')
        return redirect('/')


            #     with open("testy.txt", "w") as f:
            # print(f"Name:{cform.name.data}, E-mail:{cform.email.data},"
            #       f"message:{cform.message.data}")
    return render_template("contact.html", form=cform)


@app.route('/page/<page>')
def page(page):
    page = page
    return render_template(f"pages/{page}.html")


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
