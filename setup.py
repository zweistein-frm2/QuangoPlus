#  -*- coding: utf-8 -*-
#***************************************************************************
#* Copyright (C) 2019-2020 by Andreas Langhoff *
#* <andreas.langhoff@frm2.tum.de> *
#* This program is free software; you can redistribute it and/or modify *
#* it under the terms of the GNU General Public License as published by *
#* the Free Software Foundation; *
# **************************************************************************

from os import listdir, path
from setuptools import find_packages, setup
import cmh.version

uidir = path.join(path.dirname(__file__), 'cmh', 'ui')
uis = [path.join('ui', entry) for entry in listdir(uidir)]

setup(
    name='quangoplus',
    version=cmh.version.get_version(),
    packages=find_packages(),
    scripts=['bin/quango+'],
    install_requires=["quango"],
    package_data={"cmh": ['RELEASE-VERSION'] +uis},
    author='Andreas Langhoff',
    author_email='andreas.langhoff@frm2.tum.de',
    description='Simple remote front end for neutron detector Histogram display (source can be listmode replay or live  measurement)',
    classifiers=[
        'License :: OSI Approved :: GPL License',
    ],
    python_requires='>=3.6',
)
