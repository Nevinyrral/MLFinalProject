from enum import Enum

class Mode(Enum):
    HEURISTIC = 1
    NEURAL_NETWORK = 2

class Method(Enum):
    STOCHASTIC = 1
    DETERMINISTIC = 2