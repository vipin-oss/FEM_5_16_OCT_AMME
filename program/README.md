# FEM 5 — FINEL numerical program and figure reproduction

This folder accompanies `manuscript_FINEL.tex` in the repository root and contains the **revised classical-root-clamp** numerical model used in the *Finite Elements in Analysis and Design* manuscript.

**Open this README first.** There is no need to request the scripts, input parameters, figure generators, or precomputed principal CSV results separately. The manuscript is in the repository root, with the bibliography in `references_FINEL.bib`.

## Read the distinction before comparing results

Two related programs exist, but they solve **different root constraints**:

| Case, 80 x 40 mesh | Original Python program (all root derivatives fixed) | Revised FINEL program (classical displacement clamp) |
| --- | ---: | ---: |
| D: pyroelectric only | -3.438647248138 V | -3.438647248139 V |
| A: piezoelectric + pyroelectric | -1.499597997679 V | -1.497978813925 V |
| E: piezoelectric + thermal (p3 = 0) | +0.193211761048 V | +0.193459055513 V |

The original code came from the user-supplied `PAPER5_FINAL_PACKAGE.zip` and its 20 tests passed when run in the analysis environment. **The original ZIP is not copied into this GitHub folder.** The main `program/verification/tpfem.py` is a separately implemented BFS/Q9 solver for the classical-clamp FINEL revision, with its own unit tests and CSV outputs. Do not present the original all-derivative program as producing the main manuscript's classical-clamp results.

An historical all-derivative simulation is also accessible through `tpfem.solve_bfs(..., clamp='all')`, so the results can be re-created here without the older program.

## Folder layout

- `verification/tpfem.py`: linear plane-strain coupled thermopiezoelectric solver; BFS/Hermite and independent Q9 FE implementations, all-derivative and classical root constraints, material constants and thermal loading.
- `verification/unit_tests.py`: basis, algebraic, analytic and boundary-condition unit checks.
- `verification/run_p2.py`: BFS and Q9 mesh and thermal-stress-reduction comparison; regenerates `verification/results/voltages_all.csv`.
- `verification/run_checks.py`: analytical interior limit, root-constraint sensitivity, electrodes, coupling and conditioning checks.
- `verification/conv_stats.py`: convergence statistics.
- `verification/run_alpha_grid.py`: the parameter sensitivity grid.
- `verification/results/*.csv`: **checked-in reference CSVs** (not promised bit-identical across BLAS implementations).
- `figure_code/make_fig1.py`: Fig. 1 generator.
- `figure_code/make_figures.py`: Figs. 2, 3, 4, 5, 6 and 9 generators from the checked-in CSVs and numeric scripts.
- `figures/*.pdf`: figure assets matching the root manuscript.
- `figures_new/*.pdf`: baseline output copies in the location used by the figure-generator script.

## Requirements and commands

Python 3.11+ with NumPy, SciPy and Matplotlib. Start from the **`program/` directory**, not from the repository root. The verification scripts use relative `results/` paths, so they **must run inside `program/verification/`**. Then return to `program/` for figure generation:

```bash
python3 -m pip install -r requirements.txt
cd verification
python3 unit_tests.py
python3 run_p2.py > results/run_p2.log
python3 run_checks.py > results/run_checks.log
python3 conv_stats.py > results/conv_stats.log
python3 run_alpha_grid.py > results/run_alpha_grid.log
cd ..
python3 figure_code/make_fig1.py
python3 figure_code/make_figures.py
```

The programs perform actual coupled solves, which can be computationally expensive on an 80 x 40 mesh. Run all programs sequentially. Do not claim new regression passes without executing the commands. The figure generation reads the new `run_checks.log` produced by the command above; it is **not** generated from a placeholder file. Check the newly generated images against the checked-in figures before replacing the manuscript assets.

**IMPORTANT:** `figure_code/make_fig1.py` writes `figures/Fig1_model_schematic.pdf` while `figure_code/make_figures.py` writes other PDFs to `figures_new/`. This is the source scripts' existing behavior; the outputs are not automatically installed into the manuscript's root `figures/` folder.

The production inputs are defined directly in `verification/tpfem.py` (BaTiO3 4mm, `L=10e-6`, `H=1e-6`, `DT=10`, `alpha1=21.8e-6`, `alpha3=-4.3e-6`, `p3=-3.41e-4`; other coefficients there). This repository is the numerical source for the revised FINEL manuscript. It reports internal mathematical/code verification, **not** experimental or 3-D validation.

## Manuscript source and audit trail

- Manuscript: `../manuscript_FINEL.tex`
- Bibliography: `../references_FINEL.bib`
- Journal figures actually used: `../figures/Fig1_model_schematic.pdf` through `../figures/Fig9_root_constraint_and_span.pdf` (seven explicitly referenced files, not a continuous sequence).
- Full detailed audit/history (kept outside the streamlined Overleaf branch): branch `revision/finel-submission-2026-11`, path `audit/`; especially `audit/ORIGINAL_PROGRAM_VS_FINEL_REVIEW_2026-11-21.md` and `audit/P6_FINAL_SUBMISSION_AUDIT.md`.

No equations or numerical outcomes have been changed in order to populate this folder. The historical all-derivative code's authoritative input ZIP remains with the author; a copy would be needed only to reproduce that **historical independent implementation**, rather than the current paper's results.
