# 
# game_engine.py
# 

import network
# import GPIO
import jungleMode
import puzzleMode

if __name__ == "__main__":
   
    net = network.Network()
    jungle = jungleMode.Jungle(net)
    puzzle = puzzleMode.Puzzle()
    # GPIO = GPIO.GPIO()
    MODE = "JUNGLE"

    while True:
        # GPIO.read()
        if MODE == "JUNGLE":
            jungle.run(net)
        elif MODE == "PUZZLE":
            puzzle.run(net)
