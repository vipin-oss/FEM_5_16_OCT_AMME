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
V_E = 0.01529·α1 + 0.03253·α3 (V per 1e-6 K⁻¹). Sign change at α3/α1 = −0.470, i.e. α3 ≈ −10.2e-6 for α1=21.8e-6. The ±1σ corners from the fit errors (α1 ±1.65, α3 ±3.26) give V_E between +0.087 and +0.300 V: positive in all corners. Caveat: the fit uses four lattice-parameter points, α3 is only ≈1.3σ from zero, and these are not independent samples.

## Limits of this verification
No access to the authors' original code; original numerical values were reproduced, not read back. Energy-term audit, partition-of-unity, alpha regression and manuscript Figs 2–4, 6–8 were not regenerated here.
