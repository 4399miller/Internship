# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sub_main.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QPushButton, QScrollArea,
    QSizePolicy, QWidget)

class Ui_SubMain(object):
    def setupUi(self, SubMain):
        if not SubMain.objectName():
            SubMain.setObjectName(u"SubMain")
        SubMain.resize(800, 600)
        self.layoutWidget = QWidget(SubMain)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 791, 591))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.file_choose1 = QPushButton(self.layoutWidget)
        self.file_choose1.setObjectName(u"file_choose1")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_choose1.sizePolicy().hasHeightForWidth())
        self.file_choose1.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.file_choose1, 2, 0, 1, 1)

        self.file_delete2 = QPushButton(self.layoutWidget)
        self.file_delete2.setObjectName(u"file_delete2")

        self.gridLayout.addWidget(self.file_delete2, 3, 1, 1, 1)

        self.file_choose2 = QPushButton(self.layoutWidget)
        self.file_choose2.setObjectName(u"file_choose2")
        sizePolicy.setHeightForWidth(self.file_choose2.sizePolicy().hasHeightForWidth())
        self.file_choose2.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.file_choose2, 2, 1, 1, 1)

        self.file_choose3 = QPushButton(self.layoutWidget)
        self.file_choose3.setObjectName(u"file_choose3")
        sizePolicy.setHeightForWidth(self.file_choose3.sizePolicy().hasHeightForWidth())
        self.file_choose3.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.file_choose3, 2, 2, 1, 1)

        self.file_delete1 = QPushButton(self.layoutWidget)
        self.file_delete1.setObjectName(u"file_delete1")

        self.gridLayout.addWidget(self.file_delete1, 3, 0, 1, 1)

        self.scrollArea_2 = QScrollArea(self.layoutWidget)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 257, 467))
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout.addWidget(self.scrollArea_2, 5, 1, 1, 1)

        self.scrollArea = QScrollArea(self.layoutWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 257, 467))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 5, 0, 1, 1)

        self.add_button = QPushButton(self.layoutWidget)
        self.add_button.setObjectName(u"add_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.add_button.sizePolicy().hasHeightForWidth())
        self.add_button.setSizePolicy(sizePolicy1)
        self.add_button.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout.addWidget(self.add_button, 0, 0, 1, 1)

        self.file_delete3 = QPushButton(self.layoutWidget)
        self.file_delete3.setObjectName(u"file_delete3")

        self.gridLayout.addWidget(self.file_delete3, 3, 2, 1, 1)

        self.scrollArea_3 = QScrollArea(self.layoutWidget)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 257, 467))
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.gridLayout.addWidget(self.scrollArea_3, 5, 2, 1, 1)

        self.data_file_choose4 = QPushButton(self.layoutWidget)
        self.data_file_choose4.setObjectName(u"data_file_choose4")
        sizePolicy1.setHeightForWidth(self.data_file_choose4.sizePolicy().hasHeightForWidth())
        self.data_file_choose4.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.data_file_choose4, 0, 1, 1, 1)

        self.form_triples = QPushButton(self.layoutWidget)
        self.form_triples.setObjectName(u"form_triples")

        self.gridLayout.addWidget(self.form_triples, 6, 2, 1, 1)

        self.labelstudio_Button = QPushButton(self.layoutWidget)
        self.labelstudio_Button.setObjectName(u"labelstudio_Button")

        self.gridLayout.addWidget(self.labelstudio_Button, 6, 0, 1, 1)


        self.retranslateUi(SubMain)

        QMetaObject.connectSlotsByName(SubMain)
    # setupUi

    def retranslateUi(self, SubMain):
        SubMain.setWindowTitle(QCoreApplication.translate("SubMain", u"SubMain", None))
        self.file_choose1.setText(QCoreApplication.translate("SubMain", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.file_delete2.setText(QCoreApplication.translate("SubMain", u"\u5220\u9664\u6b64\u533a\u5757", None))
        self.file_choose2.setText(QCoreApplication.translate("SubMain", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.file_choose3.setText(QCoreApplication.translate("SubMain", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.file_delete1.setText(QCoreApplication.translate("SubMain", u"\u5220\u9664\u6b64\u533a\u5757", None))
        self.add_button.setText(QCoreApplication.translate("SubMain", u"\u6dfb\u52a0\u533a\u5757", None))
        self.file_delete3.setText(QCoreApplication.translate("SubMain", u"\u5220\u9664\u6b64\u533a\u5757", None))
        self.data_file_choose4.setText(QCoreApplication.translate("SubMain", u"\u9009\u62e9\u65e5\u671f\u6587\u4ef6\u5939", None))
        self.form_triples.setText(QCoreApplication.translate("SubMain", u"\u5f62\u6210\u4e09\u5143\u7ec4", None))
        self.labelstudio_Button.setText(QCoreApplication.translate("SubMain", u"label-studio\u542f\u52a8\u5165\u53e3", None))
    # retranslateUi

