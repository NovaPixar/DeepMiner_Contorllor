import sys

import cv2
from PIL.ImageQt import QPixmap
from PySide6 import QtGui, QtCore
from PySide6.QtCore import QTimer, QObject
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QWidget, QApplication
from qfluentwidgets import InfoBar, InfoBarPosition, IconWidget, ProgressRing, ToolButton

from app.common.icon import Icon
from app.ui2py.homePage import Ui_homeInterface
from app.utils.labelPixmapResizer import LabelPixmapResizer


class HomeInterface(QWidget, Ui_homeInterface):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.timer = None
        self.camera = None
        self.labelPixmapResizer = LabelPixmapResizer()

        self.setupUi(self)
        self.__initWidget()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.__initLayout()

        # 初始化相机模块
        self.cameraImageLabel.setPixmap(QtGui.QPixmap(":/app/images/gradiant_white.svg"))
        self.cameraImageLabel.setMinimumSize(0, 0)
        self.cameraImageLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))

        self.CameraSwitchButton.setVisible(False)
        # 让相机列表的按钮不可选中，直到测试之后可以连接到相机
        self.CameralListTransparentDropDownPushButton.setIcon(Icon.CAMERA_OFF)
        self.CameralListTransparentDropDownPushButton.setEnabled(False)

        # todo 初始化Cage模块
        self.CageSwitchButton.setVisible(False)
        # 将速度设置为0%
        self.CageValueTitleLabel.setText("0%")
        self.CageProgressRing.setValue(0)
        # 测试之前需要将除了测试按钮的其他按钮设置为不可选中
        self.SpeedOffPillToolButton.setEnabled(False)
        self.SpeedMidPillToolButton.setEnabled(False)
        self.SpeedHighPillToolButton.setEnabled(False)
        self.SpeedDownToolButton.setEnabled(False)
        self.SpeedUpPlusToolButton.setEnabled(False)
        # todo 在CageProgressRing上叠加一个ICON

        # todo 初始化Clean模块
        self.CleanSwitchButton.setVisible(False)
        self.CleanBehindProgressRing.setValue(0)
        self.CleanFrontProgressRing.setValue(0)
        self.CleanBehindSlider.setValue(0)
        self.CleanFrontSlider.setValue(0)
        self.CleanBehindTitleLabel.setText("0%")
        self.CleanFrontTitleLabel.setText("0%")

        # todo 初始化Pose模块
        pixmap = QtGui.QPixmap(":/app/images/gradiant_white.svg")
        self.labelPixmapResizer.resizeImageLabel(self.poseImageLabel, pixmap)

        # todo 初始化Chart模块
        pixmap = QtGui.QPixmap(":/app/images/gradiant_white.svg")
        self.labelPixmapResizer.resizeImageLabel(self.chartImageLabel, pixmap)

        # todo 初始化CardWidget
        self.SpeedIconWidget.setIcon(Icon.SPEED_SHOW)

        # todo 初始化电池电量模块
        self.BatteryIconWidget.setIcon(Icon.BATTERY)

        pass

    def __initLayout(self):
        self.ImageLabel = None
        pass

    def __connectSignalToSlot(self):
        self.cameraTestPrimaryPushButton.clicked.connect(self.__cameraTest)
        self.CameraSwitchButton.checkedChanged.connect(lambda checked: self.__toggleCamera(checked))
        """
        cage的模块的Slot
        """
        self.CagePrimaryPushButton.clicked.connect(self.__cageTest)
        self.CageSwitchButton.checkedChanged.connect(lambda: self.__toggleCage(self.CageSwitchButton.isChecked()))

        self.SpeedOffPillToolButton.clicked.connect(lambda: self.__cageSpeedPillButton_clicked(
            self.SpeedOffPillToolButton, self.SpeedOffPillToolButton.isChecked()))
        self.SpeedMidPillToolButton.clicked.connect(lambda: self.__cageSpeedPillButton_clicked(
            self.SpeedMidPillToolButton, self.SpeedMidPillToolButton.isChecked()))
        self.SpeedHighPillToolButton.clicked.connect(lambda: self.__cageSpeedPillButton_clicked(
            self.SpeedHighPillToolButton, self.SpeedHighPillToolButton.isChecked()))

        self.SpeedDownToolButton.clicked.connect(lambda: self.__cageFinetuneButton_clicked(self.SpeedDownToolButton))
        self.SpeedUpPlusToolButton.clicked.connect(
            lambda: self.__cageFinetuneButton_clicked(self.SpeedUpPlusToolButton))

        pass

    def __cameraTest(self):
        """
        测试相机是否连接成功
        """
        self.camera = cv2.VideoCapture(0)
        print(self.camera)
        if not self.camera.isOpened():
            InfoBar.error(
                self.tr("无法打开摄像头"),
                self.tr('请检查摄像头是否连接'),
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self.window()
            )
        else:
            self.CameraSwitchButton.setVisible(True)
            self.CameralListTransparentDropDownPushButton.setEnabled(True)
            self.CameralListTransparentDropDownPushButton.setIcon(Icon.CAMERA)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.__updateFrame)
            pass

    def __toggleCamera(self, checked):
        if checked:
            # print("打开展示")
            self.CameraSwitchButton.setVisible(True)
            self.CameralListTransparentDropDownPushButton.setEnabled(True)
            self.timer.start(30)
        else:
            # print("关闭展示")
            self.timer.stop()
            self.cameraImageLabel.setPixmap(QtGui.QPixmap(":/app/images/gradiant_white.svg"))
            self.cameraImageLabel.setMinimumSize(0, 0)
            self.cameraImageLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))

    def __updateFrame(self):
        if self.camera is not None:
            ret, frame = self.camera.read()

            if ret:
                # 将 OpenCV 格式的图像转换为 QImage
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

                pixmap = QPixmap.fromImage(qt_image)
                self.labelPixmapResizer.resizeImageLabel(self.cameraImageLabel, pixmap)
                self.cameraImageLabel.setScaledContents(True)

    def __cageTest(self):
        isConnected = True
        # 检测连接状况
        if isConnected:
            # todo 连接成功
            self.CageSwitchButton.setVisible(True)
            self.SpeedOffPillToolButton.setEnabled(True)
            self.SpeedMidPillToolButton.setEnabled(True)
            self.SpeedHighPillToolButton.setEnabled(True)
            self.SpeedDownToolButton.setEnabled(True)
            self.SpeedUpPlusToolButton.setEnabled(True)
        else:
            # todo 连接失败
            InfoBar.error(
                self.tr("无法连接到Cage"),
                self.tr('请检查Cage模块连接是否正常'),
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self.window()
            )

    def __toggleCage(self, checked):
        if checked:
            self.CageProgressRing.setValue(30)
            self.CageValueTitleLabel.setText("30%")
            self.SpeedOffPillToolButton.setChecked(True)
            # todo 向主控输送设置速度为30的命令
        if not checked:
            self.CageProgressRing.setValue(0)
            self.CageValueTitleLabel.setText("0%")
            self.SpeedOffPillToolButton.setChecked(False)
            self.SpeedMidPillToolButton.setChecked(False)
            self.SpeedHighPillToolButton.setChecked(False)
            # todo 向主控输送设置速度为0的命令
        pass

    def __cageSpeedPillButton_clicked(self, PillButton: ToolButton, checked):
        if checked:
            """
            传入按钮的名称，通过按钮的名称来判断按钮的状态
            """
            # todo 速度调节
            # 按动的是慢速的按钮，就将快速的中速的设置checked为False，速度调整到25%
            if PillButton.objectName() == "SpeedOffPillToolButton":
                self.SpeedMidPillToolButton.setChecked(False)
                self.SpeedHighPillToolButton.setChecked(False)
                self.CageValueTitleLabel.setText("25%")
                self.CageProgressRing.setValue(25)
                # todo 向主控输送设置速度为25的命令
            elif PillButton.objectName() == "SpeedMidPillToolButton":
                self.SpeedOffPillToolButton.setChecked(False)
                self.SpeedHighPillToolButton.setChecked(False)
                self.CageValueTitleLabel.setText("50%")
                self.CageProgressRing.setValue(50)
                # todo 向主控输送设置速度为50的命令
            elif PillButton.objectName() == "SpeedHighPillToolButton":
                self.SpeedOffPillToolButton.setChecked(False)
                self.SpeedMidPillToolButton.setChecked(False)
                self.CageValueTitleLabel.setText("100%")
                self.CageProgressRing.setValue(100)
                # todo 向主控输送设置速度为100的命令
        else:
            """
            传入按钮的名称，通过按钮的名称来判断按钮的状态
            """
            # todo 速度调节
            # 按动的是慢速的按钮，就将快速的中速的设置checked为False，速度调整到25%
            if PillButton.objectName() == "SpeedOffPillToolButton":
                self.SpeedMidPillToolButton.setChecked(False)
                self.SpeedHighPillToolButton.setChecked(False)
                self.CageValueTitleLabel.setText("0%")
                self.CageProgressRing.setValue(0)
                # todo 向主控输送设置速度为0的命令
            elif PillButton.objectName() == "SpeedMidPillToolButton":
                self.SpeedOffPillToolButton.setChecked(False)
                self.SpeedHighPillToolButton.setChecked(False)
                self.CageValueTitleLabel.setText("0%")
                self.CageProgressRing.setValue(0)
                # todo 向主控输送设置速度为0的命令
            elif PillButton.objectName() == "SpeedHighPillToolButton":
                self.SpeedOffPillToolButton.setChecked(False)
                self.SpeedMidPillToolButton.setChecked(False)
                self.CageValueTitleLabel.setText("0%")
                self.CageProgressRing.setValue(0)
                # todo 向主控输送设置速度为0的命令

    def __cageFinetuneButton_clicked(self, finetuneButton: ToolButton):

        if self.CageValueTitleLabel.text() == "0%" and finetuneButton.objectName() == "SpeedDownToolButton":
            # print("速度已经是最低了")
            InfoBar.error(
                self.tr("Warning!"),
                content=self.tr("速度已经是最低了"),
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self.window()
            )
            return
        elif self.CageValueTitleLabel.text() == "100%" and finetuneButton.objectName() == "SpeedUpPlusToolButton":
            # print("速度已经是最高了")
            InfoBar.error(
                self.tr("Warning!"),
                content=self.tr("速度已经是最高了"),
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self.window()
            )
            return
        # 速度微调调节
        elif finetuneButton.objectName() == "SpeedDownToolButton":
            self.CageValueTitleLabel.setText(str(int(self.CageValueTitleLabel.text().replace("%", "")) - 10) + "%")
            self.CageProgressRing.setValue(int(self.CageValueTitleLabel.text().replace("%", "")))
            if self.CageProgressRing.value() != 100 or self.CageProgressRing.value() != 0 or self.CageProgressRing.value() != 50:
                self.SpeedHighPillToolButton.setChecked(False)
                self.SpeedMidPillToolButton.setChecked(False)
                self.SpeedOffPillToolButton.setChecked(False)
            # todo 向主控输送设置速度的命令
        elif finetuneButton.objectName() == "SpeedUpPlusToolButton":
            self.CageValueTitleLabel.setText(str(int(self.CageValueTitleLabel.text().replace("%", "")) + 10) + "%")
            self.CageProgressRing.setValue(int(self.CageValueTitleLabel.text().replace("%", "")))
            if self.CageProgressRing.value() != 100 or self.CageProgressRing.value() != 0 or self.CageProgressRing.value() != 50:
                self.SpeedHighPillToolButton.setChecked(False)
                self.SpeedMidPillToolButton.setChecked(False)
                self.SpeedOffPillToolButton.setChecked(False)
            # todo 向主控输送设置速度的命令

        if self.CageValueTitleLabel.text() == "100%":
            self.SpeedHighPillToolButton.setChecked(True)
            self.SpeedMidPillToolButton.setChecked(False)
            self.SpeedOffPillToolButton.setChecked(False)
        if self.CageValueTitleLabel.text() == "50%":
            self.SpeedMidPillToolButton.setChecked(True)
            self.SpeedOffPillToolButton.setChecked(False)
            self.SpeedHighPillToolButton.setChecked(False)
        if self.CageValueTitleLabel.text() == "30%":
            self.SpeedOffPillToolButton.setChecked(True)
            self.SpeedMidPillToolButton.setChecked(False)
            self.SpeedHighPillToolButton.setChecked(False)

    # cage模块电流警告
    def __cageCurrentWarning(self, current):
        # todo 电流警告
        if current >= 10:
            InfoBar.warning(
                self.tr("电流过大！"),
                self.tr('收集模块可能出现卡死，请检查！'),
                position=InfoBarPosition.TOP,
                duration=5000,
                parent=self.window()
            )
            # 断电操作
            self.CageValueTitleLabel.setText("0%")
            self.CageProgressRing.setValue(0)
            # 测试之前需要将除了测试按钮的其他按钮设置为不可选中
            self.SpeedOffPillToolButton.setEnabled(False)
            self.SpeedMidPillToolButton.setEnabled(False)
            self.SpeedHighPillToolButton.setEnabled(False)
            # todo 向主控输送设置速度为0的命令


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = HomeInterface()
    w.show()
    app.exec()
