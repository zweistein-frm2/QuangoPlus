#  -*- coding: utf-8 -*-
#***************************************************************************
#* Copyright (C) 2020 by Andreas Langhoff                                  *
#* <andreas.langhoff@frm2.tum.de>                                          *
#* This program is free software; you can redistribute it and/or modify    *
#* it under the terms of the GNU General Public License v3 as published    *
#* by the Free Software Foundation;                                        *
# **************************************************************************

import json
from typing import List


def isSingleChannel(lac:str)->bool:
    s = lac.split("_")
    line = ''
    address = ''
    channel = ''
    if len(s) > 0:
        line = s[0]
    if len(s) > 1:
        address = s[1]
    if len(s) > 2:
        channel = s[2]
        return True
    return False

def isModuleAddress(lac:str)->bool:
    s = lac.split("_")
    line = ''
    address = ''
    channel = ''
    if len(s) > 0:
        line = s[0]
    if len(s) > 2:
        channel = s[2]
        return False
    if len(s) > 1:
        address = s[1]
        return True
    return False


def getTransitions(transitions: str)->List[str]:
    jobjtransitions = json.loads(transitions)
    return jobjtransitions['TRANSITION']

def getTransitionNames(transitions: str)->List[str]:
    rv = []
    tr = getTransitions(transitions)
    for t in tr:
        for name in t:
            rv.append(name)
    return rv

def getStatusValue(channel: str, item: str, statusjsonstr: str):
    allj = json.loads(statusjsonstr)
    for it in allj:
        if it == channel:
            objects = allj[channel]
            for cmd in objects:
                if cmd == item:
                    vu = objects[cmd]
                    return vu['v']
    return None

def getGroupNames(groups: str)->List[str]:
    rv = []
    jobjgroups = json.loads(groups)
    groups = jobjgroups['GROUP']
    for group in groups:
        for key, val in group.items():
            rv.append(key)
    return rv

def getChannels(groups: str, groupname: str)->List[str]:
    rv = []
    jobjgroups = json.loads(groups)
    ggroups = jobjgroups['GROUP']

    for group in ggroups:
        for key, val in group.items():
            if key == groupname:
                channels = val["CHANNEL"]
                for ch in channels:
                    rv.append(ch)
    return rv
