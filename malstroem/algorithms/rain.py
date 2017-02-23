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

from PyQt4.QtCore import QDir

from malstroem_algorithm import MalstroemAlgorithm
from ..malstroem_utils import MalstroemUtils

class Rain(MalstroemAlgorithm):
    VECTOR_FORMAT = 'VECTOR_FORMAT'
    OUTPUT_EVENTS_LAYER = 'events'
    INPUT_LAYER = 'INPUT_LAYER'
    RAIN_MM = 'RAIN_MM'
    
    def __init__(self):
        MalstroemAlgorithm.__init__(self)

    def defineCharacteristics(self):
        # The name that the user will see in the toolbox
        self.name = self.tr('Calculate bluespot fill and spill volumes for specific rain event')

        # The branch of the toolbox under which the algorithm will appear
        self.group = self.tr('Individual steps')

        self.addParameters()

        self.addOutputs()

    def addParameters(self):
        self.addParameter(ParameterVector(self.INPUT_LAYER,
            self.tr('Nodes (Vector)'), False, False))

        self.addParameter(ParameterNumber(
            self.RAIN_MM, self.tr("Rain incident in mm  (required)"), 0, None, 10))
        
        self.addParameter(ParameterSelection(self.VECTOR_FORMAT,
            self.tr('Vector destination Format'), MalstroemUtils.VECTOR_FORMATS))

    def addOutputs(self):
        self.addOutput(OutputVector(self.OUTPUT_EVENTS_LAYER,
            self.tr('Events')))

    def processAlgorithm(self, progress):
        MalstroemAlgorithm.processAlgorithm(self, progress)
        command_args = self.getCommand_args()
        QDir().mkpath(self.malstroem_outdir + '/vector')
        success = MalstroemUtils.runMalstroemCommand('rain', command_args, progress)
        if success:
            self.createOutput()

    def getCommand_args(self):
        command_args = []
        inputFilename = self.getParameterValue(self.INPUT_LAYER)
        command_args.extend(['-nodes', inputFilename])
        command_args.extend(['-nodes_layer', os.path.basename(inputFilename).split(".")[0]])
        rainMM = self.getParameterValue(self.RAIN_MM)
        command_args.extend(['-r', str(rainMM)])
        command_args.extend(['-out', self.malstroem_outdir + '/vector'])
        command_args.extend(['-out_layer', self.OUTPUT_EVENTS_LAYER])
        return command_args
    
    def createOutput(self):
        self.writeVectorOutput(
            'events.shp',
            self.getOutputFromName(self.OUTPUT_EVENTS_LAYER),
            self.getParameterValue(self.VECTOR_FORMAT))
