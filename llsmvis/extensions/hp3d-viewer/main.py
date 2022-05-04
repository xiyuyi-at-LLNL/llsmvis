########################################################################
# HP3D Viewer DESIGN CODE
# Yuliang Zhang & Xiyu Yi @ LLNL. April 29, 2022
# Adapted from the template at github https://github.com/KhamisiKibet/QT-PyQt-PySide-Custom-Widgets
#
########################################################################

########################################################################
## IMPORTS
########################################################################
from distutils import filelist
from enum import auto
from fileinput import filename
import sys
import os
from PySide2 import *
from PyQt5.QtWidgets import QFileDialog
import glob
from PyQt5.QtCore import Qt

from Custom_Widgets.Widgets import *

from PIL import Image
import cv2

import platform

########################################################################
# IMPORT GUI FILE
from ui_interface import *
from ui_comparison import *
########################################################################


########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        loadJsonStyle(self,self.ui)

        #######################################################################
        ## # Remove window tittle bar
        ########################################################################    
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) 

        #######################################################################
        ## # Set main background to transparent
        ########################################################################  
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
      
        # #######################################################################
        # # Set window Icon
        # # This icon and title will not appear on our app main window because we removed the title bar
        # #######################################################################
        self.setWindowIcon(QtGui.QIcon(":/icons/icons/microscope.svg"))
        # # Set window tittle
        self.setWindowTitle("Hp3d Viwer")

        #################################################################################
        # Window Size grip to resize window
        #################################################################################
        QSizeGrip(self.ui.size_grip_bottom_right)
        QSizeGrip(self.ui.size_grip_top_right)
        
        #######################################################################
        #Minimize window
        self.ui.minimize_window_button.clicked.connect(lambda: self.showMinimized())
        #######################################################################
        #Close window
        self.ui.close_window_button.clicked.connect(lambda: self.close())
        self.ui.close_window_button.clicked.connect(lambda: self.popWin.close())
        self.ui.exit_button.clicked.connect(lambda: self.close())
        self.ui.exit_button.clicked.connect(lambda: self.popWin.close())
        self.ui.comparison.setChecked(False)
        # self.ui.gif.setChecked(False)

        #######################################################################
        #Restore/Maximize window
        #######################################################################
        self.ui.restore_window_button.clicked.connect(lambda: self.restore_or_maximize_window())
        self.ui.restore_window_button.clicked.connect(lambda: self.showThumbnail())

        # ###############################################
        # Function to Move window on mouse drag event on the tittle bar
        # ###############################################
        def moveWindow(e):
            # Detect if the window is  normal size
            # ###############################################  
            if self.isMaximized() == False: #Not maximized
                # Move window only when window is normal size  
                # ###############################################
                #if left mouse button is clicked (Only accept left mouse button clicks)
                if e.buttons() == Qt.LeftButton:  
                    #Move window 
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        #######################################################################

        #######################################################################
        # Add click event/Mouse move event/drag event to the top header to move the window
        #######################################################################
        self.ui.header_frame.mouseMoveEvent = moveWindow
        self.ui.top_left.mouseMoveEvent = moveWindow
        #######################################################################


        #######################################################################
        #Left Menu toggle button
        self.ui.open_close_side_bar_btn.clicked.connect(lambda: self.slideLeftMenu())
        self.ui.open_close_side_bar_btn.clicked.connect(lambda: self.showThumbnail())

        #######################################################################
        #Add folder list
        #######################################################################
        self.ui.get_dir_btn.clicked.connect(lambda: self.dirList())
        
        #######################################################################
        # Plot thumbnail
        #######################################################################
        self.ui.dir_listWidget.itemClicked.connect(lambda: self.showThumbnail())
        # self.ui.dir_listWidget.itemDoubleClicked.connect(lambda: self.multiSel())
        self.ui.comparison.clicked.connect(lambda: self.multiSel())
        self.ui.dir_listWidget.itemSelectionChanged.connect(lambda: self.showThumbnail())
        self.ui.raw_img_btn.clicked.connect(lambda: self.showThumbnail())
        
        #######################################################################
        # Open multiple column window
        #######################################################################
        self.ui.multi_columns.clicked.connect(lambda: self.multiCompare())
        #######################################################################
        #  Plot high resolution image
        #######################################################################
        self.ui.thumbnail.itemClicked.connect(lambda: self.showRawImage())
        self.ui.thumbnail.itemSelectionChanged.connect(lambda: self.showRawImage())

        #######################################################################
        # Reset multiple selection
        #######################################################################
        self.ui.clear_btn.clicked.connect(lambda: self.clear())

        #######################################################################
        # Plot sample type of file
        #######################################################################        
        self.ui.same_type_name.itemClicked.connect(lambda: self.compareTotal())


        # #######################################################################
        # # Plot raw gif
        # #######################################################################       
        self.ui.sameType_list.itemClicked.connect(lambda: self.showRawCompareData())
        self.ui.sameType_list.itemSelectionChanged.connect(lambda: self.showRawCompareData())

        self.ui.home_btn.clicked.connect(lambda: self.reset())
        self.ui.about_btn.clicked.connect(lambda: self.messgaeBox())
        self.multiCompare()

        if platform.system()=='Darwin' or platform.system()=='Linux':
            self.char='/*'
            self.char2='/'
        elif platform.system()=='Windows':
            self.char='\*'
            self.char2='\\'
        
        self.show()


    ######################################
    def multiCompare(self):
        self.popWin = QMainWindow()
        self.popupsUi = Ui_ComparisonWindow()
        self.popupsUi.setupUi(self.popWin)
        self.popWin.setWindowTitle("Comparison")

        self.vs1 = self.popupsUi.sample1.verticalScrollBar()
        self.vs2 = self.popupsUi.sample2.verticalScrollBar()
        self.vs3 = self.popupsUi.sample3.verticalScrollBar()
        self.vs4 = self.popupsUi.sample4.verticalScrollBar()
        self.vs5 = self.popupsUi.sample5.verticalScrollBar()
        self.vs6 = self.popupsUi.sample6.verticalScrollBar()
        self.vs7 = self.popupsUi.sample7.verticalScrollBar()
        self.vs8 = self.popupsUi.sample8.verticalScrollBar()
        self.vs9 = self.ui.short_file_name.verticalScrollBar()
        self.vs10 = self.ui.same_type_name.verticalScrollBar()
        
        self.vs1.valueChanged.connect(self.move_scrollbar)
        self.vs2.valueChanged.connect(self.move_scrollbar)
        self.vs3.valueChanged.connect(self.move_scrollbar)
        self.vs4.valueChanged.connect(self.move_scrollbar)
        self.vs5.valueChanged.connect(self.move_scrollbar)
        self.vs6.valueChanged.connect(self.move_scrollbar)
        self.vs7.valueChanged.connect(self.move_scrollbar)
        self.vs8.valueChanged.connect(self.move_scrollbar)
        self.vs9.valueChanged.connect(self.move_scrollbar)
        self.vs10.valueChanged.connect(self.move_scrollbar)
        
        self.popupsUi.sample1.clear()
        self.popupsUi.sample2.clear()
        self.popupsUi.sample3.clear()
        self.popupsUi.sample4.clear()
        self.popupsUi.sample5.clear()
        self.popupsUi.sample6.clear()
        self.popupsUi.sample7.clear()
        self.popupsUi.sample8.clear()

        self.popWin.show()

    ########################################################################
    # Slide left menu function
    ########################################################################
    def slideLeftMenu(self):
        # Get current left menu width
        width = self.ui.slide_menu_container.width()
    
        # If minimized
        if width == 500:
            # Restore menu
            newWidth = 0
            self.ui.open_close_side_bar_btn.setIcon(QtGui.QIcon(u":/icons/icons/align-left.svg"))
        # If maximized
        else:
            # Expand menu
            newWidth = 500
            self.ui.open_close_side_bar_btn.setIcon(QtGui.QIcon(u":/icons/icons/chevron-left.svg"))
            # print('Mouse click: Slide left')

        # Animate the transition
        self.animation = QPropertyAnimation(self.ui.slide_menu_container, b"maximumWidth")#Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)#Start value is the current menu width
        self.animation.setEndValue(newWidth)#end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
    #######################################################################

    #######################################################################
    # Add mouse events to the window
    #######################################################################
    def mousePressEvent(self, event):
        # ###############################################
        # Get the current position of the mouse
        self.clickPosition = event.globalPos()
        # We will use this value to move the window
    #######################################################################
    #######################################################################

    #######################################################################
    # Update restore button icon on msximizing or minimizing window
    #######################################################################
    def restore_or_maximize_window(self):
        # If window is maxmized
        if self.isMaximized():
            self.showNormal()
            # Change Icon
            self.ui.restore_window_button.setIcon(QtGui.QIcon(u":/icons/icons/maximize-2.svg"))
        else:
            self.showMaximized()
            # Change Icon
            self.ui.restore_window_button.setIcon(QtGui.QIcon(u":/icons/icons/minimize-2.svg"))
    
    ####################################################################
    # Update the directory list in the listWidget
    ####################################################################
    def dirList(self):
        self.ui.dir_listWidget.clear()
        global folderpath
        getImgfolder = QFileDialog.getExistingDirectory()
        os.chdir(getImgfolder)
        folderpath=os.getcwd()
        folderList=os.listdir(folderpath)
        totalNum=len(folderList)
        for i in range(totalNum):
            self.ui.dir_listWidget.addItem(folderList[i])
            

    ####################################################################
    # Show thumbnails in the listWidget
    ####################################################################
    def showThumbnail(self):
        self.ui.thumbnail.clear()
        self.ui.plot_img.clear()
        self.popupsUi.sample1.clear()
        self.popupsUi.sample2.clear()
        self.popupsUi.sample3.clear()
        self.popupsUi.sample4.clear()
        self.popupsUi.sample5.clear()
        self.popupsUi.sample6.clear()
        self.popupsUi.sample7.clear()
        self.popupsUi.sample8.clear()

        space = 10

        self.ui.thumbnail.setViewMode(QtWidgets.QListWidget.IconMode)
        self.ui.thumbnail.setIconSize(QtCore.QSize(128,128))
        self.ui.thumbnail.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.ui.thumbnail.setSpacing(space)
        self.ui.thumbnail.setStyleSheet('font-size:8px')
        # self.ui.thumbnail.setStyleSheet('color: rgb(0, 0, 0)')

        self.popupsUi.sample1.setViewMode(QtWidgets.QListWidget.IconMode)
        self.popupsUi.sample1.setIconSize(QtCore.QSize(256,256))
        self.popupsUi.sample1.setSpacing(space)
        self.popupsUi.sample1.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.popupsUi.sample1.setStyleSheet('font-size:18px')
        # self.popupsUi.sample1.setStyleSheet('color: rgb(0, 0, 0)')  


        self.popupsUi.sample2.setViewMode(QtWidgets.QListWidget.IconMode)
        self.popupsUi.sample2.setIconSize(QtCore.QSize(256,256))
        self.popupsUi.sample2.setSpacing(space)
        self.popupsUi.sample2.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.popupsUi.sample2.setStyleSheet('font-size:18px')
        # self.popupsUi.sample2.setStyleSheet('color: rgb(0, 0, 0)')

        self.popupsUi.sample3.setViewMode(QtWidgets.QListWidget.IconMode)
        self.popupsUi.sample3.setIconSize(QtCore.QSize(256,256))
        self.popupsUi.sample3.setSpacing(space)
        self.popupsUi.sample3.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.popupsUi.sample3.setStyleSheet('font-size:18px')
        # self.popupsUi.sample1.setStyleSheet('color: rgb(0, 0, 0)')  


        self.popupsUi.sample4.setViewMode(QtWidgets.QListWidget.IconMode)
        self.popupsUi.sample4.setIconSize(QtCore.QSize(256,256))
        self.popupsUi.sample4.setSpacing(space)
        self.popupsUi.sample4.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.popupsUi.sample4.setStyleSheet('font-size:18px')
        # self.popupsUi.sample2.setStyleSheet('color: rgb(0, 0, 0)')


        self.popupsUi.sample5.setViewMode(QtWidgets.QListWidget.IconMode)
        self.popupsUi.sample5.setIconSize(QtCore.QSize(256,256))
        self.popupsUi.sample5.setSpacing(space)
        self.popupsUi.sample5.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.popupsUi.sample5.setStyleSheet('font-size:18px')
        # self.popupsUi.sample1.setStyleSheet('color: rgb(0, 0, 0)')  


        self.popupsUi.sample6.setViewMode(QtWidgets.QListWidget.IconMode)
        self.popupsUi.sample6.setIconSize(QtCore.QSize(256,256))
        self.popupsUi.sample6.setSpacing(space)
        self.popupsUi.sample6.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.popupsUi.sample6.setStyleSheet('font-size:18px')
        # self.popupsUi.sample2.setStyleSheet('color: rgb(0, 0, 0)')

        self.popupsUi.sample7.setViewMode(QtWidgets.QListWidget.IconMode)
        self.popupsUi.sample7.setIconSize(QtCore.QSize(256,256))
        self.popupsUi.sample7.setSpacing(space)
        self.popupsUi.sample7.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.popupsUi.sample7.setStyleSheet('font-size:18px')
        # self.popupsUi.sample1.setStyleSheet('color: rgb(0, 0, 0)')  


        self.popupsUi.sample8.setViewMode(QtWidgets.QListWidget.IconMode)
        self.popupsUi.sample8.setIconSize(QtCore.QSize(256,256))
        self.popupsUi.sample8.setSpacing(space)
        self.popupsUi.sample8.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.popupsUi.sample8.setStyleSheet('font-size:18px')
        # self.popupsUi.sample2.setStyleSheet('color: rgb(0, 0, 0)')

        items = self.ui.dir_listWidget.selectedItems()
        folders = []
        for i in range(len(items)):
            folders.append(str(self.ui.dir_listWidget.selectedItems()[i].text()))

        if  len(folders) == 1:
            folders=self.ui.dir_listWidget.currentItem().text()
            path=os.path.join(folderpath,folders)
            #fileList=glob.glob(path+'\*')
            fileList=glob.glob(path+self.char)
            fileNameList=os.listdir(path)
            image_items = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir),fn) for fdir,fn in zip(fileList,fileNameList)]
            # for image_item in image_items:
            for image_item, i in zip(image_items, range(len(fileList))):
                fname=image_item.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item.setText(simpleName)
                    image_item.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.ui.thumbnail.addItem(image_item)
        elif len(folders) == 2:
            folder1=folders[0]
            self.popupsUi.lineEdit1.setText(folder1)
            self.popupsUi.lineEdit1.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit1.setAlignment(QtGui.Qt.AlignCenter)           
            path1=os.path.join(folderpath,folder1)
            fileList1=glob.glob(path1+self.char)
            fileNameList1=os.listdir(path1)
            folder2=folders[1]
            self.popupsUi.lineEdit2.setText(folder2)
            self.popupsUi.lineEdit2.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit2.setAlignment(QtGui.Qt.AlignCenter)
            path2=os.path.join(folderpath,folder2)
            fileList2=glob.glob(path2+self.char)

            # ##################################################################
            # # Padding method
            # desired_size = 256
            # im = cv2.imread(fileList2[0])
            # old_size = im.shape[:2] # old_size is in (height, width) format
            # ratio = float(desired_size)/max(old_size)
            # new_size = tuple([int(x*ratio) for x in old_size])

            # # new_size should be in (width, height) format
            # im = cv2.resize(im, (new_size[1], new_size[0])) 

            # delta_w = desired_size - new_size[1]
            # delta_h = desired_size - new_size[0]
            # top, bottom = delta_h//2, delta_h-(delta_h//2)
            # left, right = delta_w//2, delta_w-(delta_w//2)

            # color = [255, 255, 255]
            # new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT,value=color)
            # cv2.imshow("image", new_im)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # # print(new_im.shape[:2])
            # # im = Image.open(fileList2[0])
            # # im.thumbnail(size, Image.ANTIALIAS)
            # ###################################################################


            fileNameList2=os.listdir(path2)
            image_items1 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir1),fn1) for fdir1,fn1 in zip(fileList1,fileNameList1)]
            image_items2 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir2),fn2) for fdir2,fn2 in zip(fileList2,fileNameList2)]
            for image_item1 in image_items1:
                fname=image_item1.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item1.setText(simpleName)
                    image_item1.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item1.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample1.addItem(image_item1)
            for image_item2 in image_items2:
                fname=image_item2.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item2.text()
                    simpleName=self.changeName(fname)
                    image_item2.setText(simpleName)
                    image_item2.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item2.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample2.addItem(image_item2)
        ############################################

        elif len(folders) == 3:
            folder1=folders[0]
            self.popupsUi.lineEdit1.setText(folder1)
            self.popupsUi.lineEdit1.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit1.setAlignment(QtGui.Qt.AlignCenter)           
            path1=os.path.join(folderpath,folder1)
            fileList1=glob.glob(path1+self.char)
            fileNameList1=os.listdir(path1)
            image_items1 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir1),fn1) for fdir1,fn1 in zip(fileList1,fileNameList1)]
            folder2=folders[1]
            self.popupsUi.lineEdit2.setText(folder2)
            self.popupsUi.lineEdit2.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit2.setAlignment(QtGui.Qt.AlignCenter)
            path2=os.path.join(folderpath,folder2)
            fileList2=glob.glob(path2+self.char)
            fileNameList2=os.listdir(path2)
            image_items2 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir2),fn2) for fdir2,fn2 in zip(fileList2,fileNameList2)]

            folder3=folders[2]
            self.popupsUi.lineEdit3.setText(folder3)
            self.popupsUi.lineEdit3.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit3.setAlignment(QtGui.Qt.AlignCenter)           
            path3=os.path.join(folderpath,folder3)
            fileList3=glob.glob(path3+self.char)
            fileNameList3=os.listdir(path3)
            image_items3 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir3),fn3) for fdir3,fn3 in zip(fileList3,fileNameList3)]


            for image_item1 in image_items1:
                fname=image_item1.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item1.setText(simpleName)
                    image_item1.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item1.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample1.addItem(image_item1)
            for image_item2 in image_items2:
                fname=image_item2.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item2.text()
                    simpleName=self.changeName(fname)
                    image_item2.setText(simpleName)
                    image_item2.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item2.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample2.addItem(image_item2)
            for image_item3 in image_items3:
                fname=image_item3.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item3.setText(simpleName)
                    image_item3.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item3.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample3.addItem(image_item3)

        ############################################
        elif len(folders) == 4:
            folder1=folders[0]
            self.popupsUi.lineEdit1.setText(folder1)
            self.popupsUi.lineEdit1.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit1.setAlignment(QtGui.Qt.AlignCenter)           
            path1=os.path.join(folderpath,folder1)
            fileList1=glob.glob(path1+self.char)
            fileNameList1=os.listdir(path1)
            image_items1 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir1),fn1) for fdir1,fn1 in zip(fileList1,fileNameList1)]
            folder2=folders[1]
            self.popupsUi.lineEdit2.setText(folder2)
            self.popupsUi.lineEdit2.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit2.setAlignment(QtGui.Qt.AlignCenter)
            path2=os.path.join(folderpath,folder2)
            fileList2=glob.glob(path2+self.char)
            fileNameList2=os.listdir(path2)
            image_items2 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir2),fn2) for fdir2,fn2 in zip(fileList2,fileNameList2)]

            folder3=folders[2]
            self.popupsUi.lineEdit3.setText(folder3)
            self.popupsUi.lineEdit3.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit3.setAlignment(QtGui.Qt.AlignCenter)           
            path3=os.path.join(folderpath,folder3)
            fileList3=glob.glob(path3+self.char)
            fileNameList3=os.listdir(path3)
            image_items3 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir3),fn3) for fdir3,fn3 in zip(fileList3,fileNameList3)]
            folder4=folders[3]
            self.popupsUi.lineEdit4.setText(folder4)
            self.popupsUi.lineEdit4.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit4.setAlignment(QtGui.Qt.AlignCenter)
            path4=os.path.join(folderpath,folder4)
            fileList4=glob.glob(path4+self.char)
            fileNameList4=os.listdir(path4)
            image_items4 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir4),fn4) for fdir4,fn4 in zip(fileList4,fileNameList4)]


            for image_item1 in image_items1:
                fname=image_item1.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item1.setText(simpleName)
                    image_item1.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item1.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample1.addItem(image_item1)
            for image_item2 in image_items2:
                fname=image_item2.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item2.text()
                    simpleName=self.changeName(fname)
                    image_item2.setText(simpleName)
                    image_item2.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item2.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample2.addItem(image_item2)
            for image_item3 in image_items3:
                fname=image_item3.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item3.setText(simpleName)
                    image_item3.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item3.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample3.addItem(image_item3)
            for image_item4 in image_items4:
                fname=image_item4.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item4.text()
                    simpleName=self.changeName(fname)
                    image_item4.setText(simpleName)
                    image_item4.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item4.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample4.addItem(image_item4)

        ###########################################
        elif len(folders) == 5:
            folder1=folders[0]
            self.popupsUi.lineEdit1.setText(folder1)
            self.popupsUi.lineEdit1.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit1.setAlignment(QtGui.Qt.AlignCenter)           
            path1=os.path.join(folderpath,folder1)
            fileList1=glob.glob(path1+self.char)
            fileNameList1=os.listdir(path1)
            image_items1 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir1),fn1) for fdir1,fn1 in zip(fileList1,fileNameList1)]
            folder2=folders[1]
            self.popupsUi.lineEdit2.setText(folder2)
            self.popupsUi.lineEdit2.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit2.setAlignment(QtGui.Qt.AlignCenter)
            path2=os.path.join(folderpath,folder2)
            fileList2=glob.glob(path2+self.char)
            fileNameList2=os.listdir(path2)
            image_items2 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir2),fn2) for fdir2,fn2 in zip(fileList2,fileNameList2)]

            folder3=folders[2]
            self.popupsUi.lineEdit3.setText(folder3)
            self.popupsUi.lineEdit3.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit3.setAlignment(QtGui.Qt.AlignCenter)           
            path3=os.path.join(folderpath,folder3)
            fileList3=glob.glob(path3+self.char)
            fileNameList3=os.listdir(path3)
            image_items3 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir3),fn3) for fdir3,fn3 in zip(fileList3,fileNameList3)]
            folder4=folders[3]
            self.popupsUi.lineEdit4.setText(folder4)
            self.popupsUi.lineEdit4.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit4.setAlignment(QtGui.Qt.AlignCenter)
            path4=os.path.join(folderpath,folder4)
            fileList4=glob.glob(path4+self.char)
            fileNameList4=os.listdir(path4)
            image_items4 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir4),fn4) for fdir4,fn4 in zip(fileList4,fileNameList4)]

            folder5=folders[4]
            self.popupsUi.lineEdit5.setText(folder5)
            self.popupsUi.lineEdit5.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit5.setAlignment(QtGui.Qt.AlignCenter)           
            path5=os.path.join(folderpath,folder5)
            fileList5=glob.glob(path5+self.char)
            fileNameList5=os.listdir(path5)
            image_items5 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir5),fn5) for fdir5,fn5 in zip(fileList5,fileNameList5)]

            for image_item1 in image_items1:
                fname=image_item1.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item1.setText(simpleName)
                    image_item1.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item1.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample1.addItem(image_item1)
            for image_item2 in image_items2:
                fname=image_item2.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item2.text()
                    simpleName=self.changeName(fname)
                    image_item2.setText(simpleName)
                    image_item2.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item2.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample2.addItem(image_item2)
            for image_item3 in image_items3:
                fname=image_item3.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item3.setText(simpleName)
                    image_item3.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item3.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample3.addItem(image_item3)
            for image_item4 in image_items4:
                fname=image_item4.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item4.text()
                    simpleName=self.changeName(fname)
                    image_item4.setText(simpleName)
                    image_item4.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item4.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample4.addItem(image_item4)
            for image_item5 in image_items5:
                fname=image_item5.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item5.setText(simpleName)
                    image_item5.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item5.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample5.addItem(image_item5)

        ############################################
        elif len(folders) == 6:
            folder1=folders[0]
            self.popupsUi.lineEdit1.setText(folder1)
            self.popupsUi.lineEdit1.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit1.setAlignment(QtGui.Qt.AlignCenter)           
            path1=os.path.join(folderpath,folder1)
            fileList1=glob.glob(path1+self.char)
            fileNameList1=os.listdir(path1)
            image_items1 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir1),fn1) for fdir1,fn1 in zip(fileList1,fileNameList1)]
            folder2=folders[1]
            self.popupsUi.lineEdit2.setText(folder2)
            self.popupsUi.lineEdit2.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit2.setAlignment(QtGui.Qt.AlignCenter)
            path2=os.path.join(folderpath,folder2)
            fileList2=glob.glob(path2+self.char)
            fileNameList2=os.listdir(path2)
            image_items2 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir2),fn2) for fdir2,fn2 in zip(fileList2,fileNameList2)]

            folder3=folders[2]
            self.popupsUi.lineEdit3.setText(folder3)
            self.popupsUi.lineEdit3.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit3.setAlignment(QtGui.Qt.AlignCenter)           
            path3=os.path.join(folderpath,folder3)
            fileList3=glob.glob(path3+self.char)
            fileNameList3=os.listdir(path3)
            image_items3 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir3),fn3) for fdir3,fn3 in zip(fileList3,fileNameList3)]
            folder4=folders[3]
            self.popupsUi.lineEdit4.setText(folder4)
            self.popupsUi.lineEdit4.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit4.setAlignment(QtGui.Qt.AlignCenter)
            path4=os.path.join(folderpath,folder4)
            fileList4=glob.glob(path4+self.char)
            fileNameList4=os.listdir(path4)
            image_items4 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir4),fn4) for fdir4,fn4 in zip(fileList4,fileNameList4)]

            folder5=folders[4]
            self.popupsUi.lineEdit5.setText(folder5)
            self.popupsUi.lineEdit5.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit5.setAlignment(QtGui.Qt.AlignCenter)           
            path5=os.path.join(folderpath,folder5)
            fileList5=glob.glob(path5+self.char)
            fileNameList5=os.listdir(path5)
            image_items5 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir5),fn5) for fdir5,fn5 in zip(fileList5,fileNameList5)]
            folder6=folders[5]
            self.popupsUi.lineEdit6.setText(folder6)
            self.popupsUi.lineEdit6.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit6.setAlignment(QtGui.Qt.AlignCenter)
            path6=os.path.join(folderpath,folder6)
            fileList6=glob.glob(path6+self.char)
            fileNameList6=os.listdir(path6)
            image_items6 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir6),fn6) for fdir6,fn6 in zip(fileList6,fileNameList6)]

    
            for image_item1 in image_items1:
                fname=image_item1.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item1.setText(simpleName)
                    image_item1.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item1.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample1.addItem(image_item1)
            for image_item2 in image_items2:
                fname=image_item2.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item2.text()
                    simpleName=self.changeName(fname)
                    image_item2.setText(simpleName)
                    image_item2.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item2.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample2.addItem(image_item2)
            for image_item3 in image_items3:
                fname=image_item3.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item3.setText(simpleName)
                    image_item3.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item3.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample3.addItem(image_item3)
            for image_item4 in image_items4:
                fname=image_item4.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item4.text()
                    simpleName=self.changeName(fname)
                    image_item4.setText(simpleName)
                    image_item4.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item4.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample4.addItem(image_item4)
            for image_item5 in image_items5:
                fname=image_item5.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item5.setText(simpleName)
                    image_item5.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item5.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample5.addItem(image_item5)
            for image_item6 in image_items6:
                fname=image_item6.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item6.text()
                    simpleName=self.changeName(fname)
                    image_item6.setText(simpleName)
                    image_item6.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item6.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample6.addItem(image_item6)

        ############################################
        elif len(folders) == 7:
            folder1=folders[0]
            self.popupsUi.lineEdit1.setText(folder1)
            self.popupsUi.lineEdit1.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit1.setAlignment(QtGui.Qt.AlignCenter)           
            path1=os.path.join(folderpath,folder1)
            fileList1=glob.glob(path1+self.char)
            fileNameList1=os.listdir(path1)
            image_items1 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir1),fn1) for fdir1,fn1 in zip(fileList1,fileNameList1)]
            folder2=folders[1]
            self.popupsUi.lineEdit2.setText(folder2)
            self.popupsUi.lineEdit2.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit2.setAlignment(QtGui.Qt.AlignCenter)
            path2=os.path.join(folderpath,folder2)
            fileList2=glob.glob(path2+self.char)
            fileNameList2=os.listdir(path2)
            image_items2 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir2),fn2) for fdir2,fn2 in zip(fileList2,fileNameList2)]

            folder3=folders[2]
            self.popupsUi.lineEdit3.setText(folder3)
            self.popupsUi.lineEdit3.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit3.setAlignment(QtGui.Qt.AlignCenter)           
            path3=os.path.join(folderpath,folder3)
            fileList3=glob.glob(path3+self.char)
            fileNameList3=os.listdir(path3)
            image_items3 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir3),fn3) for fdir3,fn3 in zip(fileList3,fileNameList3)]
            folder4=folders[3]
            self.popupsUi.lineEdit4.setText(folder4)
            self.popupsUi.lineEdit4.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit4.setAlignment(QtGui.Qt.AlignCenter)
            path4=os.path.join(folderpath,folder4)
            fileList4=glob.glob(path4+self.char)
            fileNameList4=os.listdir(path4)
            image_items4 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir4),fn4) for fdir4,fn4 in zip(fileList4,fileNameList4)]

            folder5=folders[4]
            self.popupsUi.lineEdit5.setText(folder5)
            self.popupsUi.lineEdit5.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit5.setAlignment(QtGui.Qt.AlignCenter)           
            path5=os.path.join(folderpath,folder5)
            fileList5=glob.glob(path5+self.char)
            fileNameList5=os.listdir(path5)
            image_items5 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir5),fn5) for fdir5,fn5 in zip(fileList5,fileNameList5)]
            folder6=folders[5]
            self.popupsUi.lineEdit6.setText(folder6)
            self.popupsUi.lineEdit6.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit6.setAlignment(QtGui.Qt.AlignCenter)
            path6=os.path.join(folderpath,folder6)
            fileList6=glob.glob(path6+self.char)
            fileNameList6=os.listdir(path6)
            image_items6 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir6),fn6) for fdir6,fn6 in zip(fileList6,fileNameList6)]

            folder7=folders[6]
            self.popupsUi.lineEdit7.setText(folder7)
            self.popupsUi.lineEdit7.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit7.setAlignment(QtGui.Qt.AlignCenter)           
            path7=os.path.join(folderpath,folder7)
            fileList7=glob.glob(path7+self.char)
            fileNameList7=os.listdir(path7)
            image_items7 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir7),fn7) for fdir7,fn7 in zip(fileList7,fileNameList7)]

            for image_item1 in image_items1:
                fname=image_item1.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item1.setText(simpleName)
                    image_item1.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item1.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample1.addItem(image_item1)
            for image_item2 in image_items2:
                fname=image_item2.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item2.text()
                    simpleName=self.changeName(fname)
                    image_item2.setText(simpleName)
                    image_item2.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item2.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample2.addItem(image_item2)
            for image_item3 in image_items3:
                fname=image_item3.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item3.setText(simpleName)
                    image_item3.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item3.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample3.addItem(image_item3)
            for image_item4 in image_items4:
                fname=image_item4.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item4.text()
                    simpleName=self.changeName(fname)
                    image_item4.setText(simpleName)
                    image_item4.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item4.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample4.addItem(image_item4)
            for image_item5 in image_items5:
                fname=image_item5.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item5.setText(simpleName)
                    image_item5.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item5.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample5.addItem(image_item5)
            for image_item6 in image_items6:
                fname=image_item6.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item6.text()
                    simpleName=self.changeName(fname)
                    image_item6.setText(simpleName)
                    image_item6.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item6.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample6.addItem(image_item6)
            for image_item7 in image_items7:
                fname=image_item7.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item7.setText(simpleName)
                    image_item7.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item7.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample7.addItem(image_item7)

        ############################################
        elif len(folders) == 8:
            folder1=folders[0]
            self.popupsUi.lineEdit1.setText(folder1)
            self.popupsUi.lineEdit1.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit1.setAlignment(QtGui.Qt.AlignCenter)           
            path1=os.path.join(folderpath,folder1)
            fileList1=glob.glob(path1+self.char)
            fileNameList1=os.listdir(path1)
            image_items1 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir1),fn1) for fdir1,fn1 in zip(fileList1,fileNameList1)]
            folder2=folders[1]
            self.popupsUi.lineEdit2.setText(folder2)
            self.popupsUi.lineEdit2.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit2.setAlignment(QtGui.Qt.AlignCenter)
            path2=os.path.join(folderpath,folder2)
            fileList2=glob.glob(path2+self.char)
            fileNameList2=os.listdir(path2)
            image_items2 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir2),fn2) for fdir2,fn2 in zip(fileList2,fileNameList2)]

            folder3=folders[2]
            self.popupsUi.lineEdit3.setText(folder3)
            self.popupsUi.lineEdit3.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit3.setAlignment(QtGui.Qt.AlignCenter)           
            path3=os.path.join(folderpath,folder3)
            fileList3=glob.glob(path3+self.char)
            fileNameList3=os.listdir(path3)
            image_items3 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir3),fn3) for fdir3,fn3 in zip(fileList3,fileNameList3)]
            folder4=folders[3]
            self.popupsUi.lineEdit4.setText(folder4)
            self.popupsUi.lineEdit4.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit4.setAlignment(QtGui.Qt.AlignCenter)
            path4=os.path.join(folderpath,folder4)
            fileList4=glob.glob(path4+self.char)
            fileNameList4=os.listdir(path4)
            image_items4 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir4),fn4) for fdir4,fn4 in zip(fileList4,fileNameList4)]

            folder5=folders[4]
            self.popupsUi.lineEdit5.setText(folder5)
            self.popupsUi.lineEdit5.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit5.setAlignment(QtGui.Qt.AlignCenter)           
            path5=os.path.join(folderpath,folder5)
            fileList5=glob.glob(path5+self.char)
            fileNameList5=os.listdir(path5)
            image_items5 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir5),fn5) for fdir5,fn5 in zip(fileList5,fileNameList5)]
            folder6=folders[5]
            self.popupsUi.lineEdit6.setText(folder6)
            self.popupsUi.lineEdit6.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit6.setAlignment(QtGui.Qt.AlignCenter)
            path6=os.path.join(folderpath,folder6)
            fileList6=glob.glob(path6+self.char)
            fileNameList6=os.listdir(path6)
            image_items6 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir6),fn6) for fdir6,fn6 in zip(fileList6,fileNameList6)]

            folder7=folders[6]
            self.popupsUi.lineEdit7.setText(folder7)
            self.popupsUi.lineEdit7.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit7.setAlignment(QtGui.Qt.AlignCenter)           
            path7=os.path.join(folderpath,folder7)
            fileList7=glob.glob(path7+self.char)
            fileNameList7=os.listdir(path7)
            image_items7 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir7),fn7) for fdir7,fn7 in zip(fileList7,fileNameList7)]
            folder8=folders[7]
            self.popupsUi.lineEdit8.setText(folder8)
            self.popupsUi.lineEdit8.setStyleSheet('color: rgb(255, 255, 255)')
            self.popupsUi.lineEdit8.setAlignment(QtGui.Qt.AlignCenter)
            path8=os.path.join(folderpath,folder8)
            fileList8=glob.glob(path8+self.char)
            fileNameList8=os.listdir(path8)
            image_items8 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir8),fn8) for fdir8,fn8 in zip(fileList8,fileNameList8)]


            for image_item1 in image_items1:
                fname=image_item1.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item1.setText(simpleName)
                    image_item1.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item1.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample1.addItem(image_item1)
            for image_item2 in image_items2:
                fname=image_item2.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item2.text()
                    simpleName=self.changeName(fname)
                    image_item2.setText(simpleName)
                    image_item2.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item2.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample2.addItem(image_item2)
            for image_item3 in image_items3:
                fname=image_item3.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item3.setText(simpleName)
                    image_item3.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item3.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample3.addItem(image_item3)
            for image_item4 in image_items4:
                fname=image_item4.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item4.text()
                    simpleName=self.changeName(fname)
                    image_item4.setText(simpleName)
                    image_item4.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item4.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample4.addItem(image_item4)
            for image_item5 in image_items5:
                fname=image_item5.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item5.setText(simpleName)
                    image_item5.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item5.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample5.addItem(image_item5)
            for image_item6 in image_items6:
                fname=image_item6.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item6.text()
                    simpleName=self.changeName(fname)
                    image_item6.setText(simpleName)
                    image_item6.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item6.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample6.addItem(image_item6)
            for image_item7 in image_items7:
                fname=image_item7.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    simpleName=self.changeName(fname)
                    image_item7.setText(simpleName)
                    image_item7.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item7.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample7.addItem(image_item7)
            for image_item8 in image_items8:
                fname=image_item8.text()
                if fname[-3:] == 'png' or fname[-3:] == 'gif':
                    fname=image_item8.text()
                    simpleName=self.changeName(fname)
                    image_item8.setText(simpleName)
                    image_item8.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item8.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.popupsUi.sample8.addItem(image_item8)


    ####################################################################
    # Plot raw iamge data
    ####################################################################       
    def showRawImage(self):
        self.ui.plot_img.clear()
        self.ui.plot_img.setStyleSheet('background-color: rgb(240, 240, 240)') 
        samplename=self.ui.thumbnail.currentItem().text()
        filename=self.originalName(samplename)
        fext=filename[-3:]
        folder=self.ui.dir_listWidget.currentItem().text()
        path=os.path.join(folderpath,folder,filename)
        if fext == 'png':
            label_img=self.ui.plot_img.setPixmap(QtGui.QPixmap(path))
            # self.ui.plot_img.setScaledContents(True)
            self.ui.plot_img.setAlignment(QtGui.Qt.AlignCenter)
            self.ui.plot_img.show()
        elif fext == 'gif':
            movie = QtGui.QMovie(path)
            self.ui.plot_img.setMovie(movie)
            self.ui.plot_img.setAlignment(QtGui.Qt.AlignCenter)
            movie.start()
        else:
            print('Not a image')
    ####################################################################
    # Reset selection during comparison
    #################################################################### 
    def clear(self):
        for i in range(self.ui.dir_listWidget.count()):
            item = self.ui.dir_listWidget.item(i)
            self.ui.dir_listWidget.setItemSelected(item, False)
        self.ui.thumbnail.clear()
        self.ui.plot_img.clear()
        self.popupsUi.sample1.clear()
        self.popupsUi.sample2.clear()
        self.popupsUi.sample3.clear()
        self.popupsUi.sample4.clear()
        self.popupsUi.sample5.clear()
        self.popupsUi.sample6.clear()
        self.popupsUi.sample7.clear()
        self.popupsUi.sample8.clear()
        self.popupsUi.lineEdit1.clear()
        self.popupsUi.lineEdit2.clear()
        self.popupsUi.lineEdit3.clear()
        self.popupsUi.lineEdit4.clear()
        self.popupsUi.lineEdit5.clear()
        self.popupsUi.lineEdit6.clear()
        self.popupsUi.lineEdit7.clear()
        self.popupsUi.lineEdit8.clear()

    def multiSel(self):
        if self.ui.comparison.isChecked() == True:
            self.ui.dir_listWidget.setSelectionMode(QtWidgets.QListWidget.MultiSelection)
        else:
            self.ui.dir_listWidget.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
            # print(self.ui.dir_listWidget.selectedItems(0))

    def compareTotal(self):
        self.ui.sameType_list.clear()
        self.ui.thumbnail.clear()
        self.ui.sameType_list.setViewMode(QtWidgets.QListWidget.IconMode)
        self.ui.sameType_list.setIconSize(QtCore.QSize(256,256))
        self.ui.sameType_list.setSpacing(10)
        # self.ui.thumbnail.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.ui.sameType_list.setStyleSheet('font-size:18px')
        self.ui.sameType_list.setStyleSheet('color: rgb(0, 0, 0)')
        fname=self.ui.same_type_name.currentItem().text()
        # backSlash='\\'
        # truncate_fn=fname[:-3]
        # print(truncate_fn)
        folderList=os.listdir(folderpath)
        for i in range(len(folderList)):
            folders=folderList[i]
            path=os.path.join(folderpath,folders)
            # fileList=glob.glob(path+self.char+truncate_fn)# run faster
            fileList=glob.glob(path+self.char2+fname)# run faster
            # print(fileList)
            image_items = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir),folders) for fdir in fileList]# run faster
            # path=os.path.join(folderpath,folders,fname)# run slowly
            # image_items = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir),folders) for fdir in path]# run slowly
            for image_item in image_items:
                image_item.setBackground(QtGui.QColor('#C0C0C0'))
                image_item.setTextAlignment(QtGui.Qt.AlignCenter)
                self.ui.sameType_list.addItem(image_item)

    ####################################################################
    # Plot raw gif data
    ####################################################################       
    def showRawCompareData(self):
        self.ui.plot_img.setStyleSheet('background-color: rgb(240, 240, 240)')  
        self.ui.plot_img.clear()
        folder=self.ui.sameType_list.currentItem().text()
        filename=self.ui.same_type_name.currentItem().text()
        path=os.path.join(folderpath,folder,filename)
        # print(self.ui.sameType_list.selectedIndexes())
        movie = QtGui.QMovie(path)
        self.ui.plot_img.setMovie(movie)
        self.ui.plot_img.setAlignment(QtGui.Qt.AlignCenter)
        movie.start()

    ######################################################################
    # Vertical scrollbar synchronization. It will be useful for comparison
    ######################################################################
    def move_scrollbar(self, value):
        self.vs1.setValue(value)
        self.vs2.setValue(value)
        self.vs3.setValue(value)
        self.vs4.setValue(value)
        self.vs5.setValue(value)
        self.vs6.setValue(value)
        self.vs7.setValue(value)
        self.vs8.setValue(value)
        self.vs9.setValue(value)
        self.vs10.setValue(value)

    def changeName(self,fname):
        simpleName=''
        if fname=='check_mass_center_on_smip_XY.png':
            simpleName='MC_XY'
        elif fname=='check_mass_center_on_smip_XZ.png':
            simpleName='MC_XZ'
        elif fname=='check_mass_center_on_smip_YZ.png':
            simpleName='MC_YZ'
        elif fname=='inspect_rgbas_after_cropping_lb2sp_XY.png':
            simpleName='lb2sp_XY'
        elif fname=='inspect_rgbas_after_cropping_lb2sp_XY_overlay.png':
            simpleName='lb2sp_XY_overlay'
        elif fname=='inspect_rgbas_after_cropping_lb2sp_XZ.png':
            simpleName='lb2sp_XZ'
        elif fname=='inspect_rgbas_after_cropping_lb2sp_XZ_overlay.png':
            simpleName='lb2sp_XZ_overlay'
        elif fname=='inspect_rgbas_after_cropping_lb2sp_YZ.png':
            simpleName='lb2sp_YZ'
        elif fname=='inspect_rgbas_after_cropping_lb2sp_YZ_overlay.png':
            simpleName='YZ_overlay'
        elif fname=='inspect_rgbas_after_cropping_peri2sp_XY.png':
            simpleName='peri2sp_XY'
        elif fname=='inspect_rgbas_after_cropping_peri2sp_XY_overlay.png':
            simpleName='peri2sp_XY_overlay'
        elif fname=='inspect_rgbas_after_cropping_peri2sp_XZ.png':
            simpleName='peri2sp_XZ'
        elif fname=='inspect_rgbas_after_cropping_peri2sp_XZ_overlay.png':
            simpleName='peri2sp_XZ_overlay'
        elif fname=='inspect_rgbas_after_cropping_peri2sp_YZ.png':
            simpleName='peri2sp_YZ'
        elif fname=='inspect_rgbas_after_cropping_peri2sp_YZ_overlay.png':
            simpleName='peri2sp_YZ_overlay'
        elif fname=='inspect_rgbas_after_cropping_sp2ub_XY.png':
            simpleName='sp2ub_XY'
        elif fname=='inspect_rgbas_after_cropping_sp2ub_XY_overlay.png':
            simpleName='sp2ub_XY_overlay'
        if fname=='inspect_rgbas_after_cropping_sp2ub_XZ.png':
            simpleName='sp2ub_XZ'
        elif fname=='inspect_rgbas_after_cropping_sp2ub_XZ_overlay.png':
            simpleName='sp2ub_XZ_overlay'
        elif fname=='inspect_rgbas_after_cropping_sp2ub_YZ.png':
            simpleName='sp2ub_YZ'
        elif fname=='inspect_rgbas_after_cropping_sp2ub_YZ_overlay.png':
            simpleName='sp2ub_YZ_overlay'
        elif fname=='inspect_rgbas_before_cropping_XY.png':
            simpleName='before_X_XY'
        elif fname=='inspect_rgbas_before_cropping_XY_overlay.png':
            simpleName='before_X_XY_overlay'
        elif fname=='inspect_rgbas_before_cropping_XZ.png':
            simpleName='before_X_XZ'
        elif fname=='inspect_rgbas_before_cropping_XZ_overlay.png':
            simpleName='before_X_XZ_overlay'
        elif fname=='inspect_rgbas_before_cropping_YZ.png':
            simpleName='before_X_YZ'
        elif fname=='inspect_rgbas_before_cropping_YZ_overlay.png':
            simpleName='before_X_YZ_overlay'
        elif fname=='internal.gif':
            simpleName='internal'
        elif fname=='mass_center_trajecotry.png':
            simpleName='MC trajecotry'
        elif fname=='MyParser_cell3_Iter_0.parser':
            simpleName='N.A.'
        elif fname=='MyRep_data_specifics.png':
            simpleName='Data specifics'
        elif fname=='MyRep_MIP_channel0_wLabels.mp4':
            simpleName='N.A.'
        elif fname=='peripheral.gif':
            simpleName='peripheral'
        elif fname=='peripheral_and_internal.gif':
            simpleName='peripheral_and_internal'          
        elif fname=='rouphness.png':
            simpleName='rouphness'
        elif fname=='thresholds.png':
            simpleName='thresholds'
        elif fname=='volume_center_trajectory.png':
            simpleName='VC trajectory'
        return simpleName

    def originalName(self,fname):
        fullName=''
        if fname=='MC_XY':
            fullName='check_mass_center_on_smip_XY.png'
        elif fname=='MC_XZ':
            fullName='check_mass_center_on_smip_XZ.png'
        elif fname=='MC_YZ':
            fullName='check_mass_center_on_smip_YZ.png'
        elif fname=='lb2sp_XY':
            fullName='inspect_rgbas_after_cropping_lb2sp_XY.png'
        elif fname=='lb2sp_XY_overlay':
            fullName='inspect_rgbas_after_cropping_lb2sp_XY_overlay.png'
        elif fname=='lb2sp_XZ':
            fullName='inspect_rgbas_after_cropping_lb2sp_XZ.png'
        elif fname=='lb2sp_XZ_overlay':
            fullName='inspect_rgbas_after_cropping_lb2sp_XZ_overlay.png'
        elif fname=='lb2sp_YZ':
            fullName='inspect_rgbas_after_cropping_lb2sp_YZ.png'
        elif fname=='YZ_overlay':
            fullName='inspect_rgbas_after_cropping_lb2sp_YZ_overlay.png'
        elif fname=='peri2sp_XY':
            fullName='inspect_rgbas_after_cropping_peri2sp_XY.png'
        elif fname=='peri2sp_XY_overlay':
            fullName='inspect_rgbas_after_cropping_peri2sp_XY_overlay.png'
        elif fname=='peri2sp_XZ':
            fullName='inspect_rgbas_after_cropping_peri2sp_XZ.png'
        elif fname=='peri2sp_XZ_overlay':
            fullName='inspect_rgbas_after_cropping_peri2sp_XZ_overlay.png'
        elif fname=='peri2sp_YZ':
            fullName='inspect_rgbas_after_cropping_peri2sp_YZ.png'
        elif fname=='peri2sp_YZ_overlay':
            fullName='inspect_rgbas_after_cropping_peri2sp_YZ_overlay.png'
        elif fname=='sp2ub_XY':
            fullName='inspect_rgbas_after_cropping_sp2ub_XY.png'
        elif fname=='sp2ub_XY_overlay':
            fullName='inspect_rgbas_after_cropping_sp2ub_XY_overlay.png'
        if fname=='sp2ub_XZ':
            fullName='inspect_rgbas_after_cropping_sp2ub_XZ.png'
        elif fname=='sp2ub_XZ_overlay':
            fullName='inspect_rgbas_after_cropping_sp2ub_XZ_overlay.png'
        elif fname=='sp2ub_YZ':
            fullName='inspect_rgbas_after_cropping_sp2ub_YZ.png'
        elif fname=='sp2ub_YZ_overlay':
            fullName='inspect_rgbas_after_cropping_sp2ub_YZ_overlay.png'
        elif fname=='before_X_XY':
            fullName='inspect_rgbas_before_cropping_XY.png'
        elif fname=='before_X_XY_overlay':
            fullName='inspect_rgbas_before_cropping_XY_overlay.png'
        elif fname=='before_X_XZ':
            fullName='inspect_rgbas_before_cropping_XZ.png'
        elif fname=='before_X_XZ_overlay':
            fullName='inspect_rgbas_before_cropping_XZ_overlay.png'
        elif fname=='before_X_YZ':
            fullName='inspect_rgbas_before_cropping_YZ.png'
        elif fname=='before_X_YZ_overlay':
            fullName='inspect_rgbas_before_cropping_YZ_overlay.png'
        elif fname=='internal':
            fullName='internal.gif'
        elif fname=='MC trajecotry':
            fullName='mass_center_trajecotry.png'
        elif fname=='N.A.':
            fullName='MyParser_cell3_Iter_0.parser'
        elif fname=='Data specifics':
            fullName='MyRep_data_specifics.png'
        elif fname=='N.A.':
            fullName='MyRep_MIP_channel0_wLabels.mp4'
        elif fname=='peripheral':
            fullName='peripheral.gif'
        elif fname=='peripheral_and_internal':
            fullName='peripheral_and_internal.gif'          
        elif fname=='rouphness':
            fullName='rouphness.png'
        elif fname=='thresholds':
            fullName='thresholds.png'
        elif fname=='VC trajectory':
            fullName='volume_center_trajectory.png'
        return fullName

    def reset(self):

        self.ui.thumbnail.clear()
        self.ui.plot_img.clear()
        self.ui.dir_listWidget.clear()
        self.ui.sameType_list.clear()
        self.ui.dir_listWidget.clear()
        self.ui.tableWidget.clear()
        self.popupsUi.sample1.clear()
        self.popupsUi.sample2.clear()
        self.popupsUi.sample3.clear()
        self.popupsUi.sample4.clear()
        self.popupsUi.sample5.clear()
        self.popupsUi.sample6.clear()
        self.popupsUi.sample7.clear()
        self.popupsUi.sample8.clear()
        self.popupsUi.lineEdit1.clear()
        self.popupsUi.lineEdit2.clear()
        self.popupsUi.lineEdit3.clear()
        self.popupsUi.lineEdit4.clear()
        self.popupsUi.lineEdit5.clear()
        self.popupsUi.lineEdit6.clear()
        self.popupsUi.lineEdit7.clear()
        self.popupsUi.lineEdit8.clear()

    def messgaeBox(self):
        msgBox = QMessageBox()
        msgBox.setText("This app will be used to view the LLSM data.")
        msgBox.setWindowTitle("About LLSM Viwer")
        msgBox.setStyleSheet('color: rgb(0, 0, 0)') #; background-color: rgb(13, 0, 20)
        msgBox.exec_()

    
########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
########################################################################
## END===>
########################################################################  
