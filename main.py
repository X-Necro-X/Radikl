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
        self.root.setGeometry(0, 0, self.dimensions.width(), self.dimensions.height())
        # stem
        self.stem = QtWidgets.QFrame(self.root)
        self.stem.setGeometry(0, 0, self.dimensions.width(), self.dimensions.height()-self.dimensions.height()//10)
        # levels
        self.levels = []
        self.levels.append(QtWidgets.QFrame(self.stem))
        self.levels[0].setGeometry(0, 0, self.dimensions.width(), (self.dimensions.height()-self.dimensions.height()//10)//3)
        self.levels.append(QtWidgets.QFrame(self.stem))
        self.levels[1].setGeometry(0, (self.dimensions.height()-self.dimensions.height()//10)//3, self.dimensions.width(), (self.dimensions.height()-self.dimensions.height()//10)//3)
        self.levels.append(QtWidgets.QFrame(self.stem))
        self.levels[2].setGeometry(0, 2*(self.dimensions.height()-self.dimensions.height()//10)//3, self.dimensions.width(), (self.dimensions.height()-self.dimensions.height()//10)//3)
        # layers
        self.layers =[[],[],[]]
        for level in range(3):
            for layer in range(9):
                self.layers[level].append(QtWidgets.QFrame(self.levels[level]))
                # self.layers[level][layer].setStyleSheet('background-color: rgb('+str(level+layer)+'0,'+str(level+layer)+'0,'+str(level+layer)+'0)')
                self.layers[level][layer].setGeometry(self.dimensions.width()//9*layer, 0, self.dimensions.width()//9, self.levels[level].height())
        # app initializer
        self.drives = str(subprocess.check_output("fsutil fsinfo drives")).split()[1:-1]
        # self.worker(self.drives)
        self.worker(['c:/windows','c:/windows','c:/windows','c:/windows','c:/windows','c:/windows','c:/windows'])
        self.showMaximized() 
    def worker(self, content):
        items = self.extract(content)
        self.display(level=0, items=items)
        self.display(level=1, items=items)
        self.display(level=2, items=items)

    def display(self, level, items):
        icon = QtWidgets.QLabel(self.layers[level][0])
        icon.setGeometry(0, 0, self.layers[level][0].width(), self.layers[level][0].height())
        icon.setPixmap(QtGui.QPixmap('double-left.png').scaled(QtCore.QSize(self.layers[level][0].width()//5, self.layers[level][0].height()//5), aspectRatioMode=1))
        icon.setAlignment(QtCore.Qt.AlignCenter)
        layer = [4,4,3,3,2,2,1][len(items[0])-1] 
        for item in range(len(items[0])):
            icon = QtWidgets.QLabel(self.layers[level][layer])
            icon.setGeometry(0, 0, self.layers[level][layer].width(), 7*self.layers[level][layer].height()//10)
            icon.setPixmap(QtGui.QIcon.pixmap(items[1][item], items[1][item].actualSize(QtCore.QSize(min(self.layers[level][layer].width(), 7*self.layers[level][layer].height()//10),  min(self.layers[level][layer].width(), 7*self.layers[level][layer].height()//10)))))
            icon.setAlignment(QtCore.Qt.AlignCenter)
            name = QtWidgets.QLabel(self.layers[level][layer])
            name.setGeometry(0, 7*self.layers[level][layer].height()//10, self.layers[level][layer].width(), 2*self.layers[level][layer].height()//10)
            name.setText(items[0][item])
            name.setFont(QtGui.QFont('Arial', 1*self.layers[level][layer].height()//25))
            name.setAlignment(QtCore.Qt.AlignCenter)
            if layer == 4 and level != 2:
                downArrow = QtWidgets.QLabel(self.layers[level][layer])
                downArrow.setGeometry(0, 9*self.layers[level][layer].height()//10, self.layers[level][layer].width(), 1*self.layers[level][layer].height()//10)
                downArrow.setPixmap(QtGui.QPixmap('double-down.png').scaled(QtCore.QSize(self.layers[level][layer].width(), 1*self.layers[level][layer].height()//10), aspectRatioMode=1))
                downArrow.setAlignment(QtCore.Qt.AlignCenter)
            layer += 1
        icon = QtWidgets.QLabel(self.layers[level][8])
        icon.setGeometry(0, 0, self.layers[level][8].width(), self.layers[level][8].height())
        icon.setPixmap(QtGui.QPixmap('double-right.png').scaled(QtCore.QSize(self.layers[level][8].width()//5, self.layers[level][8].height()//5), aspectRatioMode=1))
        icon.setAlignment(QtCore.Qt.AlignCenter)
    def extract(self, items):
        return [list(map(lambda x: self.model.fileName(self.model.index(x)), items)), list(map(lambda x: self.model.fileIcon(self.model.index(x)), items))]
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    app.exec()