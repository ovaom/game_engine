echo "Waiting 5 seconds before startup..."
#/usr/bin/pd -nogui -realtime -blocksize 1024 -audiobuf 50 -jack -r 44100 /home/pi/Documents/ovaom/puredata/main3.pd > /home/pi/Documents/ovaom/logs/puredata_stdout.log 2>&1 & 
#/usr/bin/python /home/pi/Documents/ovaom/python/game_engine.py > /home/pi/Documents/ovaom/logs/python_stdout.log 2>&1