python installer/fillversion.py installer.nsist.cfg.in installer.nsist.cfg quangoplus/RELEASE-VERSION
pynsist installer.nsist.cfg
python installer/patch_ng.py --fuzz -d build/nsis/  installer/tango_host.diff
makensis build/nsis/installer.nsi
