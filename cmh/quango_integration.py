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

import sys
from os import path

import quango.main
import quango.mlzgui
import quango.device
import quango.utils
from quango.qt import  uic

import cmh.playlist
import cmh.histogramchannel

uithisfile = [cmh.playlist.uifile, cmh.histogramchannel.uifile]
                    
quango.device.INTERFACES = [
    (quango.mlzgui.StringIO, quango.mlzgui.BASE_CMDS + ['Communicate', 'WriteLine'], [], None),
    (cmh.playlist.PlayList, ['RemoveFile','AddFile'],[],None),
    (cmh.histogramchannel.HistogramChannel, quango.mlzgui.BASE_CMDS, ['RoiWKT','value'], 'int-ro-array'),
    (quango.mlzgui.TimerChannel, quango.mlzgui.BASE_CMDS + ['Prepare'], ['value'], 'float-ro'),
    # no separate class for CounterChannel
    (quango.mlzgui.TimerChannel, quango.mlzgui.BASE_CMDS + ['Prepare'], ['value'], 'int-ro'),
    (quango.mlzgui.ImageChannel, quango.mlzgui.BASE_CMDS + ['Prepare'], ['value'], 'int-ro-array'),
    (quango.mlzgui.Motor, quango.mlzgui.ACTUATOR_CMDS + ['Reference', 'MoveCont'],
     ['value', 'rawValue', 'speed', 'accel', 'decel'], 'float-rw'),
    (quango.mlzgui.Actuator, quango.mlzgui.ACTUATOR_CMDS, ['value', 'rawValue', 'speed'], 'float-rw'),
    (quango.mlzgui.AnalogOutput, quango.mlzgui.BASE_CMDS + ['Stop'], ['value'], 'float-rw'),
    (quango.mlzgui.DiscreteOutput, quango.mlzgui.BASE_CMDS + ['Stop'], ['value'], 'int-rw'),
    (quango.mlzgui.DigitalOutput, quango.mlzgui.BASE_CMDS, ['value'], 'int-rw'),
    (quango.mlzgui.Sensor, quango.mlzgui.BASE_CMDS, ['value', 'rawValue'], 'float-ro'),
    (quango.mlzgui.AnalogInput, quango.mlzgui.BASE_CMDS, ['value'], 'float-ro'),
    (quango.mlzgui.DigitalInput, quango.mlzgui.BASE_CMDS, ['value'], 'int-ro'),
]

orig_load_ui = quango.utils.loadUi
uipath = path.dirname(__file__)

def _load_ui(widget, uiname, subdir='ui'):
    if any(x == uiname for x in uithisfile):
        uic.loadUi(path.join(uipath, subdir, uiname), widget)
    else :
        orig_load_ui(widget, uiname, subdir='ui')

quango.main.loadUi = _load_ui
quango.mlzgui.loadUi = _load_ui

def main():
 quango.main.main()

def run():
    sys.exit(main())