import json
import os.path
import re
import shutil
import traceback
from datetime import datetime

from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import *

from utility import *
from view.tuple_view import Ui_tupleview
from worker.ai_tuple_upload import form_triple


KeyWord_Mapping = {
    "source": "数据源",
    "perceptron": "渲染器输出",
    "mb_output": "MotionBuilder输出",
    "business_landing": "业务数据",
    "query_in_source": "对源角色数据Query",
    "query_in_mb_output": "对算法输出数据Query",
    "fix_by_hand": "算法直出数据上人工手修",
}


def get_mapping_value(input_key):
    if input_key in KeyWord_Mapping.keys():
        return KeyWord_Mapping[input_key]
    return input_key


def get_mapping_key(input_value):
    for k, v in KeyWord_Mapping.items():
        if v == input_value:
            return k

    return input_value


class MakeAITupleView(QWidget):
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
        "top1",
        "top2",
        "top3",
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
        super(MakeAITupleView, self).__init__(parent=par)
        self.ui = Ui_tupleview()
        self.ui.setupUi(self)
        self.init_window()

        self.config_data = {}
        self.select_config_path = ""
        self.select_data_folder = ""
        self.workdir = ""
        self.rel_work_dir = ""
        self.pre_work_dir = ""
        self.anim_name = ""
        self.figure_id = ""


    def init_window(self):
        self.ui.config_select_button.clicked.connect(self.select_config_file)
        self.ui.config_read_button.clicked.connect(self.read_config_file)
        self.ui.select_data_folder.clicked.connect(self.select_data_directory)
        self.ui.add_data_button.clicked.connect(self.exec_add_data)
        self.ui.look_tuple_button.clicked.connect(self.look_for_tuple_view)
        self.ui.put_tuple_button.clicked.connect(self.put_tuple_to_label)

        self.ui.treeWidget.clicked.connect(self.on_tree_clicked)
        self.ui.treeWidget.doubleClicked.connect(self.on_tree_double_clicked)
        self.ui.treeWidget.setColumnCount(2)
        self.ui.treeWidget.setColumnWidth(0, 160)
        self.ui.treeWidget.setHeaderLabels(["数据类型", "目录"])
        self.ui.treeWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.ui.comboBox.addItems([get_mapping_value(v) for v in self.DataItems])
        self.ui.comboBox.currentTextChanged.connect(self.on_dtype_changed)
        self.ui.comboBox_2.addItems([get_mapping_value(v) for v in self.QueryItems])
        self.ui.comboBox_2.currentTextChanged.connect(self.on_query_top_changed)
        self.ui.comboBox_2.setVisible(False)


    def on_dtype_changed(self, value):
        self.refresh_target_data_folder()

        self.ui.comboBox_2.setVisible(get_mapping_key(value) in self.QueryDataItems.keys())

    def on_query_top_changed(self, value):
        self.refresh_target_data_folder()

    def select_config_file(self):
        file_tuple = QFileDialog.getOpenFileName(self, "选择三元组数据配置文件")
        if file_tuple[0] != "":
            file_path = file_tuple[0]
            if self.read_config_data(file_path):
                return

        QMessageBox.warning(self, "", "请选择正确的三元组数据配置文件")

    def read_config_file(self):
        config_path = self.ui.config_path.text()
        if os.path.exists(config_path):
            if self.read_config_data(config_path):
                return

        QMessageBox.warning(self, "", "请选择正确的三元组数据配置文件")

    def select_data_directory(self):
        # 打开文件对话框选择目录
        directory = QFileDialog.getExistingDirectory(self, "选择数据所在目录")
        if directory:
            self.select_data_folder = directory
            self.ui.add_data_folder.setText(directory)

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
        self.workdir = f"{self.pre_work_dir}/{self.rel_work_dir}"

        self.ui.config_path.setText(config_path)
        self.ui.workspace_path.setText(self.workdir)
        self.refresh_view()

    def refresh_view(self):
        self.refresh_target_data_folder()
        self.refresh_config_list_view()

    def refresh_config_list_view(self):
        self.ui.treeWidget.clear()

        for k, v in self.config_data.items():

            node = QTreeWidgetItem(self.ui.treeWidget)
            node.setText(0, get_mapping_value(k))

            if isinstance(v, str):
                node.setText(1, v)

            if isinstance(v, dict):
                for sub_k, sub_v in v.items():
                    sub_node = QTreeWidgetItem(node)
                    sub_node.setText(0, get_mapping_value(sub_k))

                    sub_node.setText(1, sub_v)

                node.setExpanded(True)

    def refresh_target_data_folder(self):
        move_data_folder = self.get_move_target_folder()
        self.ui.data_save_folder.setText(move_data_folder)

    def look_for_tuple_view(self):

        target_folders = self.get_selected_folders()
        if target_folders:

            MessageCenter.send(MessageEnum.OpenLookTriplesView, target_folders)

    def put_tuple_to_label(self):
        target_folders = self.get_selected_folders()
        if len(target_folders) != 3:
            QMessageBox.warning(self, "三元组形成", "请选择三个目录")
            return

        current_datetime = datetime.now()
        time_name = current_datetime.strftime("%Y.%m.%d")
        folder_name = current_datetime.strftime('%Y%m%d_%H%M%S')

        combined_path = f"ai_result/{time_name}/{folder_name}"
        remote_folder = f"dataset/ai_result/{time_name}/{folder_name}"

        copy_folder_root = os.path.join(os.path.abspath("."), folder_name)
        os.makedirs(copy_folder_root)

        button = QMessageBox.information(self, "三元组形成",
                                f"将在此目录下形成三元组：{copy_folder_root}\n"
                                f"并提交到ucloud路径：{remote_folder}",
                                QMessageBox.StandardButton.Ok,
                                QMessageBox.StandardButton.Cancel)
        if button == QMessageBox.StandardButton.Cancel:
            return

        ok, err = form_triple(target_folders, copy_folder_root, remote_folder)
        if ok:
            os.startfile(copy_folder_root)
            QMessageBox.information(self, "三元组形成", "形成成功")
            MessageCenter.send(MessageEnum.OpenLabelStudio, combined_path)
        else:
            QMessageBox.warning(self, "三元组形成异常", err)

    def on_tree_clicked(self, index):
        item = self.ui.treeWidget.currentItem()


        pass

    def on_tree_double_clicked(self, index):
        item = self.ui.treeWidget.currentItem()
        item.setExpanded(not item.isExpanded())

        rel_path = item.text(1)
        if rel_path and self.workdir:
            full_path = os.path.join(self.pre_work_dir, rel_path)
            if os.path.exists(full_path):
                os.startfile(full_path)
            else:
                QMessageBox.warning(self, "", f"目录不存在")

    def get_selected_folders(self):
        items = self.ui.treeWidget.selectedItems()

        target_folders = []
        for item in items:
            if item.text(1):
                folder = os.path.join(self.pre_work_dir, item.text(1))
                target_folders.append(folder)

        for folder in target_folders:
            if not os.path.exists(folder):
                QMessageBox.warning(self, "", f"folder not exists: \n{folder}")
                return None

        if len(target_folders) > 3:
            QMessageBox.warning(self, "", "选择目录超过三个")
            return None

        return target_folders

    def get_move_target_folder(self):
        choose_dtype = get_mapping_key(self.ui.comboBox.currentText())

        if choose_dtype in self.IndentDataItems.keys():
            move_data_folder = f"{self.workdir}/{self.IndentDataItems[choose_dtype]}".format(self.figure_id, self.anim_name)
            print(move_data_folder)

            return move_data_folder

        elif choose_dtype in self.QueryDataItems.keys():
            query_top = get_mapping_key(self.ui.comboBox_2.currentText())

            move_data_folder = f"{self.pre_work_dir}/{self.rel_work_dir}/{self.QueryDataItems[choose_dtype]}".format(self.figure_id, f"[{self.anim_name}][{query_top}]")
            print(move_data_folder)

            return move_data_folder

    def exec_add_data(self):
        choose_dtype = get_mapping_key(self.ui.comboBox.currentText())
        move_data_folder = self.get_move_target_folder()

        ok, err = self.move_select_data_folder(move_data_folder)
        if not ok:
            QMessageBox.warning(self, "", f"移动到指定数据目录失败: \n{err}")
            return

        rel_target_path = move_data_folder[len(self.pre_work_dir) + 1:]

        if choose_dtype in self.IndentDataItems.keys():
            self.config_data[choose_dtype] = rel_target_path
        elif choose_dtype in self.QueryDataItems.keys():
            query_top = get_mapping_key(self.ui.comboBox_2.currentText())
            self.config_data[choose_dtype][query_top] = rel_target_path

        self.write_config_data()
        self.refresh_view()

    def move_select_data_folder(self, move_data_folder):
        if not os.path.exists(self.select_data_folder):
            return False, f"目录不存在：{self.select_data_folder}"

        try:
            if os.path.exists(move_data_folder):
                shutil.rmtree(move_data_folder)
            os.makedirs(move_data_folder, exist_ok=True)

            shutil.copytree(self.select_data_folder, move_data_folder, dirs_exist_ok=True)

            return True, None
        except Exception as e:
            print(traceback.format_exc())
            return False, str(e)

    def write_config_data(self):
        if self.select_config_path == "":
            return

        try:
            with open(self.select_config_path, "w+") as f:
                f.write(json.dumps(self.config_data, indent=2))
        except Exception as e:
            QMessageBox.warning(self, "", f"存储文件失败，请查看原因 \n{str(e)}")

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





















