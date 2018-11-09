# 
# game_engine.py
# 

import network
import jungleMode
import puzzleMode

if __name__ == "__main__":
   
    net = network.Network()
    jungle = jungleMode.Jungle(net)
    puzzle = puzzleMode.Puzzle()
    MODE = "PUZZLE"

    while True:
        if MODE == "JUNGLE":
            jungle.run(net)
        elif MODE == "PUZZLE":
            puzzle.run(net)
