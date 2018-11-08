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

    while True:
        # jungle.run(net)
        puzzle.run(net)
