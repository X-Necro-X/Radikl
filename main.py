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
            for layer in range(7):
                self.layers[level].append(QtWidgets.QFrame(self.levels[level]))
                # self.layers[level][layer].setStyleSheet('background-color: rgb('+str(level+layer)+'0,'+str(level+layer)+'0,'+str(level+layer)+'0)')
                self.layers[level][layer].setGeometry(self.dimensions.width()//7*layer, 0, self.dimensions.width()//7, self.levels[level].height())
        # app initializer
        self.drives = str(subprocess.check_output("fsutil fsinfo drives")).split()[1:-1]
        self.switch = [0, 1, 0]
        self.pointers = [0, len(self.drives)//2, 0]
        self.stacks = [[], self.drives, []]
        self.worker()
        self.showMaximized()
    def worker(self):
        if self.switch[0]:
            self.display(level=0, items=self.extract(self.stacks[0]))
        if self.switch[1]:
            self.display(level=1, items=self.extract(self.stacks[1]))
        if self.switch[2]:
            self.display(level=2, items=self.extract(self.stacks[2]))
    def display(self, level, items):
        # left button
        icon = QtWidgets.QPushButton(self.layers[level][0])
        icon.setGeometry(0, 0, self.layers[level][0].width(), self.layers[level][0].height())
        icon.setIcon(QtGui.QIcon('double-left.png'))
        icon.setIconSize(QtCore.QSize(self.layers[level][0].width()//5, self.layers[level][0].height()//5))
        icon.setFlat(True)
        icon.clicked.connect(self.shiftLeft)
        # items
        layer = 1
        for item in range(self.pointers[level]-2, self.pointers[level]):
            if item > -1:
                self.printer(items, item, layer, level)
            layer+=1
        for item in range(self.pointers[level], self.pointers[level]+3):
            if item < len(items[0]):
                self.printer(items, item, layer, level)
            layer+=1
        # right button
        icon = QtWidgets.QPushButton(self.layers[level][6])
        icon.setGeometry(0, 0, self.layers[level][6].width(), self.layers[level][6].height())
        icon.setIcon(QtGui.QIcon('double-right.png'))
        icon.setIconSize(QtCore.QSize(self.layers[level][6].width()//5, self.layers[level][6].height()//5))
        icon.setFlat(True)
        icon.clicked.connect(self.shiftRight)
    def printer(self, items, item, layer, level):
        # icon
        icon = QtWidgets.QPushButton(self.layers[level][layer])
        icon.setGeometry(0, 0, self.layers[level][layer].width(), 7*self.layers[level][layer].height()//10)
        icon.setIcon(items[1][item])
        icon.setIconSize(items[1][item].availableSizes()[3])
        icon.setFlat(True)
        # name
        name = QtWidgets.QLabel(self.layers[level][layer])
        name.setGeometry(0, 7*self.layers[level][layer].height()//10, self.layers[level][layer].width(), 2*self.layers[level][layer].height()//10)
        name.setText(items[0][item])
        name.setFont(QtGui.QFont('Arial', self.layers[level][layer].height()//25))
        name.setAlignment(QtCore.Qt.AlignCenter)
        # events
        if level == 0:
            icon.clicked.connect(self.clickTop)
        if level == 1:
            icon.clicked.connect(lambda state, item=item: self.clickMid(item))
        if level == 2:
            icon.clicked.connect(self.clickBottom)
        # down arrow
        if layer == 3 and level != 2:
            downArrow = QtWidgets.QPushButton(self.layers[level][layer])
            downArrow.setGeometry(0, 9*self.layers[level][layer].height()//10, self.layers[level][layer].width(), 1*self.layers[level][layer].height()//10)
            downArrow.setIcon(QtGui.QIcon('double-down.png'))
            downArrow.setIconSize(QtCore.QSize(self.layers[level][layer].width(), 1*self.layers[level][layer].height()//10))
            downArrow.setFlat(True)
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