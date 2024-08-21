from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton, QVBoxLayout, QWidget

class CustomDialog(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle("Custom Dialog Example")

        # 创建一个布局
        layout = QVBoxLayout()

        # 创建一个按钮，用于显示自定义弹框
        button = QPushButton("Show Dialog")
        button.clicked.connect(self.show_dialog)
        layout.addWidget(button)

        # 设置窗口的布局
        self.setLayout(layout)

    def show_dialog(self):
        # 创建一个消息框
        msg_box = QMessageBox(self)

        # 设置消息框的标题和内容
        msg_box.setWindowTitle("Custom Dialog")
        msg_box.setText("This is a custom message.")

        # 添加自定义按钮
        custom_button = msg_box.addButton("Custom Button", QMessageBox.ActionRole)
        msg_box.addButton(QMessageBox.Ok)
        msg_box.addButton(QMessageBox.Cancel)

        # 显示消息框
        msg_box.exec_()

        # 检查用户点击了哪个按钮
        if msg_box.clickedButton() == custom_button:
            print("Custom Button clicked!")
        elif msg_box.clickedButton() == msg_box.button(QMessageBox.Ok):
            print("OK clicked!")
        elif msg_box.clickedButton() == msg_box.button(QMessageBox.Cancel):
            print("Cancel clicked!")

if __name__ == "__main__":
    app = QApplication([])
    dialog = CustomDialog()
    dialog.show()
    app.exec()