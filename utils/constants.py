from enum import Enum

class Mode(Enum):
    HEURISTIC = 1
    NEURAL_NETWORK = 2

class Method(Enum):
    STOCHASTIC = 1
    DETERMINISTIC = 2

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