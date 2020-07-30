# RADIO BAGGA 2: Return of the BAGGER :stars:

### :hotsprings: The sweatlodge of the soul is back.


## Requirements

* [Raspotify](https://github.com/dtcooper/raspotify) running as a background service
* [pi_fm_rds](https://github.com/ChristopheJacquet/PiFmRds)
* [sox](http://sox.sourceforge.net/)
* Python libraries in requirements.txt

## Installation

* Set up Raspotify with pipe as an audio device pointing to `/opt/music/spotify`
* Compile and set up pi_fm_rds
* Create the following fifo pipes using `mkfifo`:
  * `rds_ctl`
  * `/opt/music/spotify`
  * `/home/pi/pipe` - Only used by main.py:76, feel free to change
* Optional: populate `.env` with a Spotify API key
