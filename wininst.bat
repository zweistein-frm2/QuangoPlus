python installer/fillversion.py installer.nsist.cfg.in installer.nsist.cfg cmh/RELEASE-VERSION
pynsist installer.nsist.cfg
python installer/patch.py -d build/nsis/  installer/tango_host.diff
makensis build/nsis/installer.nsi
