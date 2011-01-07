#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2011, TUBITAK/UEKAE
# 2011 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# D-Bus
import dbus
from dbus.mainloop.qt import DBusQtMainLoop

# Qt Libraries
from PyQt4 import QtGui
from PyQt4.QtCore import *

# UI
from pds.ui_connectionitem import Ui_ConnectionItem

# Pds
from pds.gui import *
from pds.qiconloader import QIconLoader
from pds.qprogressindicator import QProgressIndicator

QIconLoader = QIconLoader()

# NetworkManager
from networkmanager import State
from networkmanager import NetworkManager
from networkmanager import ActiveConnectionState

NM_BUS_NAME = 'org.freedesktop.NetworkManager'
NM_OBJECT_PATH = '/org/freedesktop/NetworkManager'
NM_INTERF_NAME = 'org.freedesktop.NetworkManager'

def get_icon(conn_type, state = False):
    state = "dialog-ok" if state else None

    CONN_TYPES = {"802-11-wireless":
                    QIconLoader.loadOverlayed("network-wireless", state, 32, position = QIconLoader.TopLeft),
                  "802-3-ethernet" :
                    QIconLoader.loadOverlayed("network-wired", state, 32, position = QIconLoader.TopLeft)}

    return CONN_TYPES.get(conn_type,
                QIconLoader.loadOverlayed("network-wired", state, 32, position = QIconLoader.TopLeft))

class ConnectionItem(QtGui.QWidget, Ui_ConnectionItem):

    def __init__(self, parent, connection):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.parent = parent
        self.connection = connection

        self.busy = QProgressIndicator(self)
        self.busy.setMinimumSize(QSize(32, 32))
        self.mainLayout.insertWidget(0, self.busy)
        self.busy.hide()

        self.connect(parent, SIGNAL("stateChanged()"), self.updateState)
        self.button.clicked.connect(lambda: self.parent.setState(self))

        self.updateState()
        self.toggleButtons()

    def updateState(self):
        active = self.parent.isActive(self.connection)

        if active:
            state = self.parent.getState(self.connection)
            if state == ActiveConnectionState.ACTIVATED.value:
                self.setIcon(get_icon(self.connection.settings.conn_type, True))
            elif state == ActiveConnectionState.ACTIVATING.value:
                self.showBusy()
        else:
            self.setIcon(get_icon(self.connection.settings.conn_type, False))

        self.name.setText(unicode(self.connection.settings.id))
        self.details.setText(unicode(self.connection.settings.conn_type))
        self.button.setText("Disconnect" if active else "Connect")

    def showBusy(self):
        self.busy.busy()
        self.icon.hide()

    def setIcon(self, icon):
        self.busy.hide()
        self.icon.setPixmap(icon)
        self.icon.show()

    def resizeEvent(self, event):
        if self.parent.msgbox:
            self.parent.msgbox._resizeCallBacks(event)

    def enterEvent(self, event):
        if not self.button.isVisible():
            self.toggleButtons(True)

    def leaveEvent(self, event):
        if self.button.isVisible():
            self.toggleButtons()

    def toggleButtons(self, toggle=False):
        self.button.setVisible(toggle)

class QNetworkManager(QtGui.QListWidget):

    def __init__(self, parent = None):
        QtGui.QListWidget.__init__(self, parent)
        self.setAlternatingRowColors(True)

        self.nm = NetworkManager()
        self.bus = dbus.SystemBus()

        self.nm_dbus = self.bus.get_object(NM_BUS_NAME, NM_OBJECT_PATH)
        self.nm_interface = dbus.Interface(self.nm_dbus, NM_INTERF_NAME)
        self.nm_interface.connect_to_signal("PropertiesChanged", self.handler)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hideMessage)

        self.msgbox = None
        self.fillConnections()

    def handler(self, *args):
        self.emit(SIGNAL("stateChanged()"))
        print 'DEBUG:', args

    def isActive(self, connection):
        if not self.nm.active_connections:
            return False
        return len(filter(lambda x: x.connection.settings.uuid == \
                                      connection.settings.uuid, self.nm.active_connections)) > 0

    def getState(self, connection):
        return filter(lambda x: x.connection.settings.uuid == \
                                  connection.settings.uuid, self.nm.active_connections)[0].state.value

    def fillConnections(self):
        actives = self.nm.active_connections
        for connection in self.nm.connections:
            item = QtGui.QListWidgetItem()
            item.setSizeHint(QSize(200, 38))
            self.addItem(item)
            self.setItemWidget(item, ConnectionItem(self, connection))

    def hideMessage(self):
        if self.msgbox.isVisible():
            return self.msgbox.animate(start = CURRENT, stop = BOTCENTER, direction = OUT)

    def showMessage(self, message, timed=False):
        if not self.msgbox:
            self.msgbox = PMessageBox(self.viewport())
            self.msgbox.setStyleSheet(PMessageBox.Style)

        self.msgbox.setMessage(message)
        self.msgbox.animate(start = BOTCENTER, stop = BOTCENTER)

        if timed:
            self.timer.start(2000)

    def setState(self, sender):
        if self.isActive(sender.connection):
            self.disconnect(sender.connection)
        else:
            self.connect(sender.connection)

    def disconnect(self, connection):
        self.nm.disconnect_connection_devices(connection)
        self.showMessage("Disconnected from %s... " % connection.settings.id, True)

    def connect(self, connection):
        self.nm.activate_connection(connection, guess_device = True)
        self.showMessage("Connecting to %s... " % connection.settings.id, True)

# Basic test app
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DBusQtMainLoop(set_as_default = True)
    nm = QNetworkManager()
    nm.show()
    sys.exit(app.exec_())

