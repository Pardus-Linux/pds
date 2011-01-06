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

        self.icon.setPixmap(get_icon(connection.settings.conn_type, state))
        self.name.setText(unicode(connection.settings.id))
        self.details.setText(unicode(connection.settings.conn_type))

        if state:
            self.button.setText("Disconnect")

        self.button.clicked.connect(lambda: parent.show_message("%s clicked." % self.name.text()))
        self.toggleButtons()

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

    def fillConnections(self):
        actives = self.nm.active_connections
        for connection in self.nm.connections:
            state = map(
                    lambda x: connection.proxy.object_path == \
                            x.connection.proxy.object_path, actives)[0]
            item = QtGui.QListWidgetItem()
            item.setSizeHint(QSize(200, 38))
            self.addItem(item)
            self.setItemWidget(item, ConnectionItem(self, connection, state))

    def show_message(self, message):
        if not self.msgbox:
            self.msgbox = PMessageBox(self)
            self.msgbox.setStyleSheet(PMessageBox.Style)

        token = False
        if self.msgbox.isVisible():
            token = self.msgbox.animate(start = CURRENT, stop = BOTCENTER, direction = OUT)
            self.msgbox.registerFunction(FINISHED, lambda: self.msgbox.setMessage(message))

        if not token:
            self.msgbox.setMessage(message)
        self.msgbox.animate(start = BOTCENTER, stop = BOTCENTER, start_after = token)

# Basic test app
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    nm = QNetworkManager()
    nm.show()
    sys.exit(app.exec_())

