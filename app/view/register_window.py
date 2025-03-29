# coding:utf-8
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout
from qfluentwidgets import (MSFluentTitleBar, isDarkTheme, ImageLabel, BodyLabel, LineEdit,
                            PasswordLineEdit, PrimaryPushButton, CheckBox, InfoBar,
                            InfoBarPosition, setThemeColor)

from .main_window import MainWindow
from ..common.config import cfg
from ..common.license_service import LicenseService
from ..common.tcp_connect import TcpConnect


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class RegisterWindow(Window):
    """ Register window """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        setThemeColor('#28afe9')
        self.setTitleBar(MSFluentTitleBar(self))
        self.register = LicenseService()
        # 初始化网络验证 bool
        self.connector = TcpConnect()

        self.imageLabel = ImageLabel(':/app/images/space.jpg', self)
        self.iconLabel = ImageLabel(':/app/images/DeepMinerLogo.png', self)

        self.machineIPLabel = BodyLabel(self.tr('RobotIP'), self)
        self.machineIPLineEdit = LineEdit(self)

        self.machinePortLabel = BodyLabel(self.tr('RobotPort'), self)
        self.machinePortLineEdit = LineEdit(self)

        self.testConnectButton = PrimaryPushButton(self.tr('测试连接'), self)

        self.passwordCodeLabel = BodyLabel(self.tr('密码'), self)
        self.passwordCodeLineEdit = PasswordLineEdit(self)

        # self.rememberCheckBox = CheckBox(self.tr('Remember me'), self)
        self.rememberCheckBox = CheckBox('记住密码', self)

        self.loginButton = PrimaryPushButton(self.tr('进入控制界面'), self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        # 是否连接成功
        self.isConnect = False

        self.__initWidgets()

    def __initWidgets(self):
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)
        self.rememberCheckBox.setChecked(cfg.get(cfg.rememberMe))

        self.machineIPLineEdit.setPlaceholderText('机器的IP')
        self.machinePortLineEdit.setPlaceholderText('机器的端口')
        self.passwordCodeLineEdit.setPlaceholderText('••••••••••••')

        if self.rememberCheckBox.isChecked():
            self.machineIPLineEdit.setText(cfg.get(cfg.email))
            self.passwordCodeLineEdit.setText(cfg.get(cfg.activationCode))

        self.__connectSignalToSlot()
        self.__initLayout()

        if isWin11():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            color = QColor(25, 33, 42) if isDarkTheme(
            ) else QColor(240, 244, 249)
            self.setStyleSheet(f"RegisterWindow{{background: {color.name()}}}")

        self.setWindowTitle('DeepMiner-Controller')
        self.setWindowIcon(QIcon(":/app/images/DeepMinerLogo.png"))
        self.resize(1000, 650)

        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.titleBar.raise_()

    def __initLayout(self):
        self.imageLabel.scaledToHeight(650)
        self.iconLabel.scaledToHeight(100)

        self.hBoxLayout.addWidget(self.imageLabel)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setContentsMargins(20, 0, 20, 0)
        self.vBoxLayout.setSpacing(0)
        self.hBoxLayout.setSpacing(0)

        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(
            self.iconLabel, 0, Qt.AlignmentFlag.AlignHCenter)
        self.vBoxLayout.addSpacing(38)

        # 创建一个新的水平布局来放置 machineIPLabel 和 machinePortLabel
        self.ip_port_label_layout = QHBoxLayout()
        self.ip_port_label_layout.addWidget(self.machineIPLabel)
        self.ip_port_label_layout.addWidget(self.machinePortLabel)

        # 设置 machineIPLabel 和 machinePortLabel 的比重为 3:2
        self.ip_port_label_layout.setStretchFactor(self.machineIPLabel, 3)
        self.ip_port_label_layout.setStretchFactor(self.machinePortLabel, 2)
        self.vBoxLayout.addLayout(self.ip_port_label_layout)
        self.vBoxLayout.addSpacing(11)

        # 创建一个新的水平布局来放置 machineIPLineEdit 和 machinePortLineEdit
        self.ip_port_lineEdit_layout = QHBoxLayout()
        self.ip_port_lineEdit_layout.addWidget(self.machineIPLineEdit)
        self.ip_port_lineEdit_layout.addWidget(self.machinePortLineEdit)
        self.ip_port_lineEdit_layout.setStretchFactor(self.machineIPLineEdit, 3)
        self.ip_port_lineEdit_layout.setStretchFactor(self.machinePortLineEdit, 2)
        self.vBoxLayout.addLayout(self.ip_port_lineEdit_layout)
        self.vBoxLayout.addSpacing(12)
        self.vBoxLayout.addWidget(self.testConnectButton)
        self.vBoxLayout.addSpacing(12)
        self.vBoxLayout.addWidget(self.passwordCodeLabel)
        self.vBoxLayout.addSpacing(11)
        self.vBoxLayout.addWidget(self.passwordCodeLineEdit)
        self.vBoxLayout.addSpacing(12)
        self.vBoxLayout.addWidget(self.rememberCheckBox)
        self.vBoxLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.loginButton)
        self.vBoxLayout.addSpacing(30)
        self.vBoxLayout.addStretch(1)

    def __connectSignalToSlot(self):
        self.loginButton.clicked.connect(self._login)
        self.rememberCheckBox.stateChanged.connect(
            lambda: cfg.set(cfg.rememberMe, self.rememberCheckBox.isChecked()))
        self.testConnectButton.clicked.connect(self._testConnect)

    def _testConnect(self):
        # 禁用按钮并更改文本
        self.testConnectButton.setEnabled(False)
        self.testConnectButton.setText(self.tr('正在连接'))
        # 检验IP和Port是否为空
        # print(self.machineIPLineEdit.text())
        # print(self.machinePortLineEdit.text())
        if self.machineIPLineEdit.text() == "" or self.machinePortLineEdit.text() == "":
            InfoBar.error(
                self.tr("连接失败"),
                self.tr('IP和端口不能为空'),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        else:

            # 检查连接是否成功将结果保存在self.isConnect中
            self.isConnect = self.connector.checkConnection(self.machineIPLineEdit.text(),self.machinePortLineEdit.text())
            if not self.isConnect:
                InfoBar.error(
                    self.tr("连接失败"),
                    self.tr('请检查IP和端口是否正确'),
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
            else:
                InfoBar.success(
                    self.tr("连接成功"),
                    self.tr('连接成功'),
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )

        self.testConnectButton.setEnabled(True)
        self.testConnectButton.setText(self.tr('测试连接'))

    def _login(self):
        code = self.passwordCodeLineEdit.text().strip()

        # 密码错误
        if not self.register.validate(code, self.machineIPLineEdit.text()):
            InfoBar.error(
                self.tr("登录失败"),
                self.tr('请检查密码是否正确或连接是否成功'),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
        # 连接失败
        if not self.connector.checkConnection(self.machineIPLineEdit.text(), self.machinePortLineEdit.text()):
            InfoBar.error(
                self.tr("连接失败"),
                self.tr('请检查密码是否正确或连接是否成功'),
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
        else:
            InfoBar.success(
                self.tr("Success"),
                self.tr('Activation successful'),
                position=InfoBarPosition.TOP,
                parent=self.window()
            )

            if cfg.get(cfg.rememberMe):
                cfg.set(cfg.email, self.machineIPLineEdit.text().strip())
                cfg.set(cfg.activationCode, code)

            self.loginButton.setDisabled(True)
            QTimer.singleShot(1500, self._showMainWindow)

    def _showMainWindow(self):
        self.close()
        setThemeColor('#009faa')

        w = MainWindow()
        w.show()
