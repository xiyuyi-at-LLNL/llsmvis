# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfacevAHnHB.ui'
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
        self.page.setGeometry(QRect(0, 0, 292, 425))
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
        self.page_3.setGeometry(QRect(0, 0, 292, 425))
        self.verticalLayout_6 = QVBoxLayout(self.page_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_12 = QFrame(self.page_3)
        self.frame_12.setObjectName(u"frame_12")
        sizePolicy.setHeightForWidth(self.frame_12.sizePolicy().hasHeightForWidth())
        self.frame_12.setSizePolicy(sizePolicy)
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_12)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.simp = QCheckBox(self.frame_12)
        self.simp.setObjectName(u"simp")

        self.verticalLayout_2.addWidget(self.simp)

        self.lb2sp = QCheckBox(self.frame_12)
        self.lb2sp.setObjectName(u"lb2sp")

        self.verticalLayout_2.addWidget(self.lb2sp)

        self.sp2ub = QCheckBox(self.frame_12)
        self.sp2ub.setObjectName(u"sp2ub")

        self.verticalLayout_2.addWidget(self.sp2ub)

        self.peri2sp = QCheckBox(self.frame_12)
        self.peri2sp.setObjectName(u"peri2sp")

        self.verticalLayout_2.addWidget(self.peri2sp)

        self.gif = QCheckBox(self.frame_12)
        self.gif.setObjectName(u"gif")

        self.verticalLayout_2.addWidget(self.gif)

        self.cropping = QCheckBox(self.frame_12)
        self.cropping.setObjectName(u"cropping")

        self.verticalLayout_2.addWidget(self.cropping)

        self.roughness = QCheckBox(self.frame_12)
        self.roughness.setObjectName(u"roughness")

        self.verticalLayout_2.addWidget(self.roughness)

        self.COM_traj = QCheckBox(self.frame_12)
        self.COM_traj.setObjectName(u"COM_traj")

        self.verticalLayout_2.addWidget(self.COM_traj)

        self.volume_traj = QCheckBox(self.frame_12)
        self.volume_traj.setObjectName(u"volume_traj")

        self.verticalLayout_2.addWidget(self.volume_traj)

        self.threshold = QCheckBox(self.frame_12)
        self.threshold.setObjectName(u"threshold")

        self.verticalLayout_2.addWidget(self.threshold)


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

        self.compare_btn = QPushButton(self.frame_15)
        self.compare_btn.setObjectName(u"compare_btn")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/sliders.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.compare_btn.setIcon(icon3)

        self.horizontalLayout_19.addWidget(self.compare_btn, 0, Qt.AlignBottom)


        self.verticalLayout_6.addWidget(self.frame_15, 0, Qt.AlignBottom)

        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/file-text.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolBox.addItem(self.page_3, icon4, u"Options for comparison")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 292, 425))
        self.verticalLayout_7 = QVBoxLayout(self.page_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.page_2)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_7.addWidget(self.tableWidget)

        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/info.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolBox.addItem(self.page_2, icon5, u"Info")

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
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/external-link.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.exit_button.setIcon(icon6)
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
        icon7 = QIcon()
        icon7.addFile(u":/icons/icons/align-left.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.open_close_side_bar_btn.setIcon(icon7)
        self.open_close_side_bar_btn.setIconSize(QSize(20, 20))

        self.horizontalLayout_6.addWidget(self.open_close_side_bar_btn, 0, Qt.AlignLeft)

        self.home = QPushButton(self.frame_6)
        self.home.setObjectName(u"home")
        self.home.setFont(font1)
        self.home.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon8 = QIcon()
        icon8.addFile(u":/icons/icons/home.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.home.setIcon(icon8)
        self.home.setIconSize(QSize(20, 20))

        self.horizontalLayout_6.addWidget(self.home)


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
        icon9 = QIcon()
        icon9.addFile(u":/icons/icons/chevron-down.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.raw_img_btn.setIcon(icon9)
        self.raw_img_btn.setIconSize(QSize(20, 20))

        self.horizontalLayout_11.addWidget(self.raw_img_btn)

        self.two_columns = QPushButton(self.frame_2)
        self.two_columns.setObjectName(u"two_columns")
        self.two_columns.setFont(font1)
        self.two_columns.setStyleSheet(u"color: rgb(255, 255, 255);")
        icon10 = QIcon()
        icon10.addFile(u":/icons/icons/chevrons-down.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.two_columns.setIcon(icon10)
        self.two_columns.setIconSize(QSize(20, 20))

        self.horizontalLayout_11.addWidget(self.two_columns)


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
        icon11 = QIcon()
        icon11.addFile(u":/icons/icons/arrow-down-left.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.minimize_window_button.setIcon(icon11)

        self.horizontalLayout_5.addWidget(self.minimize_window_button, 0, Qt.AlignRight|Qt.AlignTop)

        self.restore_window_button = QPushButton(self.frame)
        self.restore_window_button.setObjectName(u"restore_window_button")
        icon12 = QIcon()
        icon12.addFile(u":/icons/icons/maximize-2.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.restore_window_button.setIcon(icon12)

        self.horizontalLayout_5.addWidget(self.restore_window_button, 0, Qt.AlignRight|Qt.AlignTop)

        self.close_window_button = QPushButton(self.frame)
        self.close_window_button.setObjectName(u"close_window_button")
        icon13 = QIcon()
        icon13.addFile(u":/icons/icons/x.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.close_window_button.setIcon(icon13)

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

        self.compare_samples = QCustomSlideMenu(self.main_body_contents)
        self.compare_samples.setObjectName(u"compare_samples")
        self.compare_samples.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_17 = QHBoxLayout(self.compare_samples)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.sample1 = QListWidget(self.compare_samples)
        self.sample1.setObjectName(u"sample1")
        self.sample1.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_17.addWidget(self.sample1)

        self.sample2 = QListWidget(self.compare_samples)
        self.sample2.setObjectName(u"sample2")

        self.horizontalLayout_17.addWidget(self.sample2)


        self.horizontalLayout_13.addWidget(self.compare_samples)

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
        icon14 = QIcon()
        icon14.addFile(u":/icons/icons/help-circle.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.about_btn.setIcon(icon14)
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
        self.simp.setText(QCoreApplication.translate("MainWindow", u"simp", None))
        self.lb2sp.setText(QCoreApplication.translate("MainWindow", u"lb2sp", None))
        self.sp2ub.setText(QCoreApplication.translate("MainWindow", u"sp2ub", None))
        self.peri2sp.setText(QCoreApplication.translate("MainWindow", u"peri2sp", None))
        self.gif.setText(QCoreApplication.translate("MainWindow", u"gif", None))
        self.cropping.setText(QCoreApplication.translate("MainWindow", u"cropping", None))
        self.roughness.setText(QCoreApplication.translate("MainWindow", u"roughness", None))
        self.COM_traj.setText(QCoreApplication.translate("MainWindow", u"COM trajectory", None))
        self.volume_traj.setText(QCoreApplication.translate("MainWindow", u"Volume Center trajectory", None))
        self.threshold.setText(QCoreApplication.translate("MainWindow", u"threshold", None))
        self.same_filetype_panel_btn.setText(QCoreApplication.translate("MainWindow", u"Same filetype panel", None))
        self.compare_btn.setText(QCoreApplication.translate("MainWindow", u"Compare", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), QCoreApplication.translate("MainWindow", u"Options for comparison", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QCoreApplication.translate("MainWindow", u"Info", None))
        self.exit_button.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.open_close_side_bar_btn.setText(QCoreApplication.translate("MainWindow", u"Left Menu", None))
        self.home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.raw_img_btn.setText(QCoreApplication.translate("MainWindow", u"Raw Image", None))
        self.two_columns.setText(QCoreApplication.translate("MainWindow", u"Comparison", None))
        self.minimize_window_button.setText("")
        self.restore_window_button.setText("")
        self.close_window_button.setText("")
        self.plot_img.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Yuliang Zhang & Xiyu Yi  @ LLNL. Version 1.0", None))
        self.about_btn.setText(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

