import sys

import cv2
import qfluentwidgets
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QTimer, Qt, QRectF
from PySide6.QtGui import QImage, QPixmap, QPainter, QPainterPath, QLinearGradient, QBrush
from PySide6.QtWidgets import QWidget, QApplication
from qfluentwidgets import InfoBar, InfoBarPosition, ImageLabel
from app.common.icon import Icon
from app.ui2py.cameraPage import Ui_cameraInterface
from app.utils.labelPixmapResizer import LabelPixmapResizer


class CameraInterface(QWidget, Ui_cameraInterface):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 通过setup ui进行界面初始化
        self.timer = None
        self.camera = None
        self.labelPixmapResizer = LabelPixmapResizer()
        self.setupUi(self)
        self.__initWidget()
        self.__connectSignalToSlot()

    def __initWidget(self):
        """"
        在检测相机是否连接成功之前需要隐藏相机的相关功能按钮
        """
        self.CameraPrimaryToolButton.setVisible(False)
        self.CameraSwitchButton.setVisible(False)
        self.WIFITransparentPushButton.setIcon(Icon.WIFI_CANCEL)
        self.WIFITransparentPushButton.setText("Disconnect")
        self.WatchingTransparentPushButton.setIcon(Icon.EYE_SLASH_FILL)
        self.WatchingTransparentPushButton.setText("View Enable")
        self.CameraPrimaryPushButton.setIcon(Icon.CONNECT)

    def __initLayout(self):
        """
        初始化布局
        """
        pass

    def __connectSignalToSlot(self):
        """
        连接信号到槽函数
        """
        self.CameraPrimaryPushButton.clicked.connect(self.__cameraTest)

        # 切换相机
        self.CameraSwitchButton.checkedChanged.connect(lambda checked: self.__toggleCamera(checked))
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
            self.CameraPrimaryPushButton.setIcon(qfluentwidgets.FluentIcon.CAMERA)
            self.WIFITransparentPushButton.setIcon(qfluentwidgets.FluentIcon.WIFI)
            self.WIFITransparentPushButton.setText("Connect")

            self.CameraPrimaryPushButton.setVisible(True)
            self.CameraSwitchButton.setVisible(True)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.__updateFrame)

    def __toggleCamera(self, checked):
        """
        切换相机
        """
        if checked:
            # print("打开展示")
            self.WatchingTransparentPushButton.setIcon(qfluentwidgets.FluentIcon.VIEW)
            self.WatchingTransparentPushButton.setText("Viewing")
            self.timer.start(30)
        else:
            # print("关闭展示")
            self.timer.stop()
            self.WatchingTransparentPushButton.setIcon(Icon.EYE_SLASH_FILL)
            self.WatchingTransparentPushButton.setText("View Enable")
            self.ImageLabel.setPixmap(QtGui.QPixmap(":/app/images/gradiant_white.svg"))
            self.ImageLabel.setMinimumSize(0, 0)
            self.ImageLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))

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
                # pixmap = pixmap.scaled(1600, 1000)

                self.labelPixmapResizer.resizeImageLabel(self.ImageLabel, pixmap)
                self.ImageLabel.setScaledContents(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CameraInterface()
    w.show()
    app.exec()
