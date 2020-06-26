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
from os import listdir, path
from setuptools import find_packages, setup
import version

uidir = path.join(path.dirname(__file__), 'cmh', 'ui')
uis = [path.join('ui', entry) for entry in listdir(uidir)]

setup(
    name = 'charm-mesytec-histogram',
    version = version.get_version(),
    packages = find_packages(),
    scripts = ['bin/cmh'],
    install_requires=["quango"],
    package_data = {"cmh": ['RELEASE-VERSION'] +uis},
    author = 'Andreas Langhoff',
    author_email = 'andreas.langhoff@frm2.tum.de',
    description = 'Simple remote front end for neutron detector Histogram display (source can be live measurement data or listmode playback)',
    classifiers = [
        'License :: OSI Approved :: GPL License',
    ],
    python_requires='>=3.6',
)
