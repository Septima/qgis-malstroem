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

from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterBoolean
from processing.core.parameters import ParameterNumber
from processing.core.parameters import ParameterString
from processing.core.parameters import ParameterRaster
from processing.core.parameters import ParameterSelection
from processing.core.outputs import OutputVector, OutputRaster

from malstroem_algorithm import MalstroemAlgorithm
from ..malstroem_utils import MalstroemUtils

class Complete(MalstroemAlgorithm):
    VECTOR_FORMAT = 'VECTOR_FORMAT'
    OUTPUT_EVENTS_LAYER = 'events'
    OUTPUT_NODES_LAYER = 'nodes'
    OUTPUT_POURPOINTS_LAYER = 'pourpoints'
    OUTPUT_STREAMS_LAYER = 'streams'
    OUTPUT_DEPTHS_RASTER = 'depths'
    OUTPUT_FILLED_RASTER = 'filled'
    OUTPUT_FLOWDIR_RASTER = 'flowdir'
    OUTPUT_LABELED_RASTER = 'labeled'
    OUTPUT_WATERSHEDS_RASTER = 'watersheds'
    OUTPUT_ACCUMULATED_RASTER = 'accum'
    INPUT_LAYER = 'INPUT_LAYER'
    RAIN_MM = 'RAIN_MM'
    FILTER = 'FILTER'
    
    def __init__(self):
        MalstroemAlgorithm.__init__(self)

    def defineCharacteristics(self):
        # The name that the user will see in the toolbox
        self.name = self.tr('Complete')

        # The branch of the toolbox under which the algorithm will appear
        self.group = self.tr('Short cuts (Perform all steps in one complete analysis)')

        self.addParameters()

        self.addOutputs()

    def addParameters(self):
        self.addParameter(ParameterRaster(self.INPUT_LAYER,
            self.tr('Input DEM (Raster)'), False, False))

        self.addParameter(ParameterNumber(
            self.RAIN_MM, self.tr("Rain incident in mm  (required)"), 0, None, 10))

        self.addParameter(ParameterString(self.FILTER,
            self.tr("Filter bluespots by area, maximum depth and volume. E.g.: area > 20.5 and (maxdepth > 0.05 or volume >  2.5)"), False))
        
        self.addParameter(ParameterSelection(self.VECTOR_FORMAT,
            self.tr('Vector destination Format'), MalstroemUtils.VECTOR_FORMATS))

    def addOutputs(self):
        self.addOutput(OutputVector(self.OUTPUT_EVENTS_LAYER,
            self.tr('Events')))

        self.addOutput(OutputVector(self.OUTPUT_NODES_LAYER,
            self.tr('Nodes')))

        self.addOutput(OutputVector(self.OUTPUT_POURPOINTS_LAYER,
            self.tr('Pourpoints')))
        
        self.addOutput(OutputVector(self.OUTPUT_STREAMS_LAYER,
            self.tr('Streams')))

        self.addOutput(OutputRaster(self.OUTPUT_DEPTHS_RASTER,
            self.tr('Depths')))

        self.addOutput(OutputRaster(self.OUTPUT_FILLED_RASTER,
            self.tr('Filled')))

        self.addOutput(OutputRaster(self.OUTPUT_FLOWDIR_RASTER,
            self.tr('Flowdir')))

        self.addOutput(OutputRaster(self.OUTPUT_LABELED_RASTER,
            self.tr('Labeled')))

        self.addOutput(OutputRaster(self.OUTPUT_WATERSHEDS_RASTER,
            self.tr('watersheds')))

        self.addOutput(OutputRaster(self.OUTPUT_ACCUMULATED_RASTER,
            self.tr('accum')))

    def processAlgorithm(self, progress):
        command_args = self.getCommand_args()
        success = MalstroemUtils.runMalstroemCommand('complete', command_args, progress)
        if success:
            self.createOutput()

    def getCommand_args(self):
        #Example: complete -dem C:\Users\kpc\git\malstroem\tests\data\dtm.tif -r 10 -outdir c:\temp\kpc -accum
        command_args = []
        inputFilename = self.getParameterValue(self.INPUT_LAYER)
        command_args.extend(['-dem', inputFilename])
        rainMM = self.getParameterValue(self.RAIN_MM)
        command_args.extend(['-r', str(rainMM)])
        command_args.extend(['-outdir', self.malstroem_outdir])
        command_args.append('-accum')
        filter = self.getParameterValue(self.FILTER)
        if filter != '':
            command_args.extend(['-filter', '"' + filter + '"'])
        return command_args
    
    def createOutput(self):
         #Create processing output from malstroem complete
        
        #Create vector files
        self.writeVectorOutput(
            'events.shp',
            self.getOutputFromName(self.OUTPUT_EVENTS_LAYER),
            self.getParameterValue(self.VECTOR_FORMAT))

        self.writeVectorOutput(
            'streams.shp',
            self.getOutputFromName(self.OUTPUT_STREAMS_LAYER),
            self.getParameterValue(self.VECTOR_FORMAT))

        self.writeVectorOutput(
            'nodes.shp',
            self.getOutputFromName(self.OUTPUT_NODES_LAYER),
            self.getParameterValue(self.VECTOR_FORMAT))

        self.writeVectorOutput(
            'pourpoints.shp',
            self.getOutputFromName(self.OUTPUT_POURPOINTS_LAYER),
            self.getParameterValue(self.VECTOR_FORMAT))

        #Write output to raster file
        self.writeRasterOutput(
            'filled.tif',
            self.getOutputFromName(self.OUTPUT_FILLED_RASTER))
        
        self.writeRasterOutput(
            'depths.tif',
            self.getOutputFromName(self.OUTPUT_DEPTHS_RASTER))
        
        self.writeRasterOutput(
            'flowdir.tif',
            self.getOutputFromName(self.OUTPUT_FLOWDIR_RASTER))
        
        self.writeRasterOutput(
            'labeled.tif',
            self.getOutputFromName(self.OUTPUT_LABELED_RASTER))

        self.writeRasterOutput(
            'watersheds.tif',
            self.getOutputFromName(self.OUTPUT_WATERSHEDS_RASTER))

        self.writeRasterOutput(
            'accum.tif',
            self.getOutputFromName(self.OUTPUT_ACCUMULATED_RASTER))
