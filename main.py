from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import os

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setWindowTitle('Radikl')
        self.model = QtWidgets.QFileSystemModel()
        path = self.model.setRootPath((QtCore.QDir.rootPath()))
        # self.treeView = QtWidgets.QTreeView(self)
        # self.treeView.setModel(self.model)
        # self.treeView.setGeometry(0,0,1000,1000)
        # self.treeView.setRootIndex(self.model.index(''))
        # print(self.treeView.setTreePosition(0))
        # self.treeView.setSortingEnabled(True)
        # self.treeView.clicked.connect(self.dummy)
        # self.model.fetchMore(self.model.index('c:/windows/'))
        # print(self.model.fileName(self.model.index('.')))
        # self.iter = QtCore.QDirIterator('.')
        print(QtCore.QModelIndex.data(self.model.index('C:/Windows/')))# QtCore.QVariant.toString()
        # print(self.model.index('').data().toString())
        # self.show()
        exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Window()
    app.exec()