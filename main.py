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
            if level == 1:
                icon = QtWidgets.QPushButton(self.levels[level])
                icon.setGeometry(0, 0, self.dimensions.width()//7, self.levels[level].height())
                icon.setIcon(QtGui.QIcon('double-left.png'))
                icon.setIconSize(QtCore.QSize(self.dimensions.width()//7//5, self.levels[level].height()//5))
                icon.setFlat(True)
                icon.clicked.connect(lambda state, direction='l': self.shift(direction))
                icon = QtWidgets.QPushButton(self.levels[level])
                icon.setGeometry(6*self.dimensions.width()//7, 0, self.dimensions.width()//7, self.levels[level].height())
                icon.setIcon(QtGui.QIcon('double-right.png'))
                icon.setIconSize(QtCore.QSize(self.dimensions.width()//7//5, self.levels[level].height()//5))
                icon.setFlat(True)
                icon.clicked.connect(lambda state, direction='r': self.shift(direction))
            self.starter(level)
        # app initializer
        self.drives = str(subprocess.check_output("fsutil fsinfo drives")).split()[1:-1]
        self.switch = [0, 1, 0]
        self.stacks = [[], self.drives, []]
        self.pointers = [0, 0, 0]
        self.worker()
        self.showMaximized()
    def starter(self, level):
        if level == 0:
            self.topdarrow = QtWidgets.QPushButton(self.levels[level])
            self.topdarrow.setGeometry(3*self.dimensions.width()//7, 9*self.levels[level].height()//10, self.dimensions.width()//7, self.levels[level].height()//10)
            self.topdarrow.setIcon(QtGui.QIcon('double-down.png'))
            self.topdarrow.setIconSize(QtCore.QSize(self.dimensions.width()//7, self.levels[level].height()//10))
            self.topdarrow.setFlat(True)
            self.topdarrow.clicked.connect(self.clickTop)
        if level == 1:
            self.bottomdarrow = QtWidgets.QPushButton(self.levels[level])
            self.bottomdarrow.setGeometry(3*self.dimensions.width()//7, 9*self.levels[level].height()//10, self.dimensions.width()//7, self.levels[level].height()//10)
            self.bottomdarrow.setIcon(QtGui.QIcon('double-down.png'))
            self.bottomdarrow.setIconSize(QtCore.QSize(self.dimensions.width()//7, self.levels[level].height()//10))
            self.bottomdarrow.setFlat(True)
            self.bottomdarrow.clicked.connect(self.clickBottom)
        for layer in range(5):
            self.icons[level].append(QtWidgets.QPushButton(self.levels[level]))
            self.names[level].append(QtWidgets.QLabel(self.levels[level]))
            self.icons[level][layer].setGeometry(self.dimensions.width()//7*(layer+1), 0, self.dimensions.width()//7, 7*self.levels[level].height()//10)
            self.names[level][layer].setGeometry(self.dimensions.width()//7*(layer+1), 7*self.levels[level].height()//10, self.dimensions.width()//7, 2*self.levels[level].height()//10)
            self.icons[level][layer].setFlat(True)
            self.names[level][layer].setAlignment(QtCore.Qt.AlignCenter)    
            if level == 0:
                self.icons[level][layer].clicked.connect(self.clickTop)
            if level == 1:
                self.icons[level][layer].clicked.connect(lambda state, item=layer: self.clickMid(item))    
            if level == 2:
                self.icons[level][layer].clicked.connect(self.clickBottom)
    def reseter(self, level):
        for layer in range(5):
            self.icons[level][layer].setIcon(QtGui.QIcon())
            self.names[level][layer].setText('')
    def extract(self, items):
        return [list(map(lambda x: self.model.fileName(self.model.index(x)), items)), list(map(lambda x: self.model.fileIcon(self.model.index(x)), items))]
    def pathFinder(self, node, mode):
        if mode == 0:
            parent = os.path.dirname(node)
            grandparent = os.path.dirname(parent)
            if os.path.abspath(node) in list(map(lambda x: os.path.abspath(x), self.drives)):
                return 0, 0
            elif parent == grandparent:
                return self.drives, self.drives.index(parent)
            else:
                res = list(map(lambda x: os.path.join(grandparent, x), os.listdir(grandparent)))
                return res, res.index(parent)
        else:
            try:
                res = list(map(lambda x: os.path.join(node, x), os.listdir(node)))
            except Exception as e:
                if type(e) == PermissionError:
                    res = []
                    self.icons[2][2].setIcon(QtGui.QIcon('not-permitted.png'))
                    self.icons[2][2].setIconSize(QtCore.QSize(100, 100))
            return res
    def worker(self):
        if self.stacks[0]:
            self.topdarrow.show()
        else:
            self.topdarrow.hide()
        if self.stacks[2]:
            self.bottomdarrow.show()
        else:
            self.bottomdarrow.hide()
        if self.switch[0]:
            self.display(level=0, items=self.extract(self.stacks[0]))
        if self.switch[1]:
            self.display(level=1, items=self.extract(self.stacks[1]))
        if self.switch[2]:
            self.display(level=2, items=self.extract(self.stacks[2]))
    def display(self, level, items):
        layer = 0
        for item in range(self.pointers[level]-2, self.pointers[level]+3):
            if item < len(items[0]) and item > -1:
                self.icons[level][layer].setIcon(items[1][item])
                self.icons[level][layer].setIconSize(QtCore.QSize(320, 320))
                self.names[level][layer].setText(items[0][item])
                self.names[level][layer].setFont(QtGui.QFont('Arial', self.names[level][layer].height()//5))
            layer+=1
    def clickTop(self):
        if self.stacks[0]:
            self.reseter(0)
            self.reseter(1)
            self.reseter(2)
            self.stacks[2] = self.stacks[1]
            self.pointers[2] = self.pointers[1]
            self.stacks[1] = self.stacks[0]
            self.pointers[1] = self.pointers[0]
            res, parent = self.pathFinder(self.stacks[0][self.pointers[0]], 0)
            if res:
                self.stacks[0] = res
            else:
                self.stacks[0] = []
            self.pointers[0] = parent
            self.switch = [1, 1, 1]
            self.worker()
    def clickMid(self, item):
        if item == 2:
            if os.path.isfile(self.stacks[1][self.pointers[1]]):
                os.startfile(self.stacks[1][self.pointers[1]])
                self.reseter(2)
                self.stacks[2] = []
                self.pointers[2] = 0
                self.switch = [0, 0, 1]
                self.worker()
            else:
                if not(self.stacks[2]):
                    self.stacks[2] = self.pathFinder(self.stacks[1][self.pointers[1]], 1)
                    self.switch = [0, 0, 1]
                    self.worker()
        else:
            if item < 2:
                item = self.pointers[1]-2+item
            else:
                item = self.pointers[1]+item-2
            if item < 0 or item > len(self.stacks[1])-1:
                return
            self.pointers[1] = item
            self.reseter(1)
            self.reseter(2)
            if os.path.isdir(self.stacks[1][self.pointers[1]]):
                self.stacks[2] = self.pathFinder(self.stacks[1][self.pointers[1]], 1)
            else:
                self.stacks[2] = []
            self.pointers[2] = 0
            self.switch = [0, 1, 1]
            self.worker()
    def clickBottom(self):
        if self.stacks[2]:
            self.reseter(0)
            self.reseter(1)
            self.reseter(2)
            self.stacks[0] = self.stacks[1]
            self.pointers[0] = self.pointers[1]
            self.stacks[1] = self.stacks[2]
            self.pointers[1] = self.pointers[2]
            try:
                if os.path.isfile(self.stacks[2][self.pointers[2]]) or not(os.listdir(self.stacks[2][self.pointers[2]])):
                    self.stacks[2] = []
                else:
                    self.stacks[2] = self.pathFinder(self.stacks[2][self.pointers[2]], 1)
            except Exception as e:
                if type(e) == PermissionError:
                    self.stacks[2] = []
                    self.icons[2][2].setIcon(QtGui.QIcon('not-permitted.png'))
                    self.icons[2][2].setIconSize(QtCore.QSize(100, 100))
            self.pointers[2] = 0
            self.switch = [1, 1, 1]
            self.worker()
    def shift(self, direction):
        if direction == 'l' and self.pointers[1] > 2:
            self.pointers[1] -= 3
        elif direction == 'r' and self.pointers[1] < len(self.stacks[1])-3:
            self.pointers[1] += 3
        else:
            return
        self.reseter(1)
        self.reseter(2)
        if os.path.isdir(self.stacks[1][self.pointers[1]]):
            self.stacks[2] = self.pathFinder(self.stacks[1][self.pointers[1]], 1)
        else:
            self.stacks[2] = []
        self.pointers[2] = 0
        self.switch = [0, 1, 1]
        self.worker()
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    app.exec()