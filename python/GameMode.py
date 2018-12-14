# ============================================================================
# GameMode Class
# ============================================================================

from logger import log
import time

INACTIVE_THRESHOLD = 4 # 1 second


class GameMode(object):
    def __init__(self):
        self._instrument = [ {
            'active': 0, 
            'maxPreset': 5, 
            'currentPreset': 0,
            'lastSeen': 0,
            } for i in range(0, 4) ]
        self._prev_offline_objects = []

    def killOfflineObjects(self, data):
        offline_objects = []
        if data and 'ping' in data[0]:
            objId = int(data[2])
            self._instrument[objId]['lastSeen'] = time.time()
        for i, instr in enumerate(self._instrument):
            if (time.time() - instr['lastSeen']) > INACTIVE_THRESHOLD:
                offline_objects.append(i)
        offline_objects.sort()
        if offline_objects != self._prev_offline_objects:
            log.debug('change in offline objects list: %s', offline_objects)
            for obj in offline_objects:
                self.net.sendObjectNotConnected(obj)
            self._prev_offline_objects = list(offline_objects)



