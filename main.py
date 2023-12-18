import buildresources
import sys
sys.dont_write_bytecode = True


def main():

    buildresources.compileResources()
    buildresources.compileUis()

    from PySide6 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)

    from gitupdate import GitUpdate

    if not GitUpdate.is_up_to_date():
        GitUpdate.update()

    from mainwindow import MainWindow

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
