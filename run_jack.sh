echo "Waiting 5 seconds before startup..."
/usr/bin/jackd -d alsa -r 44100 -P > /home/pi/Documents/ovaom/logs/jackd_stdout.log 2>&1 & 
/usr/bin/pd -jack -noadc -realtime -r 44100 /home/pi/Documents/ovaom/puredata/main3.pd > /home/pi/Documents/ovaom/logs/puredata_stdout.log 2>&1 & 
/usr/bin/python /home/pi/Documents/ovaom/python/game_engine.py > /home/pi/Documents/ovaom/logs/python_stdout.log 2>&1
