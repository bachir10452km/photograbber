# OSX #

  * See [Issue 8](https://code.google.com/p/photograbber/issues/detail?id=8), be sure to run MacPython so that the build will include a universal build of python
  * Requires that py2app is installed
  * Normal SVN checkout
  * python setup-osx.py py2app

PhotoGrabber.app will now be in the ~/dist folder

# Windows #

  * Requires that py2exe is installed
  * Requires that NSIS is installed
  * Normal SVN checkout
  * python setup-win.py py2exe
  * Copy Microsoft.VC90.CRT.manifest and msvcr90.dll into the dist/ folder (available from Program Files/Microsoft Visual Studio 9.0/VC/redist/x86) - Fixes [Issue 7](https://code.google.com/p/photograbber/issues/detail?id=7)
  * makensis setup.nsi

pg.exe will now be in the current directory ~/

**NOTE:** The dep directory must be in the same directory as pg.exe

# BOTH #

  * Be sure to include INSTALL.txt and LICENSE.txt in the distributed zip archive