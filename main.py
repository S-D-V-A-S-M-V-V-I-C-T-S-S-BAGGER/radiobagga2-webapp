import atexit
import os
import signal
import subprocess
import threading

from flask import Flask, jsonify
from tendo import singleton

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
            # runstr = 'sox -t raw -c 2 -r 44k -e signed-integer -L -b 16 /opt/music/spotify -t .wav - | pi_fm_rds -freq {0} -pi 6969 -ps {1} -rt "{2}" -audio -'
            # frequency = '107.5'
            # radio_name = 'BAGGAFM'
            # radio_text = "RADIO BAGGA: De Zweethut van de Ziel"

            # p = subprocess.Popen(runstr.format(frequency, radio_name, radio_text), preexec_fn=os.setsid)

            p = subprocess.Popen(['sudo', 'huts'], preexec_fn=os.setsid)
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


def shutdown():
    os.killpg(os.getpgid(p.pid), signal.SIGTERM)


atexit.register(shutdown)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
