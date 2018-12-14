# ============================================================================
# Observer.py
# ============================================================================

from CONST import *

class Observer():
    _observers = []

    def __init__(self):
        self._observers.append(self)
        self._observables = {}

    def observe(self, eventName, callback):
        self._observables[eventName] = callback


class Event():
    def __init__(self, name, data, autofire = True):
        self.name = name
        self.data = data
        if autofire:
            self.fire()
    def fire(self):
        for observer in Observer._observers:
            if self.name in observer._observables: 
                observer._observables[self.name](self.data)
