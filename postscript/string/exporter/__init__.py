#!/usr/bin/env python3
#
#
# Copyright (c) 2019, Ryo Nakamura.
# All rights reserved.
#
# $Id: $
#

import math
import re

import postscript.string.exporter.string
import postscript.string.exporter.constants.symbol

WIDTH_OF_SPACE = 278
SUBSCRIPT_FONTSIZE_FACTOR = 0.65
SUPERSCRIPT_FONTSIZE_FACTOR = 0.65

class Exporter():
    def __init__(self, str_, xpos=0, ypos=0, font='Helvetica', fontsize=12, degree=0):
        self.xpos = xpos
        self.ypos = ypos
        self.font = font
        self.fontsize = fontsize
        self.degree = degree
        self.str_objs = []

        self._parse(str_)
        self._layout()

    def _parse(self, str_):
        for token in re.split(r'\s+', str_):
            str_obj = None

            subscript_str, superscript_str = None, None
            if (re.search(r'^\$.+\$$', token)):
                token = re.sub(r'^\$', '', token); token = re.sub(r'\$$', '', token)

                # find subscript
                m = re.search(r'_{?([^\{\}\^]+)}?', token)
                if m:
                    subscript_str = m.group(1)
                    token = re.sub(r'_{?[^\{\}\^]+}?', '', token)

                # find superscript
                m = re.search(r'\^{?([^\{\}_]+)}?', token)
                if m:
                    superscript_str = m.group(1)
                    token = re.sub(r'\^{?[^\{\}\^_]+}?', '', token)

                # find command
                font = 'Helvetica-Oblique'
                m = re.search(r'^\\(.+)', token)
                if m:
                    token = m.group(1)
                    symbol2char = postscript.string.exporter.constants.symbol.symbol2char()
                    token = symbol2char.get(token, token)
                    font = 'Symbol'

                # create a base-string object
                str_obj = self._compose_str_obj(token, font, self.fontsize)

                # attach a subscript object
                if subscript_str:
                    str_obj.subscript = self._compose_str_obj(
                        subscript_str,
                        'Helvetica-Oblique',
                        self.fontsize * SUBSCRIPT_FONTSIZE_FACTOR
                    )

                # attach a superscript object
                if superscript_str:
                    str_obj.superscript = self._compose_str_obj(
                        superscript_str,
                        'Helvetica-Oblique',
                        fontsize=self.fontsize * SUPERSCRIPT_FONTSIZE_FACTOR
                    )

            else:
                str_obj = self._compose_str_obj(token, self.font, self.fontsize)

            self.str_objs.append(str_obj)

    def _compose_str_obj(self, str_, font, fontsize):
        return postscript.string.exporter.string.Str(
            str_, font=font, fontsize=fontsize
        )

    def _layout(self):
        xpos, ypos, fontsize = self.xpos, self.ypos, self.fontsize
        theta = math.radians(self.degree)

        for obj in self.str_objs:
            obj.xpos, obj.ypos = xpos, ypos

            # subscript
            if obj.subscript:
                obj.subscript.xpos = xpos + obj.width() * math.cos(theta) + obj.fontsize * 0.14 * math.sin(theta)
                obj.subscript.ypos = ypos + obj.width() * math.sin(theta) - obj.fontsize * 0.14 * math.cos(theta)

            # superscript
            if obj.superscript:
                offset = 200 * obj.fontsize / 1000 if obj.font == 'Helvetica-Oblique' else 0
                obj.superscript.xpos = xpos + (obj.width() + offset) * math.cos(theta) - obj.fontsize * 0.5 * math.sin(theta)
                obj.superscript.ypos = ypos + (obj.width() + offset) * math.sin(theta) + obj.fontsize * 0.5 * math.cos(theta)

            xpos += obj.total_width() * math.cos(theta)
            ypos += obj.total_width() * math.sin(theta)

            xpos += WIDTH_OF_SPACE * obj.fontsize / 1000 * math.cos(theta);
            ypos += WIDTH_OF_SPACE * obj.fontsize / 1000 * math.sin(theta);

    def export(self):
        print(self.export_as_str())

    def export_as_str(self):
        buf = []
        buf.append("""\
%!
gsave
""")
        buf.append(self.export_str())
        buf.append("""\
%!
grestore
""")

        return "\n".join(buf)

    def export_str(self):
        buf = []
        for obj in self.str_objs:
            buf.append(self._render(obj))
            if obj.subscript:
                buf.append(self._render(obj.subscript))
            if obj.superscript:
                buf.append(self._render(obj.superscript))
        return "\n".join(buf)

    def _render(self, str_obj):
        return """\
/{} findfont {} scalefont setfont
{} {} moveto
gsave
  {} rotate
  0 setgray
  ({}) show
grestore
""".format(
    str_obj.font, str_obj.fontsize, str_obj.xpos, str_obj.ypos,
    self.degree, str_obj.str_)
