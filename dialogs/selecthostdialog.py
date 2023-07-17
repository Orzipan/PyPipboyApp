# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets
from .ui_selecthostdialog import Ui_SelectHostDialog

class SelectHostDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_SelectHostDialog()
        self.ui.setupUi(self)
        
    def exec(self, hosts):
        self.hosts = list()
        for h in hosts:
            i = 0
            if not h['IsBusy']:
                text = h['addr'] + ' (' + h['MachineType'] + ')'
                item = QtWidgets.QListWidgetItem(text, self.ui.listWidget)
                self.ui.listWidget.insertItem(i, item)
                if i == 0:
                    self.ui.listWidget.setCurrentRow(0)
                i += 1
                self.hosts.append(h)
        return super().exec()
        
        
    def getSelectedHost(self):
        selection = self.ui.listWidget.selectionModel().selectedRows()
        if len(selection) > 0:
            return self.hosts[selection[0].row()]
        return None
    
