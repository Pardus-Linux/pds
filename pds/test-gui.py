#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# GUI Test Script ~ test-gui.py

# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

from PyQt4 import QtGui
from PyQt4 import QtCore

class Ui_Form(object):
    def setupUi(self, Form):
        Form.resize(516, 364)
        self.gridLayout = QtGui.QGridLayout(Form)
        spacerItem = QtGui.QSpacerItem(20, 276, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(217, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.button = QtGui.QPushButton(Form)
        self.button.setText('Click')
        self.gridLayout.addWidget(self.button, 1, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(217, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 2, 1, 1, 1)


class PTest(QtGui.QWidget, Ui_Form):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    obj = PTest()
    obj.show()
    sys.exit(app.exec_())

