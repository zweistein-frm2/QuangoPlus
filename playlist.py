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
        self.playlist.addItems(li)
        [self._execute('AddFile',i)  for i in li]


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



