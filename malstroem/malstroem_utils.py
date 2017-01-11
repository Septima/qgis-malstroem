# -*- coding: utf-8 -*-
import os
import subprocess
from PyQt4.QtCore import QCoreApplication
from processing.core.ProcessingLog import ProcessingLog
from processing.core.ProcessingConfig import ProcessingConfig
from hashlib import algorithms
import shutil
from processing.tools import system
from PyQt4.QtCore import QDir

class MalstroemUtils:
    
    MALSTROEM_FOLDER = 'MALSTROEM_FOLDER' 

    @staticmethod
    def runMalstroem(commands, progress):
        exeCommands = [os.path.join(MalstroemUtils.MalstroemExePath(), 'malstroem.exe')]
        exeCommands.extend(commands)
        loglines = ['Malstroem execution console output']
        loglines.append('Executing ' + ' '.join(exeCommands))
        progress.setInfo('Executing ' + ' '.join(exeCommands))
        path = "C:\\Program Files\\ConEmu\\ConEmu\\Scripts;C:\\Program Files\\ConEmu;C:\\Program Files\\ConEmu\\ConEmu;C:\\ProgramData\\Oracle\\Java\\javapath;C:\\Program Files (x86)\\Intel\\iCLS Client\\;C:\\Program Files\\Intel\\iCLS Client\\;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\Program Files\\Intel\\Intel(R) Management Engine Components\\DAL;C:\\Program Files\\Intel\\Intel(R) Management Engine Components\\IPT;C:\\Program Files (x86)\\Intel\\Intel(R) Management Engine Components\\DAL;C:\\Program Files (x86)\\Intel\\Intel(R) Management Engine Components\\IPT;C:\\Program Files\\Intel\\WiFi\\bin\\;C:\\Program Files\\Common Files\\Intel\\WirelessCommon\\;C:\\Users\\KlavsPihlkjær\\.dnx\\bin;C:\\Program Files\\Microsoft DNX\\Dnvm\\;C:\\Program Files\\Microsoft SQL Server\\Client SDK\\ODBC\\110\\Tools\\Binn\\;C:\\Program Files (x86)\\Microsoft SQL Server\\120\\Tools\\Binn\\;C:\\Program Files\\Microsoft SQL Server\\120\\Tools\\Binn\\;C:\\Program Files\\Microsoft SQL Server\\120\\DTS\\Binn\\;C:\\Program Files (x86)\\Microsoft SQL Server\\120\\Tools\\Binn\\ManagementStudio\\;C:\\Program Files (x86)\\Microsoft SQL Server\\120\\DTS\\Binn\\;C:\\Program Files (x86)\\Windows Kits\\10\\Windows Performance Toolkit\\;C:\\Program Files\\Git\\cmd;C:\\Program Files (x86)\\VIDIA Corporation\\PhysX\\Common;C:\\Program Files\\Git\\bin;C:\\Program Files\\Eclipse Che\\eclipse-che-4.0.0-RC3\\tools\\jre\\bin;C:\\Program Files\\Docker Toolbox;C:\\Users\\kpc\\AppData\\Roaming\\pm;C:\\Program Files\\odejs\\;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\Users\\kpc\\AppData\\Roaming\\pm;C:\\Python27;C:\\Users\\kpc\\AppData\\Local\\Microsoft\\WindowsApps;C:\\OSGeo4W64\\bin"
        #progress.setInfo('Environ: ' + str(os.environ))
        proc = subprocess.Popen(
            exeCommands,
            shell=True,
            stdout=subprocess.PIPE,
            stdin=open(os.devnull),
            stderr=subprocess.STDOUT,
            universal_newlines=False,
            cwd = MalstroemUtils.MalstroemExePath(),
            env= {'path': path, 'SystemRoot': 'C:\\Windows'}
        ).stdout
        for line in iter(proc.readline, ''):
           progress.setInfo(line)
           loglines.append(line)
        ProcessingLog.addToLog(ProcessingLog.LOG_INFO, loglines)

    @staticmethod
    def getOutputDir(algorithm):
        #outputDir = ProcessingConfig.getSetting(ProcessingConfig.OUTPUT_FOLDER) + os.sep + 'malstroem' + os.sep + algorithm
        #outputDir = system.getTempDirInTempFolder()
#        if os.path.exists(outputDir):
#            shutil.rmtree(outputDir)
#        os.makedirs(outputDir)
        #return outputDir
        #outputDir = os.path.join(unicode(QDir.tempPath()), 'processing')
        outputDir = system.getTempDirInTempFolder()
        if not QDir(outputDir).exists():
            QDir().mkpath(outputDir)
        return unicode(os.path.abspath(outputDir))
        #return tempfile.mkdtemp(dir = algDir)
    
    @staticmethod
    def deleteTempDir(algorithm):
        shutil.rmtree(dir)
    
    @staticmethod
    def MalstroemExePath():
        folder = ProcessingConfig.getSetting(MalstroemUtils.MALSTROEM_FOLDER)
        if folder is None:
            folder = ''

        return folder