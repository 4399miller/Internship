import sys
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class MessageBox(QDialog):
    def __init__(self, title, message, callbacks):
        super().__init__()

        self.setWindowTitle(title)
        layout = QVBoxLayout()

        self.message_label = QLabel(message)
        layout.addWidget(self.message_label)

        button_layout = QHBoxLayout()
        for button_text, callback in callbacks.items():
            button = QPushButton(button_text)
            button.clicked.connect(callback)
            button_layout.addWidget(button)

        layout.addLayout(button_layout)
        self.setLayout(layout)


# 示例回调函数
def on_accept():
    print("Accepted!")


def on_decline():
    print("Declined!")


def on_cancel():
    print("Cancelled!")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 定义弹窗的标题、内容和按钮及其回调
    title = "消息弹窗"
    message = "这是一个消息弹窗。"
    callbacks = {
        "接受": on_accept,
        "拒绝": on_decline,
        "取消": on_cancel
    }
    message_box = MessageBox(title, message, callbacks)
    message_box.exec()
