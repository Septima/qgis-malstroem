# -*- coding: utf-8 -*-

import os

from PyQt4.QtCore import QFileInfo

from qgis.core import QgsVectorFileWriter

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.tools import dataobjects, vector

from ..malstroem_utils import MalstroemUtils

class MalstroemAlgorithm(GeoAlgorithm):

    def __init__(self):
        GeoAlgorithm.__init__(self)
        self.malstroem_outdir = MalstroemUtils.getOutputDir()
        
    def writeVectorOutput(self, input_filename, output, format_idx):
        vector_dir = os.path.join(self.malstroem_outdir, 'vector')
        input_dataobject = dataobjects.getObjectFromUri(os.path.join(vector_dir, input_filename))
        input_provider = input_dataobject.dataProvider()
        
        output_filename = output.value
        out_format = MalstroemUtils.VECTOR_FORMATS[format_idx]
        ext = MalstroemUtils.VECTOR_EXTS[format_idx]
        if not output_filename.endswith(ext):
            output_filename += ext
            output.value = output_filename

        writer = QgsVectorFileWriter(
            output_filename,
            MalstroemUtils.getSystemEncoding(),
            input_provider.fields(),
            input_provider.geometryType(),
            input_provider.crs(),
            driverName = out_format)

        for feature in vector.features(input_dataobject):
            writer.addFeature(feature)

    def writeRasterOutput(self, malstroem_out_filename, output):
        output_filename = output.value
        if not output_filename.endswith('.tif'):
            output_filename += '.tif'
            output.value = output_filename
        if output_filename == malstroem_out_filename:
            return
        else:
            MalstroemUtils.copyRasterToOutput(self.malstroem_outdir, malstroem_out_filename, output_filename)


    def checkBeforeOpeningParametersDialog(self):
        if MalstroemUtils.MalstroemScript() == '':
            return self.tr('Please set Menu->Processing->Options->Providers->Malstroem->Malstroem script')
        else:
            return None
        
    def help(self):
        path = QFileInfo(os.path.realpath(__file__)).path()
        help_path = path + '/../help/'
        helpUrl = help_path + 'help.html'
        return False, helpUrl

