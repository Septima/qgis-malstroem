# -*- coding: utf-8 -*-

from complete import Complete

from processing.core.outputs import OutputVector

from ..malstroem_utils import MalstroemUtils

class CompleteVector(Complete):
    OUTPUT_WATERSHEDS_LAYER = 'watersheds_vector'
    OUTPUT_BLUESPOTS_LAYER = 'bluespots_vector'

    def __init__(self):
        Complete.__init__(self)

    def defineCharacteristics(self):
        # The name that the user will see in the toolbox
        self.name = self.tr('Complete, vectorize watersheds and bluespots')

        # The branch of the toolbox under which the algorithm will appear
        self.group = self.tr('Short cuts (Perform all steps in one complete analysis)')

        self.addParameters()

        self.addOutputs()

    def addOutputs(self):
        Complete.addOutputs(self)
        self.addOutput(OutputVector(self.OUTPUT_WATERSHEDS_LAYER,
            self.tr('watersheds_vector')))

        self.addOutput(OutputVector(self.OUTPUT_BLUESPOTS_LAYER,
            self.tr('bluespots_vector')))

    def processAlgorithm(self, progress):
        command_args = self.getCommand_args()
        command_args.append('-vector')
        success = MalstroemUtils.runMalstroemCommand('complete', command_args, progress)
        if success:
            self.createOutput()

    def createOutput(self):
        Complete.createOutput(self)
        #Create vector files
        self.writeVectorOutput(
            'watersheds.shp',
            self.getOutputFromName(self.OUTPUT_WATERSHEDS_LAYER),
            self.getParameterValue(self.VECTOR_FORMAT))

        self.writeVectorOutput(
            'bluespots.shp',
            self.getOutputFromName(self.OUTPUT_BLUESPOTS_LAYER),
            self.getParameterValue(self.VECTOR_FORMAT))
