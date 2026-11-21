# Revision changelog (manuscript_FINEL.tex)
Each item: original issue → evidence → change → verification.
1. Root constraint stronger than a classical clamp → P1/P2, `run_checks.log` → classical clamp (u=w=u_z=w_z=0) is now the primary model; all-derivative case reported as a sensitivity (Table `rootbc`) → voltages differ by 0.11–0.13%.
2. Tables/mesh study/uncertainty/span study/α-sensitivity/polarity numbers → recomputed with the classical clamp (`voltages_all.csv`, `conv_stats.log`, `run_alpha_grid.log`). Headline values: D −3.43865, A −1.49798, E +0.19346 V.
3. "Observed order 1.3–1.5" and Aitken statements → reproduced for the old model; shown to be a root-constraint artefact; new text reports p_obs≈0.9–1.2 and a BFS/Q9/Aitken spread as uncertainty.
4. Statement that the top electrode shows a potential disturbance near the root → wrong: top electrode potential is exactly uniform; text replaced; corner ε_xx flagged as mesh dependent.
5. "Simplified" thermal-stress reduction → described as an inconsistent reduction, not an alternative model.
6. Verification table → replaced by checks that were actually run (`unit_tests.log`); the energy-balance paragraph (Eq. with 4.65e-8 … terms) and its identity row were **removed** because they could not be reproduced; the original code is not available.
7. Added exact mid-span solution (new subsection) and independent Q9 discretization.
8. Span study extended description: only 10–100 µm re-run; the earlier 500 µm statement and the "stresses 1000× smaller at 200 µm" sentence were removed and replaced by the exact σ_xx=σ_zz=0 mid-span result.
9. Limitations: no experimental/3D/commercial-code validation; Data-availability statement now refers to a reproducibility archive (DOI placeholder to be filled by the authors).
10. References: Zhou (volume, pages, claim), Gupta (volume), Panda (claim) corrected; see P3.
11. Highlights rewritten to ≤85 characters; cover letter rewritten.
12. Figures 2–6 regenerated, old 6–8 merged, new Fig. 9 added.
