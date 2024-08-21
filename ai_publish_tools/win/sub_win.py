import json
import os
from datetime import datetime

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from view.sub_main import Ui_SubMain
from task_deploy_tools.win.main_win import MainWindow
from task_deploy_tools.modules.local_cache import LocalCache
from worker.ai_tuple_upload import list_png_to_dir
from worker.get_json_file import read_json_file
from worker.ai_tuple_upload import upload_result
from worker.ai_tuple_upload import form_triple
from utility import MessageCenter, MessageEnum

class SubWindow(QWidget):
    # open_label_studio_signal = Signal(str)
    def __init__(self, par):
        super(SubWindow, self).__init__(parent=par)
        self.sub_ui = Ui_SubMain()
        self.sub_ui.setupUi(self)
        self.areas = {}
        self.next_id = 4
        self.grid_id = [1, 2, 3]
        self.initialize_sub_ui_areas()
        self.sync_scroll_bars()
        self.folder_paths = {}
        self.folder_paths_arr = []
        self.connect_buttons()
        # self.open_label_studio_signal.connect(self.open_label_studio)
        # self.__add_listener_dir()
        self.__add_listener_label_studio()
        self.cache_folder_path = LocalCache.get_folder_paths()
        self.load_saved_folder_paths()

        self.dropdown = QComboBox(self)
        self.sub_ui.gridLayout.addWidget(self.dropdown, 0, 2, 1, 1)

        self.current_directory = None
        self.ai_config_file_path = None
        self.json_data = None
        self.dropdown = None

    # def __add_listener_dir(self):
    #     MessageCenter.add(MessageEnum.RefreshWorkSpace, self.set_current_directory)

    # @Slot(str)
    def set_current_directory(self, current_directory):
        self.current_directory = current_directory
        print(f"Current directory updated to: {self.current_directory}")


    def initialize_sub_ui_areas(self):
        choose_button = getattr(self.sub_ui, f'file_choose1')
        delete_button = getattr(self.sub_ui, f'file_delete1')
        scroll_area = getattr(self.sub_ui, f'scrollArea')
        self.areas[1] = {
            'choose_button': choose_button,
            'delete_button': delete_button,
            'scroll_area': scroll_area
        }
        for i in range(2, 4):
            choose_button = getattr(self.sub_ui, f'file_choose{i}')
            delete_button = getattr(self.sub_ui, f'file_delete{i}')
            scroll_area = getattr(self.sub_ui, f'scrollArea_{i}')
            self.areas[i] = {
                'choose_button': choose_button,
                'delete_button': delete_button,
                'scroll_area': scroll_area
            }

    def sync_scroll_bars(self):
        print(f"Grid layout row count: {self.sub_ui.gridLayout.rowCount()}")
        print(f"Grid layout column count: {self.sub_ui.gridLayout.columnCount()}")
        for row in range(self.sub_ui.gridLayout.rowCount()):
            for col in range(self.sub_ui.gridLayout.columnCount()):
                item = self.sub_ui.gridLayout.itemAtPosition(row, col)
                print(f"Item at ({row}, {col}): {item}")
        for components in self.areas.values():
            components['scroll_area'].verticalScrollBar().valueChanged.connect(self.sync_all_scroll_areas)

    def sync_all_scroll_areas(self, value):
        for components in self.areas.values():
            components['scroll_area'].verticalScrollBar().setValue(value)

    def connect_buttons(self):
        self.sub_ui.add_button.clicked.connect(self.add_new_area)
        self.sub_ui.data_file_choose4.clicked.connect(self.choose_data_file)
        self.sub_ui.form_triples.clicked.connect(self.form_triples)
        self.sub_ui.labelstudio_Button.clicked.connect(self.open_label_studio)
        for area_id, components in self.areas.items():
            components['choose_button'].clicked.connect(lambda checked=False, id=area_id: self.choose_folder(id))
            components['delete_button'].clicked.connect(lambda checked=False, id=area_id: self.delete_area(id))

    def create_dropdown(self):
        if self.dropdown is None:
            self.dropdown = QComboBox(self)
            self.sub_ui.gridLayout.addWidget(self.dropdown, 0, 2, 1, 1)

        if self.ai_config_file_path:
            # 搜索并读取JSON文件
            with open(self.ai_config_file_path, "r") as f:
                self.json_data = json.loads(f.read())
            # # 搜索并读取JSON文件
            # target_file = 'config.json'
            # self.json_data = read_json_file(self.ai_config_file_path, target_file)

            if self.json_data:
                self.dropdown.clear()
                array_keys = self.get_available_keys()
                self.dropdown.addItems(array_keys)
                self.dropdown.currentIndexChanged.connect(self.display_selected_images)
                self.display_selected_images(array_keys[0] if len(array_keys) > 0 else None)
            else:
                QMessageBox.warning(self, "错误", "未找到config.json文件")
                self.dropdown.clear()
                self.dropdown.addItem("无法加载选项")
        else:
            self.dropdown.clear()
            self.dropdown.addItem("请选择文件夹")

    def get_available_keys(self):
        if not self.json_data:
            return []

        available_keys = []
        indent_items = ["business_landing", "fix_by_hand"]
        for item in indent_items:
            if item in self.json_data and self.json_data[item]:
                available_keys.append(item)

        query_items = ["query_in_source", "query_in_mb_output"]
        for item in query_items:
            for k, v in self.json_data[item].items():
                if v:
                    available_keys.append(f"{item}-{k}")

        print(available_keys)
        return available_keys


    def choose_data_file(self):
        start_directory = self.current_directory if self.current_directory else os.path.expanduser("~")
        selected_tuple = QFileDialog.getOpenFileName(self, "选择文件夹", start_directory)
        if selected_tuple[0]:
            self.ai_config_file_path = selected_tuple[0]
            self.create_dropdown()
        else:
            QMessageBox.information(self, "提示", "未选择任何文件夹")

    def delete_area(self, area_id):
        if area_id in self.folder_paths and self.folder_paths[area_id]['folder_path']:
            self.folder_paths.pop(area_id)
        # 删除区域组件
        components = self.areas.pop(area_id)
        print(f"area_id:{area_id}")
        for widget in components.values():
            self.sub_ui.gridLayout.removeWidget(widget)
            widget.deleteLater()

        self.rearrange_elements()

    def rearrange_elements(self):
        # 移除 add_button
        self.sub_ui.gridLayout.removeWidget(self.sub_ui.add_button)

        i = 0
        self.grid_id = []

        # 重新排列剩余的元素
        print(f"self.areas.item():{self.areas.items()}")
        for col, (area_id, components) in enumerate(self.areas.items()):
            self.sub_ui.gridLayout.addWidget(components['choose_button'], 2, col, 1, 1)
            self.sub_ui.gridLayout.addWidget(components['delete_button'], 3, col, 1, 1)
            self.sub_ui.gridLayout.addWidget(components['scroll_area'], 5, col, 1, 1)

            if i <len(self.areas):
                self.grid_id.append(area_id)
                i = i + 1

        self.sub_ui.gridLayout.addWidget(self.sub_ui.add_button, 0, 0, 1, 1)

        # 更新布局
        self.sub_ui.gridLayout.update()

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
            if folder_path not in self.cache_folder_path:
                self.cache_folder_path.append(folder_path)
            LocalCache.save_folder_paths(self.cache_folder_path)

    def load_saved_folder_paths(self):
        for i, folder_path in enumerate(self.cache_folder_path):
            if i < len(self.grid_id):
                self.display_images(folder_path, self.grid_id[i])

    # def display_images(self, folder_path, button_number):
    #     print(f"Grid layout row count: {self.sub_ui.gridLayout.rowCount()}")
    #     print(f"Grid layout column count: {self.sub_ui.gridLayout.columnCount()}")
    #     for row in range(self.sub_ui.gridLayout.rowCount()):
    #         for col in range(self.sub_ui.gridLayout.columnCount()):
    #             item = self.sub_ui.gridLayout.itemAtPosition(row, col)
    #             print(f"Item at ({row}, {col}): {item}")
    #     scroll_area = self.sub_ui.gridLayout.itemAtPosition(5, self.grid_id.index(button_number)).widget()
    #
    #     # self.folder_paths.append(folder_path)
    #     self.folder_paths[button_number] = {
    #         'folder_path' : folder_path
    #     }
    #
    #     layout = scroll_area.widget().layout()
    #     if layout is not None:
    #         while layout.count():
    #             child = layout.takeAt(0)
    #             if child.widget():
    #                 child.widget().deleteLater()
    #     else:
    #         layout = QVBoxLayout()
    #         scroll_area.widget().setLayout(layout)
    #
    #     image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    #
    #     for image_file in image_files:
    #         pixmap = QPixmap(os.path.join(folder_path, image_file))
    #         label = QLabel()
    #         label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Resize image
    #         layout.addWidget(label)
    #
    #     layout.addStretch()
    #
    # def display_selected_images(self, value=None):
    #     if not self.json_data:
    #         print("JSON 数据未加载")
    #         return
    #
    #     selected_key = self.dropdown.currentText()
    #     config_dir = os.path.dirname(self.ai_config_file_path)
    #
    #     sol_sou_path = self.json_data['source']
    #     sol_sou_path = sol_sou_path.split('/', 3)[-1]
    #     source_path = os.path.join(config_dir, sol_sou_path)
    #
    #     sol_mb_path = self.json_data['mb_output']
    #     sol_mb_path = sol_mb_path.split('/', 3)[-1]
    #     mb_output_path = os.path.join(config_dir, sol_mb_path)
    #
    #     if value:
    #         other_path = self.json_data[value]
    #
    #
    #     def display_spe_images(folder_path, button_number):
    #         scroll_area = self.sub_ui.gridLayout.itemAtPosition(5, button_number).widget()
    #
    #         layout = scroll_area.widget().layout()
    #         if layout is not None:
    #             while layout.count():
    #                 child = layout.takeAt(0)
    #                 if child.widget():
    #                     child.widget().deleteLater()
    #         else:
    #             layout = QVBoxLayout()
    #             scroll_area.widget().setLayout(layout)
    #
    #         image_files = [f for f in os.listdir(folder_path) if
    #                        f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    #
    #         for image_file in image_files:
    #             pixmap = QPixmap(os.path.join(folder_path, image_file))
    #             label = QLabel()
    #             label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Resize image
    #             layout.addWidget(label)
    #
    #         layout.addStretch()
    #
    #     self.folder_paths[0] ={
    #         'folder_path' : source_path
    #     }
    #     self.folder_paths[1] = {
    #         'folder_path': mb_output_path
    #     }
    #     display_spe_images(source_path, 0)
    #     display_spe_images(mb_output_path, 1)

    def display_images(self, folder_path, button_number):
        print(f"Grid layout row count: {self.sub_ui.gridLayout.rowCount()}")
        print(f"Grid layout column count: {self.sub_ui.gridLayout.columnCount()}")
        for row in range(self.sub_ui.gridLayout.rowCount()):
            for col in range(self.sub_ui.gridLayout.columnCount()):
                item = self.sub_ui.gridLayout.itemAtPosition(row, col)
                print(f"Item at ({row}, {col}): {item}")

        self._display_images_in_scroll_area(folder_path, button_number)

    def display_selected_images(self, value=None):
        if not self.json_data:
            print("JSON 数据未加载")
            return

        config_dir = os.path.dirname(self.ai_config_file_path)

        sol_sou_path = self.json_data['source'].split('/', 3)[-1]
        source_path = os.path.join(config_dir, sol_sou_path)

        sol_mb_path = self.json_data['mb_output'].split('/', 3)[-1]
        mb_output_path = os.path.join(config_dir, sol_mb_path)

        self.folder_paths[0] = {'folder_path': source_path}
        self.folder_paths[1] = {'folder_path': mb_output_path}

        self._display_images_in_scroll_area(source_path, 0)
        self._display_images_in_scroll_area(mb_output_path, 1)

        if value:
            other_path = self.json_data[value]
            # 如果需要处理 other_path，可以在这里添加代码

    def _display_images_in_scroll_area(self, folder_path, button_number):
        scroll_area = self.sub_ui.gridLayout.itemAtPosition(5, self.grid_id.index(button_number) if hasattr(self,
                                                                                                            'grid_id') else button_number).widget()

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
        self.folder_paths[button_number] = {'folder_path': folder_path}

    def form_triples(self):
        # 弹框提示用户输入文件夹名
        text, ok = QInputDialog.getText(self, '输入文件夹名', '请输入文件夹名:')
        if ok and text:
            output_folder = text
        else:
            QMessageBox.information(self, "提示", "输入无效")
            return
        current_datetime = datetime.now()
        key_path = current_datetime.strftime("%Y.%m.%d")
        self.combined_path = os.path.join(key_path, output_folder)
        remote_folder = f"dataset/ai_result/{key_path}/{os.path.basename(output_folder)}"
        # 显示路径信息
        QMessageBox.information(self, "路径信息", f"文件夹已创建。\n\n远程路径: {remote_folder}")
        MessageCenter.send(MessageEnum.OpenLabelStudio, self.combined_path)
        form_triple(self.folder_paths, output_folder)
        # self.open_label_studio_signal.emit(self.combined_path)

    def __add_listener_label_studio(self):
        MessageCenter.add(MessageEnum.OpenLabelStudio, self.open_label_studio)
    # @Slot(str)
    def open_label_studio(self, path):
        if path:
            self.labelstudio_window = MainWindow(self, path)
        else:
            self.labelstudio_window = MainWindow(self, None)
        self.labelstudio_window.setWindowFlags(Qt.Tool)
        self.labelstudio_window.show()

    # def open_label_studio(self):
    #     if hasattr(self, 'combined_path'):
    #         self.labelstudio_window = MainWindow(self.combined_path)
    #     else:
    #         self.labelstudio_window = MainWindow(self, path=None)
    #     self.labelstudio_window.setWindowFlags(Qt.Tool)
    #     self.labelstudio_window.show()