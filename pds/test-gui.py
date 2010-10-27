# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

from PyQt4 import QtCore, QtGui
from pds.gui import *
from pds.progress import Ui_ProgressDialog
from pds.new import Ui_Form

class PWidgetbox(PAbstractBox):
    def __init__(self, parent, widget):
        PAbstractBox.__init__(self, parent)
        ui = widget()
        ui.setupUi(self)
        self.enableOverlay(True)
        self._animation = 38

    def showAnimated(self):
        self.animate(start = TOPCENTER, stop = BOTCENTER)

    def hideAnimated(self):
        self.animate(start = CURRENT, stop = TOPCENTER, direction = OUT)

class PInfoBox(PAbstractBox):
    def __init__(self, parent=None):
        PAbstractBox.__init__(self, parent)
        self.label = QtGui.QLabel('Hello World !', self)

class Ui_Form2(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(743, 487)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.line = QtGui.QLineEdit(Form)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.button = QtGui.QPushButton(Form)
        self.button2 = QtGui.QPushButton(Form)
        self.button3 = QtGui.QPushButton(Form)
        self.button.setObjectName("button")
        self.gridLayout.addWidget(self.button, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.button2, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.button3, 0, 4, 1, 1)
        self.webView = QtWebKit.QWebView(Form)
        self.webView.setUrl(QtCore.QUrl("http://developer.pardus.org.tr/"))
        self.webView.setObjectName("webView")
        self.gridLayout.addWidget(self.webView, 1, 0, 1, 5)

        self.retranslateUi(Form)

        self.info = PWidgetbox(Form, Ui_Form)
        self.msg = PMessageBox(self.webView)
        self.button.clicked.connect(self.info.showAnimated)
        self.button2.clicked.connect(self.info.hideAnimated)
        self.button3.clicked.connect(lambda:self.msg.showMessage('PDS Rocks !'))

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle("Form")
        self.line.setText("This is a test message from PDS GUI !")
        self.button.setText("Show Message")
        self.button2.setText("Hide Message")
        self.button3.setText("Message")

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form2()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

