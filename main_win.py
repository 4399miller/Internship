import os
import subprocess
import sys

from PySide6.QtCore import QDir, Qt, QSize, Signal
from PySide6.QtWidgets import QFileDialog, QMainWindow, QLabel, QPushButton, QScrollArea,  QVBoxLayout, QFileSystemModel, QSlider, QListView, QWidget, QMessageBox
from PySide6.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem
from PySide6 import QtWidgets

# 创建主窗口实例
from view.main_ui import Ui_MainWindow
from win.look_triples_view import LookTriplesWindow
from win.tubiao_win import TubiaoWindow
from win.video_tool_win import VideoToolWindow

class MainWindow(QMainWindow):
    current_directory_changed = Signal(str)
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_directory = None
        self.init_window()

        #创建子窗口实例，并设置于主窗口之上
        self.sub_window = LookTriplesWindow()
        self.sub_window.setWindowFlags(Qt.Tool)
        self.tubiao_window = TubiaoWindow()
        self.tubiao_window.setWindowFlags(Qt.Tool)
        self.video_tool_window = VideoToolWindow()
        self.video_tool_window.setWindowFlags(Qt.Tool)

        #获取并同步当前工作目录
        self.current_directory_changed.connect(self.sub_window.set_current_directory)
        self.current_directory_changed.connect(self.tubiao_window.set_current_directory)
        self.current_directory_changed.connect(self.video_tool_window.set_current_directory)
        self.current_directory_changed.emit(self.current_directory)

        self.ui.open_action.triggered.connect(self.open_sub_window)
        self.ui.construct_action.triggered.connect(self.open_tubiao_window)
        self.ui.submit_action.triggered.connect(self.open_video_tool_window)

    def open_sub_window(self):
        self.sub_window.show()

    def open_tubiao_window(self):
        self.tubiao_window.show()

    def open_video_tool_window(self):
        self.video_tool_window.show()

    def init_window(self):
        self.ui.treeView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.treeView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # 创建QFileSystemModel
        self.model = QFileSystemModel()

        self.model.setRootPath(QDir.rootPath())

        # 设置模型到TreeView
        self.ui.treeView.setModel(self.model)
        # 连接按钮点击事件到选择目录方法
        self.ui.pushButton.clicked.connect(self.select_work_directory)
        self.ui.treeView.doubleClicked.connect(self.on_double_click)

    def select_work_directory(self):
        # 打开文件对话框选择目录
        directory = QFileDialog.getExistingDirectory(self, "选择工作目录")
        if directory:
            # 设置选中的目录为根路径
            root_index = self.model.setRootPath(directory)
            # 更新TreeView的根索引
            self.ui.treeView.setRootIndex(root_index)

            self.current_directory = directory
            self.current_directory_changed.emit(self.current_directory)

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