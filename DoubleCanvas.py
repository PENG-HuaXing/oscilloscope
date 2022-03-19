import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MatPlotDoubleCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, init_graph=True):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax1 = self.fig.add_subplot(111)
        self.ax2 = self.fig.add_subplot(222)
        super(MatPlotDoubleCanvas, self).__init__(self.fig)
        self.ax1.grid(True)
        self.ax2.grid(True)
        self.fig.tight_layout()
        if init_graph is True:
            self.init_graph()

    def set_limit(self, x_lim: list = None, y_lim: list = None):
        if x_lim is not None:
            self.ax1.set_xlim(*x_lim)
        if y_lim is not None:
            self.ax1.set_ylim(*y_lim)

    def init_graph(self):
        x = np.linspace(-8, 8, 200)
        self.ax1.set_ylim(-5, 5)
        self.ax2.set_ylim(-5, 5)
        self.ax1.plot(x, np.sin(x))
        self.ax1.plot(x, np.cos(x))
        self.ax2.plot(x, np.cos(x))
        self.ax2.plot(x, np.sin(x))
        self.ax1.set_xlabel("x label")
        self.ax1.set_ylabel("y label")
        self.ax1.set_title("title")
        self.ax1.minorticks_on()
        self.ax1.grid(True)
        self.ax2.minorticks_on()
        self.ax2.grid(True)
        self.fig.set_tight_layout(True)
        self.draw()

    def initial(self, grid: bool = True, x_label: str = None, y_label: str = None, title: str = None, minor: bool = True):
        self.ax1.clear()
        self.ax1.grid(grid)
        if x_label is not None:
            self.ax1.set_xlabel(x_label)
        if y_label is not None:
            self.ax1.set_ylabel(y_label)
        if title is not None:
            self.ax1.set_title(title)
        if minor is True:
            self.ax1.minorticks_on()
            self.ax2.minorticks_on()
        self.ax2.clear()
        self.ax2.grid(grid)
        self.fig.set_tight_layout(True)
