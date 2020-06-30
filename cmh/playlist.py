#  -*- coding: utf-8 -*-
# *****************************************************************************
# MLZ Tango client tool
# Copyright (c) 2020 by the authors, see LICENSE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module author(s):
#   Andreas Langhoff <andreas.langhoff@frm2.tum.de>
#
# *****************************************************************************

import quango.mlzgui


uifile = 'mlz_PlayList.ui'

class PlayList(quango.mlzgui.Base):
    UIFILE = uifile

    def reinit(self):
      
       self.playlist.clicked.connect(self.playlist_clicked)
       self.pbutton_remove.clicked.connect(self.remove_clicked)
       self.pbutton_add.clicked.connect(self.add_clicked)
       self.pbutton_add_directory.clicked.connect(self.add_directory_clicked)
       li = self._execute('FilesInDirectory','~')
       self.addlist(li)

    def addlist(self, li):
       if li is not None:
        for i in li:
           self.playlist.clear()
           li2 = self._execute('AddFile',i)
           self.playlist.addItems(li2)


    def playlist_clicked(self):
       item = self.playlist.currentItem()
       self.lineEdit.setText(str(item.text()))

    def remove_clicked(self):
       file=self.lineEdit.text()
       li = self._execute('RemoveFile',file)
       self.playlist.clear()
       self.playlist.addItems(li)

    def add_clicked(self):
       file=self.lineEdit.text()
       li = self._execute('AddFile',file)
       self.playlist.clear()
       self.playlist.addItems(li)

    def add_directory_clicked(self):
       directory = self.lineEdit_directory.text()
       li = self._execute('FilesInDirectory',directory)
       self.addlist(li)



