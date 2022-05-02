########################################################################
# LLSM Viewer DESIGN CODE
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

########################################################################
# IMPORT GUI FILE
from ui_interface import *
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
        self.setWindowTitle("LLSM Viwer")

        #################################################################################
        # Window Size grip to resize window
        #################################################################################
        QSizeGrip(self.ui.size_grip)
        
        #######################################################################
        #Minimize window
        self.ui.minimize_window_button.clicked.connect(lambda: self.showMinimized())
        #######################################################################
        #Close window
        self.ui.close_window_button.clicked.connect(lambda: self.close())
        self.ui.exit_button.clicked.connect(lambda: self.close())
        self.ui.comparison.setChecked(False)
        self.ui.gif.setChecked(False)

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
        self.ui.dir_listWidget.itemDoubleClicked.connect(lambda: self.multiSel())
        self.ui.dir_listWidget.itemSelectionChanged.connect(lambda: self.showThumbnail())
        self.ui.raw_img_btn.clicked.connect(lambda: self.showThumbnail())
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
        self.ui.compare_btn.clicked.connect(lambda: self.gifTotal())
        #######################################################################
        # Plot raw gif
        #######################################################################       
        self.ui.sameType_list.itemClicked.connect(lambda: self.showRawGif())
        self.ui.sameType_list.itemSelectionChanged.connect(lambda: self.showRawGif())

        self.ui.about_btn.clicked.connect(lambda: self.messgaeBox())
        

        self.vs1 = self.ui.sample1.verticalScrollBar()
        self.vs2 = self.ui.sample2.verticalScrollBar()

        self.vs1.valueChanged.connect(self.move_scrollbar)
        self.vs2.valueChanged.connect(self.move_scrollbar)


        self.show()




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
        self.ui.sample1.clear()
        self.ui.sample2.clear()
        self.ui.plot_img.clear()
        self.ui.thumbnail.setViewMode(QtWidgets.QListWidget.IconMode)
        self.ui.thumbnail.setIconSize(QtCore.QSize(1024,256))
        self.ui.thumbnail.setResizeMode(QtWidgets.QListWidget.Adjust)
 
        self.ui.thumbnail.setSpacing(2)
        self.ui.thumbnail.setStyleSheet('font-size:8px')
        self.ui.thumbnail.setStyleSheet('color: rgb(0, 0, 0)')

        self.ui.sample1.setViewMode(QtWidgets.QListWidget.IconMode)
        self.ui.sample1.setIconSize(QtCore.QSize(1024,256))
        self.ui.sample1.setSpacing(2)
        self.ui.thumbnail.setResizeMode(QtWidgets.QListWidget.Adjust)
        
        self.ui.sample1.setStyleSheet('font-size:18px')
        self.ui.sample1.setStyleSheet('color: rgbrgb(0, 0, 0)')  


        self.ui.sample2.setViewMode(QtWidgets.QListWidget.IconMode)
        self.ui.sample2.setIconSize(QtCore.QSize(1024,256))
        self.ui.sample2.setSpacing(2)
        self.ui.thumbnail.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.ui.sample2.setStyleSheet('font-size:18px')
        self.ui.sample2.setStyleSheet('color: rgbrgb(0, 0, 0)')

        items = self.ui.dir_listWidget.selectedItems()
        folders = []
        for i in range(len(items)):
            folders.append(str(self.ui.dir_listWidget.selectedItems()[i].text()))

        if  len(folders) == 1:
            folders=self.ui.dir_listWidget.currentItem().text()
            path=os.path.join(folderpath,folders)
            fileList=glob.glob(path+'\*')
            fileNameList=os.listdir(path)
            image_items = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir),fn) for fdir,fn in zip(fileList,fileNameList)]
            # for image_item in image_items:
            for image_item, i in zip(image_items, range(len(fileList))):
                filename=fileList[i]
                if filename[-3:] == 'png' or filename[-3:] == 'gif':
                    image_item.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.ui.thumbnail.addItem(image_item)
        elif len(folders) == 2:
            folder1=folders[0]
            path1=os.path.join(folderpath,folder1)
            fileList1=glob.glob(path1+'\*')
            fileNameList1=os.listdir(path1)
            folder2=folders[1]
            path2=os.path.join(folderpath,folder2)
            fileList2=glob.glob(path2+'\*')
            fileNameList2=os.listdir(path2)          
            image_items1 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir1),fn1) for fdir1,fn1 in zip(fileList1,fileNameList1)]
            image_items2 = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir2),fn2) for fdir2,fn2 in zip(fileList2,fileNameList2)]
            for image_item1 in image_items1:
                image_item1.setBackground(QtGui.QColor('#C0C0C0'))
                image_item1.setTextAlignment(QtGui.Qt.AlignCenter)
                self.ui.sample1.addItem(image_item1)
            for image_item2 in image_items2:
                image_item2.setBackground(QtGui.QColor('#C0C0C0'))
                image_item2.setTextAlignment(QtGui.Qt.AlignCenter)
                self.ui.sample2.addItem(image_item2)
    ####################################################################
    # Plot raw iamge data
    ####################################################################       
    def showRawImage(self):
        self.ui.plot_img.clear()
        self.ui.plot_img.setStyleSheet('background-color: rgb(240, 240, 240)') 
        filename=self.ui.thumbnail.currentItem().text()
        fext=filename[-3:]
        folder=self.ui.dir_listWidget.currentItem().text()
        path=os.path.join(folderpath,folder,filename)
        if fext == 'png':
            self.ui.plot_img.setPixmap(QtGui.QPixmap(path))
            self.ui.plot_img.setScaledContents(True)
            self.ui.plot_img.show()
        elif fext == 'gif':
            movie = QtGui.QMovie(path)
            self.ui.plot_img.setMovie(movie)
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

    def multiSel(self):
        if self.ui.comparison.isChecked() == True:
            self.ui.dir_listWidget.setSelectionMode(QtWidgets.QListWidget.MultiSelection)
        else:
            self.ui.dir_listWidget.setSelectionMode(QtWidgets.QListWidget.SingleSelection)
            print(self.ui.dir_listWidget.selectedItems(0))

    def gifTotal(self):
        self.ui.sameType_list.clear()
        self.ui.sameType_list.setViewMode(QtWidgets.QListWidget.IconMode)
        self.ui.sameType_list.setIconSize(QtCore.QSize(256,256))
        self.ui.sameType_list.setSpacing(1)
        # self.ui.thumbnail.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.ui.sameType_list.setStyleSheet('font-size:18px')
        self.ui.sameType_list.setStyleSheet('color: rgb(0, 0, 0)')  
        if self.ui.gif.isChecked() == False:
            print('Display all images')
        else:
            folderList=os.listdir(folderpath)
            for i in range(len(folderList)):
                folders=folderList[i]
                path=os.path.join(folderpath,folders)
                gif_fileList=glob.glob(path+'\*.gif')
                image_items = [QtWidgets.QListWidgetItem(QtGui.QIcon(fdir),fdir) for fdir in gif_fileList]
                for image_item in image_items:
                    image_item.setBackground(QtGui.QColor('#C0C0C0'))
                    image_item.setTextAlignment(QtGui.Qt.AlignCenter)
                    self.ui.sameType_list.addItem(image_item)

    ####################################################################
    # Plot raw gif data
    ####################################################################       
    def showRawGif(self):
        self.ui.plot_img.setStyleSheet('background-color: rgb(13, 0, 20)')  
        self.ui.plot_img.clear()
        path=self.ui.sameType_list.currentItem().text()
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