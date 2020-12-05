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
        self.root.setLayout(QtWidgets.QHBoxLayout())
        self.root.setStyleSheet('background-color: rgb(50,50,50)')
        self.root.setGeometry(0, 0, self.dimensions.width(), self.dimensions.height())
        # stem
        self.stem = QtWidgets.QFrame(self.root)
        self.stem.setLayout(QtWidgets.QHBoxLayout())
        self.stem.setStyleSheet('background-color: rgb(50,50,50)')
        self.stem.setGeometry(0, self.dimensions.height()//10, self.dimensions.width(), self.dimensions.height()-self.dimensions.height()//10)
        # branch 1
        self.branch1 = QtWidgets.QFrame(self.stem)
        self.branch1.setLayout(QtWidgets.QVBoxLayout())
        self.branch1.setStyleSheet('background-color: rgb(100,100,100)')
        self.branch1.setGeometry(0, 0, self.dimensions.width(), (self.dimensions.height()-self.dimensions.height()//10)//3)
        # branch 2
        self.branch2 = QtWidgets.QFrame(self.stem)
        self.branch2.setLayout(QtWidgets.QVBoxLayout())
        self.branch2.setStyleSheet('background-color: rgb(150,150,150)')
        self.branch2.setGeometry(0, (self.dimensions.height()-self.dimensions.height()//10)//3, self.dimensions.width(), 2*(self.dimensions.height()-self.dimensions.height()//10)//3)
        # branch 3
        self.branch3 = QtWidgets.QFrame(self.stem)
        self.branch3.setLayout(QtWidgets.QVBoxLayout())
        self.branch3.setStyleSheet('background-color: rgb(100,100,100)')
        self.branch3.setGeometry(0, 2*(self.dimensions.height()-self.dimensions.height()//10)//3, self.dimensions.width(), self.dimensions.height()-self.dimensions.height()//10)
        # app initializer
        self.drives = str(subprocess.check_output("fsutil fsinfo drives")).split()[1:-1]
        self.worker()
        self.showMaximized()
    def worker(self):
        info = self.extract(self.drives)
        size = len(info[0])
        wunit = (self.dimensions.width()-50)//7
        hunit = (self.dimensions.height()-self.dimensions.height()//10)//3
        for index in range(size):
            icon_img = QtWidgets.QLabel(self.branch2)
            icon_img.setGeometry(wunit*index+self.dimensions.width()//16, 0, wunit*(index+1)+self.dimensions.width()//16, hunit)
            icon_img.setPixmap(QtGui.QIcon.pixmap(info[1][index], info[1][index].actualSize(QtCore.QSize(wunit, hunit))))
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