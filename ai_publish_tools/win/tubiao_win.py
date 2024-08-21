import os
import subprocess
import sys
import natsort

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

# 创建主窗口实例
from view.main_ui import Ui_MainWindow
from view.sub_main_ui import Ui_SubMainWindow
from view.tubiao_ui import Ui_TuMainWindow
from view.video_tool_ui import Ui_sub_video
from utility.commandlineutility import subprocess_may_error
from worker.ffmpeg_worker import ffmpeg_generate_avi

class TubiaoWindow(QMainWindow):
    def __init__(self):
        super(TubiaoWindow, self).__init__()
        self.tubiao_ui = Ui_TuMainWindow()
        self.tubiao_ui.setupUi(self)
        self.tubiao_ui.pushButton.clicked.connect(self.tubiao_select_folder)
        self.init_tubiao_window()
        self.current_directory = None

    @Slot(str)
    def set_current_directory(self, current_directory):
        self.current_directory = current_directory
        # 在此处添加任何需要的更新操作
        print(f"Current directory updated to: {self.current_directory}")

    def tubiao_select_folder(self):
        start_directory = self.current_directory if self.current_directory else os.path.expanduser("~")
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", start_directory)
        if folder_path:
            self.tubiao_load_images(folder_path)

    def tubiao_load_images(self, folder_path):
        self.tubiao_model = QStandardItemModel()
        self.tubiao_ui.listView.setModel(self.tubiao_model)
        self.tubiao_model.clear()

        # 获取所有图片文件并进行自然排序
        image_files = [f for f in os.listdir(folder_path) if
                       f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        sorted_files = natsort.natsorted(image_files)

        for file_name in sorted_files:
            file_path = os.path.join(folder_path, file_name)
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                icon = QIcon(pixmap)
                item = QStandardItem(icon, file_name)
                self.tubiao_model.appendRow(item)

        self.tubiao_ui.listView.setViewMode(QListView.IconMode)
        self.tubiao_ui.listView.setIconSize(QSize(100, 100))
        self.tubiao_ui.listView.setResizeMode(QListView.Adjust)
        self.tubiao_ui.listView.setSpacing(10)  # 设置图标之间的间距

    def adjust_icon_size(self):
        size = self.tubiao_ui.slider.value()
        self.tubiao_ui.listView.setIconSize(QSize(size, size))

    def init_tubiao_window(self):
        self.tubiao_ui.slider = QSlider(Qt.Horizontal, self.tubiao_ui.centralwidget)
        self.tubiao_ui.slider.setObjectName(u"slider")
        self.tubiao_ui.slider.setMinimum(50)
        self.tubiao_ui.slider.setMaximum(400)
        self.tubiao_ui.slider.setValue(100)
        self.tubiao_ui.gridLayout.addWidget(self.tubiao_ui.slider, 3, 0, 1, 1)

        self.tubiao_ui.gridLayout_2.addLayout(self.tubiao_ui.gridLayout, 0, 0, 1, 1)
        self.tubiao_ui.slider.valueChanged.connect(self.adjust_icon_size)
