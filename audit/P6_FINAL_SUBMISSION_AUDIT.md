# P6 — Final submission audit (referee-style)
**DECISION: NOT READY** (scientifically much improved; blocked by items below that only the authors can resolve).

## BLOCKING
1. **Source-code provenance reconciled (resolved as an audit finding).** The authors supplied the original Python package as `PAPER5_FINAL_PACKAGE.zip`; its BFS/Q4 implementation and output CSVs were inspected, and its 20 tests passed independently. That original code uses the all-derivative root constraint, whereas the revised FINEL results use the classical root constraint in `verification/tpfem.py`. These models are deliberately retained as distinct implementations; the uploaded original must not be described as the solver producing the manuscript's classical-root primary results. See `audit/ORIGINAL_PROGRAM_VS_FINEL_REVIEW_2026-11-21.md`. A DOI or public code deposit is **not** a standing submission blocker absent an applicable journal requirement; the current manuscript instead offers source and data upon reasonable request (author approval required).
2. **Acta Mechanica status.** The manuscript was first prepared for Acta Mechanica; the authors must confirm it is not under review or published there (cover-letter placeholder).
3. **Authors must confirm final declarations**: author list/order and affiliations, CRediT roles (portal), funding and competing-interest statements, the new manuscript AI-use declaration, availability of code upon reasonable request and permission to publish. The wording is now present where applicable, but factual author approval cannot be inferred from a software audit.
4. ~~Real `elsarticle` compilation~~ **RESOLVED (supervisor T1/T7):** real class, 53 pages, 0 errors, 0 undefined references/citations (`audit/build/`). Visual page-by-page PDF review still outstanding.
5. **FINEL live Guide for Authors still not accessible (HTTP 403 for GPT and for Claude)**; highlights (4 × ≤76 characters) follow the Elsevier 85-character rule via secondary sources; the authors must check journal-specific fields on the submission site.

## MAJOR
- Novelty/desk-rejection risk is high (P3): constitutive-consistency correction of an inconsistent reduction; exact long-beam solution reproduces the result without FE.
- No validation beyond verification of the stated model (no experiment, 3D or plane-stress comparison, commercial code).
- α3 is only ≈1.3σ from zero (4-point lattice-parameter regression); the polarity result is sensitive to it (zero crossing at α3≈−10.3e-6 K⁻¹, 1.8σ).
- Hassan2026 year: GPT reports ScienceDirect lists January 2026 (vol 253) — kept 2026; not independently re-fetched by Claude; Panda/Dash/Hassan volume/pages and the claim-support of the five older FINEL papers checked from abstracts/index records only.
- GitHub PR #7 is accessible and receives revision-branch commits. Earlier connector limitations are no longer a current blocker. Do not merge automatically.
- Energy/stationary-potential identity not re-verified (paragraph removed).

## MINOR
- Fig. 1 was redrawn and authors must still approve schematic meaning. A subsequent binary-PDF inspection of all seven current figures found exactly one page per PDF, embedded font programs and no Type 3 font descriptors; this is **not** a substitute for visual inspection. α-grid and fields figures not colour-blind simulated.
- Span study re-run only to 100 µm (previous 200/500 µm statements removed).
- Intro/Discussion still long; language edit not performed beyond the changed passages.
- Table/figure float placement unchecked in the real class.

## VERIFIED (reproducible, `verification/`)
- Reduced equations, signs, reciprocity (symmetry 2e-17), fixed-strain p3, full plane-strain β (hand derivation + code).
- Case D exact to 1.5e-13; electrodes equipotential (spread 0) and net charge 1.9e-22; conditioning scaling needed (2.5e31 → 4.7e6).
- Original numbers reproduced: A −1.49960, E +0.19321 V (all-derivative, 80x40), manuscript p_obs and Aitken limits.
- Root-constraint effect 0.11–0.13% on voltage, 0.3% on tip deflection; classical clamp BFS vs Q9 differ 0.02–0.03%; exact mid-span solution V_E=+0.19754 V approached as 1/L.
- Polarity change −0.2156 → +0.1935 V persists under all three root treatments and in the exact solution.
- α sensitivity ±1σ: V_E ∈ [+0.062, +0.325] V; 2σ V_A ∈ [−1.761, −1.236] V.

## Test commands
```
cd verification
python3 unit_tests.py
python3 run_p2.py > results/run_p2.log
python3 run_checks.py | tee results/run_checks.log
python3 conv_stats.py | tee results/conv_stats.log
python3 run_alpha_grid.py | tee results/run_alpha_grid.log
cd .. && python3 figure_code/make_figures.py
```

## Supervisor status after T2–T7 (21 Nov 2026)
T1 PASS; T2 PARTIAL (guide 403); T3 metadata complete, claims checked against abstracts; T4: 3 of 4 proposed edits applied, 1 rejected (it changed a technical claim: the sign depends on α3 as well, flipping at α3≈−10.3e-6); T5 targeted check passed; T6 review only; T7 PASS (all verification scripts reproduce the stored logs exactly; `unit_tests.py` exit 0; rebuild clean). Decision unchanged: **NOT READY** (author-only items + full visual review).

## Update after author decisions (21 Nov 2026, 11:30 IST)
Funding (HSHEC/HSRF, Sanction Letter 14/66-2026 SPD/HSHEC/HSRF-38) and competing-interest (none) statements written per the authors' instruction. CRediT and AI-use disclosure are to be entered by the authors in the submission portal. The cover letter now states the manuscript is unpublished and not under consideration elsewhere — the authors must confirm that this is true. Only the archive DOI placeholder remains in the manuscript. Decision unchanged: NOT READY until the DOI, the Fig. 1 approval and the full PDF review are done.

## Independent follow-up after original program was supplied (21 Nov 2026)
- Source package ZIP SHA-256: `bd0ea7d4ca1eb7ecdff5ab1c1ac548fb33aa7e045f0f3265e8c2da533ba691e9`; original Python suite: `20 passed in 7.99 s` locally. The original model matches old all-derivative-root values, not revised classical-root headline values.
- Independent reduced constitutive solve checked analytical interior Case E +0.1975353158 V and Case A -1.4765168975 V. This is mathematical arithmetic, not external experimental validation.
- Manuscript textual fixes: precisely qualify the interior solution, remove an unfulfilled public-archive/DOI placeholder, supply a data-and-code availability sentence for author confirmation, include an AI-use declaration. The equations and numerical table entries were unchanged by these edits.
- All seven figure PDFs were inspected for embedded font program and Type 3 descriptors; font-structure preflight passed. Pixel-level page-by-page evaluation of the **new** reviewed PDF remains incomplete.
- **Current decision: NOT READY FOR FINAL SUBMISSION** until the updated LaTeX source is recompiled/visually inspected, author declarations are approved and journal submission fields are confirmed. This assessment does **not** demand a DOI.
