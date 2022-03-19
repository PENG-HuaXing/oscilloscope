import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MatPlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, init_graph=True):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super(MatPlotCanvas, self).__init__(self.fig)
        self.ax.grid(True)
        self.fig.tight_layout()
        if init_graph is True:
            self.init_graph()

    def set_limit(self, x_lim: list = None, y_lim: list = None):
        if x_lim is not None:
            self.ax.set_xlim(*x_lim)
        if y_lim is not None:
            self.ax.set_ylim(*y_lim)

    def init_graph(self):
        x = np.linspace(-7, 7, 200)
        self.ax.plot(x, np.sin(x))
        self.ax.plot(x, np.cos(x))
        self.ax.set_xlabel("x label")
        self.ax.set_ylabel("y label")
        self.ax.set_title("title")
        self.ax.set_ylim(-3, 3)
        self.ax.minorticks_on()
        self.ax.grid(True)
        self.fig.set_tight_layout(True)
        self.draw()

    def initial(self, grid: bool = True, x_label: str = None, y_label: str = None, title: str = None, minor: bool = True):
        self.ax.clear()
        self.ax.grid(grid)
        if x_label is not None:
            self.ax.set_xlabel(x_label)
        if y_label is not None:
            self.ax.set_ylabel(y_label)
        if title is not None:
            self.ax.set_title(title)
        if minor is True:
            self.ax.minorticks_on()
        self.fig.set_tight_layout(True)
