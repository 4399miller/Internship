import sys
import traceback

from PySide6.QtWidgets import *

from utility.logutility import LogUtility
from controller.maincontroller import MainController
from utility import qrc


class MainApplication:
    def __init__(self):
        self._app = QApplication(sys.argv)
        self.main_controller = MainController()

    def init_view(self):
        self.main_controller.open_view()

    def run(self):
        sys.exit(self._app.exec())


if __name__ == "__main__":
    try:
        app = MainApplication()
        app.init_view()
        app.run()


    except Exception as e:
        LogUtility().error(traceback.format_exc())
