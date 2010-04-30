#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pardus Desktop Services
# Copyright (C) 2010, TUBITAK/UEKAE
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

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
        from PyKDE4 import kdecore, kdeui
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

