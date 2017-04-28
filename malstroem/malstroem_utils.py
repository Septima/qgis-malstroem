# -*- coding: utf-8 -*-
import os
import subprocess

from shutil import copyfile
import numpy as np

from osgeo import gdal, osr
import gdal
from gdalconst import *

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import QDir

from processing.core.ProcessingLog import ProcessingLog
from processing.core.ProcessingConfig import ProcessingConfig
from processing.tools import system
from processing.tools.raster import RasterWriter
from processing.algs.gdal.GdalUtils import GdalUtils

class MalstroemUtils:
    
    MALSTROEM_SCRIPT = 'MALSTROEM_SCRIPT'
    VECTOR_FORMATS = [
        'ESRI Shapefile',
        'GeoJSON',
        'GeoRSS',
        'SQLite',
        'GMT',
        'MapInfo File',
        'INTERLIS 1',
        'INTERLIS 2',
        'GML',
        'Geoconcept',
        'DXF',
        'DGN',
        'CSV',
        'BNA',
        'S57',
        'KML',
        'GPX',
        'PGDump',
        'GPSTrackMaker',
        'ODS',
        'XLSX',
        'PDF',
    ]
    
    VECTOR_EXTS = [
        '.shp',
        '.geojson',
        '.xml',
        '.sqlite',
        '.gmt',
        '.tab',
        '.ili',
        '.ili',
        '.gml',
        '.txt',
        '.dxf',
        '.dgn',
        '.csv',
        '.bna',
        '.000',
        '.kml',
        '.gpx',
        '.pgdump',
        '.gtm',
        '.ods',
        '.xlsx',
        '.pdf',
    ]
    
    @staticmethod
    def getSystemEncoding():
        settings = QSettings()
        return settings.value('/UI/encoding', 'System')

    @staticmethod
    def runMalstroemCommand(command, command_args, progress):
        popen_commands = [MalstroemUtils.MalstroemScript()]
        popen_commands.append(command)
        popen_commands.extend(command_args)
        loglines = ['Malstroem execution console output']
        loglines.append('Executing ' + ' '.join(popen_commands))
        progress.setInfo('Executing ' + ' '.join(popen_commands))

        shell = False
        env = {}
        if system.isWindows():
            # Some os env variables are required to run python o windows
            # SystemRoot is required for python
            # NUMBER_OF_CPUS is required for scipy
            shell = True
            qgisenv = dict(os.environ)
            # Remove PYTHONHOME as the malstroem exe MAY not be using the same python environment as QGIS 
            if qgisenv.has_key('PYTHONHOME'): 
                qgisenv.pop('PYTHONHOME')
            env = qgisenv


        proc = subprocess.Popen(
            popen_commands,
            stdout=subprocess.PIPE,
            stdin=open(os.devnull),
            stderr=subprocess.STDOUT,
            universal_newlines=False,
            cwd=MalstroemUtils.MalstroemScriptPath(),
            env=env,
            shell=shell
        )
        returncode = proc.wait()
        
        status_message = 'success'
        if returncode == 0:
           progress.setInfo(status_message)
           loglines.append(status_message)
           for line in iter(proc.stdout.readline, ''):
               progress.setInfo(line)
               loglines.append(line)
               ProcessingLog.addToLog(ProcessingLog.LOG_INFO, loglines)
           return True
        else:
           status_message = 'error:'
           progress.setInfo(status_message, True)
           loglines.append(status_message)
           for line in iter(proc.stdout.readline, ''):
               progress.setInfo(line, True)
               loglines.append(line)
               ProcessingLog.addToLog(ProcessingLog.LOG_ERROR, loglines)
           return False

    @staticmethod
    def getOutputDir():
        outputDir = system.getTempDirInTempFolder()
        if not QDir(outputDir).exists():
            QDir().mkpath(outputDir)
        return unicode(os.path.abspath(outputDir))
    
    @staticmethod
    def MalstroemScript():
        script = ProcessingConfig.getSetting(MalstroemUtils.MALSTROEM_SCRIPT)
        if script is None:
            script = ''
        return script
    
    @staticmethod
    def MalstroemScriptPath():
        path = os.path.dirname(os.path.abspath(MalstroemUtils.MalstroemScript()))
        return path
    
    @staticmethod
    def copyRasterToOutput(malstroem_out_dir, malstroem_out_filename, output_filename):
        malstroem_out_raster_dir = malstroem_out_dir
        input_full_filename = os.path.join(malstroem_out_raster_dir, malstroem_out_filename)
        
        copyfile(input_full_filename, output_filename)

    @staticmethod
    def GetRasterInfo(rasterFileName):
        SourceDS = gdal.Open(rasterFileName, GA_ReadOnly)
        NDV = SourceDS.GetRasterBand(1).GetNoDataValue()
        xsize = SourceDS.RasterXSize
        ysize = SourceDS.RasterYSize
        GeoT = SourceDS.GetGeoTransform()
        Projection = osr.SpatialReference()
        Projection.ImportFromWkt(SourceDS.GetProjectionRef())
        DataType = SourceDS.GetRasterBand(1).DataType
        DataType = gdal.GetDataTypeName(DataType)
        return NDV, xsize, ysize, GeoT, Projection, DataType
        
    @staticmethod
    def CreateRasterFile(NewFileName, Array, driver, NDV, xsize, ysize, GeoT, Projection, DataType):
        if DataType == 'Float32':
            DataType = gdal.GDT_Float32
        # Set nans to the original No Data Value
        Array[np.isnan(Array)] = NDV
        # Set up the dataset
        DataSet = driver.Create( NewFileName, xsize, ysize, 1, DataType )
                # the '1' is for band 1.
        DataSet.SetGeoTransform(GeoT)
        DataSet.SetProjection( Projection.ExportToWkt() )
        # Write the array
        DataSet.GetRasterBand(1).WriteArray( Array )
        DataSet.GetRasterBand(1).SetNoDataValue(NDV)
        return NewFileName
