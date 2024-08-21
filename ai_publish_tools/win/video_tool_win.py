import os
import subprocess
import sys
import natsort

from PySide6.QtCore import QDir, Qt, QSize, Slot
from PySide6.QtWidgets import *
from PySide6 import QtWidgets

from view.video_tool_ui import Ui_sub_video
from utility.commandlineutility import subprocess_may_error
from worker.ffmpeg_worker import ffmpeg_generate_avi
from worker.ffmpeg_worker import mer_videos

class VideoToolWindow(QWidget):
    def __init__(self, par):
        super(VideoToolWindow, self).__init__(parent = par)
        self.video_tool_ui = Ui_sub_video()
        self.video_tool_ui.setupUi(self)
        self.init_video_tool_window()
        self.choose_connect_buttons()
        self.current_directory = None
        self.verify_folder = ""

    def init_video_tool_window(self):
        self.video_tool_ui.run_pushButton1.clicked.connect(self.execute_ffmpeg1)
        self.video_tool_ui.run_pushButton2.clicked.connect(self.merge_videos)
        self.video_tool_ui.run_pushButton3.clicked.connect(self.diff_images)
        self.video_tool_ui.run_pushButton4.clicked.connect(self.gen_avi)

    @Slot(str)
    def set_current_directory(self, current_directory):
        self.current_directory = current_directory
        # 在此处添加任何需要的更新操作
        print(f"Current directory updated to: {self.current_directory}")

    def choose_connect_buttons(self):
        self.video_tool_ui.choose_pushButton1.clicked.connect(
            lambda: self.video_choose_folder(self.video_tool_ui.input_pic_lineEdit1,
                                             output_line_edit=self.video_tool_ui.output_video_lineEdit2,
                                             wildcard_line_edit=self.video_tool_ui.wildcard_lineEdit3))
        self.video_tool_ui.choose_pushButton2.clicked.connect(
            lambda: self.video_choose_folder(self.video_tool_ui.input_video1_lineEdit4))
        self.video_tool_ui.choose_pushButton3.clicked.connect(
            lambda: self.video_choose_folder(self.video_tool_ui.input_video2_lineEdit5,
                                             self.video_tool_ui.output_video2_lineEdit6))
        self.video_tool_ui.choose_pushButton4.clicked.connect(
            lambda: self.video_choose_folder(self.video_tool_ui.input_folder_lineEdit7))
        self.video_tool_ui.choose_pushButton5.clicked.connect(
            lambda: self.video_choose_folder(self.video_tool_ui.input_folder_lineEdit8,
                                             self.video_tool_ui.output_pic_lineEdit9))
        self.video_tool_ui.choose_pushButton6.clicked.connect(self.select_verify_root_directory)

    def select_verify_root_directory(self):
        # 打开文件对话框选择目录
        directory = QFileDialog.getExistingDirectory(self, "选择验证文件夹")
        if directory:
            if not os.path.exists(os.path.join(directory, "1.Source")) or not os.path.exists(os.path.join(directory, "5.MotionBuilderOutput")):
                QMessageBox.warning(self, "警告", "请选择正确的验证文件夹")
                return

            self.verify_folder = directory
            self.video_tool_ui.input_folder_lineEdit10.setText(directory)


    def video_choose_folder(self, line_edit, output_line_edit=None, wildcard_line_edit=None):
        start_directory = self.current_directory if self.current_directory else os.path.expanduser("~")

        # 允许选择文件或文件夹
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog(self, "选择文件或文件夹", start_directory)
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setOption(QFileDialog.ShowDirsOnly, False)
        file_dialog.setNameFilters(["All Files (*)", "Images (*.png *.jpg *.jpeg)", "Videos (*.mp4 *.avi *.mov)"])

        if file_dialog.exec_():
            selected_path = file_dialog.selectedFiles()[0]
            line_edit.setText(selected_path)

            if os.path.isfile(selected_path):
                folder = os.path.dirname(selected_path)
            else:
                folder = selected_path

            if output_line_edit:
                # 设置默认输出路径
                default_output = os.path.join(folder, "output")

                # 检查并创建输出文件夹
                if not os.path.exists(default_output):
                    os.makedirs(default_output)

                output_line_edit.setText(default_output)

            if wildcard_line_edit:
                # 生成通配符
                wildcard = self.generate_wildcard(folder)
                print(f"Generated wildcard: {wildcard}")
                if wildcard:
                    wildcard_line_edit.setText(wildcard)
                else:
                    print("No wildcard generated")

    def generate_wildcard(self, folder):
        # 获取文件夹中的所有文件
        all_files = os.listdir(folder)

        # 筛选出所有图片文件
        image_extensions = ('.png', '.jpg', '.jpeg')
        image_files = [f for f in all_files if f.lower().endswith(image_extensions)]

        if not image_files:
            print("No image files found in the folder")  # 添加这行
            return ""

        first_image = os.path.basename(image_files[0])
        print(f"First image filename: {first_image}")  # 添加这行

        # 使用正则表达式来匹配文件名模式
        import re
        match = re.match(r'(.*?)(\d+)(\.[^.]+)$', first_image)
        if match:
            prefix, number, suffix = match.groups()
            digit_count = len(number)
            wildcard = f"{prefix}%0{digit_count}d{suffix}"
            return wildcard
        else:
            print("Could not generate wildcard from filename")  # 添加这行
            return ""

    def execute_ffmpeg1(self):
        input_folder = self.video_tool_ui.input_pic_lineEdit1.text()
        wildcard = self.video_tool_ui.wildcard_lineEdit3.text()
        output_video = self.video_tool_ui.output_video_lineEdit2.text()
        if not input_folder or not wildcard or not output_video:
            QtWidgets.QMessageBox.warning(self, "错误", "请填写所有必要的信息")
            return

        # from worker.ffmpeg_worker import pic_gen_video
        # result = pic_gen_video(input_folder, wildcard, output_video)
        # if result:
        #     print(f"STDOUT:\n{result.stdout}")
        #     print(f"STDERR:\n{result.stderr}")
        #     QtWidgets.QMessageBox.information(self, "成功", "视频已成功生成")
        # else:
        #     error_message = f"生成视频时出错"
        #     print(f"Error: {error_message}")
        #     QtWidgets.QMessageBox.critical(self, "错误", error_message)

        input_pattern = os.path.join(input_folder, wildcard)

        # 构建 ffmpeg 命令
        command = [
            "ffmpeg",
            "-framerate", "30",  # 可以根据需要调整帧率
            "-i", input_pattern,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            output_video
        ]
        # cmd = f"ffmpeg -framerate 30 -i \"{input_pattern}\" -c:v libx264 -pix_fmt yuv420p \"{output_video}\""

        # 将命令转换为字符串，以便打印和调试
        command_str = " ".join(command)
        print(f"Executing command: {command_str}")

        try:
            # 执行 ffmpeg 命令
            # result = subprocess.run(command, check=True, capture_output=True, text=True)
            result = subprocess_may_error(
                command,
                error_str="error",
                log_output=True,
                encoding="utf-8",
                check=True,
                text=True
            )
            print(f"STDOUT:\n{result.stdout}")
            print(f"STDERR:\n{result.stderr}")
            QtWidgets.QMessageBox.information(self, "成功", "视频已成功生成")
        except subprocess.CalledProcessError as e:
            error_message = f"生成视频时出错:\n{e.stderr}"
            print(f"Error: {error_message}")
            QtWidgets.QMessageBox.critical(self, "错误", error_message)

    def merge_videos(self):
        input_video1 = self.video_tool_ui.input_video1_lineEdit4.text()
        input_video2 = self.video_tool_ui.input_video2_lineEdit5.text()
        output_video = self.video_tool_ui.output_video2_lineEdit6.text()

        if not input_video1 or not input_video2 or not output_video:
            QMessageBox.warning(self, "错误", "请填写所有必要的信息")
            return

        result = mer_videos(input_video1, input_video2, output_video)
        if result:
            print(f"STDOUT:\n{result.stdout}")
            print(f"STDERR:\n{result.stderr}")
            QtWidgets.QMessageBox.information(self, "成功", "视频已成功合并")
        else:
            error_message = f"合并视频时出错"
            print(f"Error: {error_message}")
            QtWidgets.QMessageBox.critical(self, "错误", error_message)
        # with open("videos_to_concat.txt", "w") as f:
        #     f.write(f"file '{input_video1}'\n")
        #     f.write(f"file '{input_video2}'\n")
        #
        # command = [
        #     "ffmpeg",
        #     "-f", "concat",
        #     "-safe", "0",
        #     "-i", "videos_to_concat.txt",
        #     "-c", "copy",
        #     output_video
        # ]
        #
        # try:
        #     # result = subprocess.run(command, check=True, capture_output=True, text=True)
        #     result = subprocess_may_error(
        #         command,
        #         error_str="error",
        #         log_output=True,
        #         encoding="utf-8",
        #         check=True,
        #         text=True
        #     )
        #     print(f"STDOUT:\n{result.stdout}")
        #     print(f"STDERR:\n{result.stderr}")
        #     QMessageBox.information(self, "成功", "视频已成功合并")
        # except subprocess.CalledProcessError as e:
        #     error_message = f"合并视频时出错:\n{e.stderr}"
        #     print(f"Error: {error_message}")
        #     QMessageBox.critical(self, "错误", error_message)
        # finally:
        #     os.remove("videos_to_concat.txt")


    def diff_images(self):
        folder1 = self.video_tool_ui.input_folder_lineEdit7.text()
        folder2 = self.video_tool_ui.input_folder_lineEdit8.text()
        output_folder = self.video_tool_ui.output_pic_lineEdit9.text()

        if not folder1 or not folder2 or not output_folder:
            QMessageBox.warning(self, "错误", "请填写所有必要的信息")
            return

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # from worker.ffmpeg_worker import diff_image
        # diff_image(folder1, folder2, output_folder)
        # if result:
        #     QMessageBox.information(self, "成功", f"图片比较完成，结果保存在 {output_folder}")


        # 获取两个文件夹中的所有图片文件
        images1 = set(f for f in os.listdir(folder1) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')))
        images2 = set(f for f in os.listdir(folder2) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')))

        # 找出两个文件夹中共有的图片
        common_images = images1.intersection(images2)

        for image_name in common_images:
            path1 = os.path.join(folder1, image_name)
            path2 = os.path.join(folder2, image_name)
            output_path = os.path.join(output_folder, f"diff_{image_name}")

            # 构建 ffmpeg 命令
            command = [
                "ffmpeg",
                "-i", path1,
                "-i", path2,
                "-filter_complex", "[0:v][1:v]blend=difference",
                "-frames:v", "1",
                output_path
            ]

            try:
                # 执行 ffmpeg 命令
                # subprocess.run(command, check=True, capture_output=True, text=True)
                subprocess_may_error(
                    command,
                    error_str="error",
                    log_output=True,
                    encoding="utf-8",
                    check=True,
                    text=True
                )
                print(f"已生成差异图像: {output_path}")
            except subprocess.CalledProcessError as e:
                print(f"处理图片 {image_name} 时出错: {e.stderr}")

        QMessageBox.information(self, "成功", f"图片比较完成，结果保存在 {output_folder}")

    def gen_avi(self):
        if not os.path.exists(os.path.join(self.verify_folder, "1.Source")) or not os.path.exists(os.path.join(self.verify_folder, "5.MotionBuilderOutput")):
            QMessageBox.warning(self, "警告", "请选择验证文件夹")
            self.select_verify_root_directory()
            return

        try:
            ffmpeg_generate_avi(self.verify_folder)
        except Exception as e:
            QMessageBox.warning(self, "", f"执行失败，请查看详情:\n{str(e)}")
