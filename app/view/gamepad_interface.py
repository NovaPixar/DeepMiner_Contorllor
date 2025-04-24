import sys
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPainter, QPen, QBrush, QPainterPath
from PySide6.QtCore import Qt
from PySide6.QtGui import QPaintEvent  # 导入 QPaintEvent


class GamepadWidget(QWidget):
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        # 设置画笔颜色和宽度
        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        # 设置画刷为透明
        brush = QBrush(Qt.transparent)
        painter.setBrush(brush)

        # 绘制游戏手柄轮廓
        handle_width = 300
        handle_height = 200
        handle_x = (self.width() - handle_width) / 2
        handle_y = (self.height() - handle_height) / 2
        painter.drawRoundedRect(handle_x, handle_y, handle_width, handle_height, 20, 20)

        # 绘制顶部的两个按键
        button_width = 30
        button_height = 40
        button_spacing = 40
        top_button_y = handle_y - button_height - 10
        top_button_x1 = handle_x + (handle_width / 4 - button_width / 2)
        top_button_x2 = handle_x + (3 * handle_width / 4 - button_width / 2)
        # 使用 QPainterPath 绘制具有不同圆角的矩形
        path = QPainterPath()
        path.moveTo(top_button_x1, top_button_y + 10)  # 左上角
        path.arcTo(top_button_x1, top_button_y, 20, 20, 180, 90)
        path.closeSubpath()

        painter.drawPath(path)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = GamepadWidget()
    widget.show()
    sys.exit(app.exec())
