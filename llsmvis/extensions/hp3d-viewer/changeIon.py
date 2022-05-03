import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# Create a custom "QProxyStyle" to enlarge the QMenu icons
#-----------------------------------------------------------
class MyProxyStyle(QProxyStyle):
    pass
    def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

        if QStyle_PixelMetric == QStyle.PM_SmallIconSize:
            return 40
        else:
            return QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)


# This is the main window class (with a simple QMenu implemented)
# ------------------------------------------------------------------
class TestWindow(QMainWindow):
    def __init__(self):
        super(TestWindow, self).__init__()

        # 1. Set basic geometry and color.
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Hello World')
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(200, 200, 200))
        self.setPalette(palette)

        # 2. Create the central frame.
        self.centralFrame = QFrame()
        self.centralFrame.setFrameShape(QFrame.NoFrame)
        self.setCentralWidget(self.centralFrame)

        # 3. Create a menu bar.
        myMenuBar = self.menuBar()
        fileMenu = myMenuBar.addMenu("&File")

        testMenuItem = QAction(QIcon("F:\Papers\Xiyu\QT-PyQt-PySide-Custom-Widgets\hp3d-viewer\icons\microscope.svg"), "&Test", self)
        testMenuItem.setStatusTip("Test for icon size")
        testMenuItem.triggered.connect(lambda: print("Menu item has been clicked!"))

        fileMenu.addAction(testMenuItem)

        # 4. Show the window.
        self.show()

# Start your Qt application based on the new style
#---------------------------------------------------
if __name__== '__main__':
    app = QApplication(sys.argv)
    myStyle = MyProxyStyle('Fusion')    # The proxy style should be based on an existing style,
                                        # like 'Windows', 'Motif', 'Plastique', 'Fusion', ...
    app.setStyle(myStyle)

    myGUI = TestWindow()

    sys.exit(app.exec_())