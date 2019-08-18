#!/usr/bin/env python3
#
#
# Copyright (c) 2019, Ryo Nakamura.
# All rights reserved.
#
# $Id: $
#

import re

import postscript.string.exporter.constants.helvetica
import postscript.string.exporter.constants.helvetica_oblique
import postscript.string.exporter.constants.symbol

class Str():
    def __init__(self, str_, xpos=0, ypos=0, font='Helvetica', fontsize=12,
                 subscript=None, superscript=None):
        self.str_ = str_
        self.xpos = xpos
        self.ypos = ypos
        self.font = font
        self.fontsize = fontsize
        self.subscript = subscript
        self.superscript = superscript

    def total_width(self):
        width = self.width()
        subscript_width = self.subscript.width() if self.subscript else 0
        superscript_width = self.superscript.width() if self.superscript else 0
        width += max(subscript_width, superscript_width)
        return width

    def width(self):
        font = self.font.lower()
        font = re.sub('-', '_', font)
        wx = eval('postscript.string.exporter.constants.' + font).wx()
        width = sum([wx[c] for c in self.str_]) * self.fontsize / 1000
        return width
