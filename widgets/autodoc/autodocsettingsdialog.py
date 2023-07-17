import os
import logging
from widgets.autodoc.ui_autodocsettingsdialog import Ui_autodocSettingsDialog
from PyQt5 import QtCore, QtWidgets, QtGui

class AutoDocSettingsDialog(QtWidgets.QDialog):
    Settings = None
    Widgets = QtWidgets.QDialog()
    Logger = None
    
    WidgetEnabled = False
    StimpakEnabled = True
    MedXEnabled = False
    RadAwayEnabled = True
    RadXEnabled = False
    AddictolEnabled = False
    
    EnabledScene = QtWidgets.QGraphicsScene()
    DisabledScene = QtWidgets.QGraphicsScene()
    
    def __init__(self, settings, parent = None):
        super().__init__(parent)
        
        self.Settings = settings
        self.Widgets.ui = Ui_autodocSettingsDialog()
        self.Widgets.ui.setupUi(self.Widgets)
        self.Logger = logging.getLogger("pypipboyapp.widgets.autodoc")
        
        self.EnabledScene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor.fromRgb(0, 255, 0)))
        self.DisabledScene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor.fromRgb(255, 0, 0)))
        
        self.Widgets.ui.useWidgetButton.clicked.connect(self.UseWidgetButtonClicked)
        self.Widgets.ui.useStimpakButton.clicked.connect(self.UseStimpakButtonClicked)
        self.Widgets.ui.useMedXButton.clicked.connect(self.UseMedXButtonClicked)
        self.Widgets.ui.useRadAwayButton.clicked.connect(self.UseRadAwayButtonClicked)
        self.Widgets.ui.useRadXButton.clicked.connect(self.UseRadXButtonClicked)
        self.Widgets.ui.useAddictolButton.clicked.connect(self.UseAddictolButtonClicked)
        
        self.Widgets.ui.timerDelay.valueChanged.connect(self.TimerDelayValueChanged)
        
        self.Widgets.ui.stimpakPercent.valueChanged.connect(self.StimpakPercentValueChanged)
        self.Widgets.ui.stimpakLimit.valueChanged.connect(self.StimpakLimitValueChanged)
        
        self.Widgets.ui.medxUse.currentIndexChanged.connect(self.MedXUseIndexChanged)
        self.Widgets.ui.medxLimit.valueChanged.connect(self.MedXLimitValueChanged)
        
        self.Widgets.ui.radawayUse.currentIndexChanged.connect(self.RadAwayUseIndexChanged)
        self.Widgets.ui.radawayLimit.valueChanged.connect(self.RadAwayLimitValueChanged)
        
        self.Widgets.ui.radxUse.currentIndexChanged.connect(self.RadXUseIndexChanged)
        self.Widgets.ui.radxLimit.valueChanged.connect(self.RadXLimitValueChanged)
        
        self.Widgets.ui.addictolLimit.valueChanged.connect(self.AddictolLimitValueChanged)
        
        self.LoadUI()
    
    @QtCore.pyqtSlot()
    def UseWidgetButtonClicked(self):
        self.WidgetEnabled = not self.WidgetEnabled
        self.Settings.setValue("AutoDocWidget/Enabled", int(self.WidgetEnabled))
        self.Widgets.ui.useWidgetButton.setText(self.ButtonStateText(self.WidgetEnabled) + " Auto Doc")
        self.Widgets.ui.useWidgetView.setScene(self.ButtonStateScene(self.WidgetEnabled))
        self.Widgets.ui.useWidgetView.show()
    
    @QtCore.pyqtSlot()
    def UseStimpakButtonClicked(self):
        self.StimpakEnabled = not self.StimpakEnabled
        self.Settings.setValue("AutoDocWidget/Stimpak/Enabled", int(self.StimpakEnabled))
        self.Widgets.ui.useStimpakButton.setText(self.ButtonStateText(self.StimpakEnabled) + " Stimpak")
        self.Widgets.ui.useStimpakView.setScene(self.ButtonStateScene(self.StimpakEnabled))
        self.Widgets.ui.useStimpakView.show()
    
    @QtCore.pyqtSlot()
    def UseMedXButtonClicked(self):
        self.MedXEnabled = not self.MedXEnabled
        self.Settings.setValue("AutoDocWidget/MedX/Enabled", int(self.MedXEnabled))
        self.Widgets.ui.useMedXButton.setText(self.ButtonStateText(self.MedXEnabled) + " Med-X")
        self.Widgets.ui.useMedXView.setScene(self.ButtonStateScene(self.MedXEnabled))
        self.Widgets.ui.useMedXView.show()
    
    @QtCore.pyqtSlot()
    def UseRadAwayButtonClicked(self):
        self.RadAwayEnabled = not self.RadAwayEnabled
        self.Settings.setValue("AutoDocWidget/RadAway/Enabled", int(self.RadAwayEnabled))
        self.Widgets.ui.useRadAwayButton.setText(self.ButtonStateText(self.RadAwayEnabled) + " RadAway")
        self.Widgets.ui.useRadAwayView.setScene(self.ButtonStateScene(self.RadAwayEnabled))
        self.Widgets.ui.useRadAwayView.show()
    
    @QtCore.pyqtSlot()
    def UseRadXButtonClicked(self):
        self.RadXEnabled = not self.RadXEnabled
        self.Settings.setValue("AutoDocWidget/RadX/Enabled", int(self.RadXEnabled))
        self.Widgets.ui.useRadXButton.setText(self.ButtonStateText(self.RadXEnabled) + " Rad-X")
        self.Widgets.ui.useRadXView.setScene(self.ButtonStateScene(self.RadXEnabled))
        self.Widgets.ui.useRadXView.show()
    
    @QtCore.pyqtSlot()
    def UseAddictolButtonClicked(self):
        self.AddictolEnabled = not self.AddictolEnabled
        self.Settings.setValue("AutoDocWidget/Addictol/Enabled", int(self.AddictolEnabled))
        self.Widgets.ui.useAddictolButton.setText(self.ButtonStateText(self.AddictolEnabled) + " Addictol")
        self.Widgets.ui.useAddictolView.setScene(self.ButtonStateScene(self.AddictolEnabled))
        self.Widgets.ui.useAddictolView.show()
    
    @QtCore.pyqtSlot(int)
    def TimerDelayValueChanged(self, value):
        self.Settings.setValue("AutoDocWidget/General/TimerDelay", value)
    
    @QtCore.pyqtSlot(int)
    def StimpakPercentValueChanged(self, value):
        self.Settings.setValue("AutoDocWidget/Stimpak/Percent", value)
        self.Widgets.ui.stimpakPercentLabel.setText(str(value))
    
    @QtCore.pyqtSlot(int)
    def StimpakLimitValueChanged(self, value):
        self.Settings.setValue("AutoDocWidget/Stimpak/Limit", value)
    
    @QtCore.pyqtSlot(int)
    def MedXUseIndexChanged(self, index):
        self.Settings.setValue("AutoDocWidget/MedX/Use", index)
    
    @QtCore.pyqtSlot(int)
    def MedXLimitValueChanged(self, value):
        self.Settings.setValue("AutoDocWidget/MedX/Limit", value)
    
    @QtCore.pyqtSlot(int)
    def RadAwayUseIndexChanged(self, index):
        self.Settings.setValue("AutoDocWidget/RadAway/Use", index)
    
    @QtCore.pyqtSlot(int)
    def RadAwayLimitValueChanged(self, value):
        self.Settings.setValue("AutoDocWidget/RadAway/Limit", value)
    
    @QtCore.pyqtSlot(int)
    def RadXUseIndexChanged(self, index):
        self.Settings.setValue("AutoDocWidget/RadX/Use", index)
    
    @QtCore.pyqtSlot(int)
    def RadXLimitValueChanged(self, value):
        self.Settings.setValue("AutoDocWidget/RadX/Limit", value)
    
    @QtCore.pyqtSlot(int)
    def AddictolLimitValueChanged(self, value):
        self.Settings.setValue("AutoDocWidget/Addictol/Limit", value)

    def LoadUI(self):
        self.WidgetEnabled = bool(int(self.Settings.value("AutoDocWidget/Enabled", 0)))
        self.StimpakEnabled = bool(int(self.Settings.value("AutoDocWidget/Stimpak/Enabled", 1)))
        self.MedXEnabled = bool(int(self.Settings.value("AutoDocWidget/MedX/Enabled", 0)))
        self.RadAwayEnabled = bool(int(self.Settings.value("AutoDocWidget/RadAway/Enabled", 1)))
        self.RadXEnabled = bool(int(self.Settings.value("AutoDocWidget/RadX/Enabled", 0)))
        self.AddictolEnabled = bool(int(self.Settings.value("AutoDocWidget/Addictol/Enabled", 0)))
        
        self.Widgets.ui.useWidgetButton.setText(self.ButtonStateText(self.WidgetEnabled) + " Auto Doc")
        self.Widgets.ui.useWidgetView.setScene(self.ButtonStateScene(self.WidgetEnabled))
        self.Widgets.ui.useWidgetView.show()
        self.Widgets.ui.useStimpakButton.setText(self.ButtonStateText(self.StimpakEnabled) + " Stimpak")
        self.Widgets.ui.useStimpakView.setScene(self.ButtonStateScene(self.StimpakEnabled))
        self.Widgets.ui.useStimpakView.show()
        self.Widgets.ui.useMedXButton.setText(self.ButtonStateText(self.MedXEnabled) + " Med-X")
        self.Widgets.ui.useMedXView.setScene(self.ButtonStateScene(self.MedXEnabled))
        self.Widgets.ui.useMedXView.show()
        self.Widgets.ui.useRadAwayButton.setText(self.ButtonStateText(self.RadAwayEnabled) + " RadAway")
        self.Widgets.ui.useRadAwayView.setScene(self.ButtonStateScene(self.RadAwayEnabled))
        self.Widgets.ui.useRadAwayView.show()
        self.Widgets.ui.useRadXButton.setText(self.ButtonStateText(self.RadXEnabled) + " Rad-X")
        self.Widgets.ui.useRadXView.setScene(self.ButtonStateScene(self.RadXEnabled))
        self.Widgets.ui.useRadXView.show()
        self.Widgets.ui.useAddictolButton.setText(self.ButtonStateText(self.AddictolEnabled) + " Addictol")
        self.Widgets.ui.useAddictolView.setScene(self.ButtonStateScene(self.AddictolEnabled))
        self.Widgets.ui.useAddictolView.show()
        
        self.Widgets.ui.timerDelay.setValue(int(self.Settings.value("AutoDocWidget/General/TimerDelay", 2000)))
        
        self.Widgets.ui.stimpakPercent.setValue(int(self.Settings.value("AutoDocWidget/Stimpak/Percent", 80)))
        self.Widgets.ui.stimpakLimit.setValue(int(self.Settings.value("AutoDocWidget/Stimpak/Limit", 10)))
        
        self.Widgets.ui.medxUse.setCurrentIndex(int(self.Settings.value("AutoDocWidget/MedX/Use", 0)))
        self.Widgets.ui.medxLimit.setValue(int(self.Settings.value("AutoDocWidget/MedX/Limit", 5)))
        
        self.Widgets.ui.radawayUse.setCurrentIndex(int(self.Settings.value("AutoDocWidget/RadAway/Use", 0)))
        self.Widgets.ui.radawayLimit.setValue(int(self.Settings.value("AutoDocWidget/RadAway/Limit", 10)))
        
        self.Widgets.ui.radxUse.setCurrentIndex(int(self.Settings.value("AutoDocWidget/RadX/Use", 0)))
        self.Widgets.ui.radxLimit.setValue(int(self.Settings.value("AutoDocWidget/RadX/Limit", 5)))
        
        self.Widgets.ui.addictolLimit.setValue(int(self.Settings.value("AutoDocWidget/Addictol/Limit", 5)))
    
    def ButtonStateScene(self, state):
        if state:
            return self.EnabledScene
        else:
            return self.DisabledScene
    
    def ButtonStateText(self, state):
        if state:
            return "Disable"
        else:
            return "Enable"