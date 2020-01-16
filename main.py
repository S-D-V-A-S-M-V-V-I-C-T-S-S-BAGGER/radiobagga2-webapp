import atexit
import os
import signal
import subprocess
import threading

import requests
from flask import Flask, jsonify, request
from tendo import singleton

app = Flask(__name__, static_url_path='')

playing = False
p = None
radio_text = "RADIO BAGGA: De Zweethut van de Ziel"


@app.before_first_request
def startup():
    threading.Thread(target=play_loop).start()


def play_loop():
    global p
    global playing
    global radio_text
    me = singleton.SingleInstance()

    while True:
        if playing:
            frequency = '107.5'
            radio_name = 'BAGGAFM'

            p = subprocess.Popen(['sox', "-t raw -c 2 -r 44k -e signed-integer -L -b 16 /opt/music/spotify -t .wav - | pi_fm_rds -freq %s -pi 6969 -ps %s -rt %s -audio -" % (frequency, radio_name, radio_text)],
                                 preexec_fn=os.setsid)

            p.communicate()


@app.route('/start')
def start():
    global playing
    playing = True
    return jsonify(success=True)


@app.route('/stop')
def stop():
    shutdown()
    return jsonify(success=True)


@app.route('/update', methods=['POST'])
def update():
    global radio_text
    track_id = request.form['id']
    r = requests.get("https://api.spotify.com/v1/tracks/" + track_id + "?market=NL",
                     {'Accept': 'application/json', 'Content-Type': 'application/json',
                      'Authorization': 'Bearer ' + os.environ['SPOTIFY_API_TOKEN']})
    data = r.json()
    radio_text = data['artist'] + ' - ' + data['name']
    print(radio_text)


def shutdown():
    global playing
    playing = False
    try:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    except AttributeError:
        return


atexit.register(shutdown)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
