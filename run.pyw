from PyQt5.QtWidgets import QApplication
from main import Window
import sys 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())