# FEM5 original-program versus FINEL-revision audit
Date: 21 November 2026
Target: *Finite Elements in Analysis and Design* (FINEL)
Branch: `revision/finel-submission-2026-11`

## Source files actually checked
- User-supplied `PAPER5_FINAL_PACKAGE.zip`, SHA-256 `bd0ea7d4ca1eb7ecdff5ab1c1ac548fb33aa7e045f0f3265e8c2da533ba691e9`.
- `python_program/paper2/materials.py`, `paper2/fem_solver.py`, `paper2/cases.py`, `run_production.py`, `results/production_results.csv`, `results/verification_results.csv` from that uploaded ZIP.
- FINEL branch `verification/tpfem.py`, `verification/results/voltages_all.csv`, `manuscript_FINEL.tex` and existing P0–P6 audit records.

## Executed test
The user-supplied Python source was extracted and `python -m pytest tests/ -q` was run in the extracted `python_program/` directory.
Result: **20 passed in 7.99s**, exit code 0. This confirms these tests execute, not that an independent experiment or the revised model has been validated.

## Critical distinction between sources
The uploaded original implementation is a BFS/Q4 coupled FE model with all mechanical root derivative DOFs fixed. It is the source of the following 80×40 production outputs:

| Case | Uploaded original: all-derivative root (V) | Revised FINEL: BFS classical root (V) |
|---|---:|---:|
| D | -3.438647248137982 | -3.4386472481392962 |
| A | -1.4995979976791265 | -1.4979788139247516 |
| E | +0.193211761047954 | +0.19345905551324877 |

The revised results are documented in `verification/results/voltages_all.csv`, which was also inspected. The comparison is **not** evidence that the original source implements the classical-root problem: it does not. The difference is attributable to the different root constraints, which the revised paper separately compares. Do not substitute the original program for the revised-model code or its primary values.

## Independent constitutive-limit arithmetic
Using the manuscript's constants `C11=2.22e11, C12=1.08e11, C13=1.11e11, C33=1.51e11, e31=-0.7, e33=6.7, k33=56*epsilon0, alpha1=21.8e-6, alpha3=-4.3e-6, p3=-3.41e-4, deltaT=10 K, h=1 um`, the reduced 3×3 analytical system yields:
- Full 3D-contracted plane-strain beta: [6.7167e6, 4.1903e6] Pa/K;
- Inconsistent simplified beta: [4.3623e6, 1.7705e6] Pa/K;
- Full beta, Case E: **+0.1975353158 V**;
- Full beta, Case A: **-1.4765168975 V**;
- Simplified beta, Case E: **-0.2163503843 V**.

These values match the stated analytical interior limits to manuscript precision; this check is analytical arithmetic with the given coefficients and is **not** an independent external validation.

## Changes in the working manuscript
1. Described the analytical long-beam solution as a stress-free **interior limit** and made explicit that compatible displacement fields can depend on x and z even if strains and electric fields depend on z only. This avoids incorrectly claiming that the finite clamped cantilever is solved exactly by the interior algebraic system.
2. Replaced the unfulfilled statement that code was already supplied in a public archive with an author-request availability wording; **the authors must approve that availability commitment**.
3. Added a transparent declaration of the actual manuscript-preparation use of ChatGPT and Claude, with author responsibility. **The authors must review and approve this statement before submission**.

No numbered scientific formula, numerical table or figure data were modified by these three textual changes. Existing P6 scientific caveats apply.

## Remaining real issues for final author/editorial review
- Original solver and revised solver implement *different root boundary constraints*. Both are preserved, not silently merged.
- The main FINEL editorial risk is whether a constitutive-correction/verification case study has sufficient numerical-methodological novelty. This is not fixed by language editing.
- No experimental, 3D or commercial-code comparison is present. Never claim such validation.
- The final revised 53-page PDF needs visual page-by-page inspection after the latest text changes; the supervisor's earlier build check predates this commit.
- Confirm all authors' data/code-sharing consent, originality/non-simultaneous-submission declaration, author order, contributions, conflicts, and AI-use statement.
- The live FINEL Guide for Authors was not independently accessible in this environment.

No external archive deposit or DOI is a prerequisite imposed by this audit. Data/code availability should match the journal's actual policy and the authors' choice. No files under `verification/`, `figure_code/` or `figures/` were changed here.

**Status: technical manuscript amendments made; full submission-ready claim withheld until author confirmations and revised PDF preflight.**
