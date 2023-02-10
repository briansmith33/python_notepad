import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QPoint, QSize
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtPrintSupport import QPrintDialog
import sys
import json
import qtawesome as qta


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.windowControl = QFrame(self)
        self.windowControlLayout = QHBoxLayout(self)
        self.windowControl.setLayout(self.windowControlLayout)

        self.title = "Text Editor"
        self.currentFile = None
        self.setObjectName('MainWindow')
        self.setWindowTitle(self.title)
        self.defaultHeight = 600
        self.defaultWidth = 900
        self.resize(self.defaultWidth, self.defaultHeight)
        self.menuBar = self.menuBar()
        self.statusBar = self.statusBar()
        self.statusBar.showMessage('Message in statusbar.')
        self.statusBar.setStyleSheet("color: #666666; font-size: 14px;")
        self.setStatusBar(self.statusBar)

        self.fileMenu = self.menuBar.addMenu('&File')
        self.newWindowAction = QAction('New Window')
        self.newAction = QAction('&New')
        self.openAction = QAction('&Open')
        self.saveAction = QAction('&Save')
        self.saveAsAction = QAction('Save as')
        self.printAction = QAction('&Print')
        self.exitAction = QAction('Exit', self)

        self.editMenu = self.menuBar.addMenu('&Edit')
        self.undoAction = QAction('Undo')
        self.cutAction = QAction('Cut')
        self.copyAction = QAction('Copy')
        self.pasteAction = QAction('Paste')
        self.deleteAction = QAction('Delete')
        self.findAction = QAction('Find')
        self.findNextAction = QAction('Find next')
        self.findPrevAction = QAction('Find previous')
        self.replaceAction = QAction('Replace')
        self.goToAction = QAction('Go to')
        self.selectAllAction = QAction('Select all')
        self.fontAction = QAction('Font')

        self.viewMenu = self.menuBar.addMenu('View')
        self.zoomAction = QAction('Zoom')
        self.statusBarAction = QAction('Status bar')
        self.wordWrapAction = QAction('Word wrap')

        self.close_btn = QPushButton(self.menuBar)
        self.max_btn = QPushButton(self.menuBar)
        self.min_btn = QPushButton(self.menuBar)

        self.oldPos = self.pos()
        self.screen = app.desktop()
        self.winX = int((self.screen.width() / 2) - (self.width() / 2))
        self.winY = int((self.screen.height() / 2) - (self.height() / 2))
        self.pressed = False

        self.mainLayout = QVBoxLayout(self)
        self.mainFrame = QFrame(self)
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.mainFrame)
        self.setCentralWidget(self.mainFrame)
        self.editorLayout = QVBoxLayout(self)
        self.mainFrame.setLayout(self.editorLayout)
        self.textEdit = QPlainTextEdit(self)
        self.textEdit.setStyleSheet("background-color: #eeeeee; font-size: 16px; padding: 20px; border: 1px solid #bbbbbb;")
        self.scrollBar = QScrollBar(self)
        with open('scrollbar.qss', 'r') as f:
            self.scrollBar.setStyleSheet(f.read())
        self.textEdit.setVerticalScrollBar(self.scrollBar)
        self.editorLayout.addWidget(self.textEdit)

        self.fullScreen = False

        self.initUI()

    def initUI(self):

        self.menuBar.setMouseTracking(True)

        self.setStyleSheet('background-color: #cccccc; border: 2px solid #cccccc;')
        with open('menubar.qss', 'r') as f:
            self.menuBar.setStyleSheet(f.read())

        self.newAction.setShortcut('Ctrl+N')
        self.fileMenu.addAction(self.newAction)

        self.newWindowAction.setShortcut('Ctrl+Shift+N')
        self.fileMenu.addAction(self.newWindowAction)

        self.openAction.setShortcut('Ctrl+O')
        self.openAction.triggered.connect(self.openFile)
        self.fileMenu.addAction(self.openAction)

        self.fileMenu.addSeparator()

        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.triggered.connect(self.save)
        self.fileMenu.addAction(self.saveAction)

        self.saveAsAction.setShortcut('Ctrl+Shift+S')
        self.saveAsAction.triggered.connect(self.saveAs)
        self.fileMenu.addAction(self.saveAsAction)

        self.printAction.setShortcut('Ctrl+P')
        self.printAction.triggered.connect(self.print)
        self.fileMenu.addAction(self.printAction)

        self.fileMenu.addSeparator()

        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit)
        self.fileMenu.addAction(self.exitAction)

        self.undoAction.setShortcut('Ctrl+Z')
        self.editMenu.addAction(self.undoAction)

        self.editMenu.addSeparator()

        self.cutAction.setShortcut('Ctrl+X')
        self.editMenu.addAction(self.cutAction)

        self.copyAction.setShortcut('Ctrl+C')
        self.editMenu.addAction(self.copyAction)

        self.pasteAction.setShortcut('Ctrl+V')
        self.editMenu.addAction(self.pasteAction)

        self.deleteAction.setShortcut('Del')
        self.editMenu.addAction(self.deleteAction)

        self.editMenu.addSeparator()

        self.findAction.setShortcut('Ctrl+F')
        self.editMenu.addAction(self.findAction)

        self.findNextAction.setShortcut('F3')
        self.editMenu.addAction(self.findNextAction)

        self.findPrevAction.setShortcut('Shift+F3')
        self.editMenu.addAction(self.findPrevAction)

        self.replaceAction.setShortcut('Ctrl+H')
        self.editMenu.addAction(self.replaceAction)

        self.goToAction.setShortcut('Ctrl+G')
        self.editMenu.addAction(self.goToAction)

        self.editMenu.addSeparator()

        self.selectAllAction.setShortcut('Ctrl+A')
        self.editMenu.addAction(self.selectAllAction)

        self.editMenu.addSeparator()

        self.fontAction.triggered.connect(self.openFont)
        self.editMenu.addAction(self.fontAction)

        self.viewMenu.addAction(self.zoomAction)

        self.viewMenu.addAction(self.statusBarAction)

        self.viewMenu.addAction(self.wordWrapAction)

        self.menuBar.setCornerWidget(self.windowControl, Qt.TopRightCorner)
        self.windowControlLayout.addWidget(self.min_btn, alignment=Qt.AlignLeft)
        self.windowControlLayout.addWidget(self.max_btn, alignment=Qt.AlignCenter)
        self.windowControlLayout.addWidget(self.close_btn, alignment=Qt.AlignRight)

        self.min_btn.setStyleSheet("width: 30px; height:20px; border: none;")
        self.min_btn.setIcon(qta.icon('fa5s.window-minimize', color="#444444"))
        self.min_btn.setIconSize(QSize(20, 20))
        self.min_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.min_btn.clicked.connect(self.minButton)

        self.max_btn.setStyleSheet("width: 30px; height:20px; border: none;")
        self.max_btn.setIcon(qta.icon('fa5s.window-maximize', color="#444444"))
        self.max_btn.setIconSize(QSize(20, 20))
        self.max_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.max_btn.clicked.connect(self.maxButton)

        self.close_btn.setStyleSheet("width: 30px; height:20px; border: none;")
        self.close_btn.setIcon(qta.icon('fa5s.times', color="#444444"))
        self.close_btn.setIconSize(QSize(20, 20))
        self.close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.close_btn.clicked.connect(self.closeButton)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.move(self.winX, self.winY)

        self.show()

    def openFile(self):
        file, check = QFileDialog.getOpenFileName(self, 'Open file',
                                            os.path.join(os.path.expanduser('~'), 'Documents'), "Text files (*.txt);;All Files (*)")
        if check:
            with open(file, 'r') as f:
                self.textEdit.setPlainText(f.read())

    def save(self):
        if self.currentFile:
            with open(self.currentFile, 'w') as f:
                f.write(self.textEdit.toPlainText())
        else:
            file, check = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()",
                                                      "", "Text Files (*.txt);;All Files (*)")
            if check:
                with open(file, 'w') as f:
                    f.write(self.textEdit.toPlainText())
                self.currentFile = file

    def saveAs(self):
        file, check = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()",
                                                  "", "Text Files (*.txt);;All Files (*)")
        if check:
            with open(file, 'w') as f:
                f.write(self.textEdit.toPlainText())

    def print(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.textEdit.document().print_(dialog.printer())

    def openFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.pressed = True

    def mouseReleaseEvent(self, event):
        self.oldPos = event.globalPos()
        self.pressed = False

    def mouseMoveEvent(self, event):
        if self.pressed:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    @pyqtSlot()
    def minButton(self):
        self.showMinimized()

    @pyqtSlot()
    def maxButton(self):
        if self.fullScreen:
            self.winX = int((self.screen.size().width() / 2) - (self.defaultWidth / 2))
            self.winY = int((self.screen.size().height() / 2) - (self.defaultHeight / 2))
            self.setGeometry(self.winX, self.winY, self.defaultWidth, self.defaultHeight)
            self.fullScreen = False

        else:
            self.setGeometry(0, 0, self.screen.size().width(), self.screen.size().height())
            self.fullScreen = True

    @pyqtSlot()
    def closeButton(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = App()
    sys.exit(app.exec_())

