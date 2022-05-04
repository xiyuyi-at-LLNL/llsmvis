# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfacepYhPYU.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from Custom_Widgets.Widgets import QCustomSlideMenu

import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(889, 626)
        MainWindow.setStyleSheet(u"background-color: rgb(13, 0, 20);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.slide_menu_container = QFrame(self.centralwidget)
        self.slide_menu_container.setObjectName(u"slide_menu_container")
        self.slide_menu_container.setMinimumSize(QSize(0, 0))
        self.slide_menu_container.setMaximumSize(QSize(500, 16777215))
        self.slide_menu_container.setFrameShape(QFrame.StyledPanel)
        self.slide_menu_container.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.slide_menu_container)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.slide_menu_container)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(296, 0))
        self.frame_7.setMaximumSize(QSize(16777215, 16777215))
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_7)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.frame_7)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_7.setSpacing(30)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 10, 0, 10)
        self.label_2 = QLabel(self.frame_8)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.label_2.setTextFormat(Qt.AutoText)
        self.label_2.setScaledContents(False)

        self.horizontalLayout_7.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame_8)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setPixmap(QPixmap(u":/icons/icons/microscope.svg"))

        self.horizontalLayout_7.addWidget(self.label_3)


        self.verticalLayout_4.addWidget(self.frame_8, 0, Qt.AlignLeft|Qt.AlignTop)

        self.frame_9 = QFrame(self.frame_7)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy)
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.toolBox = QToolBox(self.frame_9)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setAutoFillBackground(False)
        self.toolBox.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.toolBox.setFrameShadow(QFrame.Plain)
        self.toolBox.setLineWidth(2)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setGeometry(QRect(0, 0, 335, 425))
        self.page.setStyleSheet(u"")
        self.verticalLayout_5 = QVBoxLayout(self.page)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.dir_listWidget = QListWidget(self.page)
        self.dir_listWidget.setObjectName(u"dir_listWidget")

        self.verticalLayout_5.addWidget(self.dir_listWidget)

        self.frame_11 = QFrame(self.page)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.get_dir_btn = QPushButton(self.frame_11)
        self.get_dir_btn.setObjectName(u"get_dir_btn")
        self.get_dir_btn.setStyleSheet(u"background-color: rgb(13, 0, 20);")
        icon = QIcon()
        icon.addFile(u":/icons/icons/folder-plus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.get_dir_btn.setIcon(icon)

        self.horizontalLayout_18.addWidget(self.get_dir_btn)

        self.comparison = QCheckBox(self.frame_11)
        self.comparison.setObjectName(u"comparison")

        self.horizontalLayout_18.addWidget(self.comparison)

        self.clear_btn = QPushButton(self.frame_11)
        self.clear_btn.setObjectName(u"clear_btn")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/trash-2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.clear_btn.setIcon(icon1)

        self.horizontalLayout_18.addWidget(self.clear_btn)


        self.verticalLayout_5.addWidget(self.frame_11)

        self.toolBox.addItem(self.page, icon, u"Directory list")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setGeometry(QRect(0, 0, 335, 425))
        self.verticalLayout_6 = QVBoxLayout(self.page_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_12 = QFrame(self.page_3)
        self.frame_12.setObjectName(u"frame_12")
        sizePolicy.setHeightForWidth(self.frame_12.sizePolicy().hasHeightForWidth())
        self.frame_12.setSizePolicy(sizePolicy)
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.short_file_name = QListWidget(self.frame_12)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        QListWidgetItem(self.short_file_name)
        self.short_file_name.setObjectName(u"short_file_name")
        self.short_file_name.setMinimumSize(QSize(150, 0))
        self.short_file_name.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_17.addWidget(self.short_file_name)

        self.same_type_name = QListWidget(self.frame_12)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        QListWidgetItem(self.same_type_name)
        self.same_type_name.setObjectName(u"same_type_name")

        self.horizontalLayout_17.addWidget(self.same_type_name)


        self.verticalLayout_6.addWidget(self.frame_12)

        self.frame_15 = QFrame(self.page_3)
        self.frame_15.setObjectName(u"frame_15")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_15.sizePolicy().hasHeightForWidth())
        self.frame_15.setSizePolicy(sizePolicy1)
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.same_filetype_panel_btn = QPushButton(self.frame_15)
        self.same_filetype_panel_btn.setObjectName(u"same_filetype_panel_btn")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/pause.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.same_filetype_panel_btn.setIcon(icon2)

        self.horizontalLayout_19.addWidget(self.same_filetype_panel_btn)


        self.verticalLayout_6.addWidget(self.frame_15, 0, Qt.AlignBottom)

        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/file-text.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolBox.addItem(self.page_3, icon3, u"Options for comparison")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 335, 425))
        self.verticalLayout_7 = QVBoxLayout(self.page_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.page_2)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_7.addWidget(self.tableWidget)

        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/info.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolBox.addItem(self.page_2, icon4, u"Info")

        self.horizontalLayout_10.addWidget(self.toolBox)


        self.verticalLayout_4.addWidget(self.frame_9)

        self.frame_10 = QFrame(self.frame_7)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.exit_button = QPushButton(self.frame_10)
        self.exit_button.setObjectName(u"exit_button")
        font1 = QFont()
        font1.setPointSize(10)
        self.exit_button.setFont(font1)
        self.exit_button.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/external-link.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.exit_button.setIcon(icon5)
        self.exit_button.setIconSize(QSize(32, 23))

        self.horizontalLayout_8.addWidget(self.exit_button)


        self.verticalLayout_4.addWidget(self.frame_10, 0, Qt.AlignLeft|Qt.AlignBottom)


        self.horizontalLayout_4.addWidget(self.frame_7)


        self.horizontalLayout.addWidget(self.slide_menu_container)

        self.main_body = QFrame(self.centralwidget)
        self.main_body.setObjectName(u"main_body")
        self.main_body.setMaximumSize(QSize(16777215, 16777215))
        self.main_body.setFrameShape(QFrame.StyledPanel)
        self.main_body.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.main_body)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(self.main_body)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setStyleSheet(u"background-color: rgb(13, 0, 20);")
        self.header_frame.setFrameShape(QFrame.StyledPanel)
        self.header_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.header_frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.header_frame)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.open_close_side_bar_btn = QPushButton(self.frame_6)
        self.open_close_side_bar_btn.setObjectName(u"open_close_side_bar_btn")
        self.open_close_side_bar_btn.setFont(font1)
        self.open_close_side_bar_btn.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/align-left.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.open_close_side_bar_btn.setIcon(icon6)
        self.open_close_side_bar_btn.setIconSize(QSize(20, 20))

        self.horizontalLayout_6.addWidget(self.open_close_side_bar_btn, 0, Qt.AlignLeft)

        self.home_btn = QPushButton(self.frame_6)
        self.home_btn.setObjectName(u"home_btn")
        self.home_btn.setFont(font1)
        self.home_btn.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon7 = QIcon()
        icon7.addFile(u":/icons/icons/home.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.home_btn.setIcon(icon7)
        self.home_btn.setIconSize(QSize(20, 20))

        self.horizontalLayout_6.addWidget(self.home_btn)


        self.horizontalLayout_2.addWidget(self.frame_6)

        self.frame_13 = QFrame(self.header_frame)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_2.addWidget(self.frame_13)

        self.frame_3 = QFrame(self.header_frame)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy2)
        self.frame_3.setMaximumSize(QSize(16777215, 16777215))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_2.addWidget(self.frame_3, 0, Qt.AlignHCenter)

        self.frame_2 = QFrame(self.header_frame)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 50, 0)
        self.raw_img_btn = QPushButton(self.frame_2)
        self.raw_img_btn.setObjectName(u"raw_img_btn")
        self.raw_img_btn.setFont(font1)
        self.raw_img_btn.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon8 = QIcon()
        icon8.addFile(u":/icons/icons/chevron-down.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.raw_img_btn.setIcon(icon8)
        self.raw_img_btn.setIconSize(QSize(20, 20))

        self.horizontalLayout_11.addWidget(self.raw_img_btn)

        self.multi_columns = QPushButton(self.frame_2)
        self.multi_columns.setObjectName(u"multi_columns")
        self.multi_columns.setFont(font1)
        self.multi_columns.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon9 = QIcon()
        icon9.addFile(u":/icons/icons/chevrons-down.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.multi_columns.setIcon(icon9)
        self.multi_columns.setIconSize(QSize(20, 20))

        self.horizontalLayout_11.addWidget(self.multi_columns)


        self.horizontalLayout_2.addWidget(self.frame_2)

        self.frame = QFrame(self.header_frame)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.minimize_window_button = QPushButton(self.frame)
        self.minimize_window_button.setObjectName(u"minimize_window_button")
        icon10 = QIcon()
        icon10.addFile(u":/icons/icons/arrow-down-left.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.minimize_window_button.setIcon(icon10)

        self.horizontalLayout_5.addWidget(self.minimize_window_button, 0, Qt.AlignRight|Qt.AlignTop)

        self.restore_window_button = QPushButton(self.frame)
        self.restore_window_button.setObjectName(u"restore_window_button")
        icon11 = QIcon()
        icon11.addFile(u":/icons/icons/maximize-2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.restore_window_button.setIcon(icon11)

        self.horizontalLayout_5.addWidget(self.restore_window_button, 0, Qt.AlignRight|Qt.AlignTop)

        self.close_window_button = QPushButton(self.frame)
        self.close_window_button.setObjectName(u"close_window_button")
        icon12 = QIcon()
        icon12.addFile(u":/icons/icons/x.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.close_window_button.setIcon(icon12)

        self.horizontalLayout_5.addWidget(self.close_window_button, 0, Qt.AlignRight|Qt.AlignTop)


        self.horizontalLayout_2.addWidget(self.frame, 0, Qt.AlignRight|Qt.AlignTop)


        self.verticalLayout.addWidget(self.header_frame, 0, Qt.AlignTop)

        self.main_body_contents = QFrame(self.main_body)
        self.main_body_contents.setObjectName(u"main_body_contents")
        sizePolicy.setHeightForWidth(self.main_body_contents.sizePolicy().hasHeightForWidth())
        self.main_body_contents.setSizePolicy(sizePolicy)
        self.main_body_contents.setStyleSheet(u"background-color: rgb(13, 0, 20);")
        self.main_body_contents.setFrameShape(QFrame.StyledPanel)
        self.main_body_contents.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.main_body_contents)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 10, 0, 5)
        self.sameType_widget = QCustomSlideMenu(self.main_body_contents)
        self.sameType_widget.setObjectName(u"sameType_widget")
        self.sameType_widget.setMaximumSize(QSize(100, 16777215))
        self.horizontalLayout_14 = QHBoxLayout(self.sameType_widget)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.sameType_list = QListWidget(self.sameType_widget)
        self.sameType_list.setObjectName(u"sameType_list")
        self.sameType_list.setMaximumSize(QSize(16777215, 16777215))
        self.sameType_list.setStyleSheet(u"border-color: rgb(240, 240, 240);")

        self.horizontalLayout_14.addWidget(self.sameType_list)


        self.horizontalLayout_13.addWidget(self.sameType_widget)

        self.thumbnail_widget = QWidget(self.main_body_contents)
        self.thumbnail_widget.setObjectName(u"thumbnail_widget")
        self.thumbnail_widget.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_15 = QHBoxLayout(self.thumbnail_widget)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.thumbnail = QListWidget(self.thumbnail_widget)
        self.thumbnail.setObjectName(u"thumbnail")
        self.thumbnail.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_15.addWidget(self.thumbnail)


        self.horizontalLayout_13.addWidget(self.thumbnail_widget)

        self.raw_img_widget = QCustomSlideMenu(self.main_body_contents)
        self.raw_img_widget.setObjectName(u"raw_img_widget")
        self.raw_img_widget.setMaximumSize(QSize(0, 16777215))
        self.horizontalLayout_16 = QHBoxLayout(self.raw_img_widget)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.plot_img = QLabel(self.raw_img_widget)
        self.plot_img.setObjectName(u"plot_img")

        self.horizontalLayout_16.addWidget(self.plot_img)


        self.horizontalLayout_13.addWidget(self.raw_img_widget)


        self.verticalLayout.addWidget(self.main_body_contents)

        self.footer = QFrame(self.main_body)
        self.footer.setObjectName(u"footer")
        self.footer.setFrameShape(QFrame.StyledPanel)
        self.footer.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.footer)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.footer)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"color: rgb(0, 255, 255);")

        self.verticalLayout_3.addWidget(self.label)


        self.horizontalLayout_3.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.footer)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.about_btn = QPushButton(self.frame_5)
        self.about_btn.setObjectName(u"about_btn")
        self.about_btn.setFont(font1)
        self.about_btn.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon13 = QIcon()
        icon13.addFile(u":/icons/icons/help-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.about_btn.setIcon(icon13)
        self.about_btn.setIconSize(QSize(20, 20))

        self.horizontalLayout_9.addWidget(self.about_btn)


        self.horizontalLayout_3.addWidget(self.frame_5, 0, Qt.AlignBottom)

        self.size_grip = QFrame(self.footer)
        self.size_grip.setObjectName(u"size_grip")
        self.size_grip.setMinimumSize(QSize(10, 10))
        self.size_grip.setMaximumSize(QSize(10, 10))
        self.size_grip.setFrameShape(QFrame.StyledPanel)
        self.size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_3.addWidget(self.size_grip, 0, Qt.AlignRight|Qt.AlignBottom)


        self.verticalLayout.addWidget(self.footer, 0, Qt.AlignBottom)


        self.horizontalLayout.addWidget(self.main_body)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.toolBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.label_2.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">sfsfs</span></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Hp3d Viewer", None))
        self.label_3.setText("")
        self.get_dir_btn.setText(QCoreApplication.translate("MainWindow", u"Get directory", None))
        self.comparison.setText(QCoreApplication.translate("MainWindow", u"Comparison", None))
        self.clear_btn.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QCoreApplication.translate("MainWindow", u"Directory list", None))

        __sortingEnabled = self.short_file_name.isSortingEnabled()
        self.short_file_name.setSortingEnabled(False)
        ___qlistwidgetitem = self.short_file_name.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"MC_XY", None));
        ___qlistwidgetitem1 = self.short_file_name.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"MC_XZ", None));
        ___qlistwidgetitem2 = self.short_file_name.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"MC_YZ", None));
        ___qlistwidgetitem3 = self.short_file_name.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"lb2sp_XY", None));
        ___qlistwidgetitem4 = self.short_file_name.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("MainWindow", u"lb2sp_XY_overlay", None));
        ___qlistwidgetitem5 = self.short_file_name.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("MainWindow", u"lb2sp_XZ", None));
        ___qlistwidgetitem6 = self.short_file_name.item(6)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("MainWindow", u"lb2sp_XZ_overlay", None));
        ___qlistwidgetitem7 = self.short_file_name.item(7)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("MainWindow", u"lb2sp_YZ", None));
        ___qlistwidgetitem8 = self.short_file_name.item(8)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("MainWindow", u"YZ_overlay", None));
        ___qlistwidgetitem9 = self.short_file_name.item(9)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("MainWindow", u"peri2sp_XY", None));
        ___qlistwidgetitem10 = self.short_file_name.item(10)
        ___qlistwidgetitem10.setText(QCoreApplication.translate("MainWindow", u"peri2sp_XY_overlay", None));
        ___qlistwidgetitem11 = self.short_file_name.item(11)
        ___qlistwidgetitem11.setText(QCoreApplication.translate("MainWindow", u"peri2sp_XZ", None));
        ___qlistwidgetitem12 = self.short_file_name.item(12)
        ___qlistwidgetitem12.setText(QCoreApplication.translate("MainWindow", u"peri2sp_XZ_overlay", None));
        ___qlistwidgetitem13 = self.short_file_name.item(13)
        ___qlistwidgetitem13.setText(QCoreApplication.translate("MainWindow", u"peri2sp_YZ", None));
        ___qlistwidgetitem14 = self.short_file_name.item(14)
        ___qlistwidgetitem14.setText(QCoreApplication.translate("MainWindow", u"peri2sp_YZ_overlay", None));
        ___qlistwidgetitem15 = self.short_file_name.item(15)
        ___qlistwidgetitem15.setText(QCoreApplication.translate("MainWindow", u"sp2ub_XY", None));
        ___qlistwidgetitem16 = self.short_file_name.item(16)
        ___qlistwidgetitem16.setText(QCoreApplication.translate("MainWindow", u"sp2ub_XY_overlay", None));
        ___qlistwidgetitem17 = self.short_file_name.item(17)
        ___qlistwidgetitem17.setText(QCoreApplication.translate("MainWindow", u"sp2ub_XZ", None));
        ___qlistwidgetitem18 = self.short_file_name.item(18)
        ___qlistwidgetitem18.setText(QCoreApplication.translate("MainWindow", u"sp2ub_XZ_overlay", None));
        ___qlistwidgetitem19 = self.short_file_name.item(19)
        ___qlistwidgetitem19.setText(QCoreApplication.translate("MainWindow", u"sp2ub_YZ", None));
        ___qlistwidgetitem20 = self.short_file_name.item(20)
        ___qlistwidgetitem20.setText(QCoreApplication.translate("MainWindow", u"sp2ub_YZ_overlay", None));
        ___qlistwidgetitem21 = self.short_file_name.item(21)
        ___qlistwidgetitem21.setText(QCoreApplication.translate("MainWindow", u"before_X_XY", None));
        ___qlistwidgetitem22 = self.short_file_name.item(22)
        ___qlistwidgetitem22.setText(QCoreApplication.translate("MainWindow", u"before_X_XY_overlay", None));
        ___qlistwidgetitem23 = self.short_file_name.item(23)
        ___qlistwidgetitem23.setText(QCoreApplication.translate("MainWindow", u"before_X_XZ", None));
        ___qlistwidgetitem24 = self.short_file_name.item(24)
        ___qlistwidgetitem24.setText(QCoreApplication.translate("MainWindow", u"before_X_XZ_overlay", None));
        ___qlistwidgetitem25 = self.short_file_name.item(25)
        ___qlistwidgetitem25.setText(QCoreApplication.translate("MainWindow", u"before_X_YZ", None));
        ___qlistwidgetitem26 = self.short_file_name.item(26)
        ___qlistwidgetitem26.setText(QCoreApplication.translate("MainWindow", u"before_X_YZ_overlay", None));
        ___qlistwidgetitem27 = self.short_file_name.item(27)
        ___qlistwidgetitem27.setText(QCoreApplication.translate("MainWindow", u"internal", None));
        ___qlistwidgetitem28 = self.short_file_name.item(28)
        ___qlistwidgetitem28.setText(QCoreApplication.translate("MainWindow", u"MC trajecotry", None));
        ___qlistwidgetitem29 = self.short_file_name.item(29)
        ___qlistwidgetitem29.setText(QCoreApplication.translate("MainWindow", u"Data specifics", None));
        ___qlistwidgetitem30 = self.short_file_name.item(30)
        ___qlistwidgetitem30.setText(QCoreApplication.translate("MainWindow", u"peripheral", None));
        ___qlistwidgetitem31 = self.short_file_name.item(31)
        ___qlistwidgetitem31.setText(QCoreApplication.translate("MainWindow", u"peripheral_and_internal", None));
        ___qlistwidgetitem32 = self.short_file_name.item(32)
        ___qlistwidgetitem32.setText(QCoreApplication.translate("MainWindow", u"rouphness", None));
        ___qlistwidgetitem33 = self.short_file_name.item(33)
        ___qlistwidgetitem33.setText(QCoreApplication.translate("MainWindow", u"thresholds", None));
        ___qlistwidgetitem34 = self.short_file_name.item(34)
        ___qlistwidgetitem34.setText(QCoreApplication.translate("MainWindow", u"VC trajectory", None));
        self.short_file_name.setSortingEnabled(__sortingEnabled)


        __sortingEnabled1 = self.same_type_name.isSortingEnabled()
        self.same_type_name.setSortingEnabled(False)
        ___qlistwidgetitem35 = self.same_type_name.item(0)
        ___qlistwidgetitem35.setText(QCoreApplication.translate("MainWindow", u"check_mass_center_on_smip_XY.png", None));
        ___qlistwidgetitem36 = self.same_type_name.item(1)
        ___qlistwidgetitem36.setText(QCoreApplication.translate("MainWindow", u"check_mass_center_on_smip_XZ.png", None));
        ___qlistwidgetitem37 = self.same_type_name.item(2)
        ___qlistwidgetitem37.setText(QCoreApplication.translate("MainWindow", u"check_mass_center_on_smip_YZ.png", None));
        ___qlistwidgetitem38 = self.same_type_name.item(3)
        ___qlistwidgetitem38.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_lb2sp_XY.png", None));
        ___qlistwidgetitem39 = self.same_type_name.item(4)
        ___qlistwidgetitem39.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_lb2sp_XY_overlay.png", None));
        ___qlistwidgetitem40 = self.same_type_name.item(5)
        ___qlistwidgetitem40.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_lb2sp_XZ.png", None));
        ___qlistwidgetitem41 = self.same_type_name.item(6)
        ___qlistwidgetitem41.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_lb2sp_XZ_overlay.png", None));
        ___qlistwidgetitem42 = self.same_type_name.item(7)
        ___qlistwidgetitem42.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_lb2sp_YZ.png", None));
        ___qlistwidgetitem43 = self.same_type_name.item(8)
        ___qlistwidgetitem43.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_lb2sp_YZ_overlay.png", None));
        ___qlistwidgetitem44 = self.same_type_name.item(9)
        ___qlistwidgetitem44.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_peri2sp_XY.png", None));
        ___qlistwidgetitem45 = self.same_type_name.item(10)
        ___qlistwidgetitem45.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_peri2sp_XY_overlay.png", None));
        ___qlistwidgetitem46 = self.same_type_name.item(11)
        ___qlistwidgetitem46.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_peri2sp_XZ.png", None));
        ___qlistwidgetitem47 = self.same_type_name.item(12)
        ___qlistwidgetitem47.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_peri2sp_XZ_overlay.png", None));
        ___qlistwidgetitem48 = self.same_type_name.item(13)
        ___qlistwidgetitem48.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_peri2sp_YZ.png", None));
        ___qlistwidgetitem49 = self.same_type_name.item(14)
        ___qlistwidgetitem49.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_peri2sp_YZ_overlay.png", None));
        ___qlistwidgetitem50 = self.same_type_name.item(15)
        ___qlistwidgetitem50.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_sp2ub_XY.png", None));
        ___qlistwidgetitem51 = self.same_type_name.item(16)
        ___qlistwidgetitem51.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_peri2sp_XY_overlay.png", None));
        ___qlistwidgetitem52 = self.same_type_name.item(17)
        ___qlistwidgetitem52.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_sp2ub_XZ.png", None));
        ___qlistwidgetitem53 = self.same_type_name.item(18)
        ___qlistwidgetitem53.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_sp2ub_XZ_overlay.png", None));
        ___qlistwidgetitem54 = self.same_type_name.item(19)
        ___qlistwidgetitem54.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_sp2ub_YZ.png", None));
        ___qlistwidgetitem55 = self.same_type_name.item(20)
        ___qlistwidgetitem55.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_after_cropping_sp2ub_YZ_overlay.png", None));
        ___qlistwidgetitem56 = self.same_type_name.item(21)
        ___qlistwidgetitem56.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_before_cropping_XY.png", None));
        ___qlistwidgetitem57 = self.same_type_name.item(22)
        ___qlistwidgetitem57.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_before_cropping_XY_overlay.png", None));
        ___qlistwidgetitem58 = self.same_type_name.item(23)
        ___qlistwidgetitem58.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_before_cropping_XZ.png", None));
        ___qlistwidgetitem59 = self.same_type_name.item(24)
        ___qlistwidgetitem59.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_before_cropping_XZ_overlay.png", None));
        ___qlistwidgetitem60 = self.same_type_name.item(25)
        ___qlistwidgetitem60.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_before_cropping_YZ.png", None));
        ___qlistwidgetitem61 = self.same_type_name.item(26)
        ___qlistwidgetitem61.setText(QCoreApplication.translate("MainWindow", u"inspect_rgbas_before_cropping_YZ_overlay.png", None));
        ___qlistwidgetitem62 = self.same_type_name.item(27)
        ___qlistwidgetitem62.setText(QCoreApplication.translate("MainWindow", u"internal.gif", None));
        ___qlistwidgetitem63 = self.same_type_name.item(28)
        ___qlistwidgetitem63.setText(QCoreApplication.translate("MainWindow", u"mass_center_trajecotry.png", None));
        ___qlistwidgetitem64 = self.same_type_name.item(29)
        ___qlistwidgetitem64.setText(QCoreApplication.translate("MainWindow", u"MyRep_data_specifics.png", None));
        ___qlistwidgetitem65 = self.same_type_name.item(30)
        ___qlistwidgetitem65.setText(QCoreApplication.translate("MainWindow", u"peripheral.gif", None));
        ___qlistwidgetitem66 = self.same_type_name.item(31)
        ___qlistwidgetitem66.setText(QCoreApplication.translate("MainWindow", u"peripheral_and_internal.gif", None));
        ___qlistwidgetitem67 = self.same_type_name.item(32)
        ___qlistwidgetitem67.setText(QCoreApplication.translate("MainWindow", u"rouphness.png", None));
        ___qlistwidgetitem68 = self.same_type_name.item(33)
        ___qlistwidgetitem68.setText(QCoreApplication.translate("MainWindow", u"thresholds.png", None));
        ___qlistwidgetitem69 = self.same_type_name.item(34)
        ___qlistwidgetitem69.setText(QCoreApplication.translate("MainWindow", u"volume_center_trajectory.png", None));
        self.same_type_name.setSortingEnabled(__sortingEnabled1)

        self.same_filetype_panel_btn.setText(QCoreApplication.translate("MainWindow", u"Same filetype compare", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), QCoreApplication.translate("MainWindow", u"Options for comparison", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QCoreApplication.translate("MainWindow", u"Info", None))
        self.exit_button.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.open_close_side_bar_btn.setText(QCoreApplication.translate("MainWindow", u"Left Menu", None))
        self.home_btn.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.raw_img_btn.setText(QCoreApplication.translate("MainWindow", u"Raw Image", None))
        self.multi_columns.setText(QCoreApplication.translate("MainWindow", u"Multi column", None))
        self.minimize_window_button.setText("")
        self.restore_window_button.setText("")
        self.close_window_button.setText("")
        self.plot_img.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Yuliang Zhang & Xiyu Yi  @ LLNL. Version 1.0", None))
        self.about_btn.setText(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

