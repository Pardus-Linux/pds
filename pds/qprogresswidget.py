#!/usr/bin/python
# -*- coding: utf-8 -*-

""" QProgressWidget provides step by step progress widget. """

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
from PyQt4.QtGui import QBoxLayout
from PyQt4.QtGui import QScrollArea
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QResizeEvent

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

class QProgressItemWidget(QWidget):
    """ FIXME The QProgressItemWidget """

    def __init__(self, parent, title, state = None, button = False):
        """ Creates a new QProgressItemWidget

        parent: QWidget parent
        title: Title for the progress
        """
        # First initialize, QPageWidget is based on QScrollArea
        QWidget.__init__(self, parent)

        self.layout = QHBoxLayout(self)
        self.layout.setMargin(0)

        self.icon = QLabel(self)

        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.icon.sizePolicy().hasHeightForWidth())

        self.icon.setSizePolicy(sizePolicy)
        self.icon.setMinimumSize(QSize(22, 22))
        self.icon.setMaximumSize(QSize(22, 22))
        self.icon.setText("")
        self.layout.addWidget(self.icon)

        self.message = QLabel(self.widget)
        self.message.setText("")
        self.layout.addWidget(self.message)

        self.button = QPushButton(self.widget, "...")
        self.layout.addWidget(self.button)
        self.layout.setStretch(1, 1)

