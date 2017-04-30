#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
import PIL


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
            print("QPushButton.windowResizeEvent {}, {}".format(w_width, w_height))
        else:
            print("INITIAL")

    def setBaseGeometry(self, *args):
        if len(args) == 1:
            rect = args[0]
            x, y, width, height = rect.x(), rect.y(), rect.width(), rect.height()
        else:
            x, y, width, height = args
        self.setBaseSize(width, height)
        self.setBasePos(x, y)
        print("QPushButton.setBaseGeometry")
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
        print("QMainWindow.resizeEvent")

    def setBaseSize(self, *args):
        super().setBaseSize(*args)
        self.resize(*args)
        print("QMainWindow.setBaseSize")


class PushButton(QtWidgets.QPushButton, BYONDWidget):
    pass

class Input(QtWidgets.QLineEdit, BYONDWidget):
    pass

class Child(QtWidgets.QWidget, BYONDWidget):
    pass

class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("Dream Seeker")
        MainWindow.setBaseSize(640, 440+39)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralWidget)

        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        # self.statusBar.setGeometry(QtCore.QRect(0, 50, 640, 12))
        MainWindow.setStatusBar(self.statusBar)
        self.statusBar.showMessage('water')
        self.statusBar.setFixedHeight(15)

        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuIcons = QtWidgets.QMenu(self.menuBar)
        self.menuIcons.setObjectName("menuIcons")
        MainWindow.setMenuBar(self.menuBar)


        self.action_group = QtWidgets.QActionGroup(MainWindow)

        self.actionOptions_and_Messages = QtWidgets.QAction(MainWindow)
        self.actionOptions_and_Messages.setObjectName("actionOptions_and_Messages")
        self.actionQuick_screenshot_F2 = QtWidgets.QAction(MainWindow)
        self.actionQuick_screenshot_F2.setObjectName("actionQuick_screenshot_F2")
        self.actionSave_image_as_screenshot = QtWidgets.QAction(MainWindow)
        self.actionSave_image_as_screenshot.setObjectName("actionSave_image_as_screenshot")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.action_Stretch_to_fit = QtWidgets.QAction(self.action_group)
        self.action_Stretch_to_fit.setCheckable(True)
        self.action_Stretch_to_fit.setChecked(True)
        self.action_Stretch_to_fit.setObjectName("action_Stretch_to_fit")
        self.action_32x32 = QtWidgets.QAction(self.action_group)
        self.action_32x32.setCheckable(True)
        self.action_32x32.setObjectName("action_32x32")
        self.action_16x16 = QtWidgets.QAction(self.action_group)
        self.action_16x16.setCheckable(True)
        self.action_16x16.setObjectName("action_16x16")
        self.actionText = QtWidgets.QAction(MainWindow)
        self.actionText.setCheckable(True)
        self.actionText.setObjectName("actionText")
        self.menuFile.addAction(self.actionOptions_and_Messages)
        self.menuFile.addAction(self.actionQuick_screenshot_F2)
        self.menuFile.addAction(self.actionSave_image_as_screenshot)
        self.menuFile.addAction(self.actionQuit)
        self.menuIcons.addAction(self.action_Stretch_to_fit)
        self.menuIcons.addAction(self.action_32x32)
        self.menuIcons.addAction(self.action_16x16)
        self.menuIcons.addSeparator()
        self.menuIcons.addAction(self.actionText)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuIcons.menuAction())
        self.menuFile.setTitle("&File")
        self.menuIcons.setTitle("&Icons")
        self.actionOptions_and_Messages.setText("&Options and Messages...                    F1")
        self.actionQuick_screenshot_F2.setText("&Quick screenshot                                F2")
        self.actionSave_image_as_screenshot.setText("&Save screenshot as...                Shift+F2")
        self.actionQuit.setText("&Quit")
        self.action_Stretch_to_fit.setText("&Stretch to fit")
        self.action_32x32.setText("&32x32")
        self.action_16x16.setText("&16x16")
        self.actionText.setText("Text")

        self.mainvsplit = Child(self.centralWidget)
        self.mainvsplit.setGeometry(3, 0, 634, 400)
        self.mainvsplit.setObjectName("mainvsplit")
        self.mainvsplit.setAnchor1(0, 0)
        self.mainvsplit.setAnchor2(100, 100)

        self.mainvsplit_layout = QtWidgets.QHBoxLayout(self.mainvsplit)
        self.mainvsplit_layout.setContentsMargins(0, 0, 0, 0)
        self.mainvsplit_layout.setSpacing(6)
        self.mainvsplit_layout.setObjectName("horizontalLayout")

        self.lineEdit = Input(self.centralWidget)
        self.lineEdit.setBaseGeometry(3, 420, 517, 20)
        self.lineEdit.setAnchor1(0, 100)
        self.lineEdit.setAnchor2(100, 100)
        MainWindow.resized.connect(self.lineEdit.windowResizeEvent)

        self.pushButton = PushButton(self.centralWidget)
        self.pushButton.setCheckable(True)
        self.pushButton.setChecked(False)
        self.pushButton.setText("Chat")
        self.pushButton.setBaseGeometry(520, 420, 40, 20)
        self.pushButton.setAnchor1(100, 100)
        MainWindow.resized.connect(self.pushButton.windowResizeEvent)

        self.pushButton_2 = PushButton(self.centralWidget)
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setChecked(False)
        self.pushButton_2.setText("Alt")
        self.pushButton_2.setBaseGeometry(560, 420, 30, 20)
        self.pushButton_2.setAnchor1(100, 100)
        MainWindow.resized.connect(self.pushButton_2.windowResizeEvent)

        self.pushButton_3 = PushButton(self.centralWidget)
        self.pushButton_3.setChecked(False)
        self.pushButton_3.setText("Host...")
        self.pushButton_3.setBaseGeometry(590, 420, 47, 20)
        self.pushButton_3.setAnchor1(100, 100)
        MainWindow.resized.connect(self.pushButton_3.windowResizeEvent)

        self.retlanslateUi(MainWindow)
        # self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retlanslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
