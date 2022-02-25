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
    DoubleGauss = auto()
    TripleGauss = auto()
    FourGauss = auto()
    QDC = auto()


class AfterPulse(Enum):
    Pedestal = auto()
    NoPedestal = auto()


class Extremum(Enum):
    Max = auto()
    Min = auto()


class Processing(Enum):
    Go = auto()
    Stop = auto()
    Pause = auto()


class Active(Enum):
    Ped = auto()
    NoPed = auto()
    ExtMin = auto()
    ExtMax = auto()
    NoExt = auto()
    Tri = auto()
    NoTri = auto()
