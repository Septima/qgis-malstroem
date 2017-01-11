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

import os

from PyQt4.QtCore import QSettings
from qgis.core import QgsVectorFileWriter

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterBoolean
from processing.core.parameters import ParameterNumber
from processing.core.parameters import ParameterString
from processing.core.parameters import ParameterRaster
from processing.core.outputs import OutputVector, OutputRaster
from processing.tools import dataobjects, vector

from ..malstroem_utils import MalstroemUtils


class Complete(GeoAlgorithm):
    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT_FILL_RASTER = 'fill'
    OUTPUT_STREAMS_LAYER = 'streams'
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

#        self.addOutput(OutputRaster(self.OUTPUT_FILL_RASTER,
#            self.tr('Output raster with fill')))

        self.addOutput(OutputVector(self.OUTPUT_STREAMS_LAYER,
            self.tr('Output layer with streams')))

        self.addParameter(ParameterNumber(
            self.RAIN_MM, self.tr("Rain incident in mm  (required)"), 0, None, 10))

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
        outDir = MalstroemUtils.getOutputDir('complete')
        commands.extend(['-outdir', outDir])
        MalstroemUtils.runMalstroem(commands, progress)
        
        #Do output
        settings = QSettings()
        systemEncoding = settings.value('/UI/encoding', 'System')
        
        #Streams
        streams_output = self.getOutputValue(self.OUTPUT_STREAMS_LAYER)
        streams_layer = dataobjects.getObjectFromUri(os.path.join(outDir, 'streams.shp'))
        streams_provider = streams_layer.dataProvider()
        
        streams_writer = QgsVectorFileWriter(streams_output, systemEncoding,
                                     streams_provider.fields(),
                                     streams_provider.geometryType(), streams_provider.crs())
        
        streams_features = vector.features(streams_layer)
        for f in streams_features:
            streams_writer.addFeature(f)


        
        
