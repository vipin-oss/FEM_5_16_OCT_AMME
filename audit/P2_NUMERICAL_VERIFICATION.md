# P2 — Numerical verification
Commands (from repo root): `cd verification && python3 run_p2.py > results/run_p2.log` (≈2 min) ; `python3 run_checks.py | tee results/run_checks.log`. Python 3 with numpy 2.5, scipy 1.18. Data: `verification/results/voltages_all.csv`, logs in same folder.

## Independence
Solver 1 (BFS, 9 dof/node): same discretization as the manuscript but written fresh. Solver 2 (Q9 biquadratic u,w,φ, 3x3 Gauss, classical clamp): different basis, order, continuity and quadrature. Analytical benchmark (P1): no discretization. Agreement of all three is the model evidence; changing the mesh alone is not counted.

## Results, 80x40 (Q9: same element counts)
| Model | V_D | V_A | V_E |
|---|---|---|---|
| BFS all-deriv, full β | −3.438647 | −1.499598 | +0.193212 |
| BFS classical clamp, full β | −3.438647 | −1.497979 | +0.193459 |
| Q9 classical clamp, full β | −3.438647 | −1.498328 | +0.193393 |
| Analytic long beam, full β | −3.438647 | −1.476517 | +0.197535 |
| BFS all-deriv, simplified β | −3.438647 | −1.908274 | −0.215464 |
| BFS classical, simplified β | −3.438647 | −1.907010 | −0.215573 |
| Q9 classical, simplified β | −3.438647 | −1.907281 | −0.215560 |
BFS-classical vs Q9 differ by 0.02% (A) and 0.03% (E): two independent discretizations agree. Absolute tolerance on Case D vs 1D exact: ≤1e-12 V (relative <1e-12).

## Checklist
1 Hermite/BFS: reproduces exact results above; partition-of-unity not separately re-run (PENDING). 2 Assembly: symmetric to 2e-17 (VERIFIED). 3 Gauss: 4x4 (BFS), 3x3 (Q9) exact for the rectangular integrands (by degree count; not separately tested). 4 Convergence: all meshes in `run_p2.log`. 5 1D pyroelectric limit: VERIFIED. 6 Electrode equipotential and zero charge: VERIFIED (P1). 7 Conditioning: cond(K)=2.5e31 raw vs 4.7e6 after diagonal scaling at 16x8 — the manuscript's scaling is essential (VERIFIED). 8 Energy/stationary identity: NOT re-run. 9 Root constraint: P1 table. 10 Thermal-stress reduction: see below.

## Polarity shift
Case E changes from −0.2155 V (simplified β) to +0.1932 V (full β). It persists under the classical clamp (−0.2156→+0.1935), under an independent Q9 discretization, and in the exact mid-span benchmark (−0.2164→+0.1975). **The shift is therefore a robust consequence of the reduction used, not a boundary-condition artefact.** But because the simplified reduction is mechanically inconsistent (P1), the result is a *correction of an inconsistent model*, not a physical sensitivity.

## Thermal-expansion sensitivity (Case E is linear in α)
V_E = 0.01529·α1 + 0.03253·α3 (V per 1e-6 K⁻¹). Sign change at α3/α1 = −0.470, i.e. α3 ≈ −10.2e-6 for α1=21.8e-6. Over all four ±1σ corners (α1 ±1.646, α3 ±3.261) V_E lies between +0.062 and +0.325 V (80x40, classical clamp): positive in all corners, matching the manuscript's +0.062/+0.324. Caveat: the fit uses four lattice-parameter points, α3 is only ≈1.3σ from zero, and these are not independent samples.

## Limits of this verification
No access to the authors' original code; original numerical values were reproduced, not read back. Energy-term audit, partition-of-unity, alpha regression and manuscript Figs 2–4, 6–8 were not regenerated here.

## Additions after the first pass (all in `verification/results/`)
- `unit_tests.log`: element-level linear-field recovery, load kernel, potential energy, symmetry, 4x4 vs 6x6 Gauss, null limits, Case D vs 1D, p3 linearity (slope −1.6909 V per unit scale, classical clamp). All PASS.
- `conv_stats.log`: classical clamp converges non-monotonically with p_obs≈0.9–1.2 and changes <0.06% from 8x4 onward; the all-derivative constraint reproduces the manuscript's p_obs 1.35/1.31 (A), 1.46/1.53 (E) and Aitken limits −1.4985/−1.4982, +0.19349/+0.19343 exactly, i.e. the manuscript's "observed order" is a property of the over-constraint.
- `run_alpha_grid.log`: 80x40 classical sensitivity (V_E = 0.01529 α1 + 0.03253 α3; ±1σ range +0.062…+0.325 V; 2σ V_A range −1.761…−1.236 V; zero crossing at α3≈−10.25e-6, 1.8σ) and the 3x3 grid (48x24).
- Still NOT re-run: integrated-enthalpy/stationary-potential identity (energy terms of the original Eq. 18). That paragraph was removed from the manuscript rather than kept unverified.
