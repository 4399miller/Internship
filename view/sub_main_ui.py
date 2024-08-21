# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sub_main_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QStatusBar,
    QWidget)

class Ui_SubMainWindow(object):
    def setupUi(self, SubMainWindow):
        if not SubMainWindow.objectName():
            SubMainWindow.setObjectName(u"SubMainWindow")
        SubMainWindow.resize(800, 600)
        self.centralwidget = QWidget(SubMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.file_choose1 = QPushButton(self.centralwidget)
        self.file_choose1.setObjectName(u"file_choose1")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_choose1.sizePolicy().hasHeightForWidth())
        self.file_choose1.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.file_choose1, 2, 0, 1, 1)

        self.file_delete2 = QPushButton(self.centralwidget)
        self.file_delete2.setObjectName(u"file_delete2")

        self.gridLayout.addWidget(self.file_delete2, 3, 1, 1, 1)

        self.file_choose2 = QPushButton(self.centralwidget)
        self.file_choose2.setObjectName(u"file_choose2")
        sizePolicy.setHeightForWidth(self.file_choose2.sizePolicy().hasHeightForWidth())
        self.file_choose2.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.file_choose2, 2, 1, 1, 1)

        self.file_choose3 = QPushButton(self.centralwidget)
        self.file_choose3.setObjectName(u"file_choose3")
        sizePolicy.setHeightForWidth(self.file_choose3.sizePolicy().hasHeightForWidth())
        self.file_choose3.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.file_choose3, 2, 2, 1, 1)

        self.file_delete1 = QPushButton(self.centralwidget)
        self.file_delete1.setObjectName(u"file_delete1")

        self.gridLayout.addWidget(self.file_delete1, 3, 0, 1, 1)

        self.scrollArea_2 = QScrollArea(self.centralwidget)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 244, 372))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout.addWidget(self.scrollArea_2, 5, 1, 1, 1)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 243, 372))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 5, 0, 1, 1)

        self.add_button = QPushButton(self.centralwidget)
        self.add_button.setObjectName(u"add_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.add_button.sizePolicy().hasHeightForWidth())
        self.add_button.setSizePolicy(sizePolicy1)
        self.add_button.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout.addWidget(self.add_button, 0, 0, 1, 1)

        self.file_delete3 = QPushButton(self.centralwidget)
        self.file_delete3.setObjectName(u"file_delete3")

        self.gridLayout.addWidget(self.file_delete3, 3, 2, 1, 1)

        self.scrollArea_3 = QScrollArea(self.centralwidget)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 243, 372))
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.gridLayout.addWidget(self.scrollArea_3, 5, 2, 1, 1)

        self.data_file_choose4 = QPushButton(self.centralwidget)
        self.data_file_choose4.setObjectName(u"data_file_choose4")
        sizePolicy1.setHeightForWidth(self.data_file_choose4.sizePolicy().hasHeightForWidth())
        self.data_file_choose4.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.data_file_choose4, 0, 1, 1, 1)

        self.form_triples = QPushButton(self.centralwidget)
        self.form_triples.setObjectName(u"form_triples")

        self.gridLayout.addWidget(self.form_triples, 6, 2, 1, 1)

        self.labelstudio_Button = QPushButton(self.centralwidget)
        self.labelstudio_Button.setObjectName(u"labelstudio_Button")

        self.gridLayout.addWidget(self.labelstudio_Button, 6, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)

        SubMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(SubMainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 37))
        SubMainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(SubMainWindow)
        self.statusbar.setObjectName(u"statusbar")
        SubMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SubMainWindow)

        QMetaObject.connectSlotsByName(SubMainWindow)
    # setupUi

    def retranslateUi(self, SubMainWindow):
        SubMainWindow.setWindowTitle(QCoreApplication.translate("SubMainWindow", u"\u4e09\u5143\u7ec4\u89c6\u56fe", None))
        self.file_choose1.setText(QCoreApplication.translate("SubMainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.file_delete2.setText(QCoreApplication.translate("SubMainWindow", u"\u5220\u9664\u6b64\u533a\u5757", None))
        self.file_choose2.setText(QCoreApplication.translate("SubMainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.file_choose3.setText(QCoreApplication.translate("SubMainWindow", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.file_delete1.setText(QCoreApplication.translate("SubMainWindow", u"\u5220\u9664\u6b64\u533a\u5757", None))
        self.add_button.setText(QCoreApplication.translate("SubMainWindow", u"\u6dfb\u52a0\u533a\u5757", None))
        self.file_delete3.setText(QCoreApplication.translate("SubMainWindow", u"\u5220\u9664\u6b64\u533a\u5757", None))
        self.data_file_choose4.setText(QCoreApplication.translate("SubMainWindow", u"\u9009\u62e9\u65e5\u671f\u6587\u4ef6\u5939", None))
        self.form_triples.setText(QCoreApplication.translate("SubMainWindow", u"\u5f62\u6210\u4e09\u5143\u7ec4", None))
        self.labelstudio_Button.setText(QCoreApplication.translate("SubMainWindow", u"label-studio\u542f\u52a8\u5165\u53e3", None))
    # retranslateUi

