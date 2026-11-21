# P0 — Repository and evidence audit
Branch `revision/finel-submission-2026-11` (head e40ac7e at audit start). Audit date 2026-11-21.

## Inventory
Tracked files: `manuscript_FINEL.tex`, `references_FINEL.bib`, `cover_letter_FINEL.txt`, `highlights_FINEL.txt`, `FINEL_SUBMISSION_CHECKS.md`, eight figures (7 PDF, `Fig5_solved_fields.png`), original Acta Mechanica files, `tools/check_acta.py` (static text checks only).

**BLOCKING finding P0-1: the repository (all 10 branches, all history) contains no numerical program, no raw results and no figure-generation code.** Every number in the manuscript (Tables 3–5, Figs 2–8, energy audit) has no source in the repository. Exact reproduction of the authors' original run is therefore impossible; "Data availability" cannot be truthfully satisfied as is.

## Mitigation performed in this audit
An independent solver was written from the manuscript's stated formulation only (`verification/tpfem.py`). It reproduces the headline numbers (80x40, BFS, all-derivative root, full beta): Case A −1.499598 V (manuscript −1.49960), Case E +0.193212 V (+0.19321), Case D −3.438647248 V (exact). Mesh-change percentages 8x4→16x8 match to 3 digits (A −1.12%, E +2.41%). This is evidence the *stated* model is what produced the numbers; it is **not** an audit of the authors' original code.

## Claim → evidence map
| Claim / quantity | Where | Generating program | Inputs | Source data in repo | Verification status | Uncertainty |
|---|---|---|---|---|---|---|
| V_D = −3.438647 V | Eq. 8, Tab. 5 | none in repo | p3, κ33, h, ΔT | no | VERIFIED analytically and by independent FE | none |
| V_A = −1.4996 V | Tab. 5 | none | Tab. 3 | no | Reproduced (this audit); also −1.4983 (Q9, classical clamp) and −1.4765 (long-beam analytic) | clamp-dependent ≈0.1% |
| V_E = +0.1932 V | Tab. 5 | none | Tab. 3 | no | Reproduced; +0.1935 classical clamp; +0.19339 Q9; +0.19753 analytic long beam | ≈0.1–0.2% |
| beta_PS values, Tab. 4 | Eq. 5, Tab. 4 | none | Tab. 3 | no | VERIFIED by arithmetic and re-derivation | none |
| polarity shift −0.22→+0.19 V | Sec. 6.4 | none | beta modes | no | Reproduced: −0.21546→+0.19321 (original BC), −0.21557→+0.19346 (classical clamp), Q9 −0.21556→+0.19339 | see P2 |
| mesh table / p_obs / Aitken | Tab. 6 | none | — | no | Reproduced qualitatively; full re-run in `verification/results/` | — |
| alpha fits (21.76, −4.34) | Sec. 5 | none | Tab. 3-raw | table in text | NOT re-run in this pass | OLS on 4 points |
| energy audit terms, 11-check table | Eq. 18, Tab. 7 | none | — | no | Symmetry, null limits partly re-checked; energy terms NOT independently re-evaluated | — |
| Figures 2–8 | figures/ | none | — | no source data | Fig. 5 spot-checked (tip ≈7 nm, eps_xx top ≈1.4e-4: consistent) ; others not regenerated | — |
