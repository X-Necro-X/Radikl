# imports
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import os, subprocess
# app
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # window settings
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle('Radikl')
        self.model = QtWidgets.QFileSystemModel()
        self.dimensions = QtGui.QScreen.availableGeometry(QtGui.QGuiApplication.primaryScreen())
        # root
        self.root = QtWidgets.QFrame(self)
        self.root.setStyleSheet('background-color: rgb(0,0,0)')
        self.root.setGeometry(0, 0, self.dimensions.width(), self.dimensions.height())
        # stem
        self.stem = QtWidgets.QFrame(self.root)
        self.stem.setStyleSheet('background-color: rgb(50,50,50)')
        self.stem.setGeometry(0, self.dimensions.height()//10, self.dimensions.width(), self.dimensions.height()-self.dimensions.height()//10)
        # branch 1
        self.top = QtWidgets.QFrame(self.stem)
        self.top.setStyleSheet('background-color: rgb(100,100,100)')
        self.top.setGeometry(0, 0, self.dimensions.width(), (self.dimensions.height()-self.dimensions.height()//10)//3)
        # branch 2
        self.mid = QtWidgets.QFrame(self.stem)
        self.mid.setStyleSheet('background-color: rgb(150,150,150)')
        self.mid.setGeometry(0, (self.dimensions.height()-self.dimensions.height()//10)//3, self.dimensions.width(), (self.dimensions.height()-self.dimensions.height()//10)//3)
        # branch 3
        # self.bottom = QtWidgets.QFrame(self.stem)
        # self.bottom.setStyleSheet('background-color: rgb(100,100,100)')
        # self.bottom.setGeometry(0, 2*(self.dimensions.height()-self.dimensions.height()//10)//3, self.dimensions.width(), self.dimensions.height()-self.dimensions.height()//10)
        # app initializer
        self.drives = str(subprocess.check_output("fsutil fsinfo drives")).split()[1:-1]
        self.drives.extend(self.drives)
        self.drives.append(self.drives[0])
        self.worker()
        self.showMaximized() 
    def worker(self):
        info = self.extract(self.drives)
        size = len(info[0])
        wunit = self.dimensions.width()//8
        hunit = (self.dimensions.height()-self.dimensions.height()//10)//3
        for index in range(size):
            icon = QtWidgets.QLabel(self.mid)
            icon.setGeometry(wunit*index+wunit//2, 0, wunit, info[1][index].actualSize(QtCore.QSize(wunit, hunit)).height())
            icon.setPixmap(QtGui.QIcon.pixmap(info[1][index], info[1][index].actualSize(QtCore.QSize(wunit, hunit))))
            icon.setAlignment(QtCore.Qt.AlignCenter)
            name = QtWidgets.QLabel(self.mid)
            name.setGeometry(wunit*index+wunit//2, info[1][index].actualSize(QtCore.QSize(wunit, hunit)).height(), wunit, self.mid.height()-info[1][index].actualSize(QtCore.QSize(wunit, hunit)).height())
            name.setText(info[0][index])
            name.setAlignment(QtCore.Qt.AlignCenter)
    def top(self, items, active):
        pass
    def middle(self, items, active):
        pass
    def bottom(self, items):
        pass
    def extract(self, items):
        return [list(map(lambda x: self.model.fileName(self.model.index(x)), items)), list(map(lambda x: self.model.fileIcon(self.model.index(x)), items))]
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    app.exec()