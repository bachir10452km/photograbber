### [Revision 99](https://code.google.com/p/photograbber/source/detail?r=99): 3 June 2012 ###
  * **FEATURE**: Download 'liked' and 'subscribed' pages and users ([Issue 99](https://code.google.com/p/photograbber/issues/detail?id=99) and [Issue 101](https://code.google.com/p/photograbber/issues/detail?id=101))
  * **FIX** - [Issue 81](https://code.google.com/p/photograbber/issues/detail?id=81): Download highest resolution photo available
  * **FIX** - [Issue 40](https://code.google.com/p/photograbber/issues/detail?id=40): Preserve Facebook file naming

### [Revision 94](https://code.google.com/p/photograbber/source/detail?r=94): 15 April 2012 ###
  * **FEATURE**: Download multiple people at once, [Issue 18](https://code.google.com/p/photograbber/issues/detail?id=18)
  * **FEATURE**: Only download albums uploaded by the user, [Issue 79](https://code.google.com/p/photograbber/issues/detail?id=79)
  * **FIX** - [Issue 108](https://code.google.com/p/photograbber/issues/detail?id=108): Download interrupted by album fix error
  * **FIX** - [Issue 72](https://code.google.com/p/photograbber/issues/detail?id=72): Off by one display error
  * **FIX** - [Issue 35](https://code.google.com/p/photograbber/issues/detail?id=35): Login token display error

Known Issues:
  * Non-ascii album/path names may still cause error ([Issue 28](https://code.google.com/p/photograbber/issues/detail?id=28))
  * Paste login token does not work occasionally ([Issue 59](https://code.google.com/p/photograbber/issues/detail?id=59))

### [Revision 83](https://code.google.com/p/photograbber/source/detail?r=83): 6 July 2010 ###
  * **FIX** - [Issue 30](https://code.google.com/p/photograbber/issues/detail?id=30): "Entire album if it contains a tagged photo" feature now works
  * **FIX** - [Issue 31](https://code.google.com/p/photograbber/issues/detail?id=31): Error with pipe character in folder path
  * **FIX** - [Issue 32](https://code.google.com/p/photograbber/issues/detail?id=32): Retry option when obtaining profile information fails
  * **FIX** - [Issue 28](https://code.google.com/p/photograbber/issues/detail?id=28): Potentially fixed a Tkinter unicode path error

### [Revision 74](https://code.google.com/p/photograbber/source/detail?r=74): 1 July 2010 ###
  * **FIX** - [Issue 13](https://code.google.com/p/photograbber/issues/detail?id=13): silently ignore 404 errors
  * **FIX** - [Issue 15](https://code.google.com/p/photograbber/issues/detail?id=15): correctly create the download folder
  * **FEATURE**: Download a user's albums, [Issue 9](https://code.google.com/p/photograbber/issues/detail?id=9)
  * **FEATURE**: Download all albums a user is tagged in
  * **FEATURE**: Download comments/tag information
  * **FEATURE**: HTML album viewer created when downloading comments/tags
  * **FEATURE**: Concurrently download photos
  * Improved threading and handling of exit scenarios, [Issue 22](https://code.google.com/p/photograbber/issues/detail?id=22)
  * Improved error handling and logging
  * Failed queries are now repeated until successful
  * Photos are now sorted into album folders
  * File modification timestamps are now properly set
  * Updated Facebook authentication to work with the new API (http://developers.facebook.com/docs/authentication/desktop)

A special thanks to [Bryce Boe](http://www.bryceboe.com/) for his contributions ([Issue 27](https://code.google.com/p/photograbber/issues/detail?id=27))

![http://photograbber.googlecode.com/files/pg-r74.png](http://photograbber.googlecode.com/files/pg-r74.png)

### [Revision 36](https://code.google.com/p/photograbber/source/detail?r=36): 6 Jan 2010 ###
  * **FIX** - [Issue 7](https://code.google.com/p/photograbber/issues/detail?id=7): missing dll files on Windows
  * **FIX** - [Issue 8](https://code.google.com/p/photograbber/issues/detail?id=8): wrong python version on OSX
  * Updated distribution to include instructions and proper license

### [Revision 27](https://code.google.com/p/photograbber/source/detail?r=27): 20 Dec 2009 ###
  * **FIX** - [Issue 6](https://code.google.com/p/photograbber/issues/detail?id=6): Crash when selecting nothing from the "creep" list
  * Updated UI for clarity

![http://photograbber.googlecode.com/files/pg-r27.png](http://photograbber.googlecode.com/files/pg-r27.png)

### [Revision 23](https://code.google.com/p/photograbber/source/detail?r=23): 19 Dec 2009 ###
  * **FIX** - [Issue 5](https://code.google.com/p/photograbber/issues/detail?id=5): Exception thrown in download step on Ubuntu 9.04
  * **FIX** - [Issue 4](https://code.google.com/p/photograbber/issues/detail?id=4): Program hang on no available pictures
  * **FEATURE** - Now have the ability to download friends' pictures
  * Updated button graphics
  * Added option to post a story to your wall

![http://photograbber.googlecode.com/files/pg-r20.png](http://photograbber.googlecode.com/files/pg-r20.png)

### [Revision 7](https://code.google.com/p/photograbber/source/detail?r=7): 12 Oct 2009 ###
  * Initial Release

![http://photograbber.googlecode.com/files/pg.png](http://photograbber.googlecode.com/files/pg.png)