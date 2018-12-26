# ============================================================================
# GameMode Class
# ============================================================================

from logger import log
import time
from AudioPlay import AudioPlay

INACTIVE_THRESHOLD = 4 # in seconds

class GameMode(object):
    ''' GameMode Class: puzzleMode and jungleMode must inherit from this class '''

    instrument = [ {
            'active': 0, 
            'maxPreset': 5, 
            'currentPreset': 0,
            'lastSeen': -1,
            } for i in range(0, 4) ]
    prev_offline_objects = []

    def __init__(self, net):
        self.net = net
        self._audio = AudioPlay(net)
        self.instructionsPlaying = False
        self.net.sendAllObjectsIdle()

    def run(self, data):
        self._storeObjectsState(data)
        self._killOfflineObjects(data)

    def _killOfflineObjects(self, data):
        offline_objects = []
        if data and 'ping' in data[0]:
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
            


