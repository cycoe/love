#/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
from downloader import Fetcher

class LoveWallpaper(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(QMainWindow, self).__init__(*args, **kwargs)
        self.initVar()
        self.initWindow()

    def initVar(self):
        self.sheetList = ['ranking', 'banner', 'wallpaper', 'recommend', 'category']
        self.labelList = []
        self.layoutList = []
        self.centerWidgetList = []
        self.actionList = []
        self.downloadedImg = []

        self.defaultCenterWidget = 0
        self.offline = False
        self.verNum = 4
        self.allowDownload = -1
        self.width, self.height = self.getScreenSize()

    def initWindow(self):
        self.setWindowTitle("LoveWallpaper")
        self.setGeometry(150, 80, 1080, 600)
        self.setWindowIcon(QIcon('love-wallpaper.jpg'))

        self.createActions()
        self.createToolBar()
        self.createLayouts()
        self.createCenterWidget()
        self.createStack()
        self.createView()
        self.startThread()
        self.createConnects()

    def getScreenSize(self):
        screen = QDesktopWidget().screenGeometry()
        return screen.width(), screen.height()

    def createActions(self):
        self.downloadAction = QAction('Download', self)
        self.downloadAction.setStatusTip('Download this wallpaper')
        self.downloadAction.setShortcut(QKeySequence('Ctrl+d'))

    def createToolBar(self):
        self.toolbar = QToolBar('Category')
        self.toolbar.setIconSize(QSize(16, 16))
        self.createComboBox()
        self.toolbar.addWidget(self.comboBox)
        self.toolbar.addAction(self.downloadAction)
        self.createProgressBar()
        self.toolbar.addWidget(self.progressBar)
        self.addToolBar(self.toolbar)

    def createComboBox(self):
        self.comboBox = QComboBox()
        self.comboBox.addItems(self.sheetList)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)

    def createLayouts(self):
        for sheet in self.sheetList:
            layout = QGridLayout()
            self.layoutList.append(layout)

    def createStack(self):
        self.stack = QStackedWidget()
        for widget in self.centerWidgetList:
            self.stack.addWidget(widget)
        self.mainlabel = QLabel()
        self.mainlabel.setScaledContents(True)
        self.stack.addWidget(self.mainlabel)

    def createCenterWidget(self):
        for sheet in self.sheetList:
            centerWidget = QWidget()
            self.centerWidgetList.append(centerWidget)

    def createConnects(self):
        """
        Signals & Slots
        """
        self.fetchImgs.signal[int, str].connect(self.setImgThumb)
        self.fetchImgs.signal[int, int].connect(self.setProgressValue)
        self.comboBox.activated.connect(self.changeStack)
        self.comboBox.activated.connect(self.disableDownload)
        self.downloadAction.triggered.connect(self.downloadIt)

    def createView(self):
        try:
            self.fetcher = Fetcher()
            self.fetcher.setImgSize(self.width, self.height)
            self.cateLib = self.fetcher.getCateLib()
            self.rankImgList = self.fetcher.fetchRankImgList()
        except Exception as e:
            print(e)
            self.offline = True
            exit(0)

        self.scrollArea = QScrollArea()

        for i in range(len(self.rankImgList)):
            self.label = MyLabel(self.rankImgList[i]['key'])
            self.label.setIndex(i)
            self.label.setScaledContents(True)
            self.labelList.append(self.label)
            self.layoutList[self.defaultCenterWidget].addWidget(self.label, i//self.verNum, i%self.verNum)

        self.centerWidgetList[self.defaultCenterWidget].setLayout(self.layoutList[self.defaultCenterWidget])
        self.scrollArea.setWidget(self.stack)
        self.scrollArea.setAutoFillBackground(True)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMinimumSize(1080, 600)
        self.scrollArea.setAlignment(Qt.AlignHCenter)
        self.setCentralWidget(self.scrollArea)

        self.setStatusBar(QStatusBar(self))

    def startThread(self):
        self.fetchImgs = FetchImgs(self.fetcher, self.rankImgList)
        self.fetchImgs.start()



    """
    slots
    """
    def setImgName(self, i, imgName):
        self.labelList[i].setText(imgName)
        self.labelList[i].setStatusTip(imgName)

    def setImgThumb(self, i, imgPath):
        self.labelList[i].setPixmap(QPixmap(imgPath))
        self.labelList[i].signal.connect(self.enterMain)
        self.labelList[i].signal.connect(self.prepareDownload)

    def enterMain(self, selected):
        imgPath = '.cache/samll/rank/' + self.rankImgList[selected]['key'] + '.jpg'
        self.mainlabel.setText(self.rankImgList[selected]['key'])
        self.mainlabel.setPixmap(QPixmap(imgPath))
        self.changeStack(self.comboBox.count())
        self.fetchImg = FetchImg(self.fetcher, self.rankImgList, selected)
        self.fetchImg.start()
        self.fetchImg.signal.connect(self.setMain)

    def setMain(self, selected, imgPath):
        self.mainlabel.setPixmap(QPixmap(imgPath))

    def changeStack(self, sheetNum):
        self.stack.setCurrentIndex(sheetNum)

    def disableDownload(self, sheetNum):
        self.allowDownload = -1

    def finishDownload(self, selected, imgPath):
        self.downloadedImg.append(selected)
        print('%s download complete!' % imgPath)

    def setProgressValue(self, pro, fullPro):
        self.progressBar.setValue(int(pro / fullPro * 100))

    def prepareDownload(self, index):
        if index not in self.downloadedImg:
            self.allowDownload = index

    def downloadIt(self):
        if self.allowDownload != -1:
            self.download = Download(self.fetcher, self.rankImgList, self.allowDownload)
            self.allowDownload = -1
            self.download.start()
            self.download.signal.connect(self.finishDownload)



class FetchImgs(QThread):
    signal = pyqtSignal([int, str], [int, int])
    def __init__(self, fetcher, rankImgList):
        super(FetchImgs, self).__init__()
        self.fetcher = fetcher
        self.rankImgList = rankImgList

    def run(self):
        for i in range(len(self.rankImgList)):
            imgPath = self.fetcher.fetchImgCache('rank', self.rankImgList[i]['small'], self.rankImgList[i]['key'], 0)
            self.signal[int, str].emit(i, imgPath)
            self.signal[int ,int].emit(i, len(self.rankImgList))

class FetchImg(QThread):
    signal = pyqtSignal(int, str)
    def __init__(self, fetcher, rankImgList, selected):
        super(FetchImg, self).__init__()
        self.fetcher = fetcher
        self.rankImgList = rankImgList
        self.selected = selected

    def run(self):
        imgPath = self.fetcher.fetchImgCache('rank', self.rankImgList[self.selected]['big'], self.rankImgList[self.selected]['key'], 1)
        self.signal.emit(self.selected, imgPath)

class Download(QThread):
    signal = pyqtSignal(int, str)
    def __init__(self, fetcher, rankImgList, selected):
        super(Download, self).__init__()
        self.fetcher = fetcher
        self.rankImgList = rankImgList
        self.selected = selected

    def run(self):
        print('downloading...')
        imgPath = self.fetcher.fetchImgCache('rank', self.rankImgList[self.selected]['big'], self.rankImgList[self.selected]['key'], 3)
        self.signal.emit(self.selected, imgPath)

class MyLabel(QLabel):
    signal = pyqtSignal(int)
    def __init__(self, *argvs, **kwargs):
        super(MyLabel, self).__init__(*argvs, **kwargs)
    def mouseDoubleClickEvent(self, event):
        self.signal.emit(self.index)
    def setIndex(self, index):
        self.index = index


app = QApplication(sys.argv)

window = LoveWallpaper()
window.show()

sys.exit(app.exec_())
