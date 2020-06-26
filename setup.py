#  -*- coding: utf-8 -*-
from os import listdir, path
from setuptools import find_packages, setup
import version

uidir = path.join(path.dirname(__file__), 'ui')
uis = [path.join('ui', entry) for entry in listdir(uidir)]

setup(
    name = 'charm-mesytec-histogram',
    version = version.get_version(),
    packages = find_packages(),
    scripts = ['cmh.py'],
    install_requires=["quango"],
    py_modules=['histogramchannel','playlist','polygon','quango_integration'],
    package_data = {"": uis},
    author = 'Andreas Langhoff',
    author_email = 'andreas.langhoff@frm2.tum.de',
    description = 'Histogram display and listmode replay for MLZ devices',
    classifiers = [
        'License :: OSI Approved :: GPL License',
    ],
)
