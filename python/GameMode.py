# ============================================================================
# GameMode Class
# ============================================================================

from logger import logging, log
import time
from AudioPlay import AudioPlay

battLog = logging.getLogger('BATTERY')
batt_handler = logging.FileHandler('/home/pi/Documents/ovaom/logs/battery_monitor.log')
battLog.addHandler(batt_handler)

INACTIVE_THRESHOLD = 5 # in seconds

class GameMode(object):
    ''' GameMode Class: puzzleMode and jungleMode must inherit from this class '''

    instrument = [ {
            'active': 0, 
            'maxPreset': 1, 
            'currentPreset': 0,
            'lastSeen': -1,
            'battery': 0,
            } for i in range(0, 4) ]
    prev_offline_objects = []
    prevMonitoring = 0

    def __init__(self, net):
        self.net = net
        self._audio = AudioPlay(net)
        self.instructionsPlaying = False
        self.net.sendAllObjectsIdle()

    def run(self, data):
        self._storeObjectsState(data)
        self._killOfflineObjects(data)
        self._getBatteryLevels(data)
        self._ObjectsMonitoringLog()

    def _killOfflineObjects(self, data):
        offline_objects = []
        if data and ('ping' in data[0] or 'params' in data[0]):
            objId = int(data[2])
            GameMode.instrument[objId]['lastSeen'] = time.time()
        for i, instr in enumerate(GameMode.instrument):
            if (time.time() - instr['lastSeen']) > INACTIVE_THRESHOLD:
                offline_objects.append(i)
        offline_objects.sort()
        if offline_objects != GameMode.prev_offline_objects:
            log.debug('change in offline objects list: %s', offline_objects)
            for obj in offline_objects:
                self.net.sendObjectNotConnected(obj)
                GameMode.instrument[obj]['active'] = 0
            GameMode.prev_offline_objects = list(offline_objects)

    def _storeObjectsState(self, data):
        if data and 'state' in data[0]:
            objId = int(data[0][8])
            GameMode.instrument[objId]["active"] = data[2]
        if data and 'ping' in data[0]:
            objId = int(data[2])
            state = int(data[3])  
            if state != GameMode.instrument[objId]['active']:
                log.debug('Notice: object state %d out of sync, resync', objId)
                self.net.sendState(objId, state)
                GameMode.instrument[objId]['active'] = state

    def _getBatteryLevels(self, data):
        if data and 'ping' in data[0]:
            objId = int(data[2])
            GameMode.instrument[objId]["battery"] = data[4]

    def _ObjectsMonitoringLog(self):
        if (time.time() - GameMode.prevMonitoring) > 10:
            out  = 'BATTERY: '
            levels = [0, 0, 0, 0]
            for i, inst in enumerate(GameMode.instrument):
                levels[i] = inst['battery']
            
            battLog.info('grelot:%d | ocarina:%d | bolstick:%d | corail:%d', levels[0], levels[1], levels[2], levels[3])
            GameMode.prevMonitoring = time.time()