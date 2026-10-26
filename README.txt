AMM-formatted manuscript source package
=======================================

Files
-----
manuscript_AMM.tex   AMM-formatted manuscript (Anjali Patel first; Vipin Gupta corresponding)
cover_letter_AMM.tex AMM cover letter, signed by corresponding author Vipin Gupta
Shangda1226.sty      Supplied AMM style file; abstract environment closure corrected
references.bib       Bibliography database
figures/             All eight figures referenced by the manuscript

Compile (from this directory)
-----------------------------
pdflatex manuscript_AMM.tex
bibtex manuscript_AMM
pdflatex manuscript_AMM.tex
pdflatex manuscript_AMM.tex
pdflatex cover_letter_AMM.tex

The AMM running-header fields (year, volume, issue, first page, and DOI) are
set to the values used in the supplied AMM example and can be changed in the
preamble if the journal requests different submission metadata. The manuscript
and cover-letter sources were not compiled to PDF in this workspace because a
LaTeX toolchain is not installed here.

Acta Mechanica version
---------------------
See ACTA_MECHANICA_NOTES.md for the new Springer Nature two-column source,
numbered mathematics/physics references, build commands, and author-review checklist.
Main file: manuscript_ActaMechanica.tex
Build: make acta
Static checks: make check
The AMM originals are preserved. The Acta version has not been compiled here;
a compiled, visually inspected PDF must be added before journal submission.
