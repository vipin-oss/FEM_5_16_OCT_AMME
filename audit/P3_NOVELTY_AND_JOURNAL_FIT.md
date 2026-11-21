# P3 — FINEL novelty and journal-fit assessment

## Sources actually consulted
- FINEL aims and scope (Elsevier shop page): the journal emphasises mathematical/theoretical foundations, computer implementation of numerical methods, and numerical procedures for practical but challenging problems, with interest in synergy between emerging fields and traditional computational mechanics. The full "Guide for authors" could **not** be opened in this session; highlights/cover-letter rules below are the standard Elsevier ones and must be re-checked against the live guide.
- Co-authored papers: publisher pages (doi.org → linkinghub) return only redirect stubs, so the published full texts were not read. Metadata verified with Crossref; content assessed from the editorial-system submission drafts and abstracts in the authors' Google Drive (FINEL-D-26-00567R2, FINEL-D-26-00692). **Content statements below are therefore from the submitted versions, not the final published PDFs.**

## The two co-authored papers
| | 10.1016/j.finel.2026.104681 | 10.1016/j.finel.2026.104685 |
|---|---|---|
| Authors (Crossref) | Gupta, Kumawat, Yadav, Maruyama, Almohsen | Rezk, Kumawat, Lotfy, Yadav, Gupta |
| Volume/article/date | 263 / 104681 / Jan 2027 | 263 / 104685 / Jan 2027 |
| Theory | second-order strain-gradient elasticity, ellipsoidal nonlocal characteristic-length tensor | Mindlin Form-II strain-gradient elasticity with ellipsoidal microstructure |
| Discretization | C¹-continuous FE | C¹ Bogner–Fox–Schmit |
| Physics | purely mechanical, size-dependent stiffening | purely mechanical, boundary layers, size dependence |
Present manuscript: classical (ℓ=0, μ=0) linear thermo-piezo-pyroelectric plane strain; BFS used only as the interpolation. **No strain-gradient, flexoelectric or size-effect result is computed.** The BFS C¹ continuity is unnecessary for the reported model (shown here: a C⁰ Q9 discretization gives the same voltages to 0.02–0.03%). The manuscript is correct to say the two papers are not validation of this calculation.

## What the contribution actually is
1. **New numerical method?** No. Standard coupled FE, standard BFS from the authors' earlier work.
2. **New coupled benchmark?** Partly: the exact mid-span solution (Eq. `eq:midspan` in the revised text, a 3x3 algebraic system) is a useful verification target, but it is simple, and it was added in this audit, not by the authors.
3. **Constitutive consistency correction?** Yes — this is the real content: the plane-strain thermal-stress vector must include C12α1 and the second C13α1 term, and the fixed-strain p3 must be used. That is a textbook point; the "simplified" reduction is an error that careful authors would not make, which makes the headline "polarity reversal" a correction of a straw-man model rather than a surprising physical prediction.
4. **New physical prediction?** Modest: for the specific BaTiO3 data set, a positive piezoelectric-thermal voltage that opposes the pyroelectric one; sensitive to α3 (only ≈1.3σ from zero from a 4-point lattice-parameter fit).
5. **Application of existing methodology?** Primarily yes.

## Realistic FINEL editorial assessment
- **Desk-rejection risk: HIGH.** (i) Little numerical-methods novelty; (ii) result is reproducible by hand with a 3x3 solve away from the ends, the FE adds only an ~2% end effect; (iii) no validation against experiment, 3D, or independent code; (iv) the manuscript carries several self-citations/author-group FINEL papers that concern a different (strain-gradient) physics, which an editor may read as citation padding — keep the discussion minimal and factual; (v) the Acta Mechanica history must be disclosed/cleared.
- A more defensible framing for FINEL: a verification-oriented study of the constitutive and boundary-condition consistency of coupled thermo-piezo-pyroelectric FE models, with the exact mid-span benchmark and a documented root-constraint test as reusable verification tools.
- Additional work that would directly close a gap (only these): (a) a 3D or plane-stress comparison (identified as a limitation); (b) validation of the thermo-piezo FE against a published benchmark with measured pyroelectric/piezo voltage; (c) deposit of code. Do **not** add flexoelectric calculations to look novel.

## Reference verification (seven FINEL citations)
| Key | Status |
|---|---|
| FINELPanda2008 | Title, authors, 2008, DOI 10.1016/j.finel.2008.01.001 consistent in two indexes; vol 44(8) pp 493–504 not independently re-checked. Citing sentence corrected to match the abstract (nonlinear static FG plates with PFRC actuators, with/without thermal environment). |
| FINELDash2009 | Title, authors, 2009, pp 686–694 confirmed (index record). Supports "nonlinear vibration of piezoelectric laminates". |
| FINELZhou2015 | Crossref: vol 102–103, pp 85–94, Sept 2015 (bib was missing vol/pages — fixed). Title concerns **precision positioning** with secondary converse piezoelectric effect; the earlier claim "laminated beams" came from a different venue's paper and was removed. |
| FINELPalma2017 | Vol 129, pp 32–41, DOI confirmed; supports the sentence (Timoshenko-beam elasto-thermoelectric formulation compared with a 3D FE model). |
| FINELHassan2026 | Authors/title/DOI/article 104488 vol 253 confirmed; year shown as 2025 (Greenwich repository) and 2026 (OUCI). Keep 2026 only if the publisher issue date is 2026 — **unresolved, check on ScienceDirect**. |
| FINELGupta2026 → key name, year 2027 | Crossref: authors in the bib order, vol 263, article 104681, issued Jan 2027 (volume added; "available online" note removed). |
| FINELRezk2027 | Crossref: authors in bib order, vol 263, article 104685, Jan 2027 ✓. |
The article-level claim "supports its surrounding claim" was checked from abstracts only for the five non-self papers (full texts not read).
