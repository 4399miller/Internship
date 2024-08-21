# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'video_tool_ui_new.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_sub_video(object):
    def setupUi(self, sub_video):
        if not sub_video.objectName():
            sub_video.setObjectName(u"sub_video")
        sub_video.resize(1059, 613)
        self.gridLayout_5 = QGridLayout(sub_video)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.outputvideo_groupBox1 = QGroupBox(sub_video)
        self.outputvideo_groupBox1.setObjectName(u"outputvideo_groupBox1")
        self.gridLayout = QGridLayout(self.outputvideo_groupBox1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.input_pic_lineEdit1 = QLineEdit(self.outputvideo_groupBox1)
        self.input_pic_lineEdit1.setObjectName(u"input_pic_lineEdit1")

        self.gridLayout.addWidget(self.input_pic_lineEdit1, 0, 0, 1, 1)

        self.wildcard_lineEdit3 = QLineEdit(self.outputvideo_groupBox1)
        self.wildcard_lineEdit3.setObjectName(u"wildcard_lineEdit3")

        self.gridLayout.addWidget(self.wildcard_lineEdit3, 0, 1, 1, 1)

        self.choose_pushButton1 = QPushButton(self.outputvideo_groupBox1)
        self.choose_pushButton1.setObjectName(u"choose_pushButton1")

        self.gridLayout.addWidget(self.choose_pushButton1, 0, 2, 1, 1)

        self.run_pushButton1 = QPushButton(self.outputvideo_groupBox1)
        self.run_pushButton1.setObjectName(u"run_pushButton1")

        self.gridLayout.addWidget(self.run_pushButton1, 1, 2, 1, 1)

        self.output_video_lineEdit2 = QLineEdit(self.outputvideo_groupBox1)
        self.output_video_lineEdit2.setObjectName(u"output_video_lineEdit2")

        self.gridLayout.addWidget(self.output_video_lineEdit2, 1, 0, 1, 2)


        self.gridLayout_5.addWidget(self.outputvideo_groupBox1, 0, 0, 1, 1)

        self.mergevideo_groupBox2 = QGroupBox(sub_video)
        self.mergevideo_groupBox2.setObjectName(u"mergevideo_groupBox2")
        self.gridLayout_2 = QGridLayout(self.mergevideo_groupBox2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.output_video2_lineEdit6 = QLineEdit(self.mergevideo_groupBox2)
        self.output_video2_lineEdit6.setObjectName(u"output_video2_lineEdit6")

        self.gridLayout_2.addWidget(self.output_video2_lineEdit6, 2, 0, 1, 1)

        self.input_video2_lineEdit5 = QLineEdit(self.mergevideo_groupBox2)
        self.input_video2_lineEdit5.setObjectName(u"input_video2_lineEdit5")

        self.gridLayout_2.addWidget(self.input_video2_lineEdit5, 1, 0, 1, 1)

        self.input_video1_lineEdit4 = QLineEdit(self.mergevideo_groupBox2)
        self.input_video1_lineEdit4.setObjectName(u"input_video1_lineEdit4")

        self.gridLayout_2.addWidget(self.input_video1_lineEdit4, 0, 0, 1, 1)

        self.run_pushButton2 = QPushButton(self.mergevideo_groupBox2)
        self.run_pushButton2.setObjectName(u"run_pushButton2")

        self.gridLayout_2.addWidget(self.run_pushButton2, 2, 5, 1, 1)

        self.choose_pushButton2 = QPushButton(self.mergevideo_groupBox2)
        self.choose_pushButton2.setObjectName(u"choose_pushButton2")

        self.gridLayout_2.addWidget(self.choose_pushButton2, 0, 5, 1, 1)

        self.choose_pushButton3 = QPushButton(self.mergevideo_groupBox2)
        self.choose_pushButton3.setObjectName(u"choose_pushButton3")

        self.gridLayout_2.addWidget(self.choose_pushButton3, 1, 5, 1, 1)


        self.gridLayout_5.addWidget(self.mergevideo_groupBox2, 1, 0, 1, 1)

        self.diffpict_groupBox3 = QGroupBox(sub_video)
        self.diffpict_groupBox3.setObjectName(u"diffpict_groupBox3")
        self.gridLayout_3 = QGridLayout(self.diffpict_groupBox3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.input_folder_lineEdit8 = QLineEdit(self.diffpict_groupBox3)
        self.input_folder_lineEdit8.setObjectName(u"input_folder_lineEdit8")

        self.gridLayout_3.addWidget(self.input_folder_lineEdit8, 1, 0, 1, 1)

        self.output_pic_lineEdit9 = QLineEdit(self.diffpict_groupBox3)
        self.output_pic_lineEdit9.setObjectName(u"output_pic_lineEdit9")

        self.gridLayout_3.addWidget(self.output_pic_lineEdit9, 2, 0, 1, 1)

        self.run_pushButton3 = QPushButton(self.diffpict_groupBox3)
        self.run_pushButton3.setObjectName(u"run_pushButton3")

        self.gridLayout_3.addWidget(self.run_pushButton3, 2, 1, 1, 1)

        self.choose_pushButton4 = QPushButton(self.diffpict_groupBox3)
        self.choose_pushButton4.setObjectName(u"choose_pushButton4")

        self.gridLayout_3.addWidget(self.choose_pushButton4, 0, 1, 1, 1)

        self.choose_pushButton5 = QPushButton(self.diffpict_groupBox3)
        self.choose_pushButton5.setObjectName(u"choose_pushButton5")

        self.gridLayout_3.addWidget(self.choose_pushButton5, 1, 1, 1, 1)

        self.input_folder_lineEdit7 = QLineEdit(self.diffpict_groupBox3)
        self.input_folder_lineEdit7.setObjectName(u"input_folder_lineEdit7")

        self.gridLayout_3.addWidget(self.input_folder_lineEdit7, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.diffpict_groupBox3, 2, 0, 1, 1)

        self.avi_groupBox4 = QGroupBox(sub_video)
        self.avi_groupBox4.setObjectName(u"avi_groupBox4")
        self.gridLayout_4 = QGridLayout(self.avi_groupBox4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.run_pushButton4 = QPushButton(self.avi_groupBox4)
        self.run_pushButton4.setObjectName(u"run_pushButton4")

        self.gridLayout_4.addWidget(self.run_pushButton4, 0, 2, 1, 1)

        self.input_folder_lineEdit10 = QLineEdit(self.avi_groupBox4)
        self.input_folder_lineEdit10.setObjectName(u"input_folder_lineEdit10")

        self.gridLayout_4.addWidget(self.input_folder_lineEdit10, 0, 0, 1, 1)

        self.choose_pushButton6 = QPushButton(self.avi_groupBox4)
        self.choose_pushButton6.setObjectName(u"choose_pushButton6")

        self.gridLayout_4.addWidget(self.choose_pushButton6, 0, 1, 1, 1)


        self.gridLayout_5.addWidget(self.avi_groupBox4, 3, 0, 1, 1)


        self.retranslateUi(sub_video)

        QMetaObject.connectSlotsByName(sub_video)
    # setupUi

    def retranslateUi(self, sub_video):
        sub_video.setWindowTitle(QCoreApplication.translate("sub_video", u"Form", None))
        self.outputvideo_groupBox1.setTitle(QCoreApplication.translate("sub_video", u"1.\u8f93\u51fa\u89c6\u9891", None))
        self.input_pic_lineEdit1.setPlaceholderText(QCoreApplication.translate("sub_video", u"\u8f93\u5165\u56fe\u7247\u7684\u4f4d\u7f6e", None))
        self.wildcard_lineEdit3.setText("")
        self.wildcard_lineEdit3.setPlaceholderText(QCoreApplication.translate("sub_video", u"\u901a\u914d\u7b26\uff0c\u4f8b\u5982scene0001.png\uff0c\u5219\u8f93\u5165scene%04d.png", None))
        self.choose_pushButton1.setText(QCoreApplication.translate("sub_video", u"\u9009\u62e9", None))
        self.run_pushButton1.setText(QCoreApplication.translate("sub_video", u"\u6267\u884c", None))
        self.output_video_lineEdit2.setPlaceholderText(QCoreApplication.translate("sub_video", u"\u8f93\u51fa\u89c6\u9891\u7684\u4f4d\u7f6e\uff0c\u624b\u52a8\u586b\u5199\u4f4d\u7f6e", None))
        self.mergevideo_groupBox2.setTitle(QCoreApplication.translate("sub_video", u"2.\u5408\u5e76\u89c6\u9891", None))
        self.output_video2_lineEdit6.setPlaceholderText(QCoreApplication.translate("sub_video", u"\u8f93\u51fa\u89c6\u9891\u7684\u4f4d\u7f6e\uff0c\u683c\u5f0f\u540c\u4e0a\uff0c\u624b\u52a8\u586b\u5199\u4f4d\u7f6e", None))
        self.input_video2_lineEdit5.setPlaceholderText(QCoreApplication.translate("sub_video", u"\u8f93\u5165\u7b2c\u4e8c\u4e2a\u89c6\u9891\u7684\u4f4d\u7f6e,\u683c\u5f0f\u540c\u4e0a", None))
        self.input_video1_lineEdit4.setPlaceholderText(QCoreApplication.translate("sub_video", u"\u8f93\u5165\u7b2c\u4e00\u4e2a\u89c6\u9891\u7684\u4f4d\u7f6e,\u5e76\u5728\u672b\u5c3e\u6dfb\u52a0\u89c6\u9891\u540d\u79f0\u3002\u4f8b\u5982\uff1a/Users/test.mp4", None))
        self.run_pushButton2.setText(QCoreApplication.translate("sub_video", u"\u6267\u884c", None))
        self.choose_pushButton2.setText(QCoreApplication.translate("sub_video", u"\u9009\u62e9", None))
        self.choose_pushButton3.setText(QCoreApplication.translate("sub_video", u"\u9009\u62e9", None))
        self.diffpict_groupBox3.setTitle(QCoreApplication.translate("sub_video", u"3.diff\u4e24\u4e2a\u6587\u4ef6\u5939\u5185\u7684\u56fe\u7247", None))
        self.input_folder_lineEdit8.setPlaceholderText(QCoreApplication.translate("sub_video", u"\u8f93\u5165\u7b2c\u4e8c\u4e2a\u6587\u4ef6\u5939\u7684\u4f4d\u7f6e", None))
        self.output_pic_lineEdit9.setPlaceholderText(QCoreApplication.translate("sub_video", u"\u8f93\u51fa\u56fe\u50cf\u4f4d\u7f6e\uff0c\u624b\u52a8\u586b\u5199\u4f4d\u7f6e", None))
        self.run_pushButton3.setText(QCoreApplication.translate("sub_video", u"\u6267\u884c", None))
        self.choose_pushButton4.setText(QCoreApplication.translate("sub_video", u"\u9009\u62e9", None))
        self.choose_pushButton5.setText(QCoreApplication.translate("sub_video", u"\u9009\u62e9", None))
        self.input_folder_lineEdit7.setPlaceholderText(QCoreApplication.translate("sub_video", u"\u8f93\u5165\u7b2c\u4e00\u4e2a\u6587\u4ef6\u5939\u7684\u4f4d\u7f6e", None))
        self.avi_groupBox4.setTitle(QCoreApplication.translate("sub_video", u"4.\u9a8c\u8bc1\u6d41\u7a0b\uff0c\u8bf7\u9009\u62e9\u6587\u4ef6\u5939(\u5982\uff1a//ai_center/Retarget/Samples/20240625/)", None))
        self.run_pushButton4.setText(QCoreApplication.translate("sub_video", u"\u6267\u884c", None))
        self.input_folder_lineEdit10.setPlaceholderText(QCoreApplication.translate("sub_video", u"\u8f93\u5165\u56fe\u7247\u6587\u4ef6\u5939\u4f4d\u7f6e", None))
        self.choose_pushButton6.setText(QCoreApplication.translate("sub_video", u"\u9009\u62e9", None))
    # retranslateUi

