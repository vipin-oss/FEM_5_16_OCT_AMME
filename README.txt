Acta Mechanica submission source package
=======================================

Layout:          Single-column working version
Main manuscript: manuscript_ActaMechanica.tex
Cover letter:    cover_letter_ActaMechanica.tex
Bibliography:    references.bib
Template:        sn-jnl.cls and sn-mathphys-num.bst
Figures:         figures/ (all eight manuscript figures)

Overleaf
--------
Pull the latest GitHub changes, select manuscript_ActaMechanica.tex as the
Main document, use pdfLaTeX, then Recompile from scratch.
To compile the cover letter, temporarily select cover_letter_ActaMechanica.tex.

Local build
-----------
make acta   (requires a full TeX Live/MiKTeX installation)
make check  (Python 3 static checks; no LaTeX compiler needed)

Review status
-------------
See ACTA_MECHANICA_NOTES.md and ACTA_SECOND_PASS_REVIEW.md for template
provenance, author-review items, bibliography gaps and modelling limitations.
Static checks do not replace PDF compilation and visual review.
No compiled or visually inspected submission PDF has been produced here.

Supplementary material
----------------------
No separate supplementary-material file or dataset is included. The eight figures
in figures/ belong to the main manuscript.
