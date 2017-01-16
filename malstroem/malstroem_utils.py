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

from qgis.core import QgsVectorFileWriter

from processing.core.ProcessingLog import ProcessingLog
from processing.core.ProcessingConfig import ProcessingConfig
from processing.tools import system
from processing.tools import dataobjects, vector
from processing.tools.raster import RasterWriter

from processing.algs.gdal.GdalUtils import GdalUtils

class MalstroemUtils:
    
    MALSTROEM_FOLDER = 'MALSTROEM_FOLDER'
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
        popen_commands = [os.path.join(MalstroemUtils.MalstroemExePath(), 'malstroem.exe')]
        popen_commands.append(command)
        popen_commands.extend(command_args)
        loglines = ['Malstroem execution console output']
        loglines.append('Executing ' + ' '.join(popen_commands))
        progress.setInfo('Executing ' + ' '.join(popen_commands))
        #path = "C:\\Program Files\\ConEmu\\ConEmu\\Scripts;C:\\Program Files\\ConEmu;C:\\Program Files\\ConEmu\\ConEmu;C:\\ProgramData\\Oracle\\Java\\javapath;C:\\Program Files (x86)\\Intel\\iCLS Client\\;C:\\Program Files\\Intel\\iCLS Client\\;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\Program Files\\Intel\\Intel(R) Management Engine Components\\DAL;C:\\Program Files\\Intel\\Intel(R) Management Engine Components\\IPT;C:\\Program Files (x86)\\Intel\\Intel(R) Management Engine Components\\DAL;C:\\Program Files (x86)\\Intel\\Intel(R) Management Engine Components\\IPT;C:\\Program Files\\Intel\\WiFi\\bin\\;C:\\Program Files\\Common Files\\Intel\\WirelessCommon\\;C:\\Users\\KlavsPihlkjær\\.dnx\\bin;C:\\Program Files\\Microsoft DNX\\Dnvm\\;C:\\Program Files\\Microsoft SQL Server\\Client SDK\\ODBC\\110\\Tools\\Binn\\;C:\\Program Files (x86)\\Microsoft SQL Server\\120\\Tools\\Binn\\;C:\\Program Files\\Microsoft SQL Server\\120\\Tools\\Binn\\;C:\\Program Files\\Microsoft SQL Server\\120\\DTS\\Binn\\;C:\\Program Files (x86)\\Microsoft SQL Server\\120\\Tools\\Binn\\ManagementStudio\\;C:\\Program Files (x86)\\Microsoft SQL Server\\120\\DTS\\Binn\\;C:\\Program Files (x86)\\Windows Kits\\10\\Windows Performance Toolkit\\;C:\\Program Files\\Git\\cmd;C:\\Program Files (x86)\\VIDIA Corporation\\PhysX\\Common;C:\\Program Files\\Git\\bin;C:\\Program Files\\Eclipse Che\\eclipse-che-4.0.0-RC3\\tools\\jre\\bin;C:\\Program Files\\Docker Toolbox;C:\\Users\\kpc\\AppData\\Roaming\\pm;C:\\Program Files\\odejs\\;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\Users\\kpc\\AppData\\Roaming\\pm;C:\\Python27;C:\\Users\\kpc\\AppData\\Local\\Microsoft\\WindowsApps;C:\\OSGeo4W64\\bin"

        proc = subprocess.Popen(
            popen_commands,
            shell=True,
            stdout=subprocess.PIPE,
            stdin=open(os.devnull),
            stderr=subprocess.STDOUT,
            universal_newlines=False,
            cwd = MalstroemUtils.MalstroemExePath(),
            env= {'SystemRoot': 'C:\\Windows'}
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
    def MalstroemExePath():
        folder = ProcessingConfig.getSetting(MalstroemUtils.MALSTROEM_FOLDER)
        if folder is None:
            folder = ''
        return folder
    
    @staticmethod
    def writeVectorOutput(malstroem_outdir, input_filename, output, format_idx):
        vector_dir = os.path.join(malstroem_outdir, 'vector')
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

    @staticmethod
    def writeRasterOutput(malstroem_out_dir, malstroem_out_filename, output):
        output_filename = output.value
        if os.path.basename(output_filename) == malstroem_out_filename:
            #if file names are equal just copy
            MalstroemUtils.copyRasterToOutput(malstroem_out_dir, malstroem_out_filename, output_filename)
        else:
            if not output_filename.endswith('.tif'):
                output_filename += '.tif'
                output.value = output_filename
            #Convert
            malstroem_out_raster_dir = malstroem_out_dir
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
    
