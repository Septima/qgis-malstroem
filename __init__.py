# -*- coding: utf-8 -*-
"""
/***************************************************************************
 class_name
                                 A QGIS plugin
 plugin_description
                              -------------------
        begin                : 2017-01-09
        copyright            : (C) 2017 by Septima for Kortforsyningen
        email                : kontakt(at)septima(dot)dk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Septima for Kortforsyningen'
__date__ = '2017-01-09'
__copyright__ = '(C) 2017 by Septima for Kortforsyningen'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load class_name class from file class_name.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .module_name import class_namePlugin
    return class_namePlugin()
