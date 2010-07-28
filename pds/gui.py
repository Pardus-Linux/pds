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

# PREDEFINED POSITIONS
# --------------------
TOPLEFT     = 1
TOPCENTER   = 2
TOPRIGHT    = 3
MIDLEFT     = 4
MIDCENTER   = 5
MIDRIGHT    = 6
BOTLEFT     = 7
BOTCENTER   = 8
BOTRIGHT    = 9
# --------------------

class PAbstractBox:
    def __init__(self, *args):

class PInfoBox(PAbstractBox):
    def __init__(self, *args):
        PAbstractBox.__init__(self, args)

a = PInfoBox()

