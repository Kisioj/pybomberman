#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets

NULL_SIZE = QtCore.QSize(-1, -1)


class BYONDWidget:
    base_pos = QtCore.QPoint(-1, -1)

    def __init__(self, *args):
        # super().__init__(*args)
        self.anchor_1 = None
        self.anchor_2 = None

    def setAnchor1(self, *args):
        if len(args) == 1:
            self.anchor_1, = args
        else:
            x, y = args
            self.anchor_1 = QtCore.QPointF(x/100, y/100)

    def setAnchor2(self, *args):
        if len(args) == 1:
            self.anchor_2, = args
        else:
            x, y = args
            self.anchor_2 = QtCore.QPointF(x/100, y/100)

    def windowResizeEvent(self, QResizeEvent):
        if not QResizeEvent.oldSize() == NULL_SIZE:
            w_size = QResizeEvent.size()
            w_width, w_height = w_size.width(), w_size.height()

            wb_size = window.baseSize()
            wb_width, wb_height = wb_size.width(), wb_size.height()

            # width_ratio = w_width / wb_width
            # height_ratio = w_height / wb_height
            width_offset = w_width - wb_width
            height_offset = w_height - wb_height

            size = self.baseSize()
            width, height = size.width(), size.height()

            pos = self.basePos()
            x, y = pos.x(), pos.y()

            x2, y2 = x + width, y + height

            if self.anchor_1:
                x += width_offset * self.anchor_1.x()
                y += height_offset * self.anchor_1.y()

            if self.anchor_2:
                x2 += width_offset * self.anchor_2.x()
                y2 += height_offset * self.anchor_2.y()
                width = x2 - x
                height = y2 - y

            self.setGeometry(QtCore.QRect(x, y, width, height))
            logging.info("QPushButton.windowResizeEvent {}, {}".format(w_width, w_height))
        else:
            logging.info("INITIAL")

    def setBaseGeometry(self, *args):
        if len(args) == 1:
            rect = args[0]
            x, y, width, height = rect.x(), rect.y(), rect.width(), rect.height()
        else:
            x, y, width, height = args
        self.setBaseSize(width, height)
        self.setBasePos(x, y)
        logging.info("QPushButton.setBaseGeometry")
        self.setGeometry(*args)

    def basePos(self):
        return self.base_pos

    def setBasePos(self, x, y):
        self.base_pos = QtCore.QPoint(x, y)


class QMainWindow(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal(QtGui.QResizeEvent)

    def resizeEvent(self, QResizeEvent):
        super().resizeEvent(QResizeEvent)
        self.resized.emit(QResizeEvent)
        logging.info("QMainWindow.resizeEvent")

    def setBaseSize(self, *args):
        super().setBaseSize(*args)
        self.resize(*args)
        logging.info("QMainWindow.setBaseSize")


class PushButton(QtWidgets.QPushButton, BYONDWidget):
    pass

class Input(QtWidgets.QLineEdit, BYONDWidget):
    pass

class Child(QtWidgets.QWidget, BYONDWidget):
    pass

class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Dream Seeker")
        MainWindow.setBaseSize(640, 479)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralWidget)
        
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusBar)
        self.statusBar.showMessage("water")
        self.statusBar.setFixedHeight(15)
        
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menuBar.setObjectName("menuBar")
        
        self.sizeGroup = QtWidgets.QActionGroup(MainWindow)
        
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        
        self.actionOptions_and_Messages = QtWidgets.QAction(self.menuFile)
        self.actionOptions_and_Messages.setObjectName("actionOptions_and_Messages")
        self.menuFile.addAction(self.actionOptions_and_Messages)
        self.actionOptions_and_Messages.setText("&Options and Messages...\tF1")
        
        self.actionQuick_screenshot = QtWidgets.QAction(self.menuFile)
        self.actionQuick_screenshot.setObjectName("actionQuick_screenshot")
        self.menuFile.addAction(self.actionQuick_screenshot)
        self.actionQuick_screenshot.setText("&Quick screenshot\tF2")
        
        self.actionSave_screenshot_as = QtWidgets.QAction(self.menuFile)
        self.actionSave_screenshot_as.setObjectName("actionSave_screenshot_as")
        self.menuFile.addAction(self.actionSave_screenshot_as)
        self.actionSave_screenshot_as.setText("&Save screenshot as...\tShift+F2")
        
        self.actionQuit = QtWidgets.QAction(self.menuFile)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.actionQuit.setText("&Quit")
        
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuFile.setTitle("&File")
        
        self.menuIcons = QtWidgets.QMenu(self.menuBar)
        self.menuIcons.setObjectName("menuIcons")
        
        self.actionstretch = QtWidgets.QAction(self.sizeGroup)
        self.actionstretch.setObjectName("actionstretch")
        self.menuIcons.addAction(self.actionstretch)
        self.actionstretch.setText("&Stretch to fit")
        self.actionstretch.setCheckable(True)
        self.actionstretch.setChecked(True)
        
        self.actionicon32 = QtWidgets.QAction(self.sizeGroup)
        self.actionicon32.setObjectName("actionicon32")
        self.menuIcons.addAction(self.actionicon32)
        self.actionicon32.setText("&32x32")
        self.actionicon32.setCheckable(True)
        
        self.actionicon16 = QtWidgets.QAction(self.sizeGroup)
        self.actionicon16.setObjectName("actionicon16")
        self.menuIcons.addAction(self.actionicon16)
        self.actionicon16.setText("&16x16")
        self.actionicon16.setCheckable(True)
        self.menuIcons.addSeparator()
        
        self.actiontextmode = QtWidgets.QAction(self.menuIcons)
        self.actiontextmode.setObjectName("actiontextmode")
        self.menuIcons.addAction(self.actiontextmode)
        self.actiontextmode.setText("&Text")
        self.actiontextmode.setCheckable(True)
        
        self.menuBar.addAction(self.menuIcons.menuAction())
        self.menuIcons.setTitle("&Icons")
        MainWindow.setMenuBar(self.menuBar)
        
        self.child = Child(self.centralWidget)
        self.child.setAnchor1(0, 0)
        self.child.setAnchor2(100, 100)
        MainWindow.resized.connect(self.child.windowResizeEvent)
        self.child.setBaseGeometry(3, 0, 634, 400)
        
        self.input = Input(self.centralWidget)
        self.input.setAnchor1(0, 100)
        self.input.setAnchor2(100, 100)
        MainWindow.resized.connect(self.input.windowResizeEvent)
        self.input.setBaseGeometry(3, 420, 517, 20)
        
        self.pushButton = PushButton(self.centralWidget)
        self.pushButton.setCheckable(True)
        self.pushButton.setText("Chat")
        self.pushButton.setAnchor1(100, 100)
        MainWindow.resized.connect(self.pushButton.windowResizeEvent)
        self.pushButton.setBaseGeometry(520, 420, 40, 20)
        
        self.pushButton_2 = PushButton(self.centralWidget)
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setText("Alt")
        self.pushButton_2.setAnchor1(100, 100)
        MainWindow.resized.connect(self.pushButton_2.windowResizeEvent)
        self.pushButton_2.setBaseGeometry(560, 420, 30, 20)
        
        self.pushButton_3 = PushButton(self.centralWidget)
        self.pushButton_3.setText("Host...")
        self.pushButton_3.setAnchor1(100, 100)
        MainWindow.resized.connect(self.pushButton_3.windowResizeEvent)
        self.pushButton_3.setBaseGeometry(590, 420, 47, 20)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
