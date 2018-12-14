# 
# volumeControl.py
# 

import alsaaudio
import time

class VolumeCtrl(object):
    def __init__(self, gpio):
        self.mixer = alsaaudio.Mixer("Digital")
        self.gpio = gpio
   
    def mainVolume_RW(self):
        knob = self.gpio.getVolumeKnob()
        vol = alsaaudio.Mixer("Digital").getvolume()[1]
        if knob != None:
            if abs(knob - vol) > 1:
                alsaaudio.Mixer("Digital").setvolume(knob)
