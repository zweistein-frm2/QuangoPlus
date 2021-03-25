#  -*- coding: utf-8 -*-
#***************************************************************************
#* Copyright (C) 2020 by Andreas Langhoff                                  *
#* <andreas.langhoff@frm2.tum.de>                                          *
#* This program is free software; you can redistribute it and/or modify    *
#* it under the terms of the GNU General Public License v3 as published    *
#* by the Free Software Foundation;                                        *
# **************************************************************************

import json
from tango import DevState
import quango.mlzgui

from quango.qt import QLabel, QVBoxLayout, QWidget
import quangoplus.CC2xjsonhandling

uifile = 'mlz_igesCC2x.ui'

class PowerSupply(quango.mlzgui.MLZGuiPanel):
    UIFILE = uifile

    def reinit(self):
        self.transitions = self.props['transitions']
        self.trnames = quangoplus.CC2xjsonhandling.getTransitionNames(self.transitions)
        groups = self.props['groups']
        groupnames = quangoplus.CC2xjsonhandling.getGroupNames(groups)
        self.channels = []
        self.lblvoltage = []
        self.lblcurrent = []
        self.lblstatus = []
        for groupname in groupnames:
            groupchannels = quangoplus.CC2xjsonhandling.getChannels(groups, groupname)
            for channel in groupchannels:
                if not quangoplus.CC2xjsonhandling.isSingleChannel(channel):
                    continue
                self.channels.append(channel)
        i = 0
        for ch in self.channels:

            window = QWidget()
            lblch = QLabel(ch)
            lblv = QLabel("-")
            lblc = QLabel("-")
            lbls = QLabel(" ")
            layout = QVBoxLayout()
            layout.addWidget(lblch)
            layout.addWidget(lblv)
            layout.addWidget(lblc)
            layout.addWidget(lbls)
            self.lblvoltage.append(lblv)
            self.lblcurrent.append(lblc)
            self.lblstatus.append(lbls)
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
        tr = quangoplus.CC2xjsonhandling.getTransitions(self.transitions)

        for obj in tr:
            for o in obj:
                if o == selectedtrname:
                    self.comboBoxtransitionItems.clear()
                    tril = []
                    for it in obj[o]:
                        tril.append(json.dumps(it))
                    self.comboBoxtransitionItems.addItems(tril)
                    return

    def on_comboBoxtransitionItems_active_changed(self, value):
        item = self.comboBoxtransitionItems.itemText(value)
        self.plainTextEditTransitionItem.setPlainText(item)

    def on_saveTransitionItem_clicked(self):

        selectedtrname = self.comboBoxtransitions.currentText()
        cursel = self.comboBoxtransitionItems.currentIndex()
        newtrItem = self.plainTextEditTransitionItem.toPlainText()

        tr = quangoplus.CC2xjsonhandling.getTransitions(self.transitions)

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

        tr_modified = {'TRANSITION': tr}
        self.transitions = json.dumps(tr_modified)
        self.comboBoxtransitionItems.setItemText(cursel, newtrItem)
        self.props['transitions'] = self.transitions
        self.proxy.SetProperties(['transitions', self.transitions])

    def apply_clicked(self):
        ci = self.comboBoxtransitions.currentIndex()

        selectedtrname = self.trnames[ci]
        self._execute('applyTransition', selectedtrname)


    def on_pollData(self, attrs):

        jsonstatus = self.proxy.jsonstatus
        state = self.proxy.State()
        # pylint: disable=consider-using-in
        if (state == DevState.ON or state == DevState.OFF):
            self.pBsaveTransitionItem.setEnabled(True)
        else:
            self.pBsaveTransitionItem.setEnabled(False)

        update = json.loads(jsonstatus)
        i = 0
        # pylint: disable=too-many-nested-blocks
        for channel in self.channels:
            if channel in update:
                for kv in update[channel]:
                    if kv == "Status.currentMeasure":
                        vu = update[channel][kv]
                        self.lblcurrent[i].setText(vu['v'] +vu['u'])
                    if kv == "Status.voltageMeasure":
                        vu = update[channel][kv]
                        self.lblvoltage[i].setText(vu['v'] +vu['u'])
                    txt = self.lblstatus[i].text().split()
                    if kv in ["Status.on", "Status.currentTrip", "Event.currentTrip"]:
                        if kv in update[channel]:
                            vu = update[channel][kv]
                            if int(vu['v']):
                                if not kv in txt:
                                    txt.append(kv)
                            else:
                                if kv in txt:
                                    txt.remove(kv)
                        else:
                            if kv in txt:
                                #txt.remove(kv)
                                pass

                        status = ' '.join(txt)
                        self.lblstatus[i].setText(status)
            else:
                self.lblcurrent[i].setText('-')
                self.lblvoltage[i].setText('-')
                self.lblstatus[i].setText(' ')


            i = i + 1
