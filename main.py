from flask import Flask, render_template
import requests


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/radio")
def radio():
    r = requests.get("http://localhost:8000/radio.ogg", stream=True)
    return requests.Response((r.iter_content(chunk_size=1024), mimetype="audio/ogg"))


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
