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
        if os.path.basename(output_filename) == malstroem_out_filename:
            #if file names are equal just copy
            MalstroemUtils.copyRasterToOutput(self.malstroem_outdir, malstroem_out_filename, output_filename)
        else:
            if not output_filename.endswith('.tif'):
                output_filename += '.tif'
                output.value = output_filename
            #Convert
            malstroem_out_raster_dir = self.malstroem_outdir
            FileName = os.path.join(malstroem_out_raster_dir, malstroem_out_filename)
            DataSet = gdal.Open(FileName, GA_ReadOnly)
            # Get the first (and only) band.
            Band = DataSet.GetRasterBand(1)
            # Open as an array.
            Array = Band.ReadAsArray()
            # Get the No Data Value
            NDV = Band.GetNoDataValue()
            # Convert No Data Points to nans
            Array[Array == NDV] = np.nan
            
            # Now I'm ready to save the new file, in the meantime I have 
            # closed the original, so I reopen it to get the projection
            # information...
            NDV, xsize, ysize, GeoT, Projection, DataType = MalstroemUtils.GetRasterInfo(FileName)
            
            # Set up the correct output driver
            driver = gdal.GetDriverByName('GTiff')
            
            MalstroemUtils.CreateRasterFile(output_filename, Array, driver, NDV, xsize, ysize, GeoT, Projection, DataType)

    def checkBeforeOpeningParametersDialog(self):
        if MalstroemUtils.MalstroemExePath() == '':
            return self.tr('Please set Menu->Processing->Options->Providers->Malstroem->Malstroem folder')
        else:
            return None
        
    def help(self):
        path = QFileInfo(os.path.realpath(__file__)).path()
        help_path = path + '/../help/'
        helpUrl = help_path + 'help.html'
        return False, helpUrl

