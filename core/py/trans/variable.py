import ctypes
from enum import Enum


class VarConfig(Enum):
    BASE = ctypes.c_int

    A_STAR_MAP         = ctypes.c_int
    A_STAR_W_H         = ctypes.c_int
    A_STAR_POINT       = ctypes.c_int
    A_STAR_OUT_BUFFER  = ctypes.c_int
    A_STAR_REBACK      = ctypes.c_int

class FunctionName(Enum):
    SOLVE_A_STAR = 'solve_astar'
