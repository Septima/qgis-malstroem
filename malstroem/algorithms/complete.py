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
    OUTPUT_LABELLED_RASTER = 'labelled'
    OUTPUT_WATERSHEDS_RASTER = 'watersheds'
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

        self.addParameter(ParameterNumber(
            self.RAIN_MM, self.tr("Rain incident in mm  (required)"), 0, None, 10))

        self.addParameter(ParameterBoolean(self.ACCUMULATE,
            self.tr("Calculate accumulated flow"), False))

        self.addParameter(ParameterBoolean(self.VECTOR,
            self.tr("Vectorize bluespots and watersheds"), False))
        
        self.addParameter(ParameterString(self.FILTER,
            self.tr("Filter bluespots by area, maximum depth and volume. E.g.: 'area > 20.5 and (maxdepth > 0.05 or volume >  2.5)'"), False))
        
        self.addParameter(ParameterSelection(self.VECTOR_FORMAT,
            self.tr('Vector destination Format'), MalstroemUtils.VECTOR_FORMATS))
        
        self.addOutput(OutputVector(self.OUTPUT_EVENTS_LAYER,
            self.tr('Events')))

        self.addOutput(OutputVector(self.OUTPUT_NODES_LAYER,
            self.tr('Nodes')))

        self.addOutput(OutputVector(self.OUTPUT_POURPOINTS_LAYER,
            self.tr('Pourpoints')))
        
        self.addOutput(OutputVector(self.OUTPUT_STREAMS_LAYER,
            self.tr('Streams')))

        self.addOutput(OutputRaster(self.OUTPUT_FILLED_RASTER,
            self.tr('Filled')))

    def processAlgorithm(self, progress):
        #Prepare call to malstroem
        #Example: complete -dem C:\Users\kpc\git\malstroem\tests\data\dtm.tif -r 10 -outdir c:\temp\kpc
        command = 'complete'
        command_args = []
        inputFilename = self.getParameterValue(self.INPUT_LAYER)
        command_args.extend(['-dem', inputFilename])
        rainMM = self.getParameterValue(self.RAIN_MM)
        command_args.extend(['-r', str(rainMM)])
        malstroem_outdir = MalstroemUtils.getOutputDir()
        command_args.extend(['-outdir', malstroem_outdir])
        success = MalstroemUtils.runMalstroemCommand(command, command_args, progress)
        if success:
            #Create processing output from malstroem output
            
            #Create vector files
            MalstroemUtils.writeVectorOutput(
                malstroem_outdir,
                'events.shp',
                #self.getOutputValue(self.OUTPUT_EVENTS_LAYER),
                self.getOutputFromName(self.OUTPUT_EVENTS_LAYER),
                self.getParameterValue(self.VECTOR_FORMAT))
    
            MalstroemUtils.writeVectorOutput(
                malstroem_outdir,
                'streams.shp',
                self.getOutputFromName(self.OUTPUT_STREAMS_LAYER),
                self.getParameterValue(self.VECTOR_FORMAT))
    
            MalstroemUtils.writeVectorOutput(
                malstroem_outdir,
                'nodes.shp',
                self.getOutputFromName(self.OUTPUT_NODES_LAYER),
                self.getParameterValue(self.VECTOR_FORMAT))
    
            MalstroemUtils.writeVectorOutput(
                malstroem_outdir,
                'pourpoints.shp',
                self.getOutputFromName(self.OUTPUT_POURPOINTS_LAYER),
                self.getParameterValue(self.VECTOR_FORMAT))

            #Write output to raster file
            MalstroemUtils.writeRasterOutput(
                malstroem_outdir,
                'filled.tif',
                self.getOutputFromName(self.OUTPUT_FILLED_RASTER))
