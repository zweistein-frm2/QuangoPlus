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
import re
from quango.qt import QPoint

class Polygon():
    def __init__(self):
        self.outer=list()
    def readWKT(self,str):
        try:
            stp = "POLYGON"
            rings=str.find(stp)
            oi=str[rings+len(stp):]  #oi = outerinner
            mo1 = re.search('\(([^()]*)\)',oi)  # first object only which is outer ring
            strouter =oi[mo1.regs[1][0]:mo1.regs[1][1]]
            strpts = strouter.split(',')
            tmpouter=list()
            for strpt in strpts:
                 strxy=strpt.split(' ')
                 p = QPoint(int(strxy[0]),int(strxy[1]))
                 tmpouter.append(p)
            self.outer=tmpouter
        except :
            pass
            #print("Error reading Polygon from : "+str)

        
    def WKT(self):
        wkt="POLYGON(("
        for xy in self.outer:
               wkt+=str(xy.x())
               wkt+=" "
               wkt+=str(xy.y())
               wkt+=","
        wkt=wkt[:-1] # we strip the "," at the end
        wkt+="),())"
        return wkt

    def addPoint(self,val):
        self.outer.append(val)
        
    def close(self):
        n=len(self.outer)
        if n>=3:
            last = self.outer[n-1]
            if not (last.x() is self.outer[0].x() and last.y() is self.outer[0].y()):
                self.outer.append(self.outer[0])

    def vertices(self):
        return self.outer
