# coding: utf-8
from enum import Enum

from qfluentwidgets import FluentIconBase, getIconColor, Theme


class Icon(FluentIconBase, Enum):
    # TODO: Add your icons here

    BATTERY = "Entypo-Battery"
    SPEED_SHOW = "SimpleIcons-SpeedyPage"
    CAMERA = "Fontisto-Camera"
    CAMERA_OFF = "Material-CameraOff"
    CONNECT = "Modern-Connect"
    EYE_SLASH_FILL = "BootstrapIcons-EyeSlashFill"
    WIFI_CANCEL = "Material-WifiCancel"
    SETTINGS = "Settings"
    SETTINGS_FILLED = "SettingsFilled"
    CIRCLE = "bx_circle"

    def path(self, theme=Theme.AUTO):
        return f":/app/images/icons/{self.value}_{getIconColor(theme)}.svg"
