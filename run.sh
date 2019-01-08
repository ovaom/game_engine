echo "Waiting 3 seconds before startup..." 
sleep 3
/usr/bin/pd -nogui -realtime -blocksize 1024 -audiobuf 50 -alsa -r 44100 /home/pi/Documents/puredata/main.pd > /home/pi/Documents/ovaom/logs/puredata_stdout.log 2>&1 & 
sleep 2
/usr/bin/python /home/pi/Documents/ovaom/python/game_engine.py > /home/pi/Documents/ovaom/logs/python_stdout.log 2>&1
