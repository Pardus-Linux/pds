#!/usr/bin/python
# -*- coding: utf-8 -*-

"""QPageWidget provides wizard like animated stack widget."""

# QtCore Libraries
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QSize
from PyQt4.QtCore import QRect
from PyQt4.QtCore import QEvent
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import SIGNAL
from PyQt4.QtCore import QTimeLine
from PyQt4.QtCore import QEasingCurve

# QtGui Libraries
from PyQt4.QtGui import QFrame
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QScrollArea
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QMessageBox

__author__      = "Gökmen Göksel"
__email__       = "gokmen@pardus.org.tr"
__copyright__   = "Copyright 2011, TUBITAK/UEKAE"

__license__     = "GPLv2"
__version__     = "0.1"

# Pardus Desktop Services
# Copyright (C) 2011, TUBITAK/UEKAE
# 2011 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

class Page:
    """ Simple Page Class to store required data about the Page """

    def __init__(self, widget, inMethod = None, outMethod = None):
        """ Creates a new Page object for given widget with given in/out methods.

        widget: A QWidget which is the mainwidget for this Page
        inMethod: (optional) QPageWidget triggers this method when the Page appear
        outMethod: (optional) QPageWidget triggers this method when the Page disappear
        """
        self.widget    = widget
        self.inMethod  = inMethod
        self.outMethod = outMethod

class QPageWidget(QScrollArea):
    """ The QPageWidget provides a stack widget with animated page transitions. """

    def __init__(self, parent = None):
        """ Creates a new QPageWidget on given parent object. """

        # First initialize, QPageWidget is based on QScrollArea
        QScrollArea.__init__(self, parent)

        # Properties for QScrollArea
        self.setFrameShape(QFrame.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        # Main widget, which stores all Pages in it
        self.widget = QWidget(self)
        self.layout = QHBoxLayout(self.widget)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)

        # TMP_PAGE, its using as last page in stack
        # A workaround for a QScrollArea bug
        self.__tmp_page = Page(QWidget(self.widget))
        self.__pages = [self.__tmp_page]
        self.__current = 0
        self.__last = 0

        # Set main widget
        self.setWidget(self.widget)

        # Animation TimeLine
        self.__timeline = QTimeLine()
        self.__timeline.setUpdateInterval(2)

        # Updates scrollbar position when frame changed
        self.__timeline.frameChanged.connect(lambda x: self.horizontalScrollBar().setValue(x))

        # End of the animation
        self.__timeline.finished.connect(self._animateFinished)

        # Initializes default values
        self.setAnimation()
        self.setDuration()

    def _animateFinished(self):
        """ Its called by TimeLine when animation finished.

        It first runs the outMethod of last Page and then the inMethod of current Page
        Finally tt gives the focus to the current page and fixes the scrollBar
        """
        # Run last page's outMethod if exists
        if self.__pages[self.__last].outMethod:
            self.__pages[self.__last].outMethod()

        # Run new page's inMethod if exists
        if self.__pages[self.__current].inMethod:
            self.__pages[self.__current].inMethod()

        # Give focus to the current Page
        self.__pages[self.__current].widget.setFocus()

        # Update scrollbar position for current page
        self.horizontalScrollBar().setValue(self.__current * self.width())

    def event(self, event):
        """ Overrides the main event handler to catch resize events """
        # Catch Resize event
        if event.type() == QEvent.Resize:
            # Update each page minimumsize to mainwidget's new size
            for page in self.__pages:
                page.widget.setMinimumSize(self.size())

            # Update viewport minimumsize to mainwidget's new size
            # It's a workaround for QScrollArea updateGeometry bug
            self.viewport().setMinimumSize(self.size())

            # Update scrollbar position for current page
            self.horizontalScrollBar().setValue(self.__current * self.width())

        # Return the Event
        return QScrollArea.event(self, event)

    def keyPressEvent(self, event):
        """ Overrides the keyPressEvent to ignore them """
        pass

    def wheelEvent(self, event):
        """ Overrides the wheelEvent to ignore them """
        pass

    def createPage(self, widget, inMethod = None, outMethod = None):
        """ Creates and adds new Page for given widget with given in/out methods.

        widget: A QWidget which is the mainwidget for this Page
        inMethod: (optional) QPageWidget triggers this method when the Page appear
        outMethod: (optional) QPageWidget triggers this method when the Page disappear
        """
        self.addPage(Page(widget, inMethod, outMethod))

    def addPage(self, page):
        """ Adds the given Page to the stack.

        page: A Page object
        """
        # First remove the last page; its __tmp_page
        self.__pages.pop()

        # Add new page
        self.__pages.append(page)
        self.layout.addWidget(page.widget)

        # Add __tmp_page to end
        self.__pages.append(self.__tmp_page)
        self.layout.addWidget(self.__tmp_page.widget)

        # Create connections for page navigation signals from new page
        self.connect(page.widget, SIGNAL("pageNext()"), self.next)
        self.connect(page.widget, SIGNAL("pagePrevious()"), self.prev)
        self.connect(page.widget, SIGNAL("setCurrent(int)"), self.setCurrent)

    def __setCurrent(self, pageNumber):
        """ Internal method to set current page index. """
        self.__last = self.__current
        self.__current = min(max(0, pageNumber), len(self.__pages) - 2)

    def setCurrent(self, pageNumber = 0):
        """ Set and flip the page with given pageNumber.

        pageNumber: index number of Page (default is 0)
        """
        self.__setCurrent(pageNumber)
        self.flipPage()

    def getCurrent(self):
        """ Returns current page index. """
        return self.__current

    def count(self):
        """ Returns number of pages. """
        return len(self.__pages) - 1

    def setAnimation(self, animation = 35):
        """ Set the transition animation with the given animation.

        animation: the number represents predefined QEasingCurves
                   List of predefined QEasingCurves can be found from:
                   http://doc.qt.nokia.com/4/qeasingcurve.html#Type-enum

                   Default is QEasingCurve::InOutBack (35)
        """
        self.__animation = animation
        self.__timeline.setEasingCurve(QEasingCurve(self.__animation))

    def setDuration(self, duration = 400):
        """ Set the transition duration.

        duration: duration time in ms
        """
        self.__duration = duration
        self.__timeline.setDuration(self.__duration)

    def flipPage(self, direction=0):
        """ Flip the page with given direction.

        direction: can be -1, 0 or +1
                   -1: previous page (if exists)
                    0: just flip to current page
                   +1: next page (if exists)
        """
        # Check given direction
        direction = direction if direction == 0 else max(min(1, direction), -1)

        # If direction is equal to zero no need to re-set current
        if not direction == 0:
            self.__setCurrent(self.__current + direction)

        # If last page is different from new page, flip it !
        if not self.__last == self.__current:
            self.__timeline.setFrameRange(self.horizontalScrollBar().value(), self.__current * self.width())
            self.__timeline.start()

    def next(self):
        """ Helper method to flip next page. """
        self.flipPage(1)

    def prev(self):
        """ Helper method to flip previous page. """
        self.flipPage(-1)

