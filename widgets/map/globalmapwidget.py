# -*- coding: utf-8 -*-


import os
import json
import logging
import textwrap
import uuid
from PyQt5 import QtWidgets, QtCore, QtGui, uic, QtSvg
from widgets.shared.graphics import ImageFactory
from widgets import widgets
from widgets.shared import settings
from .marker import PipValueMarkerBase, MarkerBase
from .editpoidialog import EditPOIDialog
from .editnotedialog import EditNoteDialog

class PlayerMarker(PipValueMarkerBase):
    signalPlayerPositionUpdate = QtCore.pyqtSignal(float, float, float)
    
    def __init__(self, widget, imageFactory, color,size=32,  parent = None):
        super().__init__(widget.mapScene, widget.mapView, parent)
        self.markerType = 0
        self.uid = 'playermarker'
        self.widget = widget
        self.imageFactory = imageFactory
        self.imageFilePath = os.path.join('res', 'mapmarkerplayer.svg')
        self.pipValueListenerDepth = 1
        self.markerItem.setZValue(10)
        self.setColor(color,False)
        self.setSize(size,False)
        self.setLabelFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold), False)
        self.setLabel('Player', False)
        self.doUpdate()

        
    def _getPixmap_(self):
        return self.imageFactory.getPixmap(self.imageFilePath, size=self.size, color=self.color)
    
    @QtCore.pyqtSlot()        
    def _slotPipValueUpdated(self):
        if self.pipValue:
            self.setVisible(True)
            rx = self.pipValue.child('X').value()
            ry = self.pipValue.child('Y').value()
            px = self.mapCoords.pip2map_x(rx)
            py = self.mapCoords.pip2map_y(ry)
            pr = self.pipValue.child('Rotation').value()
            self.markerItem.setToolTip( 'Pos: (' + str(rx) + ', ' + str(ry) + ')\n'
                                    + 'Rot: ' + str(pr))
            self.setMapPos(px, py, pr)
            self.signalPlayerPositionUpdate.emit(px, py, pr)

class CustomMarker(PipValueMarkerBase):
    def __init__(self, widget, imageFactory, color,size=48, parent = None):
        super().__init__(widget.mapScene, widget.mapView, parent)
        self.markerType = 1
        self.uid = 'pipcustommarker'
        self.widget = widget
        self.imageFactory = imageFactory
        self.imageFilePath = os.path.join('res', 'mapmarkercustom.svg')
        self.pipValueListenerDepth = 1
        self.markerItem.setZValue(0)
        self.setColor(color,False)
        self.setSize(size,False)
        self.setLabelFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold), False)
        self.setLabel('Custom Marker', False)
        self.doUpdate()
        
    def _getPixmap_(self):
        return self.imageFactory.getPixmap(self.imageFilePath, size=self.size, color=self.color)
            
    def _updateMarkerOffset_(self):
        mb = self.markerItem.boundingRect()
        self.markerItem.setOffset(-mb.width()/2, -mb.height())
    
    @QtCore.pyqtSlot()        
    def _slotPipValueUpdated(self):
        if self.pipValue:
            isVisible = self.pipValue.child('Visible').value()
            if isVisible:
                self.setVisible(True)
                rx = self.pipValue.child('X').value()
                ry = self.pipValue.child('Y').value()
                px = self.mapCoords.pip2map_x(rx)
                py = self.mapCoords.pip2map_y(ry)
                height = self.pipValue.child('Height').value()
                self.markerItem.setToolTip( 'Pos: (' + str(rx) + ', ' + str(ry) + ')\n'
                                            + 'Visible: ' + str(isVisible) + '\n'
                                            + 'Height: ' +str(height) )
                self.setMapPos(px, py)
            else:
                self.setVisible(False)
        
    def _fillMarkerContextMenu_(self, event, menu):
        if self.pipValue:
            @QtCore.pyqtSlot()
            def _removeCustomMarker():
                self.datamanager.rpcRemoveCustomMarker()
            menu.addAction('Remove Marker', _removeCustomMarker)
    
class PowerArmorMarker(PipValueMarkerBase):
    def __init__(self, widget, imageFactory, color,size=32, parent = None):
        super().__init__(widget.mapScene, widget.mapView, parent)
        self.markerType = 2
        self.uid = 'powerarmormarker'
        self.widget = widget
        self.imageFactory = imageFactory
        self.imageFilePath = os.path.join('res', 'mapmarkerpowerarmor.svg')
        self.pipValueListenerDepth = 1
        self.markerItem.setZValue(0)
        self.setColor(color,False)
        self.setSize(size,False)
        self.setLabelFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold), False)
        self.setLabel('Power Armor', False)
        self.filterVisibleFlag = True
        self.PipVisible = False
        self.doUpdate()
        
    def _getPixmap_(self):
        return self.imageFactory.getPixmap(self.imageFilePath, size=self.size, color=self.color)
    
    @QtCore.pyqtSlot(bool)
    def filterSetVisible(self, value):
        self.filterVisibleFlag = value
        if not value:
            self.setVisible(False)
        elif value and self.PipVisible:
            self.setVisible(True)
            self.doUpdate()
    
    @QtCore.pyqtSlot()        
    def _slotPipValueUpdated(self):
        if self.pipValue:
            self.PipVisible = self.pipValue.child('Visible').value()
            rx = self.pipValue.child('X').value()
            ry = self.pipValue.child('Y').value()
            px = self.mapCoords.pip2map_x(rx)
            py = self.mapCoords.pip2map_y(ry)
            height = self.pipValue.child('Height').value()
            self.markerItem.setToolTip( 'Pos: (' + str(rx) + ', ' + str(ry) + ')\n'
                                        + 'Visible: ' + str(self.PipVisible) + '\n'
                                        + 'Height: ' +str(height) )
            self.setMapPos(px, py, False)
            if self.PipVisible and self.filterVisibleFlag:
                self.setVisible(True)
                self.doUpdate()
            else:
                self.setVisible(False)

class QuestMarker(PipValueMarkerBase):
    def __init__(self, widget, imageFactory, color,size=22, parent = None):
        super().__init__(widget.mapScene, widget.mapView, parent)
        self.markerType = 3
        self.uid = 'questmarker'
        self.widget = widget
        self.imageFactory = imageFactory
        self.imageFilePath = os.path.join('res', 'mapmarkerquest.svg')
        self.pipValueListenerDepth = 1
        self.QuestFormIds = None
        self.markerItem.setZValue(0)
        self.setColor(color,False)
        self.setSize(size,False)
        self.setLabelFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold), False)
        self.setLabel('Quest Marker', False)
        self.doUpdate()
        
    def _getPixmap_(self):

        return self.imageFactory.getPixmap(self.imageFilePath, size=self.size, color=self.color)
            
    def _updateMarkerOffset_(self):
        mb = self.markerItem.boundingRect()
        self.markerItem.setOffset(-mb.width()/2, -mb.height())
        
    @QtCore.pyqtSlot()        
    def _slotPipValueUpdated(self):
        if self.pipValue:
            self.setVisible(True)
            name = self.pipValue.child('Name').value()
            self.setLabel(name, False)
            rx = self.pipValue.child('X').value()
            ry = self.pipValue.child('Y').value()
            px = self.mapCoords.pip2map_x(rx)
            py = self.mapCoords.pip2map_y(ry)
            height = self.pipValue.child('Height').value()
            tttext =  'Pos: (' + str(rx) + ', ' + str(ry) + ')\n';
            tttext += 'Height: ' +str(height)
            onDoor = self.pipValue.child('OnDoor').value()
            if onDoor != None:
                tttext += '\nOnDoor: ' + str(onDoor)
            shared = self.pipValue.child('Shared').value()
            if shared != None:
                tttext += '\nShared: ' + str(shared)
            self.QuestFormIds = self.pipValue.child('QuestId').value()
            if self.QuestFormIds != None:
                tttext += '\nQuestIds: ['
                isFirst = True
                for q in self.QuestFormIds:
                    if isFirst:
                        isFirst = False
                    else:
                        tttext += ', '
                    tttext += str(q.value())
                tttext += ']'
            self.markerItem.setToolTip( tttext )
            self.setMapPos(px, py)
    
class LocationMarker(PipValueMarkerBase):
    artilleryRange = 97000
    
    def __init__(self, widget, imageFactory, imageFactory2, color,size=28,parent = None):
        super().__init__(widget.mapScene, widget.mapView, parent)
        self.markerType = 4
        self.widget = widget
        self.imageFactory = imageFactory
        self.imageFactory2 = imageFactory2
        self.pipValueListenerDepth = 1
        self.markerItem.setZValue(0)
        self.setColor(color,False)
        self.setSize(size,False)
        self.setLabelFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold), False)
        self.setLabel('Location', False)
        self.locType = -1
        self.noTypePixmapFound = False
        self.discovered = False
        self.lastKnownDiscovered = False
        self.visible = False
        self.cleared = False
        self.filterVisibleFlag = True
        self.filterVisibilityCheatFlag = False
        self.artilleryRangeCircle = None
        self.isOwnedWorkshop = False
        self.doUpdate()

    def updateZIndex(self):
        if hasattr(self.widget, 'mapMarkerZIndexes'):
            if (self.note and len(self.note) > 0):
                if (self.markerItem):
                    self.markerItem.setZValue(self.widget.mapMarkerZIndexes.get('LabelledLocationMarker', 0))
                if (self.labelItem):
                    self.labelItem.setZValue(self.widget.mapMarkerZIndexes.get('LabelledLocationMarker', 0)+1000)
            else:
                super().updateZIndex()
        
        
    def showArtilleryRange(self, value, updateSignal = True):
        idList = self.widget._app.settings.value('globalmapwidget/showArtilleryFormIDs', [])
        if idList == None: # Yes, this happens (because of buggy Linux QSettings implementation)
            idList = []
        if value:
            if self.pipValue and self.pipValue.child('LocationMarkerFormId'):
                id = hex(self.pipValue.child('LocationMarkerFormId').value()).lower()
                if not id in idList:
                    idList.append(id)
            self.artilleryRangeCircle = self.scene.addEllipse(0, 0, 0, 0)
            self.artilleryRangeCircle.setPen(QtGui.QPen(self.color, 2))
            self.positionDirty = True
        else:
            if self.pipValue and self.pipValue.child('LocationMarkerFormId'):
                id = hex(self.pipValue.child('LocationMarkerFormId').value()).lower()
                if id in idList:
                    idList.remove(id)
            if self.artilleryRangeCircle:
                self.scene.removeItem(self.artilleryRangeCircle)
            self.artilleryRangeCircle = None
            self.positionDirty = True
        self.widget._app.settings.setValue('globalmapwidget/showArtilleryFormIDs', idList)
        if updateSignal:
            self.doUpdate()
        
    @QtCore.pyqtSlot()
    def doUpdate(self):
        if self.artilleryRangeCircle:
            if self.isVisible:
                self.artilleryRangeCircle.setVisible(True)
                if self.markerPixmapDirty:
                    self.artilleryRangeCircle.setPen(QtGui.QPen(self.color, 2))
                if self.positionDirty and self.mapCoords:
                    rangeX = self.artilleryRange * self.mapCoords._ax * self.zoomLevel
                    rangeY = self.artilleryRange * self.mapCoords._ay * self.zoomLevel
                    self.artilleryRangeCircle.setRect(self.mapPosX * self.zoomLevel - rangeX/2,
                                                         self.mapPosY * self.zoomLevel - rangeY/2,
                                                         rangeX, rangeY)
            else:
                self.artilleryRangeCircle.setVisible(False)
        super().doUpdate()
            
    def destroy(self):
        if self.artilleryRangeCircle:
            self.scene.removeItem(self.artilleryRangeCircle)
            self.artilleryRangeCircle = None
        super().destroy()
            

    def _getPixmap_(self):
        def _getDefaultPixmap():
            if self.discovered:
                self.imageFilePath = os.path.join('res', 'mapmarkerloctype_default_d.svg')
            else:
                self.imageFilePath = os.path.join('res', 'mapmarkerloctype_default_u.svg')
            return self.imageFactory.getPixmap(self.imageFilePath, size=self.size, color=self.color)
        if not self.locType < 0:
            filepath = 'mapmarkerloctype_' + str(self.locType)
            if self.discovered:
                self.imageFilePath = os.path.join('res', filepath + '_d.svg')
            else:
                self.imageFilePath = os.path.join('res', filepath + '_u.svg')
            p = self.imageFactory.getPixmap(self.imageFilePath, size=self.size, color=self.color)
            if not p:
                self.noTypePixmapFound = True
                p = _getDefaultPixmap()
        else:
            p = _getDefaultPixmap()
        px = QtGui.QPixmap(p.width() + 10, p.height())
        px.fill(QtCore.Qt.transparent)
        pn = QtGui.QPainter(px)
        pn.drawPixmap(QtCore.QRect(0,0,p.width(),p.height()), p)
        overlayXOffset = p.width() + 2
        overlayYOffset = 0
        if (len(self.note) > 0):
            note = self.colouriseIcon(self.imageFactory2.getImage('note8.png'), self.color)
            pn.drawPixmap(QtCore.QRect(overlayXOffset, overlayYOffset, 8, 8), note)
            overlayYOffset += 8+2
        if (self.isOwnedWorkshop):
            hammer = self.colouriseIcon(self.imageFactory2.getImage('hammer8.png'), self.color)
            pn.drawPixmap(QtCore.QRect(overlayXOffset, overlayYOffset, 8, 8), hammer)
            overlayYOffset += 8+2
        if (self.cleared):
            tick = self.colouriseIcon(self.imageFactory2.getImage('tick8.png'), self.color)
            pn.drawPixmap(QtCore.QRect(overlayXOffset, overlayYOffset, 8, 8), tick)
            overlayYOffset += 8+2
        pn.end()
        return px
            
    def _updateMarkerOffset_(self):
        mb = self.markerItem.boundingRect()
        self.markerItem.setOffset(-(mb.width()-10)/2, -mb.height()/2)
            

    def colouriseIcon(self, img, colour):
        size = img.size()
        image = QtGui.QImage(QtCore.QSize(size.width()+1,size.height()+1), QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtCore.Qt.transparent)
        p = QtGui.QPainter(image)
        p.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
        p.drawImage(QtCore.QRect(1,1,size.width(), size.height()), img)
        p.setCompositionMode(QtGui.QPainter.CompositionMode_SourceAtop)
        p.setBrush(colour)
        p.drawRect(QtCore.QRect(0,0,size.width()+1,size.height()+1))
        p.end()
        return QtGui.QPixmap.fromImage(image)   
        
    @QtCore.pyqtSlot(bool)
    def filterSetVisible(self, value, update = True):
        self.filterVisibleFlag = value
        if not value:
            self.setVisible(False)
        elif value and self.visible:
            self.setVisible(True)
            if update:
                self.doUpdate()
    
    @QtCore.pyqtSlot(bool)
    def filterVisibilityCheat(self, value, update = True):
        self.filterVisibilityCheatFlag = value
        if not self.visible:
            if value:
                self.setVisible(True)
                if update:
                    self.doUpdate()
            else:
                self.setVisible(False)
    
    def setPipValue(self, value, datamanager, mapCoords = None, signal = True):
        super().setPipValue(value, datamanager, mapCoords, signal)
        if self.uid == None and self.pipValue and self.pipValue.child('LocationMarkerFormId'):
            self.uid = hex(self.pipValue.child('LocationMarkerFormId').value()).lower()
        if self.pipValue and self.pipValue.child('LocationMarkerFormId'):
            idList = self.widget._app.settings.value('globalmapwidget/showArtilleryFormIDs', [])
            if idList:
                if hex(self.pipValue.child('LocationMarkerFormId').value()).lower() in idList:
                    self.showArtilleryRange(True, False)
        self.invalidateMarkerPixmap(signal)
        
    @QtCore.pyqtSlot()        
    def _slotPipValueUpdated(self):
        if self.pipValue:
            self.visible = self.pipValue.child('Visible').value()
            name = self.pipValue.child('Name')
            if name:
                self.setLabel(name.value(), False)
            else:
                self.setLabel('<Location>', False)
            loctype = self.pipValue.child('type')
            if loctype:
                self.locType = loctype.value()
            else:
                self.locType = -1
            discovered = self.pipValue.child('Discovered')
            if discovered:
                self.discovered = discovered.value()
            cleared = self.pipValue.child('ClearedStatus')
            if cleared:
                self.cleared = cleared.value()
            if self.discovered != self.lastKnownDiscovered:
                self.invalidateMarkerPixmap(False)
            self.lastKnownDiscovered = self.discovered
            rx = self.pipValue.child('X').value()
            ry = self.pipValue.child('Y').value()
            px = self.mapCoords.pip2map_x(rx)
            py = self.mapCoords.pip2map_y(ry)
            tttext = 'Pos: (' + str(rx) + ', ' + str(ry) + ')'
            props = self.pipValue.value()
            for prop in props:
                if prop != 'X' and prop !='Y':
                    tttext += '\n' + prop + ': ' + str(props[prop].value())
            self.markerItem.setToolTip( tttext )
            if (self.visible or self.filterVisibilityCheatFlag) and self.filterVisibleFlag:
                self.setVisible(True)
                self.markerPixmapDirty = True
                self.setMapPos(px, py)
            else:
                self.setMapPos(px, py, False)
            if (self.pipValue.child('WorkshopOwned')):
                self.isOwnedWorkshop = self.pipValue.child('WorkshopOwned').value()

            
    def _labelStr_(self):
        tmp = self.label
        if self.pipValue:
            workshopOwned = self.pipValue.child('WorkshopOwned')
            if  workshopOwned and workshopOwned.value():
                tmp = textwrap.fill(tmp, 25)
                tmp += '\nPop: ' + str(self.pipValue.child('WorkshopPopulation').value())
                tmp += '   Happ: ' + str(int(self.pipValue.child('WorkshopHappinessPct').value())) + '%'
            elif self.cleared:
                tmp += ' [CLEARED]'
                tmp = textwrap.fill(tmp, 25)
        if self.pipValue:
            if len(self.note) > 0:
                tmp +='\n' + textwrap.fill(self.note, 25)
        return tmp
        
    def _fillMarkerContextMenu_(self, event, menu):
        if self.pipValue:
            @QtCore.pyqtSlot()
            def _fastTravel():
                if QtWidgets.QMessageBox.question(self.view, 'Fast Travel', 
                        'Do you want to travel to ' + self.label + '?') == QtWidgets.QMessageBox.Yes:
                    self.datamanager.rpcFastTravel(self.pipValue)
            menu.addAction('Fast Travel', _fastTravel)
            
            @QtCore.pyqtSlot()
            def _addMarkerNote():
                if(self.uid == None):
                    self.widget._logger.warn('marker has no uid, cannot create note')
                    return
                    
                notestr = self.note
                noteDlg = EditNoteDialog()
                noteDlg.txtNote.setText(notestr)
                noteDlg.lblLocation.setText(self.pipValue.child('Name').value())
                noteDlg.chkCharacterOnly.setText(noteDlg.chkCharacterOnly.text() + '(' +self.widget.pipPlayerName +')')
                ok = noteDlg.exec_()
                notestr = noteDlg.txtNote.text()
                thisCharOnly = noteDlg.chkCharacterOnly.isChecked()
                noteDlg.show()
            
                if (ok != 0):
                    noteSettingPath = 'globalmapwidget/locationmarkernotes/'
                    if thisCharOnly:
                        noteSettingPath = noteSettingPath + self.widget.pipPlayerName +'/'
                
                    if (len(notestr) > 0):
                        self.widget._app.settings.setValue(noteSettingPath+self.uid, notestr)
                        self.setNote(notestr, True)

                        self.widget._app.settings.setValue('globalmapwidget/stickylabels2/'+self.uid, int(True))
                        self.setStickyLabel(True, True)
                    else: 
                        self.widget._app.settings.beginGroup(noteSettingPath);
                        self.widget._app.settings.remove(self.uid); 
                        self.widget._app.settings.endGroup();
                        self.setNote(notestr, True)

                        self.widget._app.settings.beginGroup('globalmapwidget/stickylabels2/');
                        self.widget._app.settings.remove(self.uid); 
                        self.widget._app.settings.endGroup();
                        self.setStickyLabel(False, True)

            menu.addAction('Add\Edit Note', _addMarkerNote)
            
            if self.pipValue.child('WorkshopOwned'):
                @QtCore.pyqtSlot()
                def _showArtilleryRange():
                    self.showArtilleryRange(self.artilleryRangeCircle == None)
                action = menu.addAction('Artillery Range', _showArtilleryRange)
                action.setCheckable(True)
                action.setChecked(self.artilleryRangeCircle != None)
            
    def _markerDoubleClickEvent_(self, event):
        if self.pipValue:
            if QtWidgets.QMessageBox.question(self.view, 'Fast Travel', 
                    'Do you want to travel to ' + self.label + '?') == QtWidgets.QMessageBox.Yes:
                self.datamanager.rpcFastTravel(self.pipValue)

    @QtCore.pyqtSlot(str)
    def setNote(self, note, update = True):
        self.note = note
        self.labelDirty = True
        self.markerPixmapDirty = True
        self.doUpdate()
        
    def setSavedSettings(self):
        super().setSavedSettings()
        if self.uid != None and self.widget.pipPlayerName != None:
            self.setNote (self.widget._app.settings.value('globalmapwidget/locationmarkernotes/'+self.widget.pipPlayerName+'/'+self.uid, ''))
        if self.uid != None and len(self.note) == 0:
            self.setNote (self.widget._app.settings.value('globalmapwidget/locationmarkernotes/'+self.uid, ''))

class PointofInterestMarker(MarkerBase):
    def __init__(self, uid, widget, imageFactory, color,size=24, iconfile='mapmarkerpoi_1.svg', parent = None):
        super().__init__(widget.mapScene, widget.mapView, parent)
        self.markerType = 5
        self.widget = widget
        self.imageFactory = imageFactory
        self.imageFilePath = iconfile
        self.pipValueListenerDepth = 1
        self.markerItem.setZValue(0)
        self.setColor(color,False)
        self.setSize(size,False)
        self.setLabelFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold), False)
        self.setLabel('Point of Interest Marker', False)
        self.filterVisibleFlag = True
        self.uid = str(uid)
        self.thisCharOnly = True

        self.doUpdate()

    def _labelStr_(self):
        return textwrap.fill(self.label, 25)
        
    def _getPixmap_(self):
        return self.imageFactory.getPixmap(self.imageFilePath, size=self.size, color=self.color)

    def _updateMarkerOffset_(self):
        mb = self.markerItem.boundingRect()
        self.markerItem.setOffset(-mb.width()/2, -mb.height())
        
    @QtCore.pyqtSlot(bool)
    def filterSetVisible(self, value):
        self.filterVisibleFlag = value
        if not value:
            self.setVisible(False)
        elif value :
            self.setVisible(value)
            self.doUpdate()
    
    @QtCore.pyqtSlot()        
    def _slotPipValueUpdated(self):
        self.setSavedSettings()
        return
                
    def _fillMarkerContextMenu_(self, event, menu):
        @QtCore.pyqtSlot()
        def _deletePOIMarker(): 
            self.widget._logger.info ('markertodelete: ' +self.uid)
            poiSettingPath = 'globalmapwidget/pointsofinterest/' 
            if self.thisCharOnly:
                poiSettingPath = poiSettingPath + self.widget.pipPlayerName +'/'

            self.widget._app.settings.beginGroup(poiSettingPath);
            self.widget._app.settings.remove(self.uid); 
            self.widget._app.settings.endGroup();

            index = self.widget._app.settings.value(poiSettingPath+'index', None)
            if index == None: # Yes, this happens (because of buggy Linux QSettings implementation)
                index = []
            if index and len(index) > 0:
                if self.uid in index:
                    index.remove(self.uid)
                    self.widget._app.settings.setValue(poiSettingPath+'index', index)
                    
                    self.widget._app.settings.beginGroup(poiSettingPath+self.uid);
                    self.widget._app.settings.remove(""); 
                    self.widget._app.settings.endGroup();
            
            self.destroy()

        @QtCore.pyqtSlot()
        def _editPOIMarker():
            labelstr = ''
            
            editpoiDialog = EditPOIDialog(self.widget, color=self.color)
            editpoiDialog.txtPOILabel.setText(self.label)
            editpoiDialog.setSelectedIcon(self.imageFilePath)
            editpoiDialog.chkCharacterOnly.setText(editpoiDialog.chkCharacterOnly.text() + '(' +self.widget.pipPlayerName +')')
            editpoiDialog.chkCharacterOnly.setChecked(self.thisCharOnly)
            editpoiDialog.chkCharacterOnly.setEnabled(False)
            ok = editpoiDialog.exec_()
            labelstr = editpoiDialog.txtPOILabel.text()
            thisCharOnly = editpoiDialog.chkCharacterOnly.isChecked()
            
            editpoiDialog.show()
            
            if (ok != 0):
                poiSettingPath = 'globalmapwidget/pointsofinterest/' 
                if thisCharOnly:
                    poiSettingPath = poiSettingPath + self.widget.pipPlayerName +'/'
            
                markerKey = self.uid

                self.widget._app.settings.setValue(poiSettingPath+str(markerKey)+'/label', labelstr)
                self.widget._app.settings.setValue(poiSettingPath+str(markerKey)+'/color', editpoiDialog.selectedColor)
                self.widget._app.settings.setValue(poiSettingPath+str(markerKey)+'/icon', editpoiDialog.IconFile)
                self.widget._app.settings.sync()
                self.setSavedSettings()
                    
        
        menu.addAction('Edit POI Marker', _editPOIMarker)
        menu.addAction('Delete POI Marker', _deletePOIMarker)
        
    def setSavedSettings(self):
        poiSettingPath = 'globalmapwidget/pointsofinterest/'
        if self.thisCharOnly:
            poiSettingPath = poiSettingPath + self.widget.pipPlayerName +'/'
        
        label = self.widget._app.settings.value(poiSettingPath+str(self.uid)+'/label', '')
        self.imageFilePath = self.widget._app.settings.value(poiSettingPath+str(self.uid)+'/icon', 'mapmarkerpoi_1.svg')
        worldx = float(self.widget._app.settings.value(poiSettingPath+str(self.uid)+'/worldx', 0.0))
        worldy = float(self.widget._app.settings.value(poiSettingPath+str(self.uid)+'/worldy', 0.0))
        color = self.widget._app.settings.value(poiSettingPath+str(self.uid)+'/color', None)
        if (color != None):
            self.setColor(color, True)

        self.setMapPos(self.widget.mapCoords.pip2map_x(worldx), self.widget.mapCoords.pip2map_y(worldy))
        self.setLabel(label)
        self.invalidateMarkerPixmap()
        super().setSavedSettings()

class CollectableMarker(MarkerBase):
    def __init__(self, widget, imageFactory, color, parent = None, icon='StarFilled.svg'):
        super().__init__(widget.mapScene, widget.mapView, parent)
        self.markerType = 6
        self.widget = widget
        self.imageFactory = imageFactory
        self.imageFilePath = os.path.join(icon)
        self.markerItem.setZValue(0)
        self.setColor(color,False)
        self.setLabelFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold), False)
        self.setLabel('Collectable Marker', False)
        self.filterVisibleFlag = True
        self.uid = "CollectableMarker"
        self.collected = False
        self.doUpdate()

    def _labelStr_(self):
        return self.label
        
    def _getPixmap_(self):
        return self.imageFactory.getPixmap(self.imageFilePath, size=24, color=self.color)
        
    def setCollected(self, value):
        self.collected = value
        #invalidate stuff here
        self.doUpdate()

    @QtCore.pyqtSlot(bool)
    def filterSetVisible(self, value):
        self.filterVisibleFlag = value
        if not value:
            self.setVisible(False)
        elif value :
            self.setVisible(value)
            self.doUpdate()        
    @QtCore.pyqtSlot()        
    def _slotPipValueUpdated(self):
        return

class MapGraphicsItem(QtCore.QObject):
    
    class PixmapItem(QtWidgets.QGraphicsPixmapItem):
        def __init__(self, parent, qparent = None):
            super().__init__(qparent)
            self.parent = parent

    def __init__(self, gwidget, imageFactory, color = None, qparent = None):
        super().__init__(qparent)
        self.gwidget = gwidget
        self.imageFactory = imageFactory
        self.mapfile = None
        self.color = color
        self.colorable = True
        self.nw = None
        self.ne = None
        self.sw = None
        self.mapItem = self.PixmapItem(self)
        self.gwidget.mapScene.addItem(self.mapItem)
        self.mapItem.setZValue(-10)
    
    def setMapFile(self, mapfile, colorable = True, nw = [52, 52], ne = [1990, 52], sw = [52, 1990]):
        self.mapfile = mapfile
        self.colorable = colorable
        self.nw = nw
        self.ne = ne
        self.sw = sw
        if colorable:
            self._setMapPixmap(self.imageFactory.getPixmap(self.mapfile, color = self.color))
        else:
            self._setMapPixmap(self.imageFactory.getPixmap(self.mapfile, color = None))
        
    
    def _setMapPixmap(self, pixmap):
        self.mapItem.setPixmap(pixmap)
        self.gwidget.mapScene.setSceneRect(self.mapItem.sceneBoundingRect())
    
    @QtCore.pyqtSlot(float, float, float)
    def setZoomLevel(self, zoom, mapposx, mapposy):
        self.mapItem.setTransform(QtGui.QTransform.fromScale(zoom, zoom))
        self.gwidget.mapScene.setSceneRect(self.mapItem.sceneBoundingRect())
        if mapposx >= 0 and mapposy >=0:
            self.gwidget.mapView.centerOn(mapposx * zoom, mapposy * zoom)
    
    @QtCore.pyqtSlot(QtGui.QColor)
    def setColor(self, color):
        self.color = color
        if self.colorable:
            self._setMapPixmap(self.imageFactory.getPixmap(self.mapfile, color = color))



class GlobalMapWidget(widgets.WidgetBase):
    
    signalSetZoomLevel = QtCore.pyqtSignal(float, float, float)
    signalSetColor = QtCore.pyqtSignal(QtGui.QColor)
    signalSetLocationSize = QtCore.pyqtSignal(int)
    signalSetStickyLabel = QtCore.pyqtSignal(bool)
    signalLocationFilterSetVisible = QtCore.pyqtSignal(bool)
    signalLocationFilterVisibilityCheat = QtCore.pyqtSignal(bool)
    signalMarkerForcePipValueUpdate = QtCore.pyqtSignal()

    
    _signalPipWorldQuestsUpdated = QtCore.pyqtSignal()
    _signalPipWorldLocationsUpdated = QtCore.pyqtSignal()
    
    MAPZOOM_SCALE_MAX = 4.0
    MAPZOOM_SCALE_MIN = 0.05
  
    def __init__(self, handle, controller, parent):
        super().__init__('Global Map', parent)
        self.basepath = handle.basepath
        self.controller = controller
        self.widget = uic.loadUi(os.path.join(self.basepath, 'ui', 'globalmapwidget.ui'))
        self.setWidget(self.widget)
        self._logger = logging.getLogger('pypipboyapp.map.globalmap')
        self.mapZoomLevel = 1.0

    def iwcSetup(self, app):
        app.iwcRegisterEndpoint('globalmapwidget', self)
    
    def init(self, app, datamanager):
        super().init(app, datamanager)
        self._app = app
        # Read maps config file
        try:
            configFile = open(os.path.join(self.basepath, 'res', 'globalmapsconfig.json'))
            self.mapFiles = json.load(configFile)
        except Exception as e:
            self._logger.error('Could not load map-files: ' + str(e))
        self.locMarkSize = int(self._app.settings.value('globalmapwidget/locationMarkeSize', 28))
        self.selectedMapFile = self._app.settings.value('globalmapwidget/selectedMapFile', 'default')
        # Init graphics view
        self.mapColor = QtGui.QColor.fromRgb(20,255,23)
        self.mapScene = QtWidgets.QGraphicsScene()
        self.mapScene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor.fromRgb(0,0,0)))
        self.mapView = self.widget.mapGraphicsView
        self.mapView.viewport().installEventFilter(self)
        self.mapView.setScene(self.mapScene)
        self.mapView.setMouseTracking(True)
        self.mapView.centerOn(0, 0)
        # Add map graphics
        if self._app.settings.value('globalmapwidget/colour'):
            self.mapColor = self._app.settings.value('globalmapwidget/colour')
        self.mapItem = MapGraphicsItem(self, self.controller.imageFactory, self.mapColor)
        try:
            mapfile = self.mapFiles[self.selectedMapFile]
        except Exception as e:
            self._logger.error('Could not find map "' + self.selectedMapFile + '": ' + str(e))
            self.selectedMapFile = 'default'
            self._app.settings.setValue('globalmapwidget/selectedMapFile', self.selectedMapFile)
            mapfile = self.mapFiles[self.selectedMapFile]
        file = os.path.join('res', mapfile['file'])
        self.mapItem.setMapFile(file, mapfile['colorable'], mapfile['nw'], mapfile['ne'], mapfile['sw'])
        self.signalSetZoomLevel.connect(self.mapItem.setZoomLevel)
        self.signalSetColor.connect(self.mapItem.setColor)
        #Define ZOrder of different types of marker
        self.mapMarkerZIndexes = {}
        self.mapMarkerZIndexes[str(PlayerMarker)] = 100
        self.mapMarkerZIndexes[str(CustomMarker)] = 90
        self.mapMarkerZIndexes[str(QuestMarker)] = 80
        self.mapMarkerZIndexes[str(PowerArmorMarker)] = 70
        self.mapMarkerZIndexes[str(PointofInterestMarker)] = 60
        self.mapMarkerZIndexes['LabelledLocationMarker'] = 50
        self.mapMarkerZIndexes[str(CollectableMarker)] = 40
        self.mapMarkerZIndexes[str(LocationMarker)] = 30
        self.mapMarkerZIndexes[str(MarkerBase)] = 0
        # Add player marker
        self.playerMarker = PlayerMarker(self,self.controller.imageFactory, self.mapColor)
        self._connectMarker(self.playerMarker)
        self.playerMarker.signalPlayerPositionUpdate.connect(self._slotPlayerMarkerPositionUpdated)
        # Add custom marker
        self.customMarker = CustomMarker(self,self.controller.imageFactory, self.mapColor)
        self._connectMarker(self.customMarker)
        # Add powerarmor marker
        self.powerArmorMarker = PowerArmorMarker(self,self.controller.imageFactory, self.mapColor)
        self._connectMarker(self.powerArmorMarker)
        # Init zoom slider
        self.widget.mapZoomSlider.setMinimum(-100)
        self.widget.mapZoomSlider.setMaximum(100)
        self.widget.mapZoomSlider.setValue(0)
        self.widget.mapZoomSlider.setSingleStep(5)
        self.widget.mapZoomSlider.valueChanged.connect(self._slotZoomSliderTriggered)
        self.widget.locationMarkerSizeSlider.valueChanged.connect(self._slotlocationMarkerSizeSliderTriggered)
        self.widget.locationMarkerSizeSpinbox.valueChanged.connect(self._slotlocationMarkerSizeSpinboxTriggered)
        # Init zoom Spinbox
        self.widget.mapZoomSpinbox.setMinimum(self.MAPZOOM_SCALE_MIN*100.0)
        self.widget.mapZoomSpinbox.setMaximum(self.MAPZOOM_SCALE_MAX*100.0)
        self.widget.mapZoomSpinbox.setValue(100.0)
        self.widget.mapZoomSpinbox.setSingleStep(10.0)
        self.widget.mapZoomSpinbox.valueChanged.connect(self._slotZoomSpinTriggered)
        self.signalSetZoomLevel.connect(self.saveZoom)
        if (self._app.settings.value('globalmapwidget/zoom')):
            self.mapZoomLevel = float(self._app.settings.value('globalmapwidget/zoom'))
            if self.mapZoomLevel == 1.0:
                sliderValue = 0
            elif self.mapZoomLevel > 1.0:
                sliderValue = (self.mapZoomLevel/self.MAPZOOM_SCALE_MAX)*100.0
            else:
                sliderValue = -(self.MAPZOOM_SCALE_MIN/self.mapZoomLevel)*100.0
            self.widget.mapZoomSlider.blockSignals(True)
            self.widget.mapZoomSlider.setValue(sliderValue)
            self.widget.mapZoomSlider.blockSignals(False)
            self.widget.mapZoomSpinbox.blockSignals(True)
            self.widget.mapZoomSpinbox.setValue(self.mapZoomLevel*100.0)
            self.widget.mapZoomSpinbox.blockSignals(False)
            self.signalSetZoomLevel.emit(self.mapZoomLevel, 0, 0)
        #Init Location MArker size spinbox and slider
        self.widget.locationMarkerSizeSlider.setValue(self.locMarkSize)
        self.widget.locationMarkerSizeSpinbox.setValue(self.locMarkSize)
        # Init map file combo box
        i = 0
        self.mapFileComboItems = []
        for mf in self.mapFiles:
            self.widget.mapFileComboBox.addItem(self.mapFiles[mf]['label'])
            if mf == self.selectedMapFile:
                self.widget.mapFileComboBox.setCurrentIndex(i)
            i += 1
            self.mapFileComboItems.append(mf)
        self.widget.mapFileComboBox.currentIndexChanged.connect(self._slotMapFileComboTriggered)
        # Init color controls
        self.widget.mapColorButton.clicked.connect(self._slotMapColorSelectionTriggered)
        try:
            self.widget.mapColorAutoToggle.setChecked(bool(int(self._app.settings.value('globalmapwidget/autoColour', 0))))
        except ValueError:
            self.widget.mapColorAutoToggle.setChecked(bool(self._app.settings.value('globalmapwidget/autoColour', False)))
        #self.widget.mapColorAutoToggle.setChecked(False)
        
        self.widget.mapColorAutoToggle.stateChanged.connect(self._slotMapColorAutoModeTriggered)
        # Init stickyLabels Checkbox
        self.stickyLabelsEnabled = False
        self.widget.stickyLabelsCheckbox.stateChanged.connect(self._slotStickyLabelsTriggered)
        self.widget.stickyLabelsCheckbox.setChecked(bool(int(self._app.settings.value('globalmapwidget/stickyLabels', 0))))
        # Init PowerMarker Enable Checkbox
        self.widget.powerMarkerEnableCheckbox.stateChanged.connect(self._slotPowerMarkerEnableTriggered)
        self.widget.powerMarkerEnableCheckbox.setChecked(bool(int(self._app.settings.value('globalmapwidget/powerArmourMarker', 1))))
        # Init Location Enable Checkbox
        self.locationFilterEnableFlag = True
        self.widget.locationMarkerEnableCheckbox.stateChanged.connect(self._slotLocationEnableTriggered)
        self.widget.locationMarkerEnableCheckbox.setChecked(bool(int(self._app.settings.value('globalmapwidget/locationMarker', 1))))
        # Init Location Visibility Cheat Checkbox
        self.locationVisibilityCheatFlag = False
        self.widget.locationVisibilityCheatCheckbox.stateChanged.connect(self._slotLocationVisibilityCheatTriggered)
        self.widget.locationVisibilityCheatCheckbox.setChecked(bool(int(self._app.settings.value('globalmapwidget/locationVisibilityCheat', 0))))
        # Init CenterOnPlayer checkbox
        self.centerOnPlayerEnabled = False
        self.widget.centerPlayerCheckbox.stateChanged.connect(self._slotCenterOnPlayerCheckToggled)
        self.widget.centerPlayerCheckbox.setChecked(bool(int(self._app.settings.value('globalmapwidget/centerPlayer', 0))))
        # Init SaveTo Button
        self.widget.saveToButton.clicked.connect(self._slotSaveToTriggered)
        # Init Splitter
        settings.setSplitterState(self.widget.splitter, self._app.settings.value('globalmapwidget/splitterState', None))
        self.widget.splitter.splitterMoved.connect(self._slotSplitterMoved)
        # Init Toolbox
        tbCurrent = self._app.settings.value('globalmapwidget/toolboxCurrentIndex', None)
        if tbCurrent:
            self.widget.toolBox.setCurrentIndex(int(tbCurrent))
        self.widget.toolBox.currentChanged.connect(self._slotToolboxCurrentChanged)
        # Init PyPipboy stuff
        from .controller import MapCoordinates
        self.mapCoords = MapCoordinates()
        self.datamanager = datamanager
        self.pipMapObject = None
        self.pipMapWorldObject = None
        self.pipColor = None
        self.pipPlayerObject = None
        self.pipPlayerName = None
        self.pipWorldQuests = None
        self.pipMapQuestsItems = dict()
        self.pipWorldLocations = None
        self.pipMapLocationItems = dict()
        self.poiLocationItems = dict()
        self.collectableLocationItems = dict()
        # Init Collectables
        self.showCollectables = {}

        self._signalPipWorldQuestsUpdated.connect(self._slotPipWorldQuestsUpdated)
        self._signalPipWorldLocationsUpdated.connect(self._slotPipWorldLocationsUpdated)
        self.datamanager.registerRootObjectListener(self._onRootObjectEvent)

    @QtCore.pyqtSlot(float, float, float)
    def saveZoom(self, zoom, mapposx, mapposy):
        self._app.settings.setValue('globalmapwidget/zoom', zoom)

    
    @QtCore.pyqtSlot(int, int)
    def _slotSplitterMoved(self, pos, index):
        self._app.settings.setValue('globalmapwidget/splitterState', settings.getSplitterState(self.widget.splitter))
    
    @QtCore.pyqtSlot(int)
    def _slotToolboxCurrentChanged(self, index):
        self._app.settings.setValue('globalmapwidget/toolboxCurrentIndex', index)
        
    def _connectMarker(self, marker):
        self.signalSetZoomLevel.connect(marker.setZoomLevel)
        self.signalSetColor.connect(marker.setColor)

        self.signalSetStickyLabel.connect(marker.setStickyLabel)
        self.signalMarkerForcePipValueUpdate.connect(marker._slotPipValueUpdated)
        marker.signalMarkerDestroyed.connect(self._disconnectMarker)
        self.signalSetLocationSize.connect(marker.setSize)
        if marker.markerType == 4:
            self.signalLocationFilterSetVisible.connect(marker.filterSetVisible)
            self.signalLocationFilterVisibilityCheat.connect(marker.filterVisibilityCheat)
        
    @QtCore.pyqtSlot(QtCore.QObject)
    def _disconnectMarker(self, marker):
        marker.signalMarkerDestroyed.disconnect(self._disconnectMarker)
        self.signalSetZoomLevel.disconnect(marker.setZoomLevel)
        self.signalSetStickyLabel.disconnect(marker.setStickyLabel)
        self.signalSetColor.disconnect(marker.setColor)
        self.signalMarkerForcePipValueUpdate.disconnect(marker._slotPipValueUpdated)
        self.signalSetLocationSize.disconnect(marker.setSize)
        if marker.markerType == 4:
            self.signalLocationFilterSetVisible.disconnect(marker.filterSetVisible)
            self.signalLocationFilterVisibilityCheat.disconnect(marker.filterVisibilityCheat)
            
            
    
    def _onRootObjectEvent(self, rootObject):
        self.pipMapObject = rootObject.child('Map')
        if self.pipMapObject:
            self.pipMapObject.registerValueUpdatedListener(self._onPipMapReset)
            self._onPipMapReset(None, None, None)
        self.pipPlayerObject = rootObject.child('PlayerInfo')
        if self.pipPlayerObject:
            self.pipPlayerObject.registerValueUpdatedListener(self._onPipPlayerReset)
            self._onPipPlayerReset(None, None, None)

    def _onPipPlayerReset(self, caller, value, pathObjs):
        if self.pipPlayerObject:
            name = self.pipPlayerObject.child('PlayerName')
            if name:
                self.pipPlayerName = name.value()
            
    def _onPipMapReset(self, caller, value, pathObjs):
        self.pipMapWorldObject = self.pipMapObject.child('World')
        if self.pipMapWorldObject:
            extents = self.pipMapWorldObject.child('Extents')
            if extents:
                self.mapCoords.init( 
                        extents.child('NWX').value(), extents.child('NWY').value(), 
                        extents.child('NEX').value(),  extents.child('NEY').value(), 
                        extents.child('SWX').value(), extents.child('SWY').value(), 
                        self.mapItem.nw[0], self.mapItem.nw[1], 
                        self.mapItem.ne[0], self.mapItem.ne[1], 
                        self.mapItem.sw[0], self.mapItem.sw[1] )
            else:
                self._logger.warn('No "Extents" record found. Map coordinates may be off')
            if self.widget.mapColorAutoToggle.isChecked():
                self._slotMapColorAutoModeTriggered(True)
            pipWorldPlayer = self.pipMapWorldObject.child('Player')
            if pipWorldPlayer:
                self.playerMarker.setPipValue(pipWorldPlayer, self.datamanager, self.mapCoords)
                self.playerMarker.setSavedSettings()
            pipWorldCustom = self.pipMapWorldObject.child('Custom')
            if pipWorldCustom:
                self.customMarker.setPipValue(pipWorldCustom, self.datamanager, self.mapCoords)
                self.customMarker.setSavedSettings()
            pipWorldPower = self.pipMapWorldObject.child('PowerArmor')
            if pipWorldPower:
                self.powerArmorMarker.setPipValue(pipWorldPower, self.datamanager, self.mapCoords)
                self.powerArmorMarker.setSavedSettings()
            self.pipWorldQuests = self.pipMapWorldObject.child('Quests')
            if self.pipWorldQuests:
                self.pipWorldQuests.registerValueUpdatedListener(self._onPipWorldQuestsUpdated, 0)
                self._signalPipWorldQuestsUpdated.emit()
            self.pipWorldLocations = self.pipMapWorldObject.child('Locations')
            if self.pipWorldLocations:
                self.pipWorldLocations.registerValueUpdatedListener(self._onPipWorldLocationsUpdated, 0)
                self._signalPipWorldLocationsUpdated.emit()

    def loadMarkerForCollectables(self):
        for i in self.collectableLocationItems:
            self.collectableLocationItems[i].destroy()

        self._logger.warn('Reloading CollectableMarkers')
        inputFile = open(os.path.join(self.basepath, 'res', 'collectables-processed.json'))
        collectables = json.load(inputFile)

        for k, v in collectables.items():
            self.collectableLocationItems[k] = {}
            chk = QtWidgets.QCheckBox()
            chk.setObjectName(k + '_CheckBox')
            chk.setText(v.get('friendlyname', k))
            chk.setChecked(bool(int(self._app.settings.value('globalmapwidget/show' + k, 0))))
            chk.stateChanged.connect(self.chkcollectableTriggered)
            self.widget.CollectablesLayout.addWidget(chk)

            for i in v.get('items', None):
                cmx = i.get('commonwealthx', None)
                cmy = i.get('commonwealthy', None)
                if cmx is not None and cmy is not None:
                    m = CollectableMarker(self,self.controller.sharedResImageFactory, QtCore.Qt.red, icon=v.get('icon', 'Starfilled.svg'))
                    m.setLabel(textwrap.fill(i.get('name', ''), 30) + '\n' + textwrap.fill(i.get('description', ''), 30))
                    m.setMapPos(self.mapCoords.pip2map_x(float(cmx)), self.mapCoords.pip2map_y(float(cmy)))
                    m.filterSetVisible(chk.isChecked())
                    m.setZoomLevel(self.mapZoomLevel, 0.0, 0.0, True)
                    self._connectMarker(m)

                    self.collectableLocationItems[k][i.get('name', str(uuid.uuid4()))] = m
        return

    @QtCore.pyqtSlot(bool)
    def chkcollectableTriggered(self, value):
        for k in self.collectableLocationItems.keys():
            chk = self.widget.findChild(QtWidgets.QCheckBox, k + '_CheckBox')

            if chk.isChecked():
                self._app.settings.setValue('globalmapwidget/show' + k, 1)
                self.showCollectables[k] = True
                for i,j in self.collectableLocationItems[k].items():
                    j.filterSetVisible(True)
            else:
                self._app.settings.setValue('globalmapwidget/show' + k, 0)
                self.showCollectables[k] = False
                for i,j in self.collectableLocationItems[k].items():
                    j.filterSetVisible(False)

    def _onPipWorldQuestsUpdated(self, caller, value, pathObjs):
        self._signalPipWorldQuestsUpdated.emit()
        
    @QtCore.pyqtSlot() 
    def _slotPipWorldQuestsUpdated(self):
        newDict = dict()
        for q in self.pipWorldQuests.value():
            if q.pipId in self.pipMapQuestsItems:
                marker = self.pipMapQuestsItems[q.pipId]
                newDict[q.pipId] = marker
                del self.pipMapQuestsItems[q.pipId]
            else:
                marker = QuestMarker(self,self.controller.imageFactory, self.mapColor)
                self._connectMarker(marker)
                marker.setStickyLabel(self.stickyLabelsEnabled, False)
                marker.setZoomLevel(self.mapZoomLevel, 0.0, 0.0, False)
                marker.setPipValue(q, self.datamanager, self.mapCoords)
                marker.setSavedSettings()
                newDict[q.pipId] = marker
        for i in self.pipMapQuestsItems:
            self.pipMapQuestsItems[i].destroy()
        self.pipMapQuestsItems = newDict
                    
    def _onPipWorldLocationsUpdated(self, caller, value, pathObjs):
        self._signalPipWorldLocationsUpdated.emit()

    @QtCore.pyqtSlot() 
    def _slotPipWorldLocationsUpdated(self):
        newDict = dict()
        for l in self.pipWorldLocations.value():
            if l.pipId in self.pipMapLocationItems:
                marker = self.pipMapLocationItems[l.pipId]
                newDict[l.pipId] = marker
                del self.pipMapLocationItems[l.pipId]
            else:
                marker = LocationMarker(self, self.controller.imageFactory, self.controller.globalResImageFactory, self.mapColor,self.locMarkSize)

                self._connectMarker(marker)

                marker.setZoomLevel(self.mapZoomLevel, 0.0, 0.0, False)
                marker.filterSetVisible(self.locationFilterEnableFlag, False)
                marker.filterVisibilityCheat(self.locationVisibilityCheatFlag, False)
                marker.setPipValue(l, self.datamanager, self.mapCoords)
                marker.setStickyLabel(self.stickyLabelsEnabled, False)
                marker.setSize(self.locMarkSize,False)
                marker.setSavedSettings()

                #convert old coord indexed notes and stickies to new uid indexed from
                #and remove old entries - remove this block in vNext (0.9?)
                if (marker.uid != None):
                    rx = l.child('X').value()
                    ry = l.child('Y').value()

                    if not marker.stickyLabel:
                        oldsavedsticky =  bool(int(self._app.settings.value('globalmapwidget/stickylabels/'+str(rx)+','+str(ry), 0)))
                        if oldsavedsticky:
                            marker.setStickyLabel(oldsavedsticky, True)
                            self._app.settings.setValue('globalmapwidget/stickylabels2/'+marker.uid, 1)
                            self._app.settings.remove('globalmapwidget/stickylabels/'+str(rx)+','+str(ry))
                    
                    if (len(marker.note) == 0):
                        marker.setNote (self._app.settings.value('globalmapwidget/locationnotes/'+str(rx)+','+str(ry), ''))
                        if (len(marker.note) > 0):
                            self._app.settings.setValue('globalmapwidget/locationmarkernotes/'+marker.uid, marker.note)
                            self._app.settings.remove('globalmapwidget/locationnotes/'+str(rx)+','+str(ry))


                self._app.settings.beginGroup("globalmapwidget/locationnotes");
                if len(self._app.settings.childKeys()) == 0 :
                    self._app.settings.remove(''); 
                self._app.settings.endGroup();

                self._app.settings.beginGroup("globalmapwidget/stickylabels");
                if len(self._app.settings.childKeys()) == 0 :
                    self._app.settings.remove(''); 
                self._app.settings.endGroup();
                #end convert and clean up - remove this block in vNext (0.9?)
                        
                        
                newDict[l.pipId] = marker
        for i in self.pipMapLocationItems:
            self.pipMapLocationItems[i].destroy()

        for i in self.poiLocationItems:
            self.poiLocationItems[i].destroy()
            
        poisettingPath = 'globalmapwidget/pointsofinterest/'
        index = self._app.settings.value(poisettingPath+'index', None)
        poiLocDict = dict()
        if index and len(index) > 0:
            for i in index:
                poimarker = PointofInterestMarker(i,self,self.controller.sharedResImageFactory, self.mapColor)
                poimarker.thisCharOnly = False
                poimarker.setSavedSettings()
                poimarker.filterSetVisible(True)
                poimarker.setZoomLevel(self.mapZoomLevel, 0.0, 0.0, True)
                self._connectMarker(poimarker)
                poiLocDict[str(i)] = poimarker

        if self.pipPlayerName:
            index = self._app.settings.value(poisettingPath+ self.pipPlayerName +'/index', None)
            if index and len(index) > 0:
                for i in index:
                    poimarker = PointofInterestMarker(i,self,self.controller.sharedResImageFactory, self.mapColor)
                    poimarker.thisCharOnly = True
                    poimarker.setSavedSettings()
                    poimarker.filterSetVisible(True)
                    poimarker.setZoomLevel(self.mapZoomLevel, 0.0, 0.0, True)
                    self._connectMarker(poimarker)
                    poiLocDict[str(i)] = poimarker

                
        self.pipMapLocationItems = newDict
        self.poiLocationItems = poiLocDict
        
        self.loadMarkerForCollectables()
        
        self._signalPipWorldQuestsUpdated.emit()

    @QtCore.pyqtSlot()        
    def _slotMapColorSelectionTriggered(self):
        color = QtWidgets.QColorDialog.getColor(self.mapColor, self)
        if color.isValid and color.value() != QtGui.QColor.fromRgb(0,0,0).value():
            self.mapColor = color
            self._app.settings.setValue('globalmapwidget/colour', color)
            self.widget.mapColorAutoToggle.setChecked(False)
            self.signalSetColor.emit(color)
    
    
    @QtCore.pyqtSlot(int)
    def _slotMapFileComboTriggered(self, index):
        mapfile = self.mapFiles[self.mapFileComboItems[index]]
        if not mapfile:
            self._logger.error('Could not find map "' + self.selectedMapFile + '".')
        else:
            self.selectedMapFile = self.mapFileComboItems[index]
            file = os.path.join('res', mapfile['file'])
            self.mapItem.setMapFile(file, mapfile['colorable'], mapfile['nw'], mapfile['ne'], mapfile['sw'])
            if self.pipMapWorldObject:
                extents = self.pipMapWorldObject.child('Extents')
                if extents:
                    self.mapCoords.init( 
                            extents.child('NWX').value(), extents.child('NWY').value(), 
                            extents.child('NEX').value(),  extents.child('NEY').value(), 
                            extents.child('SWX').value(), extents.child('SWY').value(), 
                            self.mapItem.nw[0], self.mapItem.nw[1], 
                            self.mapItem.ne[0], self.mapItem.ne[1], 
                            self.mapItem.sw[0], self.mapItem.sw[1] )
                else:
                    self._logger.warn('No "Extents" record found. Map coordinates may be off')
            self.signalMarkerForcePipValueUpdate.emit()
            self._app.settings.setValue('globalmapwidget/selectedMapFile', self.selectedMapFile)



    @QtCore.pyqtSlot(int)        
    def _slotZoomSliderTriggered(self, zoom):
        if zoom == 0:
            mod = 0.0
        elif zoom > 0:
            mod = (self.MAPZOOM_SCALE_MAX - 1) * float(zoom)/100.0
        else:
            mod = (1 -self.MAPZOOM_SCALE_MIN) * float(zoom)/100.0
        viewport = self.mapView.mapToScene(self.mapView.rect())
        centerpos = (viewport.at(2) + viewport.at(0))/2 # (SE + NW)/2
        mcenterpos = centerpos / self.mapZoomLevel # account for previous zoom 
        self.mapZoomLevel = 1+mod
        self.widget.mapZoomSpinbox.blockSignals(True)
        self.widget.mapZoomSpinbox.setValue(self.mapZoomLevel*100.0)
        self.widget.mapZoomSpinbox.blockSignals(False)
        self.signalSetZoomLevel.emit(self.mapZoomLevel, mcenterpos.x(), mcenterpos.y())




    @QtCore.pyqtSlot(float)
    def _slotZoomSpinTriggered(self, zoom):
        viewport = self.mapView.mapToScene(self.mapView.rect())
        centerpos = (viewport.at(2) + viewport.at(0))/2 # (SE + NW)/2
        mcenterpos = centerpos / self.mapZoomLevel # account for previous zoom 
        self.mapZoomLevel = zoom/100.0
        if self.mapZoomLevel == 1.0:
            sliderValue = 0
        elif self.mapZoomLevel > 1.0:
            sliderValue = (self.mapZoomLevel/self.MAPZOOM_SCALE_MAX)*100.0
        else:
            sliderValue = -(self.MAPZOOM_SCALE_MIN/self.mapZoomLevel)*100.0
        self.widget.mapZoomSlider.blockSignals(True)
        self.widget.mapZoomSlider.setValue(sliderValue)
        self.widget.mapZoomSlider.blockSignals(False)
        self.signalSetZoomLevel.emit(self.mapZoomLevel, mcenterpos.x(), mcenterpos.y())
        
    @QtCore.pyqtSlot(int)
    def _slotlocationMarkerSizeSliderTriggered (self,size):
        self.widget.locationMarkerSizeSpinbox.blockSignals(True)
        self.widget.locationMarkerSizeSpinbox.setValue(size)
        self.widget.locationMarkerSizeSpinbox.blockSignals(False)
        self._app.settings.setValue('globalmapwidget/locationMarkeSize', size)
        self.locMarkSize = size

        self.signalSetLocationSize.emit(size)

    @QtCore.pyqtSlot(int)
    def _slotlocationMarkerSizeSpinboxTriggered (self,size):
        self.widget.locationMarkerSizeSlider.blockSignals(True)
        self.widget.locationMarkerSizeSlider.setValue(size)
        self.widget.locationMarkerSizeSlider.blockSignals(False)
        self.locMarkSize = size
        self._app.settings.setValue('globalmapwidget/locationMarkeSize', size)
        self.signalSetLocationSize.emit(size)

    @QtCore.pyqtSlot(bool)
    def _slotStickyLabelsTriggered(self, value):
        self.stickyLabelsEnabled = value
        self._app.settings.setValue('globalmapwidget/stickyLabels', int(value))
        self.signalSetStickyLabel.emit(value)
        
    @QtCore.pyqtSlot(bool)        
    def _slotPowerMarkerEnableTriggered(self, value):
        self.powerArmorMarker.filterSetVisible(value)
        self._app.settings.setValue('globalmapwidget/powerArmourMarker', int(value))
        
    @QtCore.pyqtSlot(bool)        
    def _slotLocationEnableTriggered(self, value):
        self.locationFilterEnableFlag = value
        self._app.settings.setValue('globalmapwidget/locationMarker', int(value))
        self.signalLocationFilterSetVisible.emit(value)
        
    @QtCore.pyqtSlot(bool)        
    def _slotLocationVisibilityCheatTriggered(self, value):
        self.locationVisibilityCheatFlag = value
        self._app.settings.setValue('globalmapwidget/locationVisibilityCheat', int(value))
        self.signalLocationFilterVisibilityCheat.emit(value)
        
    @QtCore.pyqtSlot(bool)        
    def _slotCenterOnPlayerCheckToggled(self, value):
        self.centerOnPlayerEnabled = value
        self._app.settings.setValue('globalmapwidget/centerPlayer', int(value))
        if value and self.playerMarker.markerItem.isVisible():
            self.playerMarker.mapCenterOn()
            
    @QtCore.pyqtSlot(float, float, float)        
    def _slotPlayerMarkerPositionUpdated(self, x, y, r):
        if self.centerOnPlayerEnabled:
            self.playerMarker.mapCenterOn()
        
    @QtCore.pyqtSlot(bool)        
    def _slotMapColorAutoModeTriggered(self, value):
        self._app.settings.setValue('globalmapwidget/autoColour', int(value))
        if self.pipMapObject:
            if value:
                self.pipColor = self.pipMapObject.pipParent.child('Status').child('EffectColor')
                self.pipColor.registerValueUpdatedListener(self._onPipColorChanged, 1)
                self._onPipColorChanged(None, None, None)
            elif self.pipColor:
                self.pipColor.unregisterValueUpdatedListener(self._onPipColorChanged)
                r = self.pipColor.child(0).value() * 255
                g = self.pipColor.child(1).value() * 255
                b = self.pipColor.child(2).value() * 255
                pipColor = QtGui.QColor.fromRgb(r,g,b)
                self.signalSetColor.emit(pipColor)

        
    @QtCore.pyqtSlot()
    def _slotSaveToTriggered(self):
        fileName = QtWidgets.QFileDialog.getSaveFileName(self, '', '', 'Images (*.png *.jpg *.gif)')
        if fileName:
            pixmap = self.mapView.grab()
            pixmap.save(fileName[0])
            
    def _onPipColorChanged(self, caller, value, pathObjs):
        if self.pipColor:
            r = self.pipColor.child(0).value() * 255
            g = self.pipColor.child(1).value() * 255
            b = self.pipColor.child(2).value() * 255
            self.mapColor = QtGui.QColor.fromRgb(r,g,b)
            self.signalSetColor.emit(self.mapColor)

    def eventFilter(self, watched, event):
        if watched == self.mapView.viewport():
            if event.type() == QtCore.QEvent.Wheel:
                # Zoom to center
                viewport = self.mapView.mapToScene(self.mapView.rect())
                centerpos = (viewport.at(2) + viewport.at(0))/2 # (SE + NW)/2
                vcenterpos = centerpos / self.mapZoomLevel # account for previous zoom 
                # Sometimes I get strange angle readings (especially after mouse move)
                #zoom = self.mapZoomLevel + event.angleDelta().y()/120 * 0.1
                if event.angleDelta().y() > 0:
                    zoom = self.mapZoomLevel * 1.1
                else:
                    zoom = self.mapZoomLevel * 0.9
                if zoom < self.MAPZOOM_SCALE_MIN:
                    zoom = self.MAPZOOM_SCALE_MIN
                elif zoom > self.MAPZOOM_SCALE_MAX:
                    zoom = self.MAPZOOM_SCALE_MAX
                if self.mapZoomLevel != zoom:
                    self.mapZoomLevel = zoom
                    if self.mapZoomLevel == 1.0:
                        sliderValue = 0
                    elif self.mapZoomLevel > 1.0:
                        sliderValue = (self.mapZoomLevel/self.MAPZOOM_SCALE_MAX)*100.0
                    else:
                        sliderValue = -(self.MAPZOOM_SCALE_MIN/self.mapZoomLevel)*100.0
                    self.widget.mapZoomSlider.blockSignals(True)
                    self.widget.mapZoomSlider.setValue(sliderValue)
                    self.widget.mapZoomSlider.blockSignals(False)
                    self.widget.mapZoomSpinbox.blockSignals(True)
                    self.widget.mapZoomSpinbox.setValue(self.mapZoomLevel*100.0)
                    self.widget.mapZoomSpinbox.blockSignals(False)
                    self.signalSetZoomLevel.emit(self.mapZoomLevel, vcenterpos.x(), vcenterpos.y())
                return True
            elif event.type() == QtCore.QEvent.ContextMenu:
                if self.mapCoords.isValid:
                    menu = QtWidgets.QMenu(self.mapView)
                    markerPos = self.mapView.mapToScene(event.pos())
                    # Check whether we clicked on a marker
                    if self.mapScene.itemAt(markerPos, QtGui.QTransform()) != self.mapItem.mapItem:
                        return False
                    markerPos = markerPos/self.mapZoomLevel # Account for zoom
                    @QtCore.pyqtSlot()
                    def _setCustomMarker():
                        self.datamanager.rpcSetCustomMarker(self.mapCoords.map2pip_x(markerPos.x()), self.mapCoords.map2pip_y(markerPos.y()))
                    action = menu.addAction('Set Custom Marker')
                    action.triggered.connect(_setCustomMarker)

                    @QtCore.pyqtSlot()
                    def _setPoiLocationMarker():
                        rx = self.mapCoords.map2pip_x(markerPos.x())
                        ry = self.mapCoords.map2pip_y(markerPos.y())
                        labelstr = ''
                        


                        editpoiDialog = EditPOIDialog(self, color=self.mapColor)
                        editpoiDialog.txtPOILabel.setText(labelstr)
                        editpoiDialog.chkCharacterOnly.setText(editpoiDialog.chkCharacterOnly.text() + '(' +self.pipPlayerName +')')
                        ok = editpoiDialog.exec_()
                        labelstr = editpoiDialog.txtPOILabel.text()
                        editpoiDialog.show()
                        thisCharOnly = editpoiDialog.chkCharacterOnly.isChecked()
                        
                        if (ok != 0):
                            poimarker = PointofInterestMarker(uuid.uuid4(), self,self.controller.sharedResImageFactory, editpoiDialog.selectedColor, editpoiDialog.IconFile)
                            poimarker.setLabel(labelstr)
                            self._connectMarker(poimarker)
                            poimarker.setMapPos(self.mapCoords.pip2map_x(rx), self.mapCoords.pip2map_y(ry))
                            poimarker.setZoomLevel(self.mapZoomLevel, 0.0, 0.0, False)
                            poimarker.filterSetVisible(True)
                            poimarker.setStickyLabel(True, True)
                            poimarker.thisCharOnly = thisCharOnly
                            
                            markerKey = poimarker.uid
                            self.poiLocationItems[markerKey] = poimarker
                        
                            poiSettingPath = 'globalmapwidget/pointsofinterest/' 
                            if thisCharOnly:
                                poiSettingPath = poiSettingPath + self.pipPlayerName +'/'

                            index = self._app.settings.value(poiSettingPath+'index', None)
                            if index == None: 
                                index = []
                            
                            index.append(str(markerKey))
                                
                            self._app.settings.setValue(poiSettingPath+'index', index)
                            
                            self._app.settings.setValue(poiSettingPath+str(markerKey)+'/worldx', rx)
                            self._app.settings.setValue(poiSettingPath+str(markerKey)+'/worldy', ry)
                            self._app.settings.setValue(poiSettingPath+str(markerKey)+'/label', labelstr)
                            self._app.settings.setValue(poiSettingPath+str(markerKey)+'/color', editpoiDialog.selectedColor)
                            self._app.settings.setValue(poiSettingPath+str(markerKey)+'/icon', editpoiDialog.IconFile)

                            settingPath = 'globalmapwidget/stickylabels2/'
                            self._app.settings.setValue(settingPath+markerKey, int(True))                                
                        return

                    menu.addAction('Add Point of Interest', _setPoiLocationMarker)


                    menu.exec(event.globalPos())
                return True
            elif event.type() == QtCore.QEvent.MouseButtonDblClick:
                
                if self.mapCoords.isValid:
                    markerPos = self.mapView.mapToScene(event.pos())
                    # Check whether we clicked on a marker
                    if self.mapScene.itemAt(markerPos, QtGui.QTransform()) != self.mapItem.mapItem:
                        return False
                    markerPos = markerPos/self.mapZoomLevel # Account for zoom
                    self.datamanager.rpcSetCustomMarker(self.mapCoords.map2pip_x(markerPos.x()), self.mapCoords.map2pip_y(markerPos.y()))
                return True
        return False
    
    
    def iwcCenterOnLocation(self, pipId):
        try:
            loc = self.pipMapLocationItems[pipId]
            loc.mapCenterOn()
        except:
            pass
    
    # CENTER MAP ON QUEST MARKER
    # formId - int - Quest formID value
    def iwcCenterOnQuest(self, formId):
        Quest = None
        
        if self.pipMapQuestsItems:
            def _searchForQuest():
                for QuestItem in self.pipMapQuestsItems:
                    for QuestFormId in self.pipMapQuestsItems[QuestItem].QuestFormIds:
                        if QuestFormId.value() == formId:
                            return self.pipMapQuestsItems[QuestItem]
            Quest = _searchForQuest()
        
        if Quest:
            Quest.mapCenterOn()


                            