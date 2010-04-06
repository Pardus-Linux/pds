#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Pardus Desktop Services
from os import path
from os import getenv
from os import popen
from glob import glob

import piksemel
import gettext
__trans = None

import sys

# PyQt4 Core Libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtNetwork

# Logging
import logging

class DefaultDe(object):
    Name                 = 'X11'
    Version              = None
    ConfigPath           = '$HOME/.config'
    ConfigFile           = None
    ConfigType           = None
    ConfigBin            = None
    DefaultIconTheme     = 'hicolor'
    DefaultIconFile      = ''
    DefaultConfigPath    = None
    ExtraDirs            = None
    IconKey              = None
    i18n                 = staticmethod(lambda x: x)

class Kde4(DefaultDe):
    Name                 = 'kde'
    Version              = '4'
    ConfigPath           = '$HOME/.kde4/'
    ConfigFile           = 'share/config/kdeglobals'
    ConfigType           = 'ini'
    ConfigBin            = 'kde4-config'
    DefaultIconFile      = '/usr/share/icons/default.kde4'
    DefaultIconTheme     = 'oxygen'
    IconKey              = 'Icons/Theme'
    try:
        from PyKDE4 import kdecore
        i18n                 = kdecore.i18n
    except:
        pass

class Kde3(DefaultDe):
    Name                 = 'kde'
    Version              = '3.5'
    ConfigPath           = '$HOME/.kde/'
    ConfigFile           = 'share/config/kdeglobals'
    ConfigType           = 'ini'
    ConfigBin            = 'kde-config'
    DefaultIconFile      = '/usr/share/icons/default.kde'
    DefaultIconTheme     = 'crystalsvg'
    IconKey              = 'Icons/Theme'
    ExtraDirs            = 'KDEDIRS'

class Xfce(DefaultDe):
    Name                 = 'xfce'
    Version              = '4'
    ConfigPath           = '$HOME/.config/xfce4/'
    ConfigFile           = 'xfconf/xfce-perchannel-xml/xsettings.xml'
    ConfigType           = 'xml'
    DefaultIconTheme     = 'hicolor'
    DefaultConfigPath    = '/etc/xdg/xfce4/%s' % ConfigFile
    IconKey              = 'IconThemeName'

class Pds:

    SupportedDesktops = (DefaultDe, Kde4, Kde3, Xfce)

    def __init__(self, catalogName='', debug=False):
        self._session           = None
        self._version           = None
        self.home               = getenv('HOME').strip()
        self._config_content    = None

        _log_file = path.join(self.home, '.pdsLogfor%s.log' % catalogName)
        if debug:
            logging.basicConfig(filename = _log_file, level = logging.DEBUG, filemode = 'w')
        else:
            logging.basicConfig(level = logging.INFO)

        if catalogName:
            __trans = gettext.translation(catalogName, fallback=True)

            @staticmethod
            def __i18n(*text):
                if len(text) == 1:
                    return __trans.ugettext(text[0])
                ttt = unicode(__trans.ugettext(text[0]))
                for i in range(1,len(text)):
                    ttt = ttt.replace('%%%d' % i, unicode(text[i]))
                return ttt

            DefaultDe.i18n = __i18n

        self._acceptedMethods   = filter(lambda x: not x.startswith('__'), 
                                         dir(self.session))

    def __getattr__(self, name):

        for method in self._acceptedMethods:
            if method == str(name):
                return getattr(self.session, str(name))

        if not self.__dict__.has_key(name):
            raise AttributeError, name

    def settings(self, key, default):
        value = None
        if self.session.ConfigType == 'ini':
            # FIXME we dont need to force everytime.
            settings = self.parse(self.config_file, force = True)
            _value = settings.value(key)
            if not _value.toString():
                # Sometimes kdeglobals stores values without quotes
                _value = _value.toStringList()
                if _value:
                    value = _value.join(',')
            else:
                value = unicode(_value.toString())
            if not value or value == '':
                logging.debug('Switching to default conf')
                alternateConfig = self.session.DefaultConfigPath or \
                        path.join(self.install_prefix, self.session.ConfigFile)
                settings = self.parse(alternateConfig, force = True)
                value = unicode(settings.value(key, default).toString())

        elif self.session.ConfigType == 'xml':
            settings = self.parse(self.config_file, 'xml').getTag('property')
            def getval(settings, key):
                for tag in settings.tags():
                    if tag.getAttribute('name') == key:
                        return tag.getAttribute('value')
            value = getval(settings, key)
            if not value or value == '':
                alternateConfig = self.session.DefaultConfigPath or \
                        path.join(self.install_prefix, self.session.ConfigFile)
                settings = self.parse(alternateConfig, 'xml',
                        force = True).getTag('property')
                value = getval(settings, key)

        return value or default

    def parse(self, fpath, ftype = 'ini', force = False):
        if self._config_content and not force:
            return self._config_content
        if ftype == 'ini':
            self._config_content = QSettings(fpath, QSettings.IniFormat)
        elif ftype == 'xml':
            self._config_content = piksemel.parse(fpath)
        return self._config_content

    @property
    def session(self):
        if not self._session:
            env = getenv('DESKTOP_SESSION')
            if env == 'default':
                session = readfile('/etc/default/desktop', DefaultDe.Name)
                env     = session.split('=')[1].strip()
            for de in Pds.SupportedDesktops:
                if de.Name == env:
                    self._session = de
            if not self._session:
                self._session = DefaultDe
            else:
                for de in Pds.SupportedDesktops:
                    if de.Version == self.version and de.Name == env:
                        self._session = de
        return self._session

    @property
    def version(self):
        for key in ('KDE_SESSION_VERSION', 'KDEDIR'):
            env = getenv(key)
            if env:
                self._version = env
                break
        if self._version:
            self._version = self._version.split('/')[-1]
        return self._version

    @property
    def config_file(self):
        cf = path.join(self.config_path, self.session.ConfigFile)
        if path.exists(cf):
            return cf
        return None

    @property
    def config_path(self):
        return self.session.ConfigPath.replace('$HOME', self.home)

    @property
    def install_prefix(self):
        return popen('%s --prefix' % self.session.ConfigBin).read().strip()

class QIconTheme:
    def __init__(self, dirList = [], parents = []):
        self.dirList = dirList
        self.parents = map(lambda x:str(x), list(parents))
        self.valid = False
        if len(dirList) > 0:
            self.valid = True

class QIconLoader:

    SizeSmall       = 16
    SizeSmallMedium = 22
    SizeMedium      = 32
    SizeLarge       = 48
    SizeHuge        = 64
    SizeEnormous    = 128

    def __init__(self, pds = None, debug = False):

        self.iconSizes = (128, 64, 48, 32, 22, 16)

        if not pds:
            pds = Pds(debug = debug)

        self.pds = pds

        # Get possible Data Directories
        dataDirs = QFile.decodeName(getenv('XDG_DATA_DIRS'))
        if dataDirs.isEmpty():
            dataDirs = QString('/usr/local/share/:/usr/share/')

        dataDirs += ':' + self.pds.config_path + 'share'
        dataDirs.prepend(QDir.homePath() + ":")

        if self.pds.session.ExtraDirs:
            dirs = QFile.decodeName(getenv(self.pds.session.ExtraDirs)).split(':')
            for dirName in dirs:
                dataDirs.append(':' + dirName + '/share')

        defaultTheme = None
        if path.exists(self.pds.session.DefaultIconFile):
            fileInfo = QFileInfo(self.pds.session.DefaultIconFile)
            dir = QDir(fileInfo.canonicalFilePath())
            if fileInfo.exists():
                defaultTheme = dir.dirName()

        if not defaultTheme:
            defaultTheme = self.pds.session.DefaultIconTheme

        self.themeName = self.pds.settings(self.pds.session.IconKey, 
                self.pds.session.DefaultIconTheme)

        # Define icon directories
        self.iconDirs =  filter(lambda x: path.exists(x), 
                map(lambda x: path.join(unicode(x), 'icons'), 
                    dataDirs.split(':')))
        self.iconDirs = list(set(self.iconDirs))
        logging.debug('Icon Dirs : %s' % ','.join(self.iconDirs))
        self.themeIndex = self.readThemeIndex(self.themeName)
        self._available_icons = self.__get_icons()

    def readThemeIndex(self, themeName):

        dirList = []
        parents = []
        themeIndex = QFile()

        # Read theme index files
        for i in range(len(self.iconDirs)):
            themeIndex.setFileName(path.join(unicode(self.iconDirs[i]), 
                unicode(themeName), "index.theme"))
            if themeIndex.exists():
                indexReader = QSettings(themeIndex.fileName(), 
                        QSettings.IniFormat)
                for key in indexReader.allKeys():
                    if key.endsWith("/Size"):
                        size = indexReader.value(key).toInt()
                        dirList.append((size[0], 
                            unicode(key.left(key.size() - 5))))
                parents = indexReader.value('Icon Theme/Inherits').toStringList()
                break
        return QIconTheme(dirList, parents)

    def __get_icons(self, themeName = ''):
        if themeName == '':
            themeName = self.themeName
        if themeName == self.themeName:
            index = self.themeIndex
        else:
            index = self.readThemeIndex(themeName)

        themes = [themeName]
        themes.extend(index.parents)
        logging.debug('Themes : %s ' % ','.join(themes))
        icons = []
        for iconDir in self.iconDirs:
            for theme in themes:
                if path.exists(path.join(iconDir, theme)):
                    for _path in index.dirList:
                        icons.extend(glob(path.join(iconDir, theme, _path[1],'*.png')))
        _icons = map(lambda a: a.split('/')[-1][:-4], icons)
        return list(set(_icons))

    def findIconHelper(self, size = int, themeName = str, iconName = str):
        pixmap = QPixmap()

        if iconName == '' or self.themeName == '':
            return pixmap

        if themeName == '':
            themeName = self.themeName

        if themeName == self.themeName:
            index = self.themeIndex
        else:
            index = self.readThemeIndex(themeName)

        subDirs = filter(lambda x:x[0] == size, index.dirList)
        for iconDir in self.iconDirs:
            if path.exists(path.join(iconDir, themeName)):
                for theme in subDirs:
                    fileName = path.join(iconDir, themeName, theme[1],
                            '%s.png' % str(iconName))
                    logging.debug('Looking for : %s' % fileName)
                    if path.exists(fileName):
                        pixmap.load(fileName)
                        logging.debug('Icon: %s found in theme %s' % \
                                (iconName, themeName))
                        return pixmap
        if len(self._themes) > 0:
            self._themes.pop(0)
            if not len(self._themes) == 0 and pixmap.isNull():
                pixmap = self.findIconHelper(size, self._themes[0], iconName)
        return pixmap

    def findIcon(self, name = str, size = int):
        for _name in name:
            pixmapName = ''.join(('$qt', str(_name), str(size)))
            if (QPixmapCache.find(pixmapName, self.pixmap)):
                logging.debug('Icon %s returned from cache' % _name)
                return self.pixmap
        self._themes = []
        if self.themeName:
            self._themes.append(self.themeName)
            for _name in name:
                self.pixmap = self.findIconHelper(int(size), 
                        self.themeName, _name)
                if not self.pixmap.isNull():
                    break
        if self.pixmap.isNull():
            for _name in name:
                self._themes.extend(self.themeIndex.parents)
                if len(self._themes) > 0:
                    self.pixmap = self.findIconHelper(int(size), 
                            self._themes[0] ,_name)
                    if not self.pixmap.isNull():
                        break
        pixmapName = ''.join(('$qt', str(_name), str(size)))
        if not self.pixmap.isNull():
            logging.debug('Icon cached with name: %s ' % pixmapName)
            QPixmapCache.insert(pixmapName, self.pixmap)
        return self.pixmap

    def load(self, name, size = 128, forceCache = False):
        icon = QIcon()
        size = int(size)
        self.pixmap = QPixmap()
        if not type(name) in (list, tuple):
            name = [str(name)]
        if forceCache:
            for _name in name:
                for _size in self.iconSizes:
                    if (QPixmapCache.find('$qt'+str(_name)+str(_size), self.pixmap)):
                        logging.debug('Icon %s returned from cache' % _name)
                        return self.pixmap

        logging.debug('Getting icon : %s size: %s' % (','.join(name), size))
        pix = self.findIcon(name, size)
        if pix.isNull():
            for _size in self.iconSizes:
                pix = self.findIcon(name, _size)
                if not pix.isNull():
                    if size == _size:
                        return pix
                    icon.addPixmap(pix)
            if icon.isNull():
                return self.pixmap
            return icon.pixmap(QSize(size, size))
        return pix

    def icon(self, pix, size=128):
        return QIcon(self.load(pix, size))

class QUniqueApplication(QApplication):

    ADDR = QtNetwork.QHostAddress(QtNetwork.QHostAddress.LocalHost)

    def __init__(self, argv, port = 0):
        QApplication.__init__(self, argv)
        self.control = QtNetwork.QTcpServer(self)
        self.control.newConnection.connect(self.onControlConnect)

        self.mainwindow = None
        self.port = port
        self.readyToRun = self.control.listen(QUniqueApplication.ADDR, port)

        if self.readyToRun:
            self.port = self.control.serverPort()

        if not self.readyToRun:
            self.sendToInstance('show-mainwindow')
            sys.exit()

    def setMainWindow(self, window):
        self.mainwindow = window

    def exec_(self):
        if self.readyToRun:
            QApplication.exec_()

    def sendToInstance(self, data = ''):
        socket = QtNetwork.QTcpSocket()
        socket.connectToHost(QUniqueApplication.ADDR, self.port)
        if socket.waitForConnected( 500 ):
            if len(data) > 0:
                socket.write(data)
                socket.flush()
            socket.close()
            return True
        return False

    def onControlConnect(self):
        self.socket = self.control.nextPendingConnection()
        self.socket.readyRead.connect(self.onControlRequest)

    def onControlRequest(self):
        request = self.socket.readAll()
        for cmd in request.split(' '):
            self.parseCommand(cmd)
        self.socket.flush()
        self.socket.close()
        self.socket.deleteLater()

    def parseCommand(self, cmd):
        if cmd == 'show-mainwindow':
            if hasattr(self.mainwindow, 'show'):
                self.mainwindow.show()

def readfile(file_path, fallback=None):
    if path.exists(file_path):
        return open(file_path).read()
    return fallback

