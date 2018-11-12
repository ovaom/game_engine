/usr/bin/pd -nogui -realtime -blocksize 1024 -audiobuf 50 -alsa -noadc -r 44100 -listdev /home/pi/Documents/ovaom/puredata/main3.pd & 
/usr/bin/python /home/pi/Documents/ovaom/python/game_engine.py 
