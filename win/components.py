from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class ListenMoveWidget(QWidget):
    def __init__(self, par):
        super(ListenMoveWidget, self).__init__()
        self.setParent(par)
        self.setAttribute(Qt.WA_StyledBackground)
        self.isPressed = False
        self.startPos = None
        self.moveCall = None

    def registerFunc(self, func):
        self.moveCall = func

    def mousePressEvent(self, event):
        self.isPressed = True
        self.startPos = event.globalPos()
        return QWidget().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.isPressed:
            movePos = event.globalPos() - self.startPos
            self.startPos = event.globalPos()
            if self.moveCall != None:
                self.moveCall(movePos)

        return QWidget().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.isPressed = False
        return QWidget().mouseReleaseEvent(event)
