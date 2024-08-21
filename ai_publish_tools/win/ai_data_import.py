import json
import os.path
import re
import shutil
import traceback

from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import *

from view.ai_data_import import Ui_ai_data_import


class AIDataImportWindow(QWidget):
    DataItems = [
        # "source",
        # "perceptron",
        # "mb_output",
        "business_landing",
        "query_in_source",
        "query_in_mb_output",
        "fix_by_hand",
    ]

    QueryItems = [
        "Top1",
        "Top2",
        "Top3",
    ]

    IndentDataItems = {
        # "source": "1.Source/{}/{}",
        # "perceptron": "",
        # "mb_output": "",
        "business_landing": "6.BusinessLanding/{}/{}",
        "fix_by_hand": "9.FixAIByHand/{}/{}",
    }

    QueryDataItems = {
        "query_in_source": "7.QueryInSource/{}/{}",
        "query_in_mb_output": "8.QueryInTargetByHand/{}/{}",
    }

    def __init__(self, par):
        super(AIDataImportWindow, self).__init__(parent=par)
        self.ui = Ui_ai_data_import()
        self.ui.setupUi(self)
        self.init_window()

        self.select_config_path = ""
        self.select_data_folder = ""
        self.rel_work_dir = ""
        self.pre_work_dir = ""
        self.anim_name = ""
        self.figure_id = ""

        self.config_data = {}



    def init_window(self):
        self.ui.select_config_button.clicked.connect(self.select_config_file)
        self.ui.select_data_folder.clicked.connect(self.select_data_directory)
        self.ui.exec_button.clicked.connect(self.exec_add_data)

        self.ui.comboBox.addItems(self.DataItems)
        self.ui.comboBox.currentTextChanged.connect(self.on_dtype_changed)
        self.ui.comboBox_2.addItems(self.QueryItems)
        self.ui.comboBox_2.currentTextChanged.connect(self.on_query_top_changed)

        self.ui.comboBox_2.setVisible(False)

    def on_dtype_changed(self, value):
        self.refresh_target_data_folder()

        self.ui.comboBox_2.setVisible(value in self.QueryDataItems.keys())

    def on_query_top_changed(self, value):
        self.refresh_target_data_folder()


    def select_config_file(self):
        # 打开文件对话框选择目录
        file_tuple = QFileDialog.getOpenFileName(self, "选择三元组数据配置文件")
        if file_tuple[0] != "":
            file_path = file_tuple[0]
            if self.read_config_data(file_path):
                return
            else:
                QMessageBox.warning(self, "", "请选择正确的三元组数据配置文件")
        else:
            QMessageBox.warning(self, "", "请选择正确的三元组数据配置文件")



    def select_data_directory(self):
        # 打开文件对话框选择目录
        directory = QFileDialog.getExistingDirectory(self, "选择数据所在目录")
        if directory:
            self.select_data_folder = directory
            self.ui.select_data_folder.setText(directory)

    def deal_config_data(self, data, config_path):
        rel_source_path = data['source']
        splits = rel_source_path.split('/')
        self.rel_work_dir = "/".join(splits[:3])
        self.anim_name = splits[-1]
        self.figure_id = splits[-2]
        self.pre_work_dir = re.split(f"{self.rel_work_dir}", config_path)[0].strip('/')

        print(self.rel_work_dir)
        print(self.pre_work_dir)
        self.select_config_path = config_path
        self.config_data = data

        self.ui.select_config_button.setText(config_path[-90:])
        self.refresh_target_data_folder()

    def refresh_target_data_folder(self):
        move_data_folder = self.get_move_target_folder()
        self.ui.target_data_folder.setText(move_data_folder)

    def get_move_target_folder(self):
        choose_dtype = self.ui.comboBox.currentText()

        if choose_dtype in self.IndentDataItems.keys():
            move_data_folder = f"{self.pre_work_dir}/{self.rel_work_dir}/{self.IndentDataItems[choose_dtype]}".format(self.figure_id, self.anim_name)
            print(move_data_folder)

            return move_data_folder

        elif choose_dtype in self.QueryDataItems.keys():
            query_top = self.ui.comboBox_2.currentText()

            move_data_folder = f"{self.pre_work_dir}/{self.rel_work_dir}/{self.QueryDataItems[choose_dtype]}".format(self.figure_id, f"[{self.anim_name}][{query_top}]")
            print(move_data_folder)

            return move_data_folder

    def exec_add_data(self):
        choose_dtype = self.ui.comboBox.currentText()

        move_data_folder = self.get_move_target_folder()

        if self.move_select_data_folder(move_data_folder):
            self.config_data[choose_dtype] = move_data_folder[len(self.pre_work_dir) + 1:]

            self.write_config_data()

    def move_select_data_folder(self, move_data_folder):
        if not os.path.exists(self.select_data_folder):
            return False

        try:
            if os.path.exists(move_data_folder):
                shutil.rmtree(move_data_folder)
            os.makedirs(move_data_folder, exist_ok=True)

            shutil.copytree(self.select_data_folder, move_data_folder, dirs_exist_ok=True)

            return True
        except:
            print(traceback.format_exc())
            return False

    def write_config_data(self):
        if self.select_config_path == "":
            return

        try:
            with open(self.select_config_path, "w+") as f:
                f.write(json.dumps(self.config_data, indent=2))

        except:
            pass

    def read_config_data(self, config_path):
        if not os.path.exists(config_path):
            return False

        try:
            with open(config_path, "r") as f:
                data = json.loads(f.read())
                if 'source' in data.keys() and 'mb_output' in data.keys():
                    self.deal_config_data(data, config_path)
                    return True

            return False

        except:
            return False

























