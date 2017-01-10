import os
import subprocess
from PyQt4.QtCore import QCoreApplication
from processing.core.ProcessingLog import ProcessingLog
from processing.core.ProcessingConfig import ProcessingConfig
from processing.tools.system import userFolder


class MalstroemUtils:
    
    @staticmethod
    def runMalstroem(commands, progress):
        exeCommands = [os.path.join(FusionUtils.FusionPath(), 'malstroem.exe')]
        exeCommands.extend(commands)
        loglines = []
        loglines.append(
            QCoreApplication.translate('Malstroem',
                                       'Malstroem execution console output'))
        proc = subprocess.Popen(
            exeCommands,
            shell=True,
            stdout=subprocess.PIPE,
            stdin=open(os.devnull),
            stderr=subprocess.STDOUT,
            universal_newlines=False,
        ).stdout
        for line in iter(proc.readline, ''):
            loglines.append(line)
        ProcessingLog.addToLog(ProcessingLog.LOG_INFO, loglines)