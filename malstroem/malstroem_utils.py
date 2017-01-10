import os
import subprocess
from PyQt4.QtCore import QCoreApplication
from processing.core.ProcessingLog import ProcessingLog
from processing.core.ProcessingConfig import ProcessingConfig
from processing.tools.system import userFolder
from hashlib import algorithms


class MalstroemUtils:
    
    MALSTROEM_FOLDER = 'MALSTROEM_FOLDER' 

    @staticmethod
    def runMalstroem(commands, progress):
        exeCommands = [os.path.join(MalstroemUtils.Path(), 'malstroem.exe')]
        exeCommands.extend(commands)
        loglines = ['Malstroem execution console output']
        
        loglines.append('Executing ' + ''.join(exeCommands))
#        proc = subprocess.Popen(
#            exeCommands,
#           shell=True,
#           stdout=subprocess.PIPE,
#           stdin=open(os.devnull),
#           stderr=subprocess.STDOUT,
#           universal_newlines=False,
#       ).stdout
#       for line in iter(proc.readline, ''):
#           loglines.append(line)
        ProcessingLog.addToLog(ProcessingLog.LOG_INFO, loglines)
        
    @staticmethod
    def getTempDir(algorithm):
        return ProcessingConfig.getSetting(ProcessingConfig.OUTPUT_FOLDER) + '/malstroem/' + algorithm
    
    @staticmethod
    def Path():
        folder = ProcessingConfig.getSetting(MalstroemUtils.MALSTROEM_FOLDER)
        if folder is None:
            folder = ''

        return folder