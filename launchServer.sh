echo "Waiting 5 seconds before startup..."
sleep 5
/usr/bin/pd -nogui /home/pi/Documents/ovaom/puredata/main3.pd > /home/pi/Documents/ovaom/puredata_stdout.log 2>&1  & 
/usr/bin/python /home/pi/Documents/ovaom/python/game_engine.py > /home/pi/Documents/ovaom/python_stdout.log 2>&1 &
