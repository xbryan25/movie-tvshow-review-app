from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, pyqtSignal


class ClickableFrame(QFrame):
    clicked = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(True)
        super().mousePressEvent(event)
