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
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QRect
from PyQt4.QtCore import QEvent

from PyQt4.QtGui import QFrame
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QScrollArea
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QPushButton

class Page:
    def __init__(self, widget, inMethod = None, outMethod = None):
        self.widget    = widget
        self.inMethod  = inMethod
        self.outMethod = outMethod

class QPageWidget(QScrollArea):
    def __init__(self, parent = None):
        QScrollArea.__init__(self, parent)

        self.setFrameShape(QFrame.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.widget = QWidget(self)
        self.layout = QHBoxLayout(self.widget)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)

        self.pages = []
        self.current = 0
        self.setWidget(self.widget)

    def addPage(self, widget, inMethod = None, outMethod = None):
        widget.setMinimumSize(self.size())
        self.pages.append(Page(widget, inMethod, outMethod))
        self.layout.addWidget(widget)

    def next(self):
        self.current = max(0, min(self.current + 1, len(self.pages)))
        self.horizontalScrollBar().setValue(self.current * self.width())

    def prev(self):
        self.current = min(len(self.pages), max(self.current - 1, 0))
        self.horizontalScrollBar().setValue(self.current * self.width())

    def event(self, event):
        if event.type() == QEvent.Resize:
            for page in self.pages:
                page.widget.setMinimumSize(self.size())
        return QWidget.event(self, event)

    def keyPressEvent(self, event):
        pass

    def wheelEvent(self, event):
        pass

# Basic test app
class Test(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.layout = QHBoxLayout(self)

        pageWidget = QPageWidget(self)
        self.layout.addWidget(pageWidget)

        btnNext = QPushButton("Next", self)
        self.layout.addWidget(btnNext)
        btnNext.clicked.connect(pageWidget.next)

        btnPrev = QPushButton("Prev", self)
        self.layout.addWidget(btnPrev)
        btnPrev.clicked.connect(pageWidget.prev)

        for color in ('red', 'green', 'blue'):
            widget = QWidget()
            widget.setStyleSheet("background-color:%s" % color)
            pageWidget.addPage(widget)

if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication

    app = QApplication(sys.argv)
    testWidget = Test()
    testWidget.show()

    sys.exit(app.exec_())

