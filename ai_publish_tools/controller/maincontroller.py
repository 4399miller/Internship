

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from utility import MessageCenter, MessageEnum
from utility.processutility import killCurProcess
from controller.notifycontroller import NotifyController
from utility.singleton import Singleton
from win.main_win import MainWindow


class MainController(Singleton):

    def __init__(self):
        self.__init_message()
        self.__init_controller()

        self.view = None

    def __init_message(self):
        MessageCenter.add(MessageEnum.ActiveHomeWindow, self.__active_home_window)

        pass

    def __init_controller(self):

        pass

    def open_view(self):
        self.view = MainWindow()
        self.view.show()

        # self.init_notify()

    def init_notify(self):
        aRestore = QAction('打开主窗口', self.view, triggered=self.activate_window)
        aQuit = QAction('退出', self.view, triggered=self.__quit_app)

        menu = QMenu(self.view)
        menu.addAction(aRestore)
        menu.addSeparator()
        menu.addAction(aQuit)

        NotifyController().try_create_tray(self.view, menu)

    def activate_window(self):
        self.view.activateWindow()
        self.view.setWindowState(self.view.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.view.showNormal()

    def __quit_app(self):
        killCurProcess()

    def __active_home_window(self, data):
        self.activate_window()




















