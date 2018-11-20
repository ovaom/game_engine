# 
# game_engine.py
# 

import network
import GPIO
import jungleMode
import puzzleMode

if __name__ == "__main__":
   
    game = {
        "mode": "PUZZLE",
    }
    try:
        GPIO = GPIO.InOut(game)
    except Exception as e:
        print "GPIO Error:"
        print e        
    net = network.Network()
    jungle = jungleMode.Jungle(net)
    puzzle = puzzleMode.Puzzle(GPIO)
    
    while True:
        GPIO.readVolumeKnob()
        if game["mode"] == "JUNGLE":
            jungle.run(net)
        elif game["mode"] == "PUZZLE":
            puzzle.run(net)
