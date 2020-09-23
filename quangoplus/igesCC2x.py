#  -*- coding: utf-8 -*-
#***************************************************************************
#* Copyright (C) 2020 by Andreas Langhoff                                  *
#* <andreas.langhoff@frm2.tum.de>                                          *
#* This program is free software; you can redistribute it and/or modify    *
#* it under the terms of the GNU General Public License v3 as published    *
#* by the Free Software Foundation;                                        *
# **************************************************************************

import json
import quango.mlzgui
from quango.qt import QLabel, QVBoxLayout, QHBoxLayout, QWidget
import quangoplus.CC2xjsonhandling

uifile = 'mlz_igesCC2x.ui'

class PowerSupply(quango.mlzgui.Base):
    UIFILE = uifile

    def reinit(self):

        self.trnames = quangoplus.CC2xjsonhandling.getTransitionNames(self.props['transitions'])
        groups = self.props['groups']
        groupnames = quangoplus.CC2xjsonhandling.getGroupNames(groups)
        self.channels = []
        self.lblvoltage = []
        for groupname in groupnames:
           groupchannels = quangoplus.CC2xjsonhandling.getChannels(groups,groupname)
           for channel in groupchannels:
               self.channels.append(channel)
        i = 0
        for ch in self.channels:
            window = QWidget()
            lblch = QLabel(ch)
            lblv = QLabel("voltage")
            layout = QVBoxLayout()
            layout.addWidget(lblch)
            layout.addWidget(lblv)
            self.lblvoltage.append(lblv)
            window.setLayout(layout)
            self.hLayout_Channels.addWidget(window)
            i = i + i


        self.comboBoxtransitions.currentIndexChanged.connect(self.on_comboBoxtransitions_active_changed)
        self.pBsaveTransitionItem.clicked.connect(self.on_saveTransitionItem_clicked)
        self.comboBoxtransitionItems.currentIndexChanged.connect(self.on_comboBoxtransitionItems_active_changed)
        self.comboBoxtransitions.addItems(self.trnames)
        self.pBApply.clicked.connect(self.apply_clicked)

    def on_comboBoxtransitions_active_changed(self, value):
        selectedtrname = self.trnames[value]
        tr = quangoplus.CC2xjsonhandling.getTransitions(self.props['transitions'])

        for obj in tr:
            for o in obj:
              if o == selectedtrname:
                self.comboBoxtransitionItems.clear()
                tril =[]
                for it in obj[o]:
                    tril.append(json.dumps(it))
                self.comboBoxtransitionItems.addItems(tril)
                return

    def on_comboBoxtransitionItems_active_changed(self,value):
        item = self.comboBoxtransitionItems.itemText(value)
        self.plainTextEditTransitionItem.setPlainText(item)

        pass

    def on_saveTransitionItem_clicked(self):

        selectedtrname = self.comboBoxtransitions.currentText()
        cursel = self.comboBoxtransitionItems.currentIndex()
        newtrItem =self.plainTextEditTransitionItem.toPlainText()

        tr = quangoplus.CC2xjsonhandling.getTransitions(self.props['transitions'])

        for obj in tr:
            for o in obj:
              if o == selectedtrname:
                index = 0
                for it in obj[o]:
                    if cursel == index:
                       desired = json.loads(newtrItem)
                       # here we should do some checks for typos etc in newtrItem
                       # newtrItem (of form:   "Control.setVoltage",[1,2,...]
                       #  array [1,2,...]  should be of same size as Group name contains channels
                       it.update(desired)
                       break
                    index = index + 1

        self.props['transitions'] = json.dumps(tr)
        self.comboBoxtransitionItems.setItemText(cursel,newtrItem)

    def apply_clicked(self):
        ci = self.comboBoxtransitions.currentIndex()
        selectedtrname = self.trnames[ci]
        self._execute('applyTransition', selectedtrname)


    def on_pollData(self, attrs):
   #   jsonstatus = self._execute('getstatusJson',arg = None)
    #  print(jsonstatus)
      pass



