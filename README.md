# NAME

postscript-string-exporter - helper for exporting strings in PostScript language

# DESCRIPTION

TBD

# EXAMPLES

```python
from postscript.string.exporter import Exporter

exporter = Exporter(r'communication delay $\tau_{1,2}$', xpos=50, ypos=700)
exporter.export()
```

# INSTALLATION

```
$ git clone https://github.com/r-nakamura/postscript-string-exporter
$ cp [PATH_TO_AFM]/{Helvetica,Helvetica-Oblique,Symbol}.afm postscript-string-exporter/util/afm/
$ (cd postscript-string-exporter/util/; make)
$ pip3 install -e postscript-string-exporter
```

Note that `util/convert-{helvetica,symbol}.pl` require extra CPAN
modules, `List::MoreUtils` and `Path::Tiny`.

# SEE ALSO

cellx - command-driven drawing/visualization/animation/presentation tool ([https://github.com/h-ohsaki/cellx](https://github.com/h-ohsaki/cellx))

# AUTHOR

Ryo Nakamura <nakamura[atmark]zebulun.net>
