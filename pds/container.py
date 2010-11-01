#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services

# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökçen Eraslan <gokcen:pardus.org.tr>
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Qt Libraries
from PyQt4 import Qt

class PApplicationContainer(Qt.QX11EmbedContainer):
    def __init__(self, parent = None, process = None, args = ()):
        Qt.QX11EmbedContainer.__init__(self, parent)

        self._label = Qt.QLabel(self)
        self._label.hide()

        self._proc = None
        self._process = process
        self._args = args

    def start(self, process = None, args = ()):
        process = process or self._process
        args = args or self._args

        if not process:
            return (False, "Executable not given")

        self._process = process
        self._args = args

        self._proc = Qt.QProcess(self)
        self._proc.finished.connect(self._finished)
        self._proc.start(process, args)

        self.clientClosed.connect(self._proc.close)

        return (True, "\"%s\" process successfully started with pid = %s" % (process, self._proc.pid()))

    def closeEvent(self, event):
        if self._proc:
            self._proc.terminate()
            self._showMessage("Terminating process %s" % self._process)
            self._proc.waitForFinished()
        event.accept()

    def _finished(self, exitCode, exitStatus):
        self.emit(Qt.SIGNAL("processFinished"), exitCode, exitStatus)
        if exitCode != 0:
            self._showMessage("%s process finished with code %s" % (self._process, exitCode))
        else:
            self.close()

    def _showMessage(self, message):
        self._label.setText(message)
        self._label.show()

class PNetworkManager(PApplicationContainer):
    def __init__(self, parent = None):
        PApplicationContainer.__init__(self, parent)

    def startNetworkManager(self):
        ret = self.start("nm-connection-editor", ("--winid", str(self.winId())))

        if ret[0]:
            self.setMinimumSize(Qt.QSize(450, 200))
            self.show()

        return ret

class PMplayer(PApplicationContainer):
    def __init__(self, parent = None):
        PApplicationContainer.__init__(self, parent)

    def openMedia(self, path):
        ret = self.start("mplayer", ("-wid", str(self.winId()), path))

        if ret[0]:
            self.resize(Qt.QSize(640, 480))
            self.show()

        return ret

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        sys.exit("Usage: %s MEDIA_FILE" % sys.argv[0])

    app = Qt.QApplication(sys.argv)

    # ui = PNetworkManager()
    # ui.startNetworkManager()

    ui = PMplayer()
    ui.openMedia(sys.argv[1])

    app.lastWindowClosed.connect(sys.exit)

    app.exec_()
