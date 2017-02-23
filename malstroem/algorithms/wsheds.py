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

class Wsheds(MalstroemAlgorithm):
    VECTOR_FORMAT = 'VECTOR_FORMAT'
    OUTPUT_WATERSHEDS_RASTER = 'watersheds'
    INPUT_LAYER = 'INPUT_LAYER'
    INPUT_LAYER2 = 'INPUT_LAYER2'
    
    def __init__(self):
        MalstroemAlgorithm.__init__(self)

    def defineCharacteristics(self):
        # The name that the user will see in the toolbox
        self.name = self.tr('Calculate bluespot watersheds')

        # The branch of the toolbox under which the algorithm will appear
        self.group = self.tr('Individual steps')

        self.addParameters()

        self.addOutputs()

    def addParameters(self):
        self.addParameter(ParameterRaster(self.INPUT_LAYER,
            self.tr('Bluespot file (Raster)'), False, False))

        self.addParameter(ParameterRaster(self.INPUT_LAYER2,
            self.tr('Flow directions file (Raster)'), False, False))

    def addOutputs(self):
        self.addOutput(OutputRaster(self.OUTPUT_WATERSHEDS_RASTER,
            self.tr('Watersheds')))

    def processAlgorithm(self, progress):
        MalstroemAlgorithm.processAlgorithm(self, progress)
        command_args = self.getCommand_args()
        success = MalstroemUtils.runMalstroemCommand('wsheds', command_args, progress)
        if success:
            self.createOutput()

    def getCommand_args(self):
        command_args = []
        inputFilename = self.getParameterValue(self.INPUT_LAYER)
        command_args.extend(['-bluespots', inputFilename])
        inputFilename2 = self.getParameterValue(self.INPUT_LAYER2)
        command_args.extend(['-flowdir', inputFilename2])
        command_args.extend(['-out', self.malstroem_outdir + '/watersheds.tif'])
        return command_args
    
    def createOutput(self):
        self.writeRasterOutput(
            'watersheds.tif',
            self.getOutputFromName(self.OUTPUT_WATERSHEDS_RASTER))
