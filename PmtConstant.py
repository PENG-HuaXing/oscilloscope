from enum import Enum, auto


class Wave(Enum):
    Trapezoid = auto()
    Riemann = auto()
    Single = auto()
    Interval = auto()
    Above = auto()
    Below = auto()

class Fit(Enum):
    Gauss = auto()
    Exp = auto()
    QDC = auto()
