from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QDialog, QGroupBox, QGridLayout, QVBoxLayout
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QRect 
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('E:/Important/Folder Controller/Icons/Game Development.ico'))
        self.setWindowTitle('Radikl')
        self.base()
        self.show()
    def base(self):
        btn = QPushButton('Click', self)
        # btn.move(50, 50)
        # btn.setGeometry(QRect(100, 100, 100, 100))
        btn.setIcon(QtGui.QIcon('E:/Important/Folder Controller/Icons/Game Development.ico'))
        # btn.setIconSize(QtCore.QSize(40, 40))
        btn.setToolTip('oho')
        btn.clicked.connect(self.clickme)
    def clickme(self):
        print('hola')

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    app.exec()