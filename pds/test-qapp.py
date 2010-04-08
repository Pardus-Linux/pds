#!/usr/bin/python
# -*- coding: utf-8 -*-

from pds import *
import sys

app = QUniqueApplication(sys.argv, catalog = 'test-app')
if app.readyToRun:
    print 'Application started !'
app.exec_()
