from enum import Enum

class Mode(Enum):
    HEURISTIC = 1
    NEURAL_NETWORK = 2

class Method(Enum):
    STOCHASTIC = 1
    DETERMINISTIC = 2

class Agent(Enum):
    PLAYER = 1
    OPPONENT = 2

class Configuration:
    VALID_MOVES = {
        "down": {
            "short": (1, 0),
            "long": (2, 0)
        },
        "up": {
            "short": (-1, 0),
            "long": (-2, 0)
        },
        "right": {
            "short": (0, 1),
            "long": (0, 2)
        },
        "left": {
            "short": (0, -1),
            "long": (0, -2)
        },
        "lower_diagonal": {
            "short": (1, 1),
            "long": (2, 2)
        },
        "upper_diagonal": {
            "short": (-1, -1),
            "long": (-2, -2)
        }
    }

    ENDGAME = {
        "player": {
            (0, 8), (0, 7), (1, 8), (0, 6), (1, 7), (2, 8), (0, 5), (1, 6),
            (2, 7), (3, 8)
        },
        "opponent": {
            (8, 0), (8, 1), (7, 0), (8, 2), (7, 1), (6, 0), (8, 3), (7, 2), 
            (6, 1), (5, 0)
        }
    }

    EXPLORATION_LEVEL = 3.5