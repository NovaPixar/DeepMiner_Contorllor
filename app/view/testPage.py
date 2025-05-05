import sys
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import QTimer
from scipy.interpolate import interp1d


class RealTimePlot(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)
        self.t = np.array([])
        self.current = np.array([])
        self.time = 0
        self.last_sample_time = -1
        self.last_current = None

    def initUI(self):
        self.setWindowTitle("实时电流 - 时间曲线")
        # 设置图表整体背景为浅蓝色
        self.figure = plt.figure(figsize=(8, 6), facecolor='#e6f7ff')
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.ax = self.figure.add_subplot(111)
        # 设置坐标轴标签颜色为深蓝色
        self.ax.set_xlabel('时间 (s)', fontsize=12, color='#004080')
        self.ax.set_ylabel('电流 (A)', fontsize=12, color='#004080')
        # 设置标题颜色为深蓝色
        self.ax.set_title("Time-Current", fontsize=16, color='#004080')
        # 设置网格线颜色为淡蓝色
        self.ax.grid(True, linestyle='--', alpha=0.7, color='#99ccff')
        # 设置绘图区域背景为白色
        self.ax.set_facecolor('white')
        # 设置坐标轴颜色为深蓝色
        for spine in self.ax.spines.values():
            spine.set_color('#004080')

    def update_plot(self):
        if self.time % 10 == 0:
            new_current = random.uniform(0, 10)
            self.last_current = new_current
            self.last_sample_time = self.time / 10
            self.t = np.append(self.t, self.last_sample_time)
            self.current = np.append(self.current, new_current)

        recent_mask = self.t >= (self.time / 10) - 60
        recent_t = self.t[recent_mask]
        recent_current = self.current[recent_mask]

        if len(recent_t) > 3:
            try:
                f = interp1d(recent_t, recent_current, kind='cubic')
                t_smooth = np.linspace(min(recent_t), max(recent_t), 500)
                current_smooth = f(t_smooth)
            except ValueError:
                unique_indices = np.unique(recent_t, return_index=True)[1]
                recent_t = recent_t[unique_indices]
                recent_current = recent_current[unique_indices]
                if len(recent_t) > 3:
                    f = interp1d(recent_t, recent_current, kind='cubic')
                    t_smooth = np.linspace(min(recent_t), max(recent_t), 500)
                    current_smooth = f(t_smooth)
                else:
                    t_smooth = recent_t
                    current_smooth = recent_current
        else:
            t_smooth = recent_t
            current_smooth = recent_current

        self.ax.clear()
        # 设置曲线颜色为蓝色
        self.ax.plot(t_smooth, current_smooth, 'b-', linewidth=2, alpha=0.8)
        self.ax.set_xlabel('Time(s)', fontsize=12, color='#004080')
        self.ax.set_ylabel('Current (A)', fontsize=12, color='#004080')
        self.ax.set_title("Time-Current Curve", fontsize=16, color='#004080')
        self.ax.grid(True, linestyle='--', alpha=0.7, color='#99ccff')
        self.ax.set_facecolor('white')
        self.ax.set_xlim([max(0, (self.time / 10) - 60), self.time / 10])
        for spine in self.ax.spines.values():
            spine.set_color('#004080')
        self.canvas.draw()
        self.time += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RealTimePlot()
    window.show()
    sys.exit(app.exec())

# todo 将采集到的电流的数据经过处理是否能够一定程度的反应矿区的矿石的颗粒度分布，绘制时间-路程-颗粒度的散点图
