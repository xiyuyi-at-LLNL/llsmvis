# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'comparisonYBEaXr.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import icons_rc

class Ui_ComparisonWindow(object):
    def setupUi(self, ComparisonWindow):
        if not ComparisonWindow.objectName():
            ComparisonWindow.setObjectName(u"ComparisonWindow")
        ComparisonWindow.resize(898, 820)
        ComparisonWindow.setStyleSheet(u"background-color: rgb(13, 0, 20);")
        self.centralwidget = QWidget(ComparisonWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_6 = QFrame(self.centralwidget)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 50))
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.lineEdit1 = QLineEdit(self.frame_6)
        self.lineEdit1.setObjectName(u"lineEdit1")
        self.lineEdit1.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit1)

        self.lineEdit2 = QLineEdit(self.frame_6)
        self.lineEdit2.setObjectName(u"lineEdit2")
        self.lineEdit2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit2)

        self.lineEdit3 = QLineEdit(self.frame_6)
        self.lineEdit3.setObjectName(u"lineEdit3")
        self.lineEdit3.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.lineEdit3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit3)

        self.lineEdit4 = QLineEdit(self.frame_6)
        self.lineEdit4.setObjectName(u"lineEdit4")

        self.horizontalLayout_3.addWidget(self.lineEdit4)

        self.lineEdit5 = QLineEdit(self.frame_6)
        self.lineEdit5.setObjectName(u"lineEdit5")

        self.horizontalLayout_3.addWidget(self.lineEdit5)

        self.lineEdit6 = QLineEdit(self.frame_6)
        self.lineEdit6.setObjectName(u"lineEdit6")

        self.horizontalLayout_3.addWidget(self.lineEdit6)

        self.lineEdit7 = QLineEdit(self.frame_6)
        self.lineEdit7.setObjectName(u"lineEdit7")

        self.horizontalLayout_3.addWidget(self.lineEdit7)

        self.lineEdit8 = QLineEdit(self.frame_6)
        self.lineEdit8.setObjectName(u"lineEdit8")

        self.horizontalLayout_3.addWidget(self.lineEdit8)


        self.verticalLayout.addWidget(self.frame_6)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.sample1 = QListWidget(self.frame_4)
        self.sample1.setObjectName(u"sample1")

        self.horizontalLayout_2.addWidget(self.sample1)

        self.sample2 = QListWidget(self.frame_4)
        self.sample2.setObjectName(u"sample2")

        self.horizontalLayout_2.addWidget(self.sample2)

        self.sample3 = QListWidget(self.frame_4)
        self.sample3.setObjectName(u"sample3")

        self.horizontalLayout_2.addWidget(self.sample3)

        self.sample4 = QListWidget(self.frame_4)
        self.sample4.setObjectName(u"sample4")

        self.horizontalLayout_2.addWidget(self.sample4)

        self.sample5 = QListWidget(self.frame_4)
        self.sample5.setObjectName(u"sample5")

        self.horizontalLayout_2.addWidget(self.sample5)

        self.sample6 = QListWidget(self.frame_4)
        self.sample6.setObjectName(u"sample6")

        self.horizontalLayout_2.addWidget(self.sample6)

        self.sample7 = QListWidget(self.frame_4)
        self.sample7.setObjectName(u"sample7")

        self.horizontalLayout_2.addWidget(self.sample7)

        self.sample8 = QListWidget(self.frame_4)
        self.sample8.setObjectName(u"sample8")

        self.horizontalLayout_2.addWidget(self.sample8)


        self.horizontalLayout.addWidget(self.frame_4)


        self.verticalLayout.addWidget(self.frame_2)

        self.frame_7 = QFrame(self.centralwidget)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.size_grip = QFrame(self.frame_7)
        self.size_grip.setObjectName(u"size_grip")
        self.size_grip.setGeometry(QRect(870, 0, 10, 10))
        self.size_grip.setMinimumSize(QSize(10, 10))
        self.size_grip.setMaximumSize(QSize(10, 10))
        self.size_grip.setFrameShape(QFrame.StyledPanel)
        self.size_grip.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.frame_7)

        ComparisonWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ComparisonWindow)

        QMetaObject.connectSlotsByName(ComparisonWindow)
    # setupUi

    def retranslateUi(self, ComparisonWindow):
        ComparisonWindow.setWindowTitle(QCoreApplication.translate("ComparisonWindow", u"MainWindow", None))
        self.lineEdit3.setText("")
    # retranslateUi

