# -*- coding: utf-8 -*-

"""
***************************************************************************
    UniqueValues.py
    ---------------------
    Date                 : August 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
from builtins import str

__author__ = 'Victor Olaya'
__date__ = 'August 2012'
__copyright__ = '(C) 2012, Victor Olaya'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
import codecs

from qgis.PyQt.QtGui import QIcon

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterTableField
from processing.core.outputs import OutputHTML
from processing.core.outputs import OutputNumber
from processing.core.outputs import OutputString
from processing.tools import dataobjects, vector

pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]


class UniqueValues(GeoAlgorithm):

    INPUT_LAYER = 'INPUT_LAYER'
    FIELD_NAME = 'FIELD_NAME'
    TOTAL_VALUES = 'TOTAL_VALUES'
    UNIQUE_VALUES = 'UNIQUE_VALUES'
    OUTPUT = 'OUTPUT'

    def getIcon(self):
        return QIcon(os.path.join(pluginPath, 'images', 'ftools', 'unique.png'))

    def defineCharacteristics(self):
        self.name, self.i18n_name = self.trAlgorithm('List unique values')
        self.group, self.i18n_group = self.trAlgorithm('Vector table tools')
        self.addParameter(ParameterVector(self.INPUT_LAYER,
                                          self.tr('Input layer')))
        self.addParameter(ParameterTableField(self.FIELD_NAME,
                                              self.tr('Target field'),
                                              self.INPUT_LAYER, ParameterTableField.DATA_TYPE_ANY))
        self.addOutput(OutputHTML(self.OUTPUT, self.tr('Unique values')))
        self.addOutput(OutputNumber(self.TOTAL_VALUES, self.tr('Total unique values')))
        self.addOutput(OutputString(self.UNIQUE_VALUES, self.tr('Unique values')))

    def processAlgorithm(self, feedback):
        layer = dataobjects.getObjectFromUri(self.getParameterValue(self.INPUT_LAYER))
        fieldName = self.getParameterValue(self.FIELD_NAME)
        outputFile = self.getOutputValue(self.OUTPUT)
        values = vector.getUniqueValues(layer, layer.fields().lookupField(fieldName))
        self.createHTML(outputFile, values)
        self.setOutputValue(self.TOTAL_VALUES, len(values))
        self.setOutputValue(self.UNIQUE_VALUES, ';'.join([str(v) for v in
                                                          values]))

    def createHTML(self, outputFile, algData):
        with codecs.open(outputFile, 'w', encoding='utf-8') as f:
            f.write('<html><head>')
            f.write('<meta http-equiv="Content-Type" content="text/html; \
                     charset=utf-8" /></head><body>')
            f.write(self.tr('<p>Total unique values: ') + str(len(algData)) + '</p>')
            f.write(self.tr('<p>Unique values:</p>'))
            f.write('<ul>')
            for s in algData:
                f.write('<li>' + str(s) + '</li>')
            f.write('</ul></body></html>')
