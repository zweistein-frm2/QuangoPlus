Quango+

1. prerequisite is Quango : to install on Linux:
 uninstall older/different version with  sudo pip3 uninstall quango, then
git clone https://forge.frm2.tum.de/review/frm2/tango/apps/quango.git
cd quango
git checkout 516a5be5aec024d6685b01e01a971475cd31f682
sudo python3 setup.py install


2. to install Quango+ :
 git clone https://github.com/zweistein-frm2/QuangoPlus.git
cd QuangoPlus
sudo python3 setup.py install

quango+ is then a command available on linux 

to uninstall :

sudo pip3 uninstall quangoplus

Windows:

a standalone executable can be build with winbuildinstaller.bat


########### for developer ############

debian package source directory from setup.py is created using stdeb:
https://pypi.org/project/stdeb/

python setup.py --command-packages=stdeb.command debianize
