# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ai_data_import.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_ai_data_import(object):
    def setupUi(self, ai_data_import):
        if not ai_data_import.objectName():
            ai_data_import.setObjectName(u"ai_data_import")
        ai_data_import.resize(716, 535)
        self.select_config_button = QPushButton(ai_data_import)
        self.select_config_button.setObjectName(u"select_config_button")
        self.select_config_button.setGeometry(QRect(220, 90, 471, 51))
        self.comboBox = QComboBox(ai_data_import)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(220, 170, 241, 31))
        self.label = QLabel(ai_data_import)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 170, 121, 31))
        self.label_2 = QLabel(ai_data_import)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(60, 220, 141, 51))
        self.select_data_folder = QPushButton(ai_data_import)
        self.select_data_folder.setObjectName(u"select_data_folder")
        self.select_data_folder.setGeometry(QRect(220, 230, 471, 51))
        self.exec_button = QPushButton(ai_data_import)
        self.exec_button.setObjectName(u"exec_button")
        self.exec_button.setGeometry(QRect(260, 400, 161, 51))
        self.label_3 = QLabel(ai_data_import)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(60, 100, 141, 31))
        self.label_4 = QLabel(ai_data_import)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(60, 300, 141, 51))
        self.target_data_folder = QLabel(ai_data_import)
        self.target_data_folder.setObjectName(u"target_data_folder")
        self.target_data_folder.setGeometry(QRect(220, 300, 471, 61))
        self.target_data_folder.setFocusPolicy(Qt.NoFocus)
        self.target_data_folder.setWordWrap(True)
        self.comboBox_2 = QComboBox(ai_data_import)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(500, 170, 161, 31))

        self.retranslateUi(ai_data_import)

        QMetaObject.connectSlotsByName(ai_data_import)
    # setupUi

    def retranslateUi(self, ai_data_import):
        ai_data_import.setWindowTitle(QCoreApplication.translate("ai_data_import", u"\u4e09\u5143\u7ec4\u6570\u636e\u5904\u7406", None))
        self.select_config_button.setText(QCoreApplication.translate("ai_data_import", u"\u9009\u62e9\u914d\u7f6e\u6587\u4ef6", None))
        self.label.setText(QCoreApplication.translate("ai_data_import", u"2\u3001\u6570\u636e\u7c7b\u578b\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("ai_data_import", u"3\u3001\u6570\u636e\u6240\u5728\u76ee\u5f55", None))
        self.select_data_folder.setText(QCoreApplication.translate("ai_data_import", u"\u9009\u62e9\u6570\u636e\u6240\u5728\u76ee\u5f55", None))
        self.exec_button.setText(QCoreApplication.translate("ai_data_import", u"4\u3001\u6dfb\u52a0\u6570\u636e\u5230\u6307\u5b9a\u8def\u5f84", None))
        self.label_3.setText(QCoreApplication.translate("ai_data_import", u"1\u3001\u9009\u62e9\u4e09\u5143\u7ec4\u914d\u7f6e\u6587\u4ef6\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("ai_data_import", u"\u6570\u636e\u5b58\u653e\u76ee\u5f55", None))
        self.target_data_folder.setText("")
    # retranslateUi

