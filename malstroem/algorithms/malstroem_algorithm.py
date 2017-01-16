# -*- coding: utf-8 -*-

import os
from PyQt4.QtCore import QFileInfo
from processing.core.GeoAlgorithm import GeoAlgorithm
from ..malstroem_utils import MalstroemUtils

class MalstroemAlgorithm(GeoAlgorithm):
    
    def checkBeforeOpeningParametersDialog(self):
        if MalstroemUtils.MalstroemExePath() == '':
            return self.tr('Please set Menu->Processing->Options->Providers->Malstroem->Malstroem folder')
        else:
            return None
        
    def help(self):
        """Returns the help with the description of this algorithm.
        It returns a tuple boolean, string. IF the boolean value is True,
        it means that the string contains the actual description. If False,
        it is an url or path to a file where the description is stored.
        In both cases, the string or the content of the file have to be HTML,
        ready to be set into the help display component.

        Returns None if there is no help file available.

        The default implementation looks for an HTML page in the QGIS
        documentation site taking into account QGIS version.
        """

        path = QFileInfo(os.path.realpath(__file__)).path()
        help_path = path + '/../help/'
        helpUrl = help_path + 'help.html'
        return False, helpUrl

