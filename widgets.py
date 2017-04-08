#!/use/bin/python3
#-*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

class MainWindow(QMainWindow):

    mySignal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("LoveWallpaper")

        label = QLabel()
        label.setPixmap(QPixmap('1.jpg'))
        label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label.setScaledContents(True)

        checkBox = QCheckBox()
        checkBox.setCheckState(Qt.PartiallyChecked)
        checkBox.stateChanged.connect(self.show_state)

        comboBox = QComboBox()
        comboBox.addItems(['one', 'two', 'three'])
        comboBox.currentIndexChanged.connect(self.index_change)
        comboBox.currentIndexChanged[str].connect(self.text_change)

        listWidget = QListWidget()
        listWidget.addItems(['one', 'two', 'three'])
        listWidget.currentItemChanged.connect(self.index_change)
        listWidget.currentTextChanged.connect(self.text_change)

        self.setCentralWidget(listWidget)

        toolbar = QToolBar('main toolbar')
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        button_action = QAction(QIcon('favicon.ico'), 'your button', self)
        button_action.setStatusTip('this is your button')
        button_action.triggered.connect(self.onToolBarButtonClick)
        button_action.setCheckable(True)
        button_action.setShortcut(QKeySequence('Ctrl+p'))

        button_action2 = QAction(QIcon('favicon.ico'), 'your button2', self)
        button_action2.setStatusTip('this is your button')
        button_action2.triggered.connect(self.onToolBarButtonClick)
        button_action2.setCheckable(True)

        toolbar.addAction(button_action)
        toolbar.addWidget(QLabel('hello'))

        self.setStatusBar(QStatusBar(self))


        menu = self.menuBar()
        menu.setNativeMenuBar(False)

        file_menu = menu.addMenu('&file')
        file_menu.addAction(button_action)

        file_menu.addSeparator()
        file_subMenu = file_menu.addMenu('SubMenu')
        file_subMenu.addAction(button_action2)


    def onToolBarButtonClick(self, s):
        print('Click', s)

    def buttonPressed(self):
        print('pressed')
        self.mySignal.emit('!!!')

    def caughtMySignal(self, s):
        print(s)

    def show_state(self, s):
        print(s)

    def index_change(self, i):
        print(i)
    def text_change(self, s):
        print(s)

app = QApplication(sys.argv)

window = MainWindow()
window.show()


app.exec_()
