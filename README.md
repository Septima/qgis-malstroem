qgis-malstroem
==============
**gis-malstroem** is a QGIS plugin which adds a number of hydrology algorithms based on 
[malstroem](https://github.com/Kortforsyningen/malstroem) to the QGIS Processing toolbox.

Installation
------------
First [install malstroem](https://github.com/Kortforsyningen/malstroem/blob/master/README.md#installation). It can be 
installed into any python interpreter on your system. Specifically, you don't have to install it into the python 
interpreter used by QGIS.

A correctly installed **malstroem** provides a CLI executable. To configure **qgis-malstroem** correctly you will need 
the path to this executable.

If you haven't installed [QGIS](http://qgis.org/). Now is a good time to do so :-)

Install **qgis-malstroem** by copying the folder `malstroem` to your QGIS plugins folder. On Windows this folder is 
usually located at `C:\Users\{username}\.qgis2\python\plugins` on other systems usually at `~/.qgis2/python/plugins`.

After a QGIS restart the plugin should be available in the _Plugins_ dialog (Plugins -> Manage and Install Plugins). 
You may have to check the box next the plugin to activate the plugin.

Now open the _Processing Options_ dialog (Processing -> Options). Now, under _Providers_ you should see a _Malstroem_ 
entry (if not, check that all the above steps have been carried out). Make sure _Activate_ is checked. In 
_Mastroem script_ you put the path to the malstroem executable. 