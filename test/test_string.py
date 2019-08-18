#!/usr/bin/env python3

import postscript.string.exporter.string

def test_init():
    str_obj = postscript.string.exporter.string.Str('dummy')

    assert str_obj.str_ == 'dummy'
    assert str_obj.xpos == 0
    assert str_obj.ypos == 0
    assert str_obj.font == 'Helvetica'
    assert str_obj.fontsize == 12
    assert str_obj.subscript == None
    assert str_obj.superscript == None

    str_obj = postscript.string.exporter.string.Str(
        'dummy', xpos=100, ypos=200, font='Helvetica', fontsize=18
    )

    assert str_obj.str_ == 'dummy'
    assert str_obj.xpos == 100
    assert str_obj.ypos == 200
    assert str_obj.font == 'Helvetica'
    assert str_obj.fontsize == 18
    assert str_obj.subscript == None
    assert str_obj.superscript == None

def test_width():
    str_obj = postscript.string.exporter.string.Str(
        'A', font='Helvetica', fontsize=12
    )
    assert str_obj.width() == 8.004

    str_obj = postscript.string.exporter.string.Str(
        'dummy', font='Helvetica', fontsize=12
    )
    assert str_obj.width() == 39.336
