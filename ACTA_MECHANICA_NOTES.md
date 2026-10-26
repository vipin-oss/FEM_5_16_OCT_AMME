# Acta Mechanica conversion — author review required

## Files
- `manuscript_ActaMechanica.tex`: main source; Springer Nature `sn-jnl`, `iicol`, `sn-mathphys-num`.
- `cover_letter_ActaMechanica.tex`: retargeted cover letter.
- `sn-jnl.cls`, `sn-mathphys-num.bst`: template dependencies.
- `references.bib`, `figures/`: original bibliography and eight figures, unchanged.
- Only the Acta Mechanica submission sources and their supporting files are retained.

## Basis and provenance
Acta Mechanica guidelines: https://link.springer.com/journal/707/submission-guidelines
(accessed 26 October 2026). The guidelines recommend the Springer Nature LaTeX
template with `iicol`; numbered citations and full DOI links are required.
Template files were obtained from this public mirror:
https://github.com/DanySK/template-latex-springer-nature-sn-jnl
The mirror carries the Springer Nature template, version 3 October 2023.
Its repository license is supplied as `SPRINGER_TEMPLATE_LICENSE.txt`; file-level
notices in the class and bibliography style remain intact. This is not a claim
that the mirror is the latest publisher distribution. Before submission, compare
against the template downloadable from the current publisher guidelines.

## Changes
- New mechanics-focused title, abstract, keywords and contribution paragraph.
- Preserved author order, affiliations and corresponding-author email.
- Replaced legacy headers/assigned-looking publication metadata with Springer author macros.
- Replaced superscript citations with numbered bracket citations; the class selects
  `sn-mathphys-num.bst`, which renders DOI fields as full https://doi.org/ links.
- Wide figures/tables use two-column floats; wide mathematical displays use `cuted`
  strips so existing equations need not be shrunk into narrow columns.
- Kept every mathematical display and numerical result unchanged.
- Clarified that the constitutive reduction is established, not a new law, and that
  BFS continuity is not required by the classical model used for reported results.
- Added explicit scope/limitations and structured existing declarations.
- Corrected one missing inline-math closing `$` inherited from the earlier source.
- No experiments, benchmarks, author roles or new scientific results were invented.

## Build
With a complete TeX Live/MiKTeX installation, run `make acta` (or upload the source
package to Overleaf and select `manuscript_ActaMechanica.tex` as main document).
Required packages include `cuted` and the dependencies of `sn-jnl.cls`.
Run `make check` for static reference/label/environment/figure checks and
cover-letter consistency checks.

## Validation status and final checks
Static checks pass. No LaTeX compiler is installed here. An attempted compiler
installation was blocked by network restrictions on the release-asset host.
**No compiled PDF or visual-layout validation has been produced.** Inspect equation
strip placement, column breaks, tables, figure sizes and bibliography after compilation.
The source files are a review/build package, not a complete submission until a PDF is added.

Before submission, authors must confirm:
1. All author names, affiliations, funding and competing-interest statements.
2. An accurate author-contribution statement, if required; none was invented.
3. Current data/code-availability requirements; existing data statement is retained.
4. Correctness of each reference/DOI and publication/acceptance status, especially
   2026 references. Bibliographic metadata has NOT been independently verified.
5. The cover letter's originality/exclusive-submission declarations remain true.
6. The mechanics-first framing and added limitations accurately describe the work.
7. The full coupled model has not been independently validated by this conversion;
   analytical-limit/discrete checks must not be described as such validation.

## Second-pass review
See `ACTA_SECOND_PASS_REVIEW.md` for wording corrections, bibliography gaps and
a mechanical boundary-condition point requiring author confirmation.
