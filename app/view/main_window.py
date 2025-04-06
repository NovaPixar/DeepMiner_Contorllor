# coding: utf-8
from PySide6.QtCore import QUrl, QSize
from PySide6.QtGui import QIcon, QColor
from PySide6.QtWidgets import QApplication

from qfluentwidgets import NavigationItemPosition, FluentWindow, SplashScreen
from qfluentwidgets import FluentIcon as FIF

from .setting_interface import SettingInterface
from .camera_interface import CameraInterface
from .home_interface import HomeInterface
from ..common.config import cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common import resource


class MainWindow(FluentWindow):
    """
    主窗口类，继承自FluentWindow。
    该类负责初始化应用程序的主窗口，包括设置窗口大小、图标、标题等，
    并且初始化导航栏和设置界面。
    """

    def __init__(self):
        """
        构造函数，初始化主窗口。
        """
        super().__init__()
        self.initWindow()

        # TODO: create sub interface
        self.settingInterface = SettingInterface(self)
        self.cameraInterface = CameraInterface(self)
        # 加入主页
        self.homeInterface = HomeInterface(self)


        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()

    def connectSignalToSlot(self):
        """
        连接信号到槽函数。
        这里将micaEnableChanged信号连接到setMicaEffectEnabled槽函数，
        用于在Mica效果启用状态改变时更新窗口效果。
        """
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)

    def initNavigation(self):
        """
        初始化导航栏。
        # self.navigationInterface.setAcrylicEnabled(True)

        # TODO： 添加导航项
        # self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))

        添加设置界面到导航栏的底部。
        """
        self.navigationInterface.setAcrylicEnabled(True)

        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'), NavigationItemPosition.TOP)
        self.addSubInterface(self.cameraInterface, FIF.CAMERA, self.tr('Camera'), NavigationItemPosition.TOP)
        self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

        self.splashScreen.finish()

    def initWindow(self):
        """
        初始化窗口设置。
        设置窗口大小、最小宽度、图标、标题等。
        同时设置自定义背景颜色和Mica效果，并创建启动屏幕。
        最后将窗口移动到屏幕中央并显示。
        """
        self.resize(1680, 1080)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/app/images/DeepMinerLogo.png'))
        self.setWindowTitle('DeepMiner Controller')

        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        """
        窗口大小改变事件。
        调用父类的resizeEvent方法后，如果存在启动屏幕，则调整其大小以适应窗口大小。
        """
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())
