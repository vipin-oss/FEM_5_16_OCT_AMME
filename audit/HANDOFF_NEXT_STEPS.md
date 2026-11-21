# Handoff: remaining tasks (read audit/P6_FINAL_SUBMISSION_AUDIT.md first)
Status: NOT READY. Scientific checks done (see audit/P0–P4, CHANGELOG_REVISION.md). Do NOT change any numerical result without re-running `verification/` scripts. Do NOT invent citations or data. Do not merge to main.

Tasks, in order (report each result back in this file or a new audit/ note):
1. **Compile in Overleaf** with the real `elsarticle` class: main file `manuscript_FINEL.tex`, pdfLaTeX + BibTeX. Fix only LaTeX errors/overfull boxes/float placement. Confirm Figs 1–6 and 9 appear (figures/*.pdf) and no "??" remain. Report the log.
2. **Open the live FINEL Guide for Authors** and check: highlights (3–5 bullets, ≤85 chars incl. spaces — currently 4 × ≤76), abstract length, keywords, graphical-abstract/CRediT/AI-use-disclosure/data-availability requirements, figure format rules. Edit `highlights_FINEL.txt`, abstract and declarations accordingly.
3. **Reference checks** on ScienceDirect: Hassan 2026 (year 2025 vs 2026, issue date of vol 253), and volume/pages of Panda 2008 (vol 44, 493–504) and Dash 2009 (vol 45, 686–694). Read the two published co-authored FINEL papers (10.1016/j.finel.2026.104681, 10.1016/j.finel.2026.104685) and confirm the one-sentence descriptions in the Introduction match the final text.
4. **Placeholders for the authors** (do not fill with guesses): reproducibility-archive DOI (Data availability), Acta Mechanica non-submission statement (cover letter), CRediT roles, AI-use disclosure, competing interests, suggested reviewers.
5. **Fig. 1**: redraw with embedded TrueType fonts, larger text, white background, remove "C¹ interpolation" wording; keep content identical.
6. **Language pass** limited to the Introduction and Discussion: simple precise English, no promotional wording; no new claims.
7. After 1–6, re-run `cd verification && python3 unit_tests.py` (must exit 0), update P6 with new statuses, and give a final READY / CONDITIONALLY READY / NOT READY decision with evidence.
