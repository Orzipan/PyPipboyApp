# -*- coding: utf-8 -*-


import datetime
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget
from .. import widgets
from .ui_datetimewidget import Ui_DateTime


class DateTimeWidget(widgets.WidgetBase):
    _signalInfoUpdated = QtCore.pyqtSignal()
    
    def __init__(self, mhandle, parent):
        super().__init__('Date/Time', parent)
        self.widget = QWidget()
        self.widget.ui = Ui_DateTime()
        self.widget.ui.setupUi(self.widget)
        self.setWidget(self.widget)
        self.pipPlayerInfo = None
        self.dateYear = 0
        self.dateMonth = 0
        self.dateDay = 0
        self.timeHour = 0
        self.timeMin = 0
        self.widget.realClockTimer = QtCore.QTimer()
        self.widget.realClockTimer.timeout.connect(self._realClockUpdate)
        self._signalInfoUpdated.connect(self._slotInfoUpdated)
        
    def init(self, app, datamanager):
        super().init(app, datamanager)
        self.dataManager = datamanager
        self._realClockUpdate()
        self.widget.realClockTimer.start(1000)
        self.dataManager.registerRootObjectListener(self._onPipRootObjectEvent)
        
    def _onPipRootObjectEvent(self, rootObject):
        self.pipPlayerInfo = rootObject.child('PlayerInfo')
        if self.pipPlayerInfo:
            self.pipPlayerInfo.registerValueUpdatedListener(self._onPipPlayerInfoUpdate, 1)
        self._signalInfoUpdated.emit()

    def _onPipPlayerInfoUpdate(self, caller, value, pathObjs):
        self._signalInfoUpdated.emit()
    
    @QtCore.pyqtSlot()
    def _realClockUpdate(self):
        realTime = datetime.datetime.now()
        realHour = realTime.strftime('%I').lstrip('0')
        self.widget.ui.realTimeLabel.setText(realTime.strftime(realHour + ':%M %p'))
        
    @QtCore.pyqtSlot()
    def _slotInfoUpdated(self):
        dateYear = self.pipPlayerInfo.child('DateYear')
        if dateYear:
            self.dateYear = dateYear.value() + 2000
        dateMonth = self.pipPlayerInfo.child('DateMonth')
        if dateMonth:
            self.dateMonth = dateMonth.value()
        dateDay = self.pipPlayerInfo.child('DateDay')
        if dateDay:
            self.dateDay = dateDay.value()
        timeHour = self.pipPlayerInfo.child('TimeHour')
        if timeHour:
            self.timeHour = int(timeHour.value())
            self.timeMin = int((timeHour.value()-self.timeHour)*60)
        # This does not work on damn Windows (complains that date is too far in the future)
        # Works fine on Linux though
        #gameDate = datetime.date(self.dateYear, self.dateMonth, self.dateDay)
        gameDate = str()
        if self.dateMonth < 10:
            gameDate += '0' + str(self.dateMonth)
        else:
            gameDate += str(self.dateMonth)
        gameDate += '/'
        if self.dateDay < 10:
            gameDate += '0' + str(self.dateDay)
        else:
            gameDate += str(self.dateDay)
        gameDate += '/'
        gameDate += str(self.dateYear)
        gameTime = datetime.time(int(self.timeHour), self.timeMin)
        gameHour = gameTime.strftime('%I').lstrip('0')
        self.widget.ui.gameTimeLabel.setText(gameTime.strftime(gameHour + ':%M %p'))
        self.widget.ui.gameDateLabel.setText(gameDate)
        