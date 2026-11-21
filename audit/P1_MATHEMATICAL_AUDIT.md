# P1 — Mathematical and constitutive audit
Method: re-derivation by hand plus executable checks (`verification/run_checks.py`, log in `verification/results/run_checks.log`).

## Verified
- **Enthalpy → constitutive relations.** With H as in Eq. 2 and E=−∇φ: σ = C(ε−αθ) − eᵀE, D = eε + κE + pθ. Reciprocal (single potential), signs consistent. The discrete system is symmetric: ‖K−Kᵀ‖/‖K‖ = 2.4e-17.
- **Fixed-strain pyroelectric coefficient.** p3 = −341 µC m⁻²K⁻¹ (primary) is the correct input for a strain-based enthalpy; using the total value would double count. VERIFIED.
- **Plane-strain thermal-stress vector.** With total ε_yy=0, β_xx=(C11+C12)α1+C13α3, β_zz=2C13α1+C33α3 — correct. The "simplified" form omits C12α1 and one C13α1 and is **physically inconsistent** for plane strain, not a legitimate alternative model. Manuscript wording ("two reductions", "polarity depends on the reduction") should say the simplified form is an error, not a modelling choice.
- **Plane-strain electrical block** (e rows, κ) correct; D_z = e31 ε_xx + e33 ε_zz + κ33 E_z + p3θ.
- **Exact reduced benchmark (new).** Away from ends, fields depend on z only; σ_zz=0, D_z=0 and (θ linear) σ_xx≡0 give a 3x3 system. Result: V_D=−3.43865, V_A=−1.47652, V_E=+0.19754 V. FEM with classical clamp converges to it as span grows (V_E: 0.19347, 0.19551, 0.19673, 0.19713 at L=10, 20, 50, 100 µm). This independently confirms the thermal-stress model, the sign of Case E and the manuscript's ~2% span effect.

## Mandatory boundary-condition test (mechanical root)
Question: is fixing all eight BFS DOFs stronger than a classical clamp? **Yes.** With ℓ=0 and μ=0 the weak form contains only first derivatives, so the classical clamp is u=w=0 on x=0, which for the Hermite basis implies u_z=w_z=0 but leaves u_x, w_x, u_xz, w_xz free (natural). The original constraint additionally sets u_x=ε_xx=0 and w_x=0 at the root: it forbids axial thermal/Poisson strain and rotation of the root edge. It is an over-constraint (a stiffer, non-classical clamp), and a genuine strain-gradient clamp would apply only if ℓ,μ ≠ 0.

Measured (80x40):
| Case | Constraint | V (V) | root ε_xx top | tip w (nm) |
|---|---|---|---|---|
| E | all-derivative | +0.193212 | 0 (imposed) | −13.717 |
| E | classical | +0.193459 | +1.9e-4 | −13.756 |
| A | all-derivative | −1.499598 | 0 (imposed) | −7.090 |
| A | classical | −1.497979 | −3.3e-4 | −7.117 |
Voltage changes: Case E +0.13%, Case A +0.11%; tip deflection ~0.3–0.4%. Classical clamp converges faster (16x8: A −1.4973, E +0.19359, already within 0.05% of 80x40) than the all-derivative clamp (16x8 error ~0.7%/1.2%), which is consistent with the latter producing the observed 1.3–1.5 "convergence order" via an artificial root boundary layer. **Recommendation: report the classical clamp as the primary model; retain the original as a sensitivity case.** The previously reported numbers are not invalidated; they differ from the physically consistent model by about 0.1%.

## Electrical boundary conditions
Bottom electrode φ=0 (max|φ|=0), top φ equipotential (max−min = 0 exactly), net floating-electrode charge −1.9e-22 C/m (vs 2.7e-10 reference scale). Open-circuit voltage = φ_top − φ_bottom. VERIFIED.
**Manuscript statement (Sec. 6.2): "top surface nearly at a single potential, apart from a small disturbance near the clamped root" is wrong/misleading.** The top electrode is exactly equipotential by constraint. What Fig. 5 shows near the root is a local feature of the *E_z field* (top-left corner of panel b, where the E_z colour departs from the band) and of an interpolated 3-D φ surface; it is a field concentration in the interior/corner, not a potential variation along the electrode. Reword and replot.

## Not yet done in P1
Stability (positive-definiteness of C and κ) and the units check were done by inspection only; the strain-gradient formulation (Sec. 3.4) was not implemented, since all reported results use ℓ=μ=0. The Hermite-C¹ claim is unnecessary for the reported results: C⁰ Q9 elements reproduce them.
