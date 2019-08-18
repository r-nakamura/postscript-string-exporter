all: ../postscript/string/exporter/constants/helvetica.py ../postscript/string/exporter/constants/helvetica_oblique.py ../postscript/string/exporter/constants/symbol.py

../postscript/string/exporter/constants/helvetica.py: afm/Helvetica.afm convert-helvetica.pl
	perl convert-helvetica.pl $< >$@

../postscript/string/exporter/constants/helvetica_oblique.py: afm/Helvetica-Oblique.afm convert-helvetica.pl
	perl convert-helvetica.pl $< >$@

../postscript/string/exporter/constants/symbol.py: afm/Symbol.afm convert-symbol.pl
	perl convert-symbol.pl $< >$@
