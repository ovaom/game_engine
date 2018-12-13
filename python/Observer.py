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

# class Button(Observer):
#     def __init__(self):
#         Observer.__init__(self)

#     def puzzleClick(self, data):
#         game['mode'] = PUZZLE
#         GPIO.setPuzzleLedON()
#         jungle.reset()
#         jungle.stopAudio()

#     def jungleClick(self, data):
#         game['mode'] = JUNGLE
#         GPIO.setJungleLedON()
#         puzzle.reset()
#         puzzle.stopAudio()

#     def repeatClick(self, data):
#         if game['mode'] == PUZZLE:
#             GPIO.setRepeatLED(data)
#         if data:
#             puzzle.stopAudio()
#             puzzle.setStep('SPEAK_INSTRUCTIONS')

#     def skipClick(self, data):
#         if game['mode'] == PUZZLE:
#             GPIO.setSkipLED(data)
#         if data:
#             puzzle.stopAudio()
#             puzzle.incrementLevel()