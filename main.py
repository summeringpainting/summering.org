from flask import Flask, render_template, Response
import requests


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


# @app.route("/audio_stream")
# def Audio_Stream():
#      r = requests.get("http://localhost:8000/radio.mp3", stream=True)
#      return Response(r.iter_content(chunk_size=1024), mimetype='audio/mp3')
@app.route("/audio_stream")
def streamwav():
    def generate():
        with open("http://localhost:8000/radio.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/x-wav")



if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)

