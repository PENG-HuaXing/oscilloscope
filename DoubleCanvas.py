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
        x = np.linspace(-3, 3, 200)
        self.ax1.plot(x, np.sin(x))
        self.ax2.plot(x, np.cos(x))
        self.draw()
