# GPT follow-up check — 21 November 2026

Base reviewed: audit/P6_FINAL_SUBMISSION_AUDIT.md and audit/HANDOFF_NEXT_STEPS.md on `revision/finel-submission-2026-11`.

## Independently confirmed this pass
1. Hassan et al., *Reduced-Order Modelling for Thermal–Mechanical Analysis of Power Electronic Modules*, is in *Finite Elements in Analysis and Design* **253 (January 2026), 104488**, DOI 10.1016/j.finel.2025.104488. ScienceDirect lists January 2026 and the University of Greenwich/Arizona State records support this. **Keep year 2026** in `references_FINEL.bib`. The DOI's 2025 component is not the volume publication year.
2. The two author-coauthored published FINEL papers, DOI 10.1016/j.finel.2026.104681 and 10.1016/j.finel.2026.104685, have full published PDFs supplied by the authors (and archived in their connected Google Drive). The final publications concern strain-gradient elasticity, and neither independently validates the active classical thermo-piezo-pyroelectric calculations in the current FEM5 manuscript.
3. Elsevier's published author guidance specifies highlights as 3–5 bullets, at most 85 characters including spaces. Current `highlights_FINEL.txt` has four lines and meets this length restriction; journal-specific final checks must still use FINEL's live submission instructions.
4. The requested project contents include `manuscript_FINEL.tex`, `references_FINEL.bib`, `verification/`, `figure_code/`, revised `figures/`, and the P0–P6 audit files. The reports state that numerical reproduction uses an **independent re-implementation**, not the missing original authors' solver.

## Remaining blockers
- No verified real `elsarticle` build with actual fonts/images/bibliography in this pass. Do not describe the stand-in article-class build as journal-ready.
- Original/independent reimplementation authorship, provenance, archive deposition and DOI must be reviewed and published by authors.
- Clarify previous Acta Mechanica submission status; confirm all-author CRediT roles, conflicts, funding, generative-AI disclosure, permission and journal submission policies. Do not invent statements.
- Fig. 1 requires a proper source recreation; no original vector drawing source has been recovered. Verify the replacement against the original geometry, constraints and mechanisms, and do not change the science.
- Language revision should remain claim-neutral and be checked against numerical logs.
- Re-run published `verification/` commands after any scientific manuscript/figure changes.

## Recommendation
**NOT READY**, consistent with the existing P6 decision. Next useful milestone is a real Overleaf compilation plus author-only declarations, followed by reproducibility DOI and figure source checks.

Sources:
- https://www.sciencedirect.com/science/article/pii/S0168874X25001775
- https://asu.elsevierpure.com/en/publications/reduced-order-modelling-for-thermalmechanical-analysis-of-power-e/
- https://www.elsevier.com/subject/next/guide-for-authors
