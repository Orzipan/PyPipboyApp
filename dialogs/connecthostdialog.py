# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets
from .ui_connecthostdialog import Ui_ConnectHostDialog

class ConnectHostDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ConnectHostDialog()
        self.ui.setupUi(self)
