import logging

log = logging.getLogger('ovaom')
log_handler = logging.FileHandler('/home/pi/Documents/ovaom/logs/game_engine.log')
log.addHandler(log_handler)
