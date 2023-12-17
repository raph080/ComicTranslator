# fmt: off
import sys
sys.dont_write_bytecode = True
from PySide6 import QtWidgets
from mainwindow import MainWindow
import buildresources
# fmt: on


def main():

    buildresources.compileResources()
    buildresources.compileUis()

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
