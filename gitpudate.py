from PySide6 import QtWidgets
from ui.updatedialog import Ui_updateDialog
import git
import os

REPOS_PATH = os.path.dirname(__file__)
REPOS = git.Repo(REPOS_PATH)


class GitUpdate():

    @classmethod
    def is_up_to_date(cls):
        REPOS.remote("origin").fetch()
        commits_ahead = REPOS.iter_commits("main..origin/main")
        count_ahead = sum(1 for c in commits_ahead)
        return (count_ahead == 0)

    @classmethod
    def update(cls):
        UpdateDialog().exec()


class UpdateDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(UpdateDialog, self).__init__(parent)

        self.ui = Ui_updateDialog()
        self.ui.setupUi(self)

        self.ui.updateButton.clicked.connect(self._update)

        self._update_log()

    def _update(self):
        o = REPOS.remotes.origin
        o.pull()
        self.accept()

    def _update_log(self):
        log = ""
        commits_ahead = REPOS.iter_commits('main..origin/main')
        for c in commits_ahead:
            log += c.message + "\n"
        self.ui.plainTextEdit.setPlainText(log)
