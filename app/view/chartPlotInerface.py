import sys

import numpy as np
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from app.ui2py.chartPlotPage import Ui_chartPlotPage
from app.utils.roundedWidget import RoundedWidget


class ChartPlotInterface(QWidget, Ui_chartPlotPage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)
        self.timeLine = np.array([])
        self.current = np.array([])
        self.time = 0
        self.last_sample_time = -1
        self.last_current = None
        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.setWindowTitle("实时电流 - 时间曲线")
        self.figure = plt.figure(figsize=(8, 6), facecolor='red')
        self.canvas = FigureCanvas()

        self.roundedWidgetCanvas = RoundedWidget(self, radius=20)
        self.roundedWidgetCanvas.setCanvas(self.canvas)
        self.verticalLayout.addWidget(self.roundedWidgetCanvas)

        pass

    def __initLayout(self):
        pass

    def __connectSignalToSlot(self):
        pass

    def update_plot(self):

        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ChartPlotInterface()
    w.show()
    app.exec()
