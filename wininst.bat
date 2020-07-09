rename installer.nsist.cfg installer.nsist.cfg.in
python installer/fillversion.py installer.nsist.cfg.in installer.nsist.cfg cmh/RELEASE-VERSION
del installer.nsist.cfg.in
pynsist installer.nsist.cfg
python installer/patch.py -d build/nsis/  installer/tango_host.diff
makensis build/nsis/installer.nsi
