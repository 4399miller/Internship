import os
import subprocess
import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from stylesheet import HOME_BK_STYLESHEET, LINE_STYLESHEET, HOME_TITLE_CONTENT, HOME_TITLE_STYLESHEET, \
    HOME_MIN_BUTTON_STYLESHEET, HOME_CLOSE_BUTTON_STYLESHEET, MENU_STYLESHEET, BUTTON_STYLESHEET
from utility.platformutility import open_local_folder

from view.main_ui import Ui_MainWindow
from win.components import ListenMoveWidget
from win.home import Home
from win.make_tuple_view import MakeAITupleView
from win.look_triples_view import LookTriplesWindow
from win.tubiao_win import TubiaoWindow
from win.video_tool_win import VideoToolWindow
from task_deploy_tools.win.main_win import MainWindow as LabelMainWindow
from task_deploy_tools.win.settings_dialog import SettingsWidget
from task_deploy_tools.win.settings_file import SettingsFile

from worker.save_config import *
from utility import MessageCenter, MessageEnum

class MainWindow(QWidget):
    current_directory_changed = Signal(str)
    WIDTH = 1000
    HEIGHT = 580

    TOP_HEIGHT = 31

    Size_Title = QSize(WIDTH, TOP_HEIGHT)
    Size_Content = QSize(WIDTH, HEIGHT-TOP_HEIGHT)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.current_directory = None

        self.setStyleSheet(MENU_STYLESHEET)
        self.__add_listener()
        self.__init_view()


    def __init_view(self):
        self.__init_title()

        self.home = Home(self)
        self.home.move(0, self.TOP_HEIGHT)
        self.home.setFixedSize(self.Size_Content)

    def __init_title(self):
        self.__top = QWidget(self)
        self.__top.move(0, 0)
        self.__top.setFixedSize(self.WIDTH, self.TOP_HEIGHT)

        widget = ListenMoveWidget(self.__top)
        widget.registerFunc(self.__move_window)
        widget.move(0, 0)
        widget.setFixedSize(self.WIDTH, self.TOP_HEIGHT)
        widget.setAttribute(Qt.WA_StyledBackground)
        widget.setStyleSheet(HOME_BK_STYLESHEET)

        line = QWidget(self.__top)
        line.move(0, self.TOP_HEIGHT-1)
        line.setFixedSize(self.WIDTH, 1)
        line.setAttribute(Qt.WA_TransparentForMouseEvents)
        line.setStyleSheet(LINE_STYLESHEET)

        x = 10
        self.iconlabel = QLabel(self.__top)
        self.iconlabel.move(x, 5)
        self.iconlabel.setAttribute(Qt.WA_TransparentForMouseEvents)
        # self.iconlabel.setPixmap(QPixmap(HOME_ICON_IMAGE_PATH))

        x += 5
        self.titlelabel = QLabel(self.__top)
        self.titlelabel.move(x, 8)
        self.titlelabel.setText(HOME_TITLE_CONTENT)
        self.titlelabel.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.titlelabel.setStyleSheet(HOME_TITLE_STYLESHEET)

        x += 50
        self.file_menu = QPushButton(self.__top)
        self.file_menu.move(x, 5)
        self.file_menu.setFixedSize(30, 25)
        self.file_menu.clicked.connect(self.open_file_menu)
        self.file_menu.setFocusPolicy(Qt.NoFocus)
        self.file_menu.setStyleSheet(BUTTON_STYLESHEET)
        self.file_menu.setText("File")
        self.file_menu.setToolTipDuration(0)

        x += 30
        self.tool_menu = QPushButton(self.__top)
        self.tool_menu.move(x, 5)
        self.tool_menu.setFixedSize(40, 25)
        self.tool_menu.clicked.connect(self.open_tool_menu)
        self.tool_menu.setFocusPolicy(Qt.NoFocus)
        self.tool_menu.setStyleSheet(BUTTON_STYLESHEET)
        self.tool_menu.setText("Tools")
        self.tool_menu.setToolTipDuration(0)

        x += 40
        self.tuple_menu = QPushButton(self.__top)
        self.tuple_menu.move(x, 5)
        self.tuple_menu.setFixedSize(50, 25)
        self.tuple_menu.clicked.connect(self.open_tuple_menu)
        self.tuple_menu.setFocusPolicy(Qt.NoFocus)
        self.tuple_menu.setStyleSheet(BUTTON_STYLESHEET)
        self.tuple_menu.setText("三元组")
        self.tuple_menu.setToolTipDuration(0)

        x += 50
        self.btn_settings_win = QPushButton(self.__top)
        self.btn_settings_win.move(x, 5)
        self.btn_settings_win.setFixedSize(30, 25)
        self.btn_settings_win.clicked.connect(self.open_settings_menu)
        self.btn_settings_win.setFocusPolicy(Qt.NoFocus)
        self.btn_settings_win.setStyleSheet(BUTTON_STYLESHEET)
        self.btn_settings_win.setText("设置")
        self.btn_settings_win.setToolTipDuration(0)

        x += 30
        self.feedback_button = QPushButton(self.__top)
        self.feedback_button.move(x, 5)
        self.feedback_button.setFixedSize(60, 25)
        self.feedback_button.clicked.connect(self.__open_user_problem)
        self.feedback_button.setFocusPolicy(Qt.NoFocus)
        self.feedback_button.setStyleSheet(BUTTON_STYLESHEET)
        self.feedback_button.setText("问题反馈")
        self.feedback_button.setToolTipDuration(0)

        x += 60
        self.user_button = QPushButton(self.__top)
        self.user_button.move(x, 5)
        self.user_button.setFixedSize(60, 25)
        self.user_button.clicked.connect(self.__open_user_tip)
        self.user_button.setFocusPolicy(Qt.NoFocus)
        self.user_button.setStyleSheet(BUTTON_STYLESHEET)
        self.user_button.setText("使用说明")
        self.user_button.setToolTipDuration(0)

        x += 665
        self.minbutton = QPushButton(self.__top)
        self.minbutton.move(x, 5)
        self.minbutton.setFixedSize(20, 20)
        self.minbutton.setStyleSheet(HOME_MIN_BUTTON_STYLESHEET)
        self.minbutton.clicked.connect(self.__show_mininized)
        self.minbutton.setFocusPolicy(Qt.NoFocus)

        x += 35
        self.closebutton = QPushButton(self.__top)
        self.closebutton.move(x, 5)
        self.closebutton.setFixedSize(20, 20)
        self.closebutton.setStyleSheet(HOME_CLOSE_BUTTON_STYLESHEET)
        self.closebutton.clicked.connect(self.__close_window)
        self.closebutton.setFocusPolicy(Qt.NoFocus)

    def __add_listener(self):
        # MessageCenter.add(MessageEnum.RefreshWorkSpace, self.__on_refresh_workspace)
        MessageCenter.add(MessageEnum.OpenLabelStudio, self.open_label_studio)
        MessageCenter.add(MessageEnum.OpenLookTriplesView, self.on_open_look_triples_view)

    def open_file_menu(self):
        menu = QMenu(self)

        action = QAction("选择工作空间", self, triggered=self.select_work_directory)
        menu.addAction(action)

        menu.exec_(QCursor.pos())

    def open_tool_menu(self):
        menu = QMenu(self)

        action = QAction("query查看工具", self, triggered=self.open_tubiao_window)
        menu.addAction(action)
        action = QAction("视频工具", self, triggered=self.open_video_tool_window)
        menu.addAction(action)
        action = QAction("文件工具", self, triggered=self.show_settings_file)
        menu.addAction(action)

        menu.exec_(QCursor.pos())

    def open_tuple_menu(self):
        menu = QMenu(self)

        action = QAction("三元组数据", self, triggered=self.open_ai_data_import_window)
        menu.addAction(action)
        action = QAction("三元组查看", self, triggered=self.open_look_triples_window)
        menu.addAction(action)
        action = QAction("上传工具", self, triggered=self.open_label_studio)
        menu.addAction(action)

        menu.exec_(QCursor.pos())

    def select_work_directory(self):
        # 打开文件对话框选择目录
        directory = QFileDialog.getExistingDirectory(self, "选择工作目录")
        if directory:
            MessageCenter.send(MessageEnum.RefreshWorkSpace, directory)
            save_user_choice('UserSettings', 'Workfolder', directory)

    def open_tubiao_window(self):
        tubiao_window = TubiaoWindow()
        tubiao_window.setWindowFlags(Qt.Tool)
        tubiao_window.show()

    def open_video_tool_window(self):
        video_tool_window = VideoToolWindow(self)
        video_tool_window.setWindowFlags(Qt.Tool)
        video_tool_window.show()

    def open_settings_menu(self):
        menu = QMenu(self)
        action = QAction("配置label-studio", self, triggered=self.show_settings)
        menu.addAction(action)
        menu.exec_(QCursor.pos())

    def show_settings(self):
        self.settings_wid = SettingsWidget(self)
        self.settings_wid.setWindowFlags(Qt.Tool)
        self.settings_wid.show()

    def show_settings_file(self):
        self.fileui_settings = SettingsFile(self)
        self.fileui_settings.setWindowFlags(Qt.Tool)
        self.fileui_settings.show()

    def open_ai_data_import_window(self):
        data_import_window = MakeAITupleView(self)
        data_import_window.setWindowFlags(Qt.Tool)
        data_import_window.show()

    def open_look_triples_window(self):
        look_triples_window = LookTriplesWindow(self)
        look_triples_window.setWindowFlags(Qt.Tool)
        look_triples_window.show()

    def open_label_studio(self, path=None):
        if path:
            labelstudio_window = LabelMainWindow(self, path)
        else:
            labelstudio_window = LabelMainWindow(self, None)
        labelstudio_window.setWindowFlags(Qt.Tool)
        labelstudio_window.show()

    def on_open_look_triples_view(self, folders):
        look_triples_window = LookTriplesWindow(self)
        look_triples_window.setWindowFlags(Qt.Tool)
        look_triples_window.init_folders(folders)
        look_triples_window.show()

    def __move_window(self, movePos):
        self.move(self.pos() + movePos)

    def __open_user_tip(self):
        # open_local_folder(USER_USE_URL)
        pass


    def __open_user_problem(self):
        # open_local_folder(FEEDBACK_URL)
        pass


    def __show_mininized(self):
        self.showMinimized()

    def __close_window(self):
        self.close()
