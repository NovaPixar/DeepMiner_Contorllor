from PySide6.QtGui import QPixmap
from qfluentwidgets import ImageLabel


class LabelPixmapResizer:
    def __init__(self):
        self.maxValue = 16777215
        self.minValue = 0

    def resizeImageLabel(self, imageLabel: ImageLabel, pixmap: QPixmap):
        imageLabel.setPixmap(pixmap)
        imageLabel.setMinimumSize(self.minValue, self.minValue)
        imageLabel.setMaximumSize(self.maxValue, self.maxValue)
