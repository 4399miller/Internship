import os
import logging
import sys

from .singleton import Singleton
from .timeutility import strf_now


class LogUtility(Singleton):
    Root = os.path.abspath(os.path.dirname(sys.argv[0])).replace('\\', '/')
    LogPath = Root + "/Log"
    LogFile = LogPath + "/app.log"

    def new(self):
        try:
            if not os.path.exists(self.LogPath):
                os.mkdir(self.LogPath)
            logging.basicConfig(filename=self.LogFile, filemode="w",
                                level=logging.DEBUG,
                                format='%(asctime)s  %(message)s',
                                encoding="utf-8")
        except Exception as e:
            print(e)

    def debug(self, text):
        print(text)
        logging.debug(f"{strf_now} :\n {text}")

    def warning(self, text):
        print(text)
        logging.warning(f"{strf_now} :\n {text}")

    def error(self, text):
        print(text)
        logging.error(f"{strf_now} :\n {text}")

    def info(self, text):
        print(text)
        logging.info(f"{strf_now} :\n {text}")






