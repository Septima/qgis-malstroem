# -*- coding: utf-8 -*-

"""
/***************************************************************************
 malstroemPlugin
                                 A QGIS plugin
 plugin_description
                              -------------------
        begin                : 2017-01-09
        copyright            : (C) 2017 by Septima
        email                : kontakt(at)septima(dot)dk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Septima'
__date__ = '2017-01-09'
__copyright__ = '(C) 2017 by Septima'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'
import os
import glob
from processing.core.AlgorithmProvider import AlgorithmProvider
from processing.core.ProcessingConfig import Setting, ProcessingConfig
from processing.modeler.ModelerAlgorithm import ModelerAlgorithm
from .algorithms.complete import Complete
from .algorithms.complete_vector import CompleteVector
from .algorithms.flowdir import Flowdir
from .algorithms.accum import Accum
from .algorithms.filled import Filled
from .algorithms.depths import Depths
from .algorithms.bspots import BSpots
from .algorithms.wsheds import Wsheds
from .algorithms.pourpts import Pourpts
from .algorithms.network import Network
from .algorithms.rain import Rain

from malstroem_utils import MalstroemUtils

pluginPath = os.path.split(os.path.realpath(__file__))[0]

class malstroemAlgorithmProvider(AlgorithmProvider):

    def __init__(self):
        AlgorithmProvider.__init__(self)

        # Deactivate provider by default
        self.activate = False

        # Load algorithms
        self.alglist = [Complete(), CompleteVector(), Flowdir(), Accum(),
                        Filled(), Depths(), BSpots(), Wsheds(), Pourpts(),
                        Network(), Rain()]

        # Note: Models are loaded dynamically below
        self.models = []
        self.modeldir = os.path.join(pluginPath, 'models/')

        for alg in self.alglist:
            alg.provider = self

    def initializeSettings(self):
        """In this method we add settings needed to configure our
        provider.

        Do not forget to call the parent method, since it takes care
        or automatically adding a setting for activating or
        deactivating the algorithms in the provider.
        """
        AlgorithmProvider.initializeSettings(self)
        ProcessingConfig.addSetting(Setting(self.getDescription(),
            MalstroemUtils.MALSTROEM_SCRIPT,
            'Malstroem script', '', valuetype=Setting.FILE))

    def unload(self):
        """Setting should be removed here, so they do not appear anymore
        when the plugin is unloaded.
        """
        AlgorithmProvider.unload(self)
        ProcessingConfig.removeSetting(
            MalstroemUtils.MALSTROEM_SCRIPT)

    def getName(self):
        """This is the name that will appear on the toolbox group.

        It is also used to create the command line name of all the
        algorithms from this provider.
        """
        return 'provider_name'

    def getDescription(self):
        return 'Malstroem'

    def getIcon(self):
        """We return the default icon.
        """
        return AlgorithmProvider.getIcon(self)

    def _loadAlgorithms(self):
        """Here we fill the list of algorithms in self.algs.

        This method is called whenever the list of algorithms should
        be updated. If the list of algorithms can change (for instance,
        if it contains algorithms from user-defined scripts and a new
        script might have been added), you should create the list again
        here.

        In this case, since the list is always the same, we assign from
        the pre-made list. This assignment has to be done in this method
        even if the list does not change, since the self.algs list is
        cleared before calling this method.
        """
        self._loadModels()
        self.algs = self.alglist + self.models

    def _loadModels(self):
        """Load models from the 'models' sub directory

        :return: List of ModelerAlgorithm
        """

        self.models = []

        for f in glob.glob(os.path.join(self.modeldir, '*.model')):
            m = ModelerAlgorithm.fromFile(f)
            m.provider = self
            self.models.append(m)