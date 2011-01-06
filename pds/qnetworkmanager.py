#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2011, TUBITAK/UEKAE
# 2011 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Qt Libraries
from PyQt4 import QtGui
from PyQt4.QtCore import *

# UI
from pds.ui_connectionitem import Ui_ConnectionItem

# Pds
from pds.gui import *
from pds.qiconloader import QIconLoader
QIconLoader = QIconLoader()

# NetworkManager
from networkmanager import NetworkManager
from networkmanager import ActiveConnection

def get_icon(conn_type, state = False):
    state = "dialog-ok" if state else None

    CONN_TYPES = {"802-11-wireless":
                    QIconLoader.loadOverlayed("network-wireless", state, 32, position = QIconLoader.TopLeft),
                  "802-3-ethernet" :
                    QIconLoader.loadOverlayed("network-wired", state, 32, position = QIconLoader.TopLeft)}

    return CONN_TYPES.get(conn_type,
                QIconLoader.loadOverlayed("network-wired", state, 32, position = QIconLoader.TopLeft))

class ConnectionItem(QtGui.QWidget, Ui_ConnectionItem):

    def __init__(self, parent, connection, state):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.connection = connection

        self.icon.setPixmap(get_icon(connection.settings.conn_type, state))
        self.name.setText(unicode(connection.settings.id))
        self.details.setText(unicode(connection.settings.conn_type))

        if state:
            self.button.setText("Disconnect")

        self.button.clicked.connect(lambda: self.parent.setState(self))
        self.toggleButtons()

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

        self.msgbox = None
        self.fillConnections()

    def isActive(self, connection):
        if not self.nm.active_connections:
            return False
        return map(lambda x: connection.settings.uuid == \
                          x.connection.settings.uuid, self.nm.active_connections)[0]

    def fillConnections(self):
        actives = self.nm.active_connections
        for connection in self.nm.connections:
            state = self.isActive(connection)
            item = QtGui.QListWidgetItem()
            item.setSizeHint(QSize(200, 38))
            self.addItem(item)
            self.setItemWidget(item, ConnectionItem(self, connection, state))

    def hideMessage(self):
        if self.msgbox.isVisible():
            return self.msgbox.animate(start = CURRENT, stop = BOTCENTER, direction = OUT)

    def showMessage(self, message, timed=False):
        if not self.msgbox:
            self.msgbox = PMessageBox(self.viewport())
            self.msgbox.setStyleSheet(PMessageBox.Style)

        token = False
        if self.msgbox.isVisible():
            token = self.hideMessage()
            self.msgbox.registerFunction(FINISHED, lambda: self.msgbox.setMessage(message))

        if not token:
            self.msgbox.setMessage(message)

        self.msgbox.animate(start = BOTCENTER, stop = BOTCENTER, start_after = token)

        if timed:
            QTimer.singleShot(2000, self.hideMessage)

    def setState(self, sender):
        if self.isActive(sender.connection):
            self.disconnect(sender.connection)
            self.showMessage("Disconnecting %s..." % sender.connection.settings.id, True)
        else:
            self.connect(sender.connection)
            self.showMessage("Connecting %s... " % sender.connection.settings.id)

    def disconnect(self, connection):
        self.nm.disconnect_connection_devices(connection)

    def connect(self, connection):
        self.nm.activate_connection(connection, guess_device = True)

# Basic test app
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    nm = QNetworkManager()
    nm.show()
    sys.exit(app.exec_())

