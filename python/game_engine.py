# 
# game_engine.py
# 

import network
import GPIO
import jungleMode
import puzzleMode
import volume
import alsaaudio

if __name__ == "__main__":
   
    game = {
        "mode": "JUNGLE",
    }
    try:
        GPIO = GPIO.InOut(game)
    except Exception as e:
        print "GPIO Error:"
        print e
    v = volume.VolumeCtrl(GPIO)
    net = network.Network()
    jungle = jungleMode.Jungle(net)
    puzzle = puzzleMode.Puzzle(GPIO)
    
    while True:
        v.mainVolume_RW()
        GPIO.getGameMode(game)
        if game["mode"] == "JUNGLE":
            jungle.run(net)
        elif game["mode"] == "PUZZLE":
            puzzle.run(net)
