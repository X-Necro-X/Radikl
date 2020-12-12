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
        self.icons =[[],[],[]]
        self.names =[[],[],[]]
        # display initializer
        for level in range(3):
            icon = QtWidgets.QPushButton(self.levels[level])
            icon.setGeometry(0, 0, self.dimensions.width()//7, self.levels[level].height())
            icon.setIcon(QtGui.QIcon('double-left.png'))
            icon.setIconSize(QtCore.QSize(self.dimensions.width()//7//5, self.levels[level].height()//5))
            icon.setFlat(True)
            icon.clicked.connect(self.shiftLeft)
            for layer in range(5):
                self.icons[level].append(QtWidgets.QPushButton(self.levels[level]))
                self.names[level].append(QtWidgets.QLabel(self.levels[level]))
                self.icons[level][layer].setGeometry(self.dimensions.width()//7*(layer+1), 0, self.dimensions.width()//7, 7*self.levels[level].height()//10)
                self.names[level][layer].setGeometry(self.dimensions.width()//7*(layer+1), 7*self.levels[level].height()//10, self.dimensions.width()//7, 2*self.levels[level].height()//10)
                self.icons[level][layer].setFlat(True)
                self.names[level][layer].setAlignment(QtCore.Qt.AlignCenter)
            icon = QtWidgets.QPushButton(self.levels[level])
            icon.setGeometry(6*self.dimensions.width()//7, 0, self.dimensions.width()//7, self.levels[level].height())
            icon.setIcon(QtGui.QIcon('double-right.png'))
            icon.setIconSize(QtCore.QSize(self.dimensions.width()//7//5, self.levels[level].height()//5))
            icon.setFlat(True)
            icon.clicked.connect(self.shiftRight)
        # app initializer
        self.drives = str(subprocess.check_output("fsutil fsinfo drives")).split()[1:-1]
        self.switch = [0, 1, 0]
        self.stacks = [[], self.drives, []]
        self.pointers = [0, len(self.drives)//2, 0]
        self.worker()
        self.showMaximized()
    def worker(self):
        if self.switch[0]:
            self.display(level=0, items=self.extract(self.stacks[0]))
        if self.switch[1]:
            self.icons[1][3].destroy()
            self.display(level=1, items=self.extract(self.stacks[1]))
        if self.switch[2]:
            self.display(level=2, items=self.extract(self.stacks[2]))
    def display(self, level, items):
        layer = 0
        for item in range(self.pointers[level]-2, self.pointers[level]):
            if item > -1:
                self.printer(items, item, layer, level)
            else:
                break
            layer+=1
        for item in range(self.pointers[level], self.pointers[level]+3):
            if item < len(items[0]):
                self.printer(items, item, layer, level)
            else:
                break
            layer+=1
    def printer(self, items, item, layer, level):
        self.icons[level][layer].setIcon(items[1][item])
        self.icons[level][layer].setIconSize(items[1][item].availableSizes()[3])
        self.names[level][layer].setText(items[0][item])
        self.names[level][layer].setFont(QtGui.QFont('Arial', self.names[level][layer].height()//5))
        if level == 0:
            self.icons[level][layer].clicked.connect(self.clickTop)
        if level == 1:
            self.icons[level][layer].clicked.connect(lambda state, item=item: self.clickMid(item))
        if level == 2:
            self.icons[level][layer].clicked.connect(self.clickBottom)
        if layer == 3 and level != 2:
            icon = QtWidgets.QPushButton(self.levels[level])
            icon.setGeometry(3*self.dimensions.width()//7, 9*self.levels[level].height()//10, self.dimensions.width()//7, self.levels[level].height()//10)
            icon.setIcon(QtGui.QIcon('double-down.png'))
            icon.setIconSize(QtCore.QSize(self.dimensions.width()//7, self.levels[level].height()//10))
            icon.setFlat(True)
    def clickTop(self):
        print('Top')
    def clickMid(self, item):
        if item == self.pointers[1]:
            if os.path.isfile(self.stacks[1][self.pointers[1]]):
                os.startfile(self.stacks[1][self.pointers[1]])
        else:
            self.pointers[1] = item
            # self.bottom(os.listdir)
            self.switch = [0, 1, 0]
            self.worker()
    def clickBottom(self):
        print('Bottom')
    def shiftLeft(self):
        print('Left')
    def shiftRight(self):
        print('Right')
    def openDir(self, level, layer):
        print(level, layer)
    def extract(self, items):
        return [list(map(lambda x: self.model.fileName(self.model.index(x)), items)), list(map(lambda x: self.model.fileIcon(self.model.index(x)), items)), list(map(lambda x: self.model.filePath(self.model.index(x)), items))]
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    app.exec()