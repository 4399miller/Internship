import os
import subprocess
import sys

from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QDir
from PySide6.QtGui import *

from stylesheet import MENU_STYLESHEET, TREEVIEW_STYLESHEET
from task_deploy_tools.win.main_win import MainWindow
from utility import MessageCenter, MessageEnum
from view.home import Ui_Home
from win.make_tuple_view import MakeAITupleView
from win.look_triples_view import LookTriplesWindow
from win.tubiao_win import TubiaoWindow
from win.video_tool_win import VideoToolWindow
from task_deploy_tools.win.settings_dialog import SettingsWidget
from task_deploy_tools.win.settings_file import SettingsFile
from worker.save_config import *


class Home(QWidget):
    def __init__(self, par):
        super(Home, self).__init__(parent=par)
        self.ui = Ui_Home()
        self.ui.setupUi(self)
        self.setStyleSheet(MENU_STYLESHEET)
        # self.sub_window = SubWindow(self)
        # self.sub_window.setWindowFlags(Qt.Tool)
        self.__add_listener()
        self.init_window()
        # self.init_settings_widget()

    def __add_listener(self):
        MessageCenter.add(MessageEnum.RefreshWorkSpace, self.__on_refresh_workspace)
        MessageCenter.add(MessageEnum.OpenLabelStudio, self.open_label_studio)
        MessageCenter.add(MessageEnum.OpenLookTriplesView, self.on_open_look_triples_view)



    def init_window(self):
        # self.ui.file_menu.clicked.connect(self.open_file_menu)
        # self.ui.tool_menu.clicked.connect(self.open_tool_menu)
        # self.ui.tuple_menu.clicked.connect(self.open_tuple_menu)
        # self.ui.btn_settings_win.clicked.connect(self.open_settings_menu)

        self.ui.treeView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.treeView.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 创建QFileSystemModel
        self.model = QFileSystemModel()

        self.model.setRootPath(QDir.rootPath())

        # 设置模型到TreeView
        self.ui.treeView.setModel(self.model)
        # 连接按钮点击事件到选择目录方法
        self.ui.treeView.doubleClicked.connect(self.on_double_click)
        self.ui.treeView.setColumnWidth(0, 300)
        self.ui.treeView.setStyleSheet(TREEVIEW_STYLESHEET)
        # 读取以前选择的工作目录
        pre_choice = load_user_choice('UserSettings', 'Workfolder')
        if pre_choice:
            MessageCenter.send(MessageEnum.RefreshWorkSpace, pre_choice)

    def __on_refresh_workspace(self, data):
        # 设置选中的目录为根路径
        root_index = self.model.setRootPath(data)
        # 更新TreeView的根索引
        self.ui.treeView.setRootIndex(root_index)


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


    def open_settings_menu(self):
        menu = QMenu(self)
        action = QAction("配置label-studio", self, triggered=self.show_settings)
        menu.addAction(action)
        menu.exec_(QCursor.pos())

    def show_settings(self):
        self.ui.settings = SettingsWidget(self)
        self.ui.settings.setWindowFlags(Qt.Tool)
        self.ui.settings.show()

    def show_settings_file(self):
        self.fileui_settings = SettingsFile(self)
        self.fileui_settings.setWindowFlags(Qt.Tool)
        self.fileui_settings.show()

    def select_work_directory(self):
        # 打开文件对话框选择目录
        directory = QFileDialog.getExistingDirectory(self, "选择工作目录")
        if directory:
            MessageCenter.send(MessageEnum.RefreshWorkSpace, directory)
            save_user_choice('UserSettings', 'Workfolder', directory)

    def open_ai_data_import_window(self):
        data_import_window = MakeAITupleView(self)
        data_import_window.setWindowFlags(Qt.Tool)
        data_import_window.show()

    def open_look_triples_window(self):
        look_triples_window = LookTriplesWindow(self)
        look_triples_window.setWindowFlags(Qt.Tool)
        look_triples_window.show()

    def open_tubiao_window(self):
        tubiao_window = TubiaoWindow()
        tubiao_window.setWindowFlags(Qt.Tool)
        tubiao_window.show()

    def open_video_tool_window(self):
        video_tool_window = VideoToolWindow(self)
        video_tool_window.setWindowFlags(Qt.Tool)
        video_tool_window.show()

    def open_label_studio(self, path=None):
        if path:
            labelstudio_window = MainWindow(self, path)
        else:
            labelstudio_window = MainWindow(self, None)
        labelstudio_window.setWindowFlags(Qt.Tool)
        labelstudio_window.show()

    def on_open_look_triples_view(self, folders):
        look_triples_window = LookTriplesWindow(self)
        look_triples_window.setWindowFlags(Qt.Tool)
        look_triples_window.init_folders(folders)
        look_triples_window.show()

    def on_double_click(self, index):
        # 获取被双击项目的文件路径
        path = self.model.filePath(index)

        # 检查是否为文件
        if QDir(path).exists():
            # 如果是目录，展开或折叠
            self.ui.treeView.setExpanded(index, not self.ui.treeView.isExpanded(index))
        else:
            # 如果是文件，打开它
            self.open_file(path)

    def open_file(self, file_path):
        if sys.platform == "win32":
            os.startfile(file_path)
        elif sys.platform == "darwin":  # macOS
            subprocess.call(["open", file_path])
        else:  # linux
            subprocess.call(["xdg-open", file_path])






















