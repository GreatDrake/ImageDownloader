from PyQt5.QtWidgets import (QPushButton, QFormLayout, QWidget, QLineEdit, QLabel, 
                             QVBoxLayout, QMessageBox, QMainWindow, QAction, QDialog, qApp)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from downloader import Downloader

class UI(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.lbl = QLabel('URL: ')
        self.lbl.setFont(QFont('Calibri', 17))
        
        self.le = QLineEdit(self)
        self.le.setMinimumHeight(40)
        self.le.setMinimumWidth(500)
        self.le.setFont(QFont('Calibri', 16))
        
        self.btn = QPushButton('Get Images')
        self.btn.setFont(QFont('Calibri', 12))
        self.btn.setFixedWidth(200)
        self.btn.setFixedHeight(40)
        
        self.form = QFormLayout()
        self.form.addRow(self.lbl, self.le)
        self.lbl.adjustSize()
        
        self.h = QVBoxLayout()
        self.h.addLayout(self.form)
        self.h.setAlignment(Qt.AlignTop)
        self.h.addWidget(self.btn)
        self.h.setAlignment(self.btn, Qt.AlignCenter)
        self.h.setAlignment(Qt.AlignCenter)
        
        self.setLayout(self.h)
        
                
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = UI()
        self.setCentralWidget(self.ui)
        self.ui.btn.clicked.connect(self.getImages)
        
        menubar = self.menuBar()
        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(qApp.quit)
        fileMenu = menubar.addMenu("File")
        fileMenu.addAction(exitAction)
        aboutAction = QAction("About", self)
        aboutAction.triggered.connect(self.showInfo)
        aboutMenu = menubar.addMenu("Help")
        aboutMenu.addAction(aboutAction)

        self.setWindowTitle('ImageDownloader')
        self.setWindowIcon(QIcon('arrow.ico'))
        self.show()
        self.resize(self.width(), self.height() * 1.8)
        self.setMaximumSize(self.width() * 1.5, self.height() * 2)
        self.ui.le.setMinimumWidth(self.ui.le.width() / 1.5)
        
    def getImages(self):
        if self.ui.le.text().isspace() or not self.ui.le.text():
            return
        
        self.temp = self.ui.le.text()
        self.ui.le.setText('Searching...')
        self.th = Downloader(self.temp)
        self.th.finished[int].connect(self.onFinished)
        self.th.error.connect(self.onError)
        self.th.start()
        
    def onError(self):
        self.ui.le.setText(self.temp)
        box = QMessageBox(self)
        box.setWindowTitle('Error')
        box.setText('Error occured while accessing URL.')
        box.setIcon(QMessageBox.Critical)
        box.setFont(QFont('Calibri', 13))
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()

    def onFinished(self, i):
        self.ui.le.setText(self.temp)
        box = QMessageBox(self)
        box.setWindowTitle('Done') 
        box.setText('Got ' + str(i) + ' images.')
        box.setIcon(QMessageBox.Information)
        box.setFont(QFont('Calibri', 13))
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()
        
    def showInfo(self):
        about = About(self.x() + self.width()/2, self.y() + self.height()/2)
        about.setWindowFlags(Qt.Window)
        about.exec_()
        
class About(QDialog):
    def __init__(self, x, y):
        super().__init__()
        
        self.lbl = QLabel("ImageDownloader\nVersion 1.0\n\n©Nitita Morozov 2017", self)
        self.lbl.setFont(QFont('Calibri', 16))
        self.lbl.move(10, 10)
        
        self.setStyleSheet("background-color: white;")
        self.setWindowTitle("About")
        self.setWindowIcon(QIcon('arrow.ico'))
        self.resize(300, 190)
        self.move(x - self.width() / 2, y - self.height() / 2)
        self.show()
        
        
        
        
        
        
        
        
