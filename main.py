from PyQt5.QtWidgets import (QPushButton, QFormLayout, QWidget, QLineEdit, QLabel, 
                             QVBoxLayout, QMessageBox, QApplication)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.lbl = QLabel('URL: ')
        self.lbl.setFont(QFont('Calibri', 18))
        
        self.le = QLineEdit(self)
        self.le.setMinimumHeight(45)
        self.le.setMinimumWidth(500)
        self.le.setFont(QFont('Calibri', 16))
        
        self.btn = QPushButton('Get Images')
        self.btn.setFont(QFont('Calibri', 12))
        self.btn.setFixedWidth(200)
        self.btn.setFixedHeight(40)
        self.btn.clicked.connect(self.getImages)
        
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
        
        self.setWindowTitle('ImageGetter')
        self.setWindowIcon(QIcon('arrow.ico'))
        
        self.show()
        self.resize(self.width(), self.height()*2)
        self.setMaximumSize(self.width() * 1.5, self.height() * 2)
        self.le.setMinimumWidth(self.le.width() / 1.5)
        
    def getImages(self):
        if self.le.text().isspace() or not self.le.text():
            return
        
        self.temp = self.le.text()
        self.le.setText('Searching...')
        self.th = Getter(self.temp)
        self.th.finished[int].connect(self.onFinished)
        self.th.error.connect(self.onError)
        self.th.start()
        
    def onError(self):
        self.le.setText(self.temp)
        box = QMessageBox(self)
        box.setWindowTitle('done')
        box.setText('Error occured while accessing URL.')
        box.setIcon(QMessageBox.Critical)
        box.setFont(QFont('Calibri', 13))
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()
        

    def onFinished(self, i):
        self.le.setText(self.temp)
        box = QMessageBox(self)
        box.setWindowTitle('done')
        box.setText('Got ' + str(i) + ' images.')
        box.setIcon(QMessageBox.Information)
        box.setFont(QFont('Calibri', 13))
        box.setStandardButtons(QMessageBox.Ok)
        box.exec_()
        
