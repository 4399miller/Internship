
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import *


from utility.message import *
from model.messagebox import *


class NotifyController(Singleton):

    def new(self):
        MessageCenter.add(MessageEnum.NotifyMessage, self.__show_tray_message)

    def try_create_tray(self, par, menu):
        self.__trayIcon = None
        if QSystemTrayIcon.isSystemTrayAvailable():
            QApplication.setQuitOnLastWindowClosed(False)
            self.__create_trayIcon(par, menu)
        else:
            QApplication.setQuitOnLastWindowClosed(True)


    def __create_trayIcon(self, par, menu):
        self.__trayIcon = QSystemTrayIcon(par)
        # self.__trayIcon.setIcon(QIcon(APP_ICON))
        self.__trayIcon.setContextMenu(menu)
        # self.__trayIcon.setToolTip(PAPER_UNITY_LAUNCHER)
        self.__trayIcon.messageClicked.connect(self.__on_message_clicked)
        self.__trayIcon.activated.connect(self.__icon_activated)

        self.__trayIcon.show()

    def __show_tray_message(self, data):
        if data is None or not isinstance(data, NotifyInfo):
            return
        if self.__trayIcon is not None and self.__trayIcon.supportsMessages():
            # self.__trayIcon.showMessage(data.title, data.content, QIcon(APP_ICON), 20000)
            pass

    def __on_message_clicked(self):
        MessageCenter.send(MessageEnum.ActiveHomeWindow, None)

    def __icon_activated(self, reason):
        print(reason)
        if reason in (QSystemTrayIcon.DoubleClick, QSystemTrayIcon.Trigger, QSystemTrayIcon.MiddleClick):
            MessageCenter.send(MessageEnum.ActiveHomeWindow, None)














