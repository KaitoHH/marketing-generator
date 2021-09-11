import os
import base64
from gtts import gTTS
from util import gen_text
from pydub import AudioSegment
from datetime import date
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
allow_origin = ["https://market.kaitohh.com", "http://market.kaitohh.com"]
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'


@app.route('/')
def hello_world():
    return render_template('index.html', copyright_year=date.today().year)


@app.route('/generate')
@cross_origin(origins=allow_origin)
def generate():
    what = request.args.get('what')
    how = request.args.get('how')
    fact = request.args.get('fact')
    name = '{0}{1}.mp3'.format(what, how)
    gTTS(text=gen_text(what, how, fact), lang='zh-cn', slow=False).save(name)
    target = AudioSegment.from_file(name)
    bgm = AudioSegment.from_file('resource/trip.m4a')
    ret = target.overlay(bgm)
    ret.export(name)
    enc = base64.b64encode(open(name, "rb").read())
    os.remove(name)
    src = b'data:audio/mpeg;base64,' + enc
    return src


@app.route('/ping')
@cross_origin(origins=allow_origin)
def ping():
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
