.PHONY: acta check
acta:
	pdflatex -interaction=nonstopmode -halt-on-error manuscript_ActaMechanica.tex
	bibtex manuscript_ActaMechanica
	pdflatex -interaction=nonstopmode -halt-on-error manuscript_ActaMechanica.tex
	pdflatex -interaction=nonstopmode -halt-on-error manuscript_ActaMechanica.tex
	pdflatex -interaction=nonstopmode -halt-on-error cover_letter_ActaMechanica.tex
check:
	python3 tools/check_acta.py
