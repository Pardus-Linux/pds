# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from pds.qpagewidget import QPageWidget

class DemoPage(QWidget):
    def __init__(self, parent = None, text = '', line_edit = ''):
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel(text, self))

        self.line = QLineEdit(line_edit, self)
        self.layout.addWidget(self.line)
        if not line_edit:
            self.line.hide()

        btnNext = QPushButton("Next", self)
        self.layout.addWidget(btnNext)
        btnNext.clicked.connect(lambda: self.emit(SIGNAL("pageNext()")))

        btnPrev = QPushButton("Previous", self)
        self.layout.addWidget(btnPrev)
        btnPrev.clicked.connect(lambda: self.emit(SIGNAL("pagePrevious()")))

    def text(self):
        return self.line.text()

# Basic test app
class Test(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.layout = QHBoxLayout(self)

        pageWidget = QPageWidget(self)
        self.layout.addWidget(pageWidget)

        pageWidget.createPage(DemoPage(text="Welcome to QPageWidget demo !"))

        for color in ('red', 'green', 'blue'):
            widget = DemoPage(text="%s colored page..." % color)
            widget.setStyleSheet("background-color:%s" % color)
            pageWidget.createPage(widget)

        line = DemoPage(text="You can embed all QWidgets as QPage, like QLineEdit", line_edit="Hello World")
        pageWidget.createPage(line)

        button = QPushButton("Click Me !", self)
        button.clicked.connect(lambda: QMessageBox.information(self,
                                "QPageWidget Information", line.text()))
        button.clicked.connect(lambda: button.emit(SIGNAL("setCurrent(int)"), 0))

        pageWidget.createPage(button, inMethod=lambda: QMessageBox.information(self, "QPageWidget Information", 
                                                        "This is a Test"))

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    testWidget = Test()
    testWidget.show()

    sys.exit(app.exec_())

