from flask import Flask
from flask import request
from flask import jsonify
import numpy as np
from lib.mct import MCT
from lib.mct_node import MCTNode

app = Flask(__name__)

@app.route('/simulate', methods=['POST'])
def simulate():
    current_state = request.get_json(force=True)
    player_state = np.array(current_state["player"], dtype = np.dtype(int))
    opponent_state = np.array(current_state["opponent"], dtype = np.dtype(int))
    states = {
        "flow": [
        ],
        "next_move": None
    }
    mct = MCT(player_state, opponent_state, current_state["iterations"])
    if mct.wins:
        current_best = max(mct.wins, 
            key = lambda win: win.upper_confidence_bound + win.mean
        )
    else:
        current_best = mct.current_best

    while current_best.parent:
        state = {}
        state["opponent_turn"] = current_best.opponent_playing
        state["times_visited"] = current_best.times_visited
        current_best.player_state[current_best.player_state > 0] = 1
        current_best.opponent_state[current_best.opponent_state > 0] = 2
        player_uniform = current_best.player_state
        opponent_uniform = current_best.opponent_state
        state["state"] = (player_uniform + opponent_uniform).tolist()
        state["actions"] = current_best.actions
        # state["piece_id"] = current_best.piece_id
        states["flow"].insert(0, state)
        current_best = current_best.parent
        if current_best.parent and not current_best.parent.parent:
            states["next_move"] = current_best.actions

    return jsonify(states)