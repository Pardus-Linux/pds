#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# GUI Module ~ gui.py

# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Python Libraries
import copy

# Qt Libraries
from PyQt4 import QtGui
from PyQt4 import QtCore

# PREDEFINED POSITIONS
# --------------------
(TOPLEFT, TOPCENTER, TOPRIGHT, \
 MIDLEFT, MIDCENTER, MIDRIGHT, \
 BOTLEFT, BOTCENTER, BOTRIGHT,
 CURRENT) = range(10)
# --------------------
FORWARD = QtCore.QTimeLine.Forward
BACKWARD = QtCore.QTimeLine.Backward
# --------------------
(IN, OUT) = range(2)
# --------------------
OVERLAY_OPACITY = 200

class PAbstractBox(QtGui.QWidget):
    def __init__(self, parent):

        # Overlay widget, it should be initialized at first
        self.overlay = QtGui.QWidget(parent)
        self.overlay.hide()
        self.__overlay_enabled = False

        # Main widget initializing on parent widget
        QtGui.QWidget.__init__(self, parent)
        self.hide()

        # Pre-defined states
        self.last_direction = IN
        self.last_move_direction = FORWARD
        self.last_start = TOPCENTER
        self.last_stop = BOTCENTER
        self.duration = 2000
        self.overlay_duration = 1400

        # Override parents resize-event
        self.parent = parent
        self.parent.resizeEvent = self.resizeCallBacks

        # Timeline for X coordinate
        self.sceneX = QtCore.QTimeLine()

        # Timeline for Y coordinate
        self.sceneY = QtCore.QTimeLine()

        # Timeline for fade-effect of overlay
        self.sceneF = QtCore.QTimeLine()

        # Animation, QEasingCurve.Type
        self.animation = 38

        # Callback functions for using at pre-defined statements
        self.call_back_functions = {IN:[], OUT:[]}

    def enableOverlay(self, animated = False):
        # Resize the overlay with parent's size
        self.overlay.resize(self.parent.size())
        self.__overlay_enabled = True
        self.sceneF.setUpdateInterval(20)

        # When animation finished, overlay animation should be stop
        self.registerFunction(IN,  self.sceneF.stop)

        if animated:
            # Register animation range for overlay fade-in/out effect
            self.sceneF.setFrameRange(0, 200)
            self.sceneF.frameChanged.connect(lambda x: self.overlay.setStyleSheet('background-color: rgba(0,0,0,%s)' % x))
            self.registerFunction(IN,  lambda: self.sceneF.setFrameRange(0, 200))
            self.registerFunction(OUT, lambda: self.sceneF.setFrameRange(200, 0))
        else:
            # Set overlay opacity
            self.overlay.setStyleSheet('background-color: rgba(0, 0, 0, %s)' % OVERLAY_OPACITY)

    def disableOverlay(self):
        self.__overlay_enabled = False

    def resizeCallBacks(self, event):
        # Run parent widget's resizeEvent and then move widget to new position
        QtGui.QWidget(self.parent).resizeEvent(event)
        if self.__overlay_enabled:
            self.overlay.resize(self.parent.size())
        if self.isVisible():
            self.__animate(self.last_direction,
                           self.last_move_direction,
                           CURRENT,
                           self.last_stop,
                           self.duration,
                           True)

    def animate(self, direction = IN, move_direction = FORWARD, start = TOPCENTER, stop = BOTCENTER, start_after = None, duration = 0):

        if start_after:
            if start_after.state() == QtCore.QTimeLine.Running:
                # If there is an animation started before this one, we can easily start it when the old one finishes
                start_after.finished.connect(lambda: self.__animate(direction, move_direction, start, stop, duration))
                return

        # Otherwise, run the animation directly and return the timeline obj for using as a reference for later animations
        return self.__animate(direction, move_direction, start, stop, duration)

    def __animate(self, direction, move_direction, start, stop, duration, just_resize = False):

        # Stop all running animations
        self.sceneX.stop()
        self.sceneY.stop()
        self.sceneF.stop()

        # Use given duration time or use the default one
        duration = duration if duration > 0 else self.duration

        # Set last used animations with given values
        self.last_stop           = stop
        self.last_start          = start
        self.last_move_direction = move_direction
        self.last_direction      = direction

        # Set X coordinate timeline settings
        self.sceneX.setDirection(move_direction)
        self.sceneX.setEasingCurve(QtCore.QEasingCurve(self.animation))
        self.sceneX.setDuration(duration)
        self.sceneX.setUpdateInterval(20)

        # Set Y coordinate timeline settings
        self.sceneY.setDirection(move_direction)
        self.sceneY.setEasingCurve(QtCore.QEasingCurve(self.animation))
        self.sceneY.setDuration(duration)
        self.sceneY.setUpdateInterval(20)

        # Update duration for overlay fade effect
        self.sceneF.setDuration(self.overlay_duration)

        # Get current sizes
        p_width  = self.parent.width()
        p_height = self.parent.height()
        width  = self.width()
        height = self.height()

        # Calculate new positions for given points
        limits = {TOPLEFT   : [0, 0],
                  TOPCENTER : [p_width/2 - width/2, 0],
                  TOPRIGHT  : [p_width - width, 0],
                  MIDLEFT   : [0, p_height/2 - height/2],
                  MIDCENTER : [p_width/2 - width/2, p_height/2 - height/2],
                  MIDRIGHT  : [p_width - width, p_height/2 - height/2],
                  BOTLEFT   : [0, p_height - height],
                  BOTCENTER : [p_width/2 - width/2, p_height - height],
                  BOTRIGHT  : [p_width - width, p_height - height],
                  CURRENT   : [self.x(), self.y()]}

        # Get start and stop positions
        # I used deepcopy in case of selecting same positions for start and stop
        start_pos = copy.deepcopy(limits[start])
        stop_pos  = copy.deepcopy(limits[stop])

        # Poor developer's debug mechanism.
        # print start_pos, stop_pos, width, height

        # Update start and stop positions for given direction
        if direction == IN:
            self.show()
            if start in (TOPLEFT, MIDLEFT, BOTLEFT):
                start_pos[0] -= width
            elif start in (TOPRIGHT, MIDRIGHT, BOTRIGHT):
                start_pos[0] += width
            elif start == TOPCENTER:
                start_pos[1] -= height
            elif start == BOTCENTER:
                start_pos[1] += height
        elif direction == OUT:
            if stop in (TOPLEFT, MIDLEFT, BOTLEFT):
                stop_pos[0] -= width
            elif stop in (TOPRIGHT, MIDRIGHT, BOTRIGHT):
                stop_pos[0] += width
            elif stop == TOPCENTER:
                stop_pos[1] -= height
            elif stop == BOTCENTER:
                stop_pos[1] += height

        # Move the widget to calculated start position
        self.move(start_pos[0], start_pos[1])

        # Set calculated start and stop positions
        self.sceneX.setFrameRange(start_pos[0], stop_pos[0])
        self.sceneX.frameChanged.connect(lambda x: self.move(x, self.y()))
        self.sceneY.setFrameRange(start_pos[1], stop_pos[1])
        self.sceneY.frameChanged.connect(lambda y: self.move(self.x(), y))

        # Run predefined callback functions for given direction
        self.runCallBacks(direction)

        # Hide widget when direction is OUT
        self.sceneX.finished.connect(lambda: self.setHidden(direction == OUT))

        # Show/hide overlay if overlay enabled
        if self.__overlay_enabled:
            self.overlay.show()
            self.sceneX.finished.connect(lambda: self.overlay.setHidden(direction == OUT))
        else:
            self.overlay.hide()

        # Start the animation !
        if self.sceneX.state() == QtCore.QTimeLine.NotRunning:
            self.sceneX.start()
            self.sceneY.start()
            if not just_resize:
                # The animation will just work for repositioning the widget,
                # so we dont need overlay fade animation
                self.sceneF.start()

        # Return the X coordinate timeline obj to use as reference for next animation
        return self.sceneX

    def flushCallBacks(self, direction, approve = False):
        # Reset given direction's call backs
        self.call_back_functions[direction] = []

    def registerFunction(self, direction, func):
        # Add function to given direction's list
        if not func in self.call_back_functions[direction]:
            self.call_back_functions[direction].append(func)

    def runCallBacks(self, direction):
        # Run all functions for given direction
        for func in self.call_back_functions[direction]:
            func()

class PMessageBox(PAbstractBox):

    def __init__(self, parent=None):
        PAbstractBox.__init__(self, parent)
        self.label = QtGui.QLabel(self)
        self.label.setStyleSheet("font: 16pt;color: white;background-color:rgba(0,0,0,200)")

    def showMessage(self, message):
        #, duration = 2, inPos = MIDLEFT, stopPos = MIDCENTER, outPos = MIDRIGHT):
        self.label.setText(message)
        self.label.resize(QtCore.QSize(300,500))
        self.label.setAlignment(QtCore.Qt.AlignVCenter)
        self.animate(start = TOPCENTER, stop = MIDCENTER)

