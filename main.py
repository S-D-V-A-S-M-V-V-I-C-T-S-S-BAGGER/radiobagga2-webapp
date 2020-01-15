import tendo as tendo
from flask import Flask, jsonify
import subprocess
import threading
import os
import signal
import atexit

from tendo import singleton
from random import shuffle

app = Flask(__name__, static_url_path='')

playing = False
p = None


@app.before_first_request
def startup():
    threading.Thread(target=play_loop).start()


def play_loop():
    global p
    me = singleton.SingleInstance()

    while True:
        if playing:
            runstr = 'sox -t raw -c 2 -r 44k -e signed-integer -L -b 16 /opt/music/spotify -t .wav - | pi_fm_rds -freq {0} -pi 6969 -ps {1} -rt "{2}" -audio -'
            frequency = '107.5'
            radio_name = 'BAGGAFM'
            radio_text = "RADIO BAGGA: De Zweethut van de Ziel"

            p = subprocess.Popen(runstr.format(frequency, radio_name, radio_text), preexec_fn=os.setsid)
            p.communicate()


@app.route('/start')
def start():
    global playing
    playing = True


@app.route('/stop')
def shutdown():
    os.killpg(os.getpgid(p.pid), signal.SIGTERM)
    return jsonify(success=True)


atexit.register(shutdown)
