# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tuple_view.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_tupleview(object):
    def setupUi(self, tupleview):
        if not tupleview.objectName():
            tupleview.setObjectName(u"tupleview")
        tupleview.resize(657, 490)
        self.gridLayoutWidget = QWidget(tupleview)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 20, 621, 451))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.config_path = QLineEdit(self.gridLayoutWidget)
        self.config_path.setObjectName(u"config_path")

        self.gridLayout.addWidget(self.config_path, 0, 1, 1, 1)

        self.config_read_button = QPushButton(self.gridLayoutWidget)
        self.config_read_button.setObjectName(u"config_read_button")

        self.gridLayout.addWidget(self.config_read_button, 0, 3, 1, 1)

        self.data_save_folder = QLabel(self.gridLayoutWidget)
        self.data_save_folder.setObjectName(u"data_save_folder")

        self.gridLayout.addWidget(self.data_save_folder, 9, 1, 1, 4)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 11, 0, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 13, 0, 1, 1)

        self.workspace_path = QLabel(self.gridLayoutWidget)
        self.workspace_path.setObjectName(u"workspace_path")

        self.gridLayout.addWidget(self.workspace_path, 1, 1, 1, 3)

        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)

        self.select_data_folder = QPushButton(self.gridLayoutWidget)
        self.select_data_folder.setObjectName(u"select_data_folder")

        self.gridLayout.addWidget(self.select_data_folder, 7, 2, 1, 1)

        self.label_9 = QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 9, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)

        self.config_select_button = QPushButton(self.gridLayoutWidget)
        self.config_select_button.setObjectName(u"config_select_button")

        self.gridLayout.addWidget(self.config_select_button, 0, 2, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.add_data_folder = QLineEdit(self.gridLayoutWidget)
        self.add_data_folder.setObjectName(u"add_data_folder")

        self.gridLayout.addWidget(self.add_data_folder, 7, 1, 1, 1)

        self.put_tuple_button = QPushButton(self.gridLayoutWidget)
        self.put_tuple_button.setObjectName(u"put_tuple_button")

        self.gridLayout.addWidget(self.put_tuple_button, 13, 1, 1, 3)

        self.comboBox = QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 3, 1, 1, 1)

        self.add_data_button = QPushButton(self.gridLayoutWidget)
        self.add_data_button.setObjectName(u"add_data_button")

        self.gridLayout.addWidget(self.add_data_button, 7, 3, 1, 1)

        self.comboBox_2 = QComboBox(self.gridLayoutWidget)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.gridLayout.addWidget(self.comboBox_2, 3, 2, 1, 2)

        self.look_tuple_button = QPushButton(self.gridLayoutWidget)
        self.look_tuple_button.setObjectName(u"look_tuple_button")

        self.gridLayout.addWidget(self.look_tuple_button, 11, 3, 1, 1)

        self.treeWidget = QTreeWidget(self.gridLayoutWidget)
        self.treeWidget.setObjectName(u"treeWidget")

        self.gridLayout.addWidget(self.treeWidget, 11, 1, 1, 2)


        self.retranslateUi(tupleview)

        QMetaObject.connectSlotsByName(tupleview)
    # setupUi

    def retranslateUi(self, tupleview):
        tupleview.setWindowTitle(QCoreApplication.translate("tupleview", u"TupleView", None))
        self.label.setText(QCoreApplication.translate("tupleview", u"\u914d\u7f6e\u6587\u4ef6\uff1a", None))
        self.config_read_button.setText(QCoreApplication.translate("tupleview", u"\u8bfb\u53d6", None))
        self.data_save_folder.setText("")
        self.label_2.setText(QCoreApplication.translate("tupleview", u"\u914d\u7f6e\u5217\u8868\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("tupleview", u"\u63d0\u4ea4\u6807\u6ce8\uff1a", None))
        self.workspace_path.setText("")
        self.label_8.setText(QCoreApplication.translate("tupleview", u"\u5de5\u4f5c\u7a7a\u95f4\uff1a", None))
        self.select_data_folder.setText(QCoreApplication.translate("tupleview", u"\u9009\u62e9", None))
        self.label_9.setText(QCoreApplication.translate("tupleview", u"\u6570\u636e\u5b58\u653e\u76ee\u5f55\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("tupleview", u"\u6dfb\u52a0\u6570\u636e\u76ee\u5f55\uff1a", None))
        self.config_select_button.setText(QCoreApplication.translate("tupleview", u"\u9009\u62e9", None))
        self.label_5.setText(QCoreApplication.translate("tupleview", u"\u6dfb\u52a0\u6570\u636e\u7c7b\u578b\uff1a", None))
        self.put_tuple_button.setText(QCoreApplication.translate("tupleview", u"\u5f62\u6210\u4e09\u5143\u7ec4\u5e76\u63d0\u4ea4", None))
        self.add_data_button.setText(QCoreApplication.translate("tupleview", u"\u6dfb\u52a0", None))
        self.look_tuple_button.setText(QCoreApplication.translate("tupleview", u"\u9009\u62e9\u5e76\u67e5\u770b\u4e09\u5143\u7ec4", None))
    # retranslateUi

