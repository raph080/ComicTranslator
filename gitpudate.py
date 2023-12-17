from PySide6 import QtWidgets, QtCore, QtGui
from ui.updatedialog import Ui_updateDialog
import git
import os

REPOS_PATH = os.path.dirname(__file__)
REPOS = git.Repo(REPOS_PATH)


class GitUpdate():

    @classmethod
    def is_up_to_date(cls):
        commits_ahead = REPOS.iter_commits('origin/main..main')
        count = sum(1 for c in commits_ahead)
        return (count == 0)

    @classmethod
    def update(cls):
        UpdateDialog().exec()


class UpdateDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(UpdateDialog, self).__init__(parent)

        self.ui = Ui_updateDialog()
        self.ui.setupUi(self)

        self.ui.updateButton.clicked.connect(self._update)

    def _update(self):
        o = REPOS.remotes.origin
        o.pull()
        print("pull")
