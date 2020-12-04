#!/usr/bin/python

import sys
sys.path.insert(0, './lib/')

import json

from lib.mct import MCT
import numpy as np

def main():
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} json')
        return 1

    file = open(sys.argv[1], 'r')
    game_state = json.loads(file.read())
    player_state = np.array(game_state["player"])
    opponent_state = np.array(game_state["opponent"])

    mct = MCT(player_state, opponent_state, 200000)



if __name__ == "__main__":
    main()