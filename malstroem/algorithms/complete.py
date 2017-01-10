# -*- coding: utf-8 -*-

"""
/***************************************************************************
 malstroemPlugin
                                 A QGIS plugin
 plugin_description
                              -------------------
        begin                : 2017-01-09
        copyright            : (C) 2017 by Septima
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
"""

__author__ = 'Septima'
__date__ = '2017-01-09'
__copyright__ = '(C) 2017 by Septima'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from PyQt4.QtCore import QSettings
from qgis.core import QgsVectorFileWriter

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterBoolean
from processing.core.parameters import ParameterNumber
from processing.core.parameters import ParameterString
from processing.core.parameters import ParameterRaster
from processing.core.outputs import OutputVector
from processing.tools import dataobjects, vector
from ..malstroem_utils import MalstroemUtils


class Complete(GeoAlgorithm):
    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT_LAYER = 'OUTPUT_LAYER'
    INPUT_LAYER = 'INPUT_LAYER'
    RAIN_MM = 'RAIN_MM'
    ACCUMULATE = 'ACCUMULATE'
    VECTOR = 'VECTOR'
    FILTER = 'FILTER'

    def defineCharacteristics(self):
        # The name that the user will see in the toolbox
        self.name = self.tr('Complete (Perform all steps in one complete analysis)')

        # The branch of the toolbox under which the algorithm will appear
        self.group = self.tr('Short cut')

        self.addParameter(ParameterRaster(self.INPUT_LAYER,
            self.tr('Input DEM (Raster)'), False, False))

#        self.addOutput(OutputVector(self.OUTPUT_LAYER,
#            self.tr('Output layer with selected features')))

        self.addParameter(ParameterNumber(
            self.RAIN_MM, self.tr("Rain incident in mm  (required)"), 0, None, 0))

        self.addParameter(ParameterBoolean(self.ACCUMULATE,
            self.tr("Calculate accumulated flow"), False))

        self.addParameter(ParameterBoolean(self.VECTOR,
            self.tr("Vectorize bluespots and watersheds"), False))
        
        self.addParameter(ParameterString(self.FILTER,
            self.tr("Filter bluespots by area, maximum depth and volume. E.g.: 'area > 20.5 and (maxdepth > 0.05 or volume >  2.5)'"), False))
        
    def processAlgorithm(self, progress):
        commands = ['complete']
        #-dem C:\Users\kpc\git\malstroem\tests\data\dtm.tif -r 10 -outdir c:\temp\kpc
        inputFilename = self.getParameterValue(self.INPUT_LAYER)
        commands.extend(['-dem', inputFilename])
        rainMM = self.getParameterValue(self.RAIN_MM)
        commands.extend(['-r', str(rainMM)])
        outDir = MalstroemUtils.getTempDir('complete')
        commands.extend(['-outdir', outDir])
        MalstroemUtils.runMalstroem(commands, progress)
