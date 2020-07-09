#  -*- coding: utf-8 -*-
#***************************************************************************
#* Copyright (C) 2019-2020 by Andreas Langhoff *
#* <andreas.langhoff@frm2.tum.de> *
#* This program is free software; you can redistribute it and/or modify *
#* it under the terms of the GNU General Public License as published by *
#* the Free Software Foundation; *
# **************************************************************************
import sys
from os import path

import quango.main
import quango.mlzgui
import quango.device
import quango.utils
from quango.qt import  uic
from quango.qt import QIcon, QMessageBox
import cmh.playlist
import cmh.histogramchannel
import cmh.version

uithisfile = [cmh.playlist.uifile, cmh.histogramchannel.uifile]

quango.device.INTERFACES.insert(0, (cmh.playlist.PlayList, ['RemoveFile', 'AddFile'], [], None))
quango.device.INTERFACES.insert(0, (cmh.histogramchannel.HistogramChannel,
                                    quango.mlzgui.BASE_CMDS,
                                    ['RoiWKT', 'value'],
                                    'int-ro-array'))


orig_load_ui = quango.utils.loadUi
uipath = path.dirname(__file__)

def _load_ui(widget, uiname, subdir='ui'):
    if any(x == uiname for x in uithisfile):
        uic.loadUi(path.join(uipath, subdir, uiname), widget)
    else:
        orig_load_ui(widget, uiname, subdir='ui')
        if uiname == "main.ui":
            widget.setWindowTitle("Quango+")
            iconpath = path.join(uipath, 'res', 'quango+.ico')
            ico = QIcon(iconpath)
            widget.setWindowIcon(ico)


quango.main.loadUi = _load_ui
quango.mlzgui.loadUi = _load_ui
quango.main.get_version = cmh.version.get_version

orig_setWindowsTitle = quango.main.MainWindow.setWindowTitle

def __setWindowsTitle(self, title):
    if not title.startswith("Quango+"):
        title = title.replace("Quango", "Quango+")
    return orig_setWindowsTitle(self, title)

quango.main.MainWindow.setWindowTitle = __setWindowsTitle


about_called = 0
def onabouttriggered(self):
    global about_called
    about_called = about_called + 1
    if about_called % 2 == 0:
        return
    QMessageBox.about(self,
                      'About Quango+',
          '''
          <h2>About Quango+</h2>
          <p style="font-style: italic">
            (C) 2020 MLZ instrument control
          </p>
          <p>
            Quango+ is an extension to <li><a href="https://forge.frm2.tum.de/cgit/cgit.cgi/frm2/tango/apps/quango.git/">Quango (a generic Tango device client)</a></li>
          </p>
          <h3>Author(s):</h3>
          <ul>
              <li>Copyright (C) 2020
              <a href="mailto:andreas.langhoff@frm2.tum.de">Andreas Langhoff</a></li>
          </ul>
          <p>
            Quango+ is published under the
            <a href="http://www.gnu.org/licenses/gpl.html">GPL
              (GNU General Public License)</a>
          </p>
          <p style="font-weight: bold">
            Version: %s
          </p>
          ''' % cmh.version.get_version())



quango.main.MainWindow.on_actionAbout_triggered = onabouttriggered

def main():
    quango.main.main()

def run():
    sys.exit(main())
