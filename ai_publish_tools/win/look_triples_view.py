import json
import os
from datetime import datetime

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from view.look_triples_view import Ui_LookTriplesView
from utility import MessageCenter, MessageEnum


class LookTriplesWindow(QWidget):
    def __init__(self, par):
        super(LookTriplesWindow, self).__init__(parent=par)
        self.ui = Ui_LookTriplesView()
        self.ui.setupUi(self)
        self.areas = {}
        self.next_id = 4
        self.grid_id = [1, 2, 3]
        self.initialize_sub_ui_areas()
        self.sync_scroll_bars()
        self.folder_paths = {}
        self.folder_paths_arr = []
        self.connect_buttons()

        self.current_directory = None
        self.ai_config_file_path = None
        self.json_data = None

        self.__add_listener()

    def __add_listener(self):
        MessageCenter.add(MessageEnum.RefreshWorkSpace, self.set_current_directory)

    def set_current_directory(self, current_directory):
        self.current_directory = current_directory
        print(f"Current directory updated to: {self.current_directory}")

    def init_folders(self, folders):
        for folder in folders:
            if not os.path.exists(folder):
                QMessageBox.warning(self, "", f"folder not exist! \n{folder}")
                return

        for idx, folder in enumerate(folders):
            self._display_images_in_scroll_area(folder, idx+1)

    def initialize_sub_ui_areas(self):
        choose_button = getattr(self.ui, f'file_choose1')
        delete_button = getattr(self.ui, f'file_delete1')
        scroll_area = getattr(self.ui, f'scrollArea')
        self.areas[1] = {
            'choose_button': choose_button,
            'delete_button': delete_button,
            'scroll_area': scroll_area
        }
        for i in range(2, 4):
            choose_button = getattr(self.ui, f'file_choose{i}')
            delete_button = getattr(self.ui, f'file_delete{i}')
            scroll_area = getattr(self.ui, f'scrollArea_{i}')
            self.areas[i] = {
                'choose_button': choose_button,
                'delete_button': delete_button,
                'scroll_area': scroll_area
            }

    def sync_scroll_bars(self):
        print(f"Grid layout row count: {self.ui.gridLayout.rowCount()}")
        print(f"Grid layout column count: {self.ui.gridLayout.columnCount()}")
        for row in range(self.ui.gridLayout.rowCount()):
            for col in range(self.ui.gridLayout.columnCount()):
                item = self.ui.gridLayout.itemAtPosition(row, col)
                print(f"Item at ({row}, {col}): {item}")
        for components in self.areas.values():
            components['scroll_area'].verticalScrollBar().valueChanged.connect(self.sync_all_scroll_areas)

    def sync_all_scroll_areas(self, value):
        for components in self.areas.values():
            components['scroll_area'].verticalScrollBar().setValue(value)

    def connect_buttons(self):
        self.ui.add_button.clicked.connect(self.add_new_area)
        for area_id, components in self.areas.items():
            components['choose_button'].clicked.connect(lambda checked=False, id=area_id: self.choose_folder(id))
            components['delete_button'].clicked.connect(lambda checked=False, id=area_id: self.delete_area(id))

    def delete_area(self, area_id):
        if area_id in self.folder_paths and self.folder_paths[area_id]['folder_path']:
            self.folder_paths.pop(area_id)
        # 删除区域组件
        components = self.areas.pop(area_id)
        print(f"area_id:{area_id}")
        for widget in components.values():
            self.ui.gridLayout.removeWidget(widget)
            widget.deleteLater()

        self.rearrange_elements()

    def rearrange_elements(self):
        # 移除 add_button
        self.ui.gridLayout.removeWidget(self.ui.add_button)

        i = 0
        self.grid_id = []

        # 重新排列剩余的元素
        print(f"self.areas.item():{self.areas.items()}")
        for col, (area_id, components) in enumerate(self.areas.items()):
            self.ui.gridLayout.addWidget(components['choose_button'], 2, col, 1, 1)
            self.ui.gridLayout.addWidget(components['delete_button'], 3, col, 1, 1)
            self.ui.gridLayout.addWidget(components['scroll_area'], 5, col, 1, 1)

            if i <len(self.areas):
                self.grid_id.append(area_id)
                i = i + 1

        self.ui.gridLayout.addWidget(self.ui.add_button, 0, 0, 1, 1)

        # 更新布局
        self.ui.gridLayout.update()

    def add_new_area(self):
        new_id = self.next_id
        self.next_id += 1

        # 创建新的选择文件夹按钮
        new_choose_button = QPushButton(self)
        new_choose_button.setText(f"选择文件夹")
        new_choose_button.clicked.connect(lambda: self.choose_folder(new_id))

        # 创建新的删除按钮
        new_delete_button = QPushButton(self)
        new_delete_button.setText("删除此区块")
        new_delete_button.clicked.connect(lambda: self.delete_area(new_id))

        # 创建新的滚动区域
        new_scroll_area = QScrollArea(self)
        new_scroll_area.setWidgetResizable(True)
        new_scroll_area_contents = QWidget()
        new_scroll_area.setWidget(new_scroll_area_contents)

        # 添加新区域到字典
        self.areas[new_id] = {
            'choose_button': new_choose_button,
            'delete_button': new_delete_button,
            'scroll_area': new_scroll_area
        }

        # 重新排列所有元素
        self.rearrange_elements()

        # 同步新的滚动区域
        new_scroll_area.verticalScrollBar().valueChanged.connect(self.sync_all_scroll_areas)

    def choose_folder(self, area_id):
        start_directory = self.current_directory if self.current_directory else os.path.expanduser("~")
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", start_directory)
        if folder_path:
            self.display_images(folder_path, area_id)

    def display_images(self, folder_path, button_number):
        print(f"Grid layout row count: {self.ui.gridLayout.rowCount()}")
        print(f"Grid layout column count: {self.ui.gridLayout.columnCount()}")
        for row in range(self.ui.gridLayout.rowCount()):
            for col in range(self.ui.gridLayout.columnCount()):
                item = self.ui.gridLayout.itemAtPosition(row, col)
                print(f"Item at ({row}, {col}): {item}")

        self._display_images_in_scroll_area(folder_path, button_number)

    def _display_images_in_scroll_area(self, folder_path, button_number):
        self.folder_paths[button_number] = {'folder_path': folder_path}

        scroll_area = self.ui.gridLayout.itemAtPosition(5, self.grid_id.index(button_number) if hasattr(self, 'grid_id') else button_number).widget()

        layout = scroll_area.widget().layout()
        if layout is None:
            layout = QVBoxLayout()
            scroll_area.widget().setLayout(layout)
        else:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        image_files = [f for f in os.listdir(folder_path) if
                       f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        for image_file in image_files:
            pixmap = QPixmap(os.path.join(folder_path, image_file))
            label = QLabel()
            label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            layout.addWidget(label)

        layout.addStretch()

