#!/usr/bin/env python3

import postscript.string.exporter

def test_init():
    exporter = postscript.string.exporter.Exporter('dummy')
    assert exporter.xpos == 0
    assert exporter.ypos == 0
    assert exporter.font == 'Helvetica'
    assert exporter.fontsize == 12
    assert exporter.degree == 0

    exporter = postscript.string.exporter.Exporter(
        'dummy', xpos=100, ypos=200, font='Helvetica-Oblique', fontsize=18, degree=45
    )
    assert exporter.xpos == 100
    assert exporter.ypos == 200
    assert exporter.font == 'Helvetica-Oblique'
    assert exporter.fontsize == 18
    assert exporter.degree == 45

def test_parse():
    exporter = postscript.string.exporter.Exporter('dummy')
    assert exporter.str_objs[0]
    assert exporter.str_objs[0].str_ == 'dummy'
    assert exporter.str_objs[0].font == 'Helvetica'

    exporter = postscript.string.exporter.Exporter(r'$x$')
    assert exporter.str_objs[0]
    assert exporter.str_objs[0].str_ == 'x'
    assert exporter.str_objs[0].font == 'Helvetica-Oblique'

    exporter = postscript.string.exporter.Exporter(r'$\alpha$')
    assert exporter.str_objs[0]
    assert exporter.str_objs[0].str_ == 'a'
    assert exporter.str_objs[0].font == 'Symbol'

    exporter = postscript.string.exporter.Exporter(r'$x^a$')
    assert exporter.str_objs[0]
    assert exporter.str_objs[0].str_ == 'x'
    assert exporter.str_objs[0].font == 'Helvetica-Oblique'
    assert exporter.str_objs[0].superscript
    assert exporter.str_objs[0].superscript.str_ == 'a'
    assert exporter.str_objs[0].superscript.font == 'Helvetica-Oblique'

    exporter = postscript.string.exporter.Exporter(r'$x_a$')
    assert exporter.str_objs[0]
    assert exporter.str_objs[0].str_ == 'x'
    assert exporter.str_objs[0].font == 'Helvetica-Oblique'
    assert exporter.str_objs[0].subscript
    assert exporter.str_objs[0].subscript.str_ == 'a'
    assert exporter.str_objs[0].subscript.font == 'Helvetica-Oblique'

    exporter = postscript.string.exporter.Exporter(r'$x^a_b$')
    assert exporter.str_objs[0]
    assert exporter.str_objs[0].str_ == 'x'
    assert exporter.str_objs[0].font == 'Helvetica-Oblique'
    assert exporter.str_objs[0].superscript
    assert exporter.str_objs[0].superscript.str_ == 'a'
    assert exporter.str_objs[0].superscript.font == 'Helvetica-Oblique'
    assert exporter.str_objs[0].subscript
    assert exporter.str_objs[0].subscript.str_ == 'b'
    assert exporter.str_objs[0].subscript.font == 'Helvetica-Oblique'

    exporter = postscript.string.exporter.Exporter('dummy1 dummy2')
    assert exporter.str_objs[0]
    assert exporter.str_objs[0].str_ == 'dummy1'
    assert exporter.str_objs[0].font == 'Helvetica'
    assert exporter.str_objs[1]
    assert exporter.str_objs[1].str_ == 'dummy2'
    assert exporter.str_objs[1].font == 'Helvetica'

def test_render():
    exporter = postscript.string.exporter.Exporter('dummy', 100, 200)
    expected = """\
/Helvetica findfont 12 scalefont setfont
100, 200 moveto
gsave
  0 rotate
  0 setgray
  (dummy) show
grestore
"""
    assert exporter._render(exporter.str_objs[0]), expected

def test_export_as_str():
    exporter = postscript.string.exporter.Exporter('dummy', 100, 200)
    expected = """\
%!
gsave

/Helvetica findfont 12 scalefont setfont
100 200 moveto
gsave
  0 rotate
  0 setgray
  (dummy) show
grestore

%!
grestore
"""
    assert exporter.export_as_str(), expected

    exporter = postscript.string.exporter.Exporter('$A$', 100, 200)
    expected = """\
%!
gsave

/Helvetica-Oblique findfont 12 scalefont setfont
100 200 moveto
gsave
  0 rotate
  0 setgray
  (A) show
grestore

%!
grestore
"""
    assert exporter.export_as_str(), expected

    exporter = postscript.string.exporter.Exporter(r'$\lambda$', 100, 200)
    expected = """\
%!
gsave

/Symbol findfont 12 scalefont setfont
100 200 moveto
gsave
  0 rotate
  0 setgray
  (l) show
grestore

%!
grestore
"""
    assert exporter.export_as_str(), expected
