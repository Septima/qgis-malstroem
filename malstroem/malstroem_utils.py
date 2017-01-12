# -*- coding: utf-8 -*-
import os
import subprocess
import shutil

from PyQt4.QtCore import QCoreApplication
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import QDir

from qgis.core import QgsVectorFileWriter

from osgeo import gdal

from processing.core.ProcessingLog import ProcessingLog
from processing.core.ProcessingConfig import ProcessingConfig
from processing.tools import system
from processing.tools import dataobjects, vector

class MalstroemUtils:
    
    MALSTROEM_FOLDER = 'MALSTROEM_FOLDER'

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
        path = "C:\\Program Files\\ConEmu\\ConEmu\\Scripts;C:\\Program Files\\ConEmu;C:\\Program Files\\ConEmu\\ConEmu;C:\\ProgramData\\Oracle\\Java\\javapath;C:\\Program Files (x86)\\Intel\\iCLS Client\\;C:\\Program Files\\Intel\\iCLS Client\\;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\Program Files\\Intel\\Intel(R) Management Engine Components\\DAL;C:\\Program Files\\Intel\\Intel(R) Management Engine Components\\IPT;C:\\Program Files (x86)\\Intel\\Intel(R) Management Engine Components\\DAL;C:\\Program Files (x86)\\Intel\\Intel(R) Management Engine Components\\IPT;C:\\Program Files\\Intel\\WiFi\\bin\\;C:\\Program Files\\Common Files\\Intel\\WirelessCommon\\;C:\\Users\\KlavsPihlkjær\\.dnx\\bin;C:\\Program Files\\Microsoft DNX\\Dnvm\\;C:\\Program Files\\Microsoft SQL Server\\Client SDK\\ODBC\\110\\Tools\\Binn\\;C:\\Program Files (x86)\\Microsoft SQL Server\\120\\Tools\\Binn\\;C:\\Program Files\\Microsoft SQL Server\\120\\Tools\\Binn\\;C:\\Program Files\\Microsoft SQL Server\\120\\DTS\\Binn\\;C:\\Program Files (x86)\\Microsoft SQL Server\\120\\Tools\\Binn\\ManagementStudio\\;C:\\Program Files (x86)\\Microsoft SQL Server\\120\\DTS\\Binn\\;C:\\Program Files (x86)\\Windows Kits\\10\\Windows Performance Toolkit\\;C:\\Program Files\\Git\\cmd;C:\\Program Files (x86)\\VIDIA Corporation\\PhysX\\Common;C:\\Program Files\\Git\\bin;C:\\Program Files\\Eclipse Che\\eclipse-che-4.0.0-RC3\\tools\\jre\\bin;C:\\Program Files\\Docker Toolbox;C:\\Users\\kpc\\AppData\\Roaming\\pm;C:\\Program Files\\odejs\\;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\Users\\kpc\\AppData\\Roaming\\pm;C:\\Python27;C:\\Users\\kpc\\AppData\\Local\\Microsoft\\WindowsApps;C:\\OSGeo4W64\\bin"

        proc = subprocess.Popen(
            popen_commands,
            shell=True,
            stdout=subprocess.PIPE,
            stdin=open(os.devnull),
            stderr=subprocess.STDOUT,
            universal_newlines=False,
            cwd = MalstroemUtils.MalstroemExePath(),
            env= {'path': path, 'SystemRoot': 'C:\\Windows'}
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
    def deleteTempDir(algorithm):
        shutil.rmtree(dir)
    
    @staticmethod
    def MalstroemExePath():
        folder = ProcessingConfig.getSetting(MalstroemUtils.MALSTROEM_FOLDER)
        if folder is None:
            folder = ''
        return folder
    
                
    @staticmethod
    def writeVectorOutput(malstroem_outdir, input_filename, output_filename):
        vector_dir = os.path.join(malstroem_outdir, 'vector')
        input_dataobject = dataobjects.getObjectFromUri(os.path.join(vector_dir, input_filename))
        input_provider = input_dataobject.dataProvider()
        writer = QgsVectorFileWriter(
            output_filename,
            MalstroemUtils.getSystemEncoding(),
            input_provider.fields(),
            input_provider.geometryType(),
            input_provider.crs())

        for feature in vector.features(input_dataobject):
            writer.addFeature(feature)
            
    @staticmethod
    def writeRasterOutput(malstroem_outdir, input_filename, output_filename):
        raster_dir = malstroem_outdir
        input_dataobject = dataobjects.getObjectFromUri(os.path.join(raster_dir, input_filename))
        input_provider = input_dataobject.dataProvider()

        output = self.getOutputFromName(output_filename)

        cellsize = (input_dataobject.extent().xMaximum() - input_dataobject.extent().xMinimum()) \
            / input_dataobject.width()

        w = RasterWriter(output.getCompatibleFileName(self),
                         input_dataobject.extent().xMinimum(),
                         input_dataobject.extent().yMinimum(),
                         input_dataobject.extent().xMaximum(),
                         input_dataobject.extent().yMaximum(),
                         cellsize,
                         1,
                         input_provider.crs(),
                         )
        #Get data
        inDs = gdal.Open(input_filename)
        band1 = inDs.GetRasterBand(1)
        rows = inDs.RasterYSize
        cols = inDs.RasterXSize
        data = band1.ReadAsArray(0,0,cols,rows)
        w.matrix= data
        w.close()
