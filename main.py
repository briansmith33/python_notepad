from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, Qt, QPoint, QSize
from PyQt5.QtGui import QFont, QCursor
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
        self.menuBar = self.menuBar()
        self.statusBar = self.statusBar()
        self.statusBar.showMessage('Message in statusbar.')
        self.statusBar.setStyleSheet("color: #666666; font-size: 14px;")
        self.setStatusBar(self.statusBar)

        self.fileMenu = self.menuBar.addMenu('&File')
        self.newProjectAction = QAction('New Project...')
        self.newAction = QAction('&New...')
        self.openAction = QAction('&Open...')
        self.saveAction = QAction('&Save')
        self.saveAsAction = QAction('Save as...')
        self.printAction = QAction('&Print...')
        self.exitAction = QAction('Exit', self)

        self.editMenu = self.menuBar.addMenu('&Edit')

        self.formatMenu = self.menuBar.addMenu('Format')
        self.fontAction = QAction('Font...')

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
        self.textEdit.setStyleSheet("background-color: #eeeeee; font-size: 16px; padding: 20px; ")
        self.scrollBar = QScrollBar(self)
        self.scrollBar.setStyleSheet("QScrollBar"
                             "{"
                             "background : #eeeeee; border:none;"
                             "}"
                             "QScrollBar::handle"
                             "{"
                             "background : #333333; margin: 12px 0px; padding: 12px 0px;"
                             "}"
                             "QScrollBar::handle::pressed"
                             "{"
                             "background : #666666;"
                             "}"
                             "QScrollBar::button"
                             "{"
                             "border: none;"
                             "}")
        self.textEdit.setVerticalScrollBar(self.scrollBar)
        self.editorLayout.addWidget(self.textEdit)

        self.fullScreen = False

        self.initUI()

    def initUI(self):
        self.setObjectName('MainWindow')
        self.setWindowTitle(self.title)
        self.resize(640, 480)
        self.menuBar.setMouseTracking(True)

        self.setStyleSheet('background-color: #333333; border: 2px solid #333333;')

        self.menuBar.setStyleSheet('color: #55D6BE; font-size: 20px;')

        self.newProjectAction.setShortcut('Ctrl+Shift+N')
        self.fileMenu.addAction(self.newProjectAction)

        self.newAction.setShortcut('Ctrl+N')
        self.fileMenu.addAction(self.newAction)

        self.openAction.setShortcut('Ctrl+O')
        self.openAction.triggered.connect(self.openFile)
        self.fileMenu.addAction(self.openAction)

        self.fileMenu.addSeparator()

        self.saveAction.setShortcut('Ctrl+S')
        self.fileMenu.addAction(self.saveAction)

        self.saveAsAction.setShortcut('Ctrl+Shift+S')
        self.fileMenu.addAction(self.saveAsAction)

        self.printAction.setShortcut('Ctrl+P')
        self.fileMenu.addAction(self.printAction)

        self.fileMenu.addSeparator()

        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit)
        self.fileMenu.addAction(self.exitAction)

        self.fontAction.triggered.connect(self.openFont)
        self.formatMenu.addAction(self.fontAction)

        self.menuBar.setCornerWidget(self.windowControl, Qt.TopRightCorner)
        self.windowControlLayout.addWidget(self.min_btn)
        self.windowControlLayout.addWidget(self.max_btn)
        self.windowControlLayout.addWidget(self.close_btn)

        self.min_btn.setStyleSheet("width: 30px; height:20px; border: none;")
        self.min_btn.setIcon(qta.icon('fa5s.window-minimize', color="#55D6BE"))
        self.min_btn.setIconSize(QSize(20, 20))
        self.min_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.min_btn.clicked.connect(self.minButton)

        self.max_btn.setStyleSheet("width: 30px; height:20px; border: none;")
        self.max_btn.setIcon(qta.icon('fa5s.window-maximize', color="#55D6BE"))
        self.max_btn.setIconSize(QSize(20, 20))
        self.max_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.max_btn.clicked.connect(self.maxButton)

        self.close_btn.setStyleSheet("width: 30px; height:20px; border: none;")
        self.close_btn.setIcon(qta.icon('fa5s.times', color="#55D6BE"))
        self.close_btn.setIconSize(QSize(20, 20))
        self.close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.close_btn.clicked.connect(self.closeButton)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.move(self.winX, self.winY)

        self.show()

    def fontMenu(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Font")
        dlgLayout = QVBoxLayout(self)
        dlg.setLayout(dlgLayout)
        fontFrame = QFrame(self)
        dlgLayout.addWidget(fontFrame)
        fontLayout = QHBoxLayout(self)
        fontFrame.setLayout(fontLayout)
        with open('font.json', 'r') as f:
            fonts = json.load(f)
            f.close()

        fontList = QListWidget(self)
        fontList.setStyleSheet("background:#eeeeee;")
        for font in fonts:
            item = QListWidgetItem(font)
            itemFont = QFont(font, 12)
            itemFont.setBold(True)
            item.setFont(itemFont)
            fontList.addItem(item)
        fontLayout.addWidget(fontList)

        styleList = QListWidget(self)
        styleList.setFixedWidth(100)
        styleList.setStyleSheet("background: #eeeeee;")
        styleList.addItem(QListWidgetItem("Bold"))
        styleList.addItem(QListWidgetItem("Italic"))
        styleList.addItem(QListWidgetItem("Bold Italic"))
        fontLayout.addWidget(styleList)

        sizeList = QListWidget(self)
        sizeList.setFixedWidth(50)
        sizeList.setStyleSheet("background:#eeeeee;")
        for i in range(100):
            item = QListWidgetItem(str(i+1))
            sizeList.addItem(item)
        fontLayout.addWidget(sizeList)

        sampleFrame = QFrame(self)
        dlgLayout.addWidget(sampleFrame)
        sampleLayout = QHBoxLayout(self)
        sampleFrame.setLayout(sampleLayout)

        sampleBox = QGroupBox("Sample Text")
        sampleBox.setStyleSheet("padding:20px;")
        sampleBox.setFixedWidth(200)
        sampleBox.setFixedHeight(100)
        sampleLayout.addWidget(sampleBox)
        sampleBoxLayout = QHBoxLayout(self)
        sampleBox.setLayout(sampleBoxLayout)
        sample = QLabel("AaBbYyZz")
        sample.setStyleSheet("padding:20px; line-height:20px;")
        sampleBoxLayout.addWidget(sample)

        okBtn = QPushButton("Ok")
        okBtn.clicked.connect(dlg.close())
        sampleLayout.addWidget(okBtn)

        cancelBtn = QPushButton("Cancel")
        cancelBtn.clicked.connect(dlg.close())
        sampleLayout.addWidget(cancelBtn)

        dlg.exec_()

    def openFont(self):
        self.fontMenu()

    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            'C:\\Users\\Brian Smith\\Documents', "Text files (*.txt)")
        with open(fname[0], 'r') as f:
            file = f.read()
            self.textEdit.setPlainText(file)
            f.close()

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
            self.winX = int((self.screen.size().width() / 2) - (640 / 2))
            self.winY = int((self.screen.size().height() / 2) - (480 / 2))
            self.setGeometry(self.winX, self.winY, 640, 480)
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
