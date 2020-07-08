#  -*- coding: utf-8 -*-
#***************************************************************************
#* Copyright (C) 2019-2020 by Andreas Langhoff *
#* <andreas.langhoff@frm2.tum.de> *
#* This program is free software; you can redistribute it and/or modify *
#* it under the terms of the GNU General Public License as published by *
#* the Free Software Foundation; *
# **************************************************************************
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
        file = self.lineEdit.text()
        li = self._execute('RemoveFile',file)
        self.playlist.clear()
        self.playlist.addItems(li)

    def add_clicked(self):
        file = self.lineEdit.text()
        li = self._execute('AddFile',file)
        self.playlist.clear()
        self.playlist.addItems(li)

    def add_directory_clicked(self):
        directory = self.lineEdit_directory.text()
        li = self._execute('FilesInDirectory',directory)
        self.addlist(li)



