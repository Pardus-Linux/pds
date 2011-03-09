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
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QTimeLine
from PyQt4.QtCore import QEasingCurve

from PyQt4.QtGui import QFrame
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QScrollArea
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QMessageBox

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

        self.__tmp_page = Page(QWidget(self.widget))
        self.pages = [self.__tmp_page]

        self.current = 0
        self.setWidget(self.widget)

        self.__timeline = QTimeLine()
        self.__timeline.setUpdateInterval(2)

        self.__timeline.frameChanged.connect(lambda x: self.horizontalScrollBar().setValue(x))
        self.__timeline.finished.connect(self._animateFinished)

        self.setAnimation()
        self.setDuration()

    def _animateFinished(self):
        self.pages[self.current].widget.setFocus()
        self.horizontalScrollBar().setValue(self.current * self.width())

    def event(self, event):
        if event.type() == QEvent.Resize:
            for page in self.pages:
                page.widget.setMinimumSize(self.size())
            self.viewport().setMinimumSize(self.size())
            self.horizontalScrollBar().setValue(self.current * self.width())
        return QScrollArea.event(self, event)

    def keyPressEvent(self, event):
        pass

    def wheelEvent(self, event):
        pass

    def addPage(self, widget, inMethod = None, outMethod = None):
        self.pages.pop()

        self.pages.append(Page(widget, inMethod, outMethod))
        self.layout.addWidget(widget)

        self.pages.append(self.__tmp_page)
        self.layout.addWidget(self.__tmp_page.widget)

        self.connect(widget, SIGNAL("pageNext()"), self.next)
        self.connect(widget, SIGNAL("pagePrevious()"), self.prev)

    def setAnimation(self, animation = 35):
        self.__animation = animation
        self.__timeline.setEasingCurve(QEasingCurve(self.__animation))

    def setDuration(self, duration = 400):
        self.__duration = duration
        self.__timeline.setDuration(self.__duration)

    def flipPage(self, direction=0):
        self.current = min(max(0, self.current + direction), len(self.pages) - 2)
        self.__timeline.setFrameRange(self.horizontalScrollBar().value(), self.current * self.width())
        self.__timeline.start()

    def next(self):
        self.flipPage(1)

    def prev(self):
        self.flipPage(-1)

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

        pageWidget.addPage(DemoPage(text="Welcome to QPageWidget demo !"))

        for color in ('red', 'green', 'blue'):
            widget = DemoPage(text="%s colored page..." % color)
            widget.setStyleSheet("background-color:%s" % color)
            pageWidget.addPage(widget)

        line = DemoPage(text="You can embed all QWidgets as QPage, like QLineEdit", line_edit="Hello World")
        pageWidget.addPage(line)

        button = QPushButton("Click Me !", self)
        button.clicked.connect(lambda: QMessageBox.information(self,
                                "QPageWidget Information", line.text()))

        pageWidget.addPage(button)

if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication

    app = QApplication(sys.argv)
    testWidget = Test()
    testWidget.show()

    sys.exit(app.exec_())

