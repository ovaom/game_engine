# 
# game_engine.py
# 

import network
import GPIO
import jungleMode
import puzzleMode
import volume
import threading

if __name__ == "__main__":   
    game = {"mode": "JUNGLE",}
    
    net = network.Network()
    GPIO = GPIO.InOut(game)
    v = volume.VolumeCtrl(GPIO)
    jungle = jungleMode.Jungle(net)
    puzzle = puzzleMode.Puzzle(net, GPIO)
    # threading.Thread(target=v.mainVolume_RW).start()
    
    while True:
        # v.mainVolume_RW()
        GPIO.getGameMode(game)
        if game["mode"] == "JUNGLE":
            jungle.run()
        elif game["mode"] == "PUZZLE":
            puzzle.run()
