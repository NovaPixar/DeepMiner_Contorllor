import sys
import os

# 将项目根目录添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import qfluentwidgets
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt

from app.ui2py.gamepadPage import Ui_gamepadPage
from app.common.icon import Icon
from app.common import resource
from app.joystick.joystick import JoystickController


class GamepadInterface(QWidget, Ui_gamepadPage):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.__initWidget()
        self.__initLayout()
        
        
        # 创建手柄控制器
        self.joystick = JoystickController()
        # 连接信号
        self.__connectSignalToSlot()
        

    def __initWidget(self):
        # 设置滑条为垂直方向
        self.Axis0Slider.setOrientation(Qt.Vertical)
        self.Axis1Slider.setOrientation(Qt.Vertical)
        self.Axis2Slider.setOrientation(Qt.Vertical)
        self.Axis3Slider.setOrientation(Qt.Vertical)

        # 设置滑条范围和初始值
        for slider in [self.Axis0Slider, self.Axis1Slider, self.Axis2Slider, self.Axis3Slider]:
            slider.setRange(-100, 100)  # 设置范围从-100到100
            slider.setValue(0)  # 设置初始值为0
            slider.setInvertedAppearance(True)  # 反转滑条方向

    def __initLayout(self):
        pass

    def __connectSignalToSlot(self):
        self.joystick.axis_changed.connect(self.__onAxisChanged)
        self.joystick.button_changed.connect(self.__onButtonChanged)
        self.joystick.hat_changed.connect(self.__onHatChanged)
        pass

    def __onAxisChanged(self, axis_id, value):
        """处理手柄轴值变化的槽函数"""
        # 将手柄的值（-1到1）映射到滑块的范围（-100到100）
        slider_value = int(value * 100)
        
        # 根据轴的ID更新对应的滑块
        if axis_id == 0:
            self.Axis0Slider.setValue(slider_value)
        elif axis_id == 1:
            self.Axis1Slider.setValue(slider_value)
        elif axis_id == 2:
            self.Axis2Slider.setValue(slider_value)
        elif axis_id == 3:
            self.Axis3Slider.setValue(slider_value)

    def __onButtonChanged(self, button_id, value):
        """处理手柄按钮值变化的槽函数"""
        # 根据按钮ID更新对应的按钮状态
        if button_id == 0:  # A按钮
            self.APillPushButton.setChecked(value)
        elif button_id == 1:  # B按钮
            self.BPillPushButton.setChecked(value)
        elif button_id == 2:  # X按钮
            self.XPillPushButton.setChecked(value)
        elif button_id == 3:  # Y按钮
            self.YPillPushButton.setChecked(value)

    def __onHatChanged(self, hat_id, value):
        """处理手柄帽子值变化的槽函数"""
        # 首先重置所有方向键的状态
        self.UpPillToolButton.setChecked(False)
        self.DownPillToolButton.setChecked(False)
        self.LeftPillToolButton.setChecked(False)
        self.RightPillToolButton.setChecked(False)

        # 根据帽子的值设置对应方向键的状态
        if value == (0, 1):  # 上
            self.UpPillToolButton.setChecked(True)
        elif value == (0, -1):  # 下
            self.DownPillToolButton.setChecked(True)
        elif value == (-1, 0):  # 左
            self.LeftPillToolButton.setChecked(True)
        elif value == (1, 0):  # 右
            self.RightPillToolButton.setChecked(True)
        # 对角线方向的处理（如果需要）
        elif value == (-1, 1):  # 左上
            self.LeftPillToolButton.setChecked(True)
            self.UpPillToolButton.setChecked(True)
        elif value == (1, 1):  # 右上
            self.RightPillToolButton.setChecked(True)
            self.UpToolButton.setChecked(True)
        elif value == (-1, -1):  # 左下
            self.LeftPillToolButton.setChecked(True)
            self.DownPillToolButton.setChecked(True)
        elif value == (1, -1):  # 右下
            self.RightPillToolButton.setChecked(True)
            self.DownPillToolButton.setChecked(True)

    def closeEvent(self, event):
        """窗口关闭时的处理"""
        self.joystick.quit()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication([])
    w = GamepadInterface()
    w.show()
    app.exec()
