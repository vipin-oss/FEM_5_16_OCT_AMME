# Instructions for GPT (executor). Claude is the supervisor/reviewer.

Repo: vipin-oss/FEM_5_16_OCT_AMME, branch `revision/finel-submission-2026-11` (PR #7). Never merge to `main`. Never force-push. Small, separate commits.
Read first: `audit/P6_FINAL_SUBMISSION_AUDIT.md`, `audit/CHANGELOG_REVISION.md`, `audit/HANDOFF_NEXT_STEPS.md`, `audit/GPT_FOLLOWUP_2026-11-21.md`.

## Hard rules
1. Do NOT change any number, equation, table value or figure data. All results come from `verification/results/`. If you think a number is wrong, stop and report it; do not edit it.
2. Do NOT invent references, DOIs, authors' statements, dates, CRediT roles, funding, AI-use or conflict declarations, or an archive DOI. Leave the existing bracketed placeholders untouched.
3. Do NOT claim "ready", "validated" or "novel method". The paper is a verified model with no experimental/3D validation and no flexoelectric results.
4. Do not edit `verification/`, `figure_code/` or `figures/` except where a task below says so.
5. Every task ends with a short report appended to `audit/GPT_PROGRESS.md`: what you did, evidence (log excerpt, page number, URL), what is still unresolved. Do not report a test as passed unless you ran it.

## Tasks (do in order; stop after each and wait for supervisor review if anything fails)
**T1 — Real compilation (BLOCKING).** In Overleaf (or local TeX Live with `elsarticle`): main file `manuscript_FINEL.tex`, pdfLaTeX → BibTeX → pdfLaTeX ×2. Deliver: zero LaTeX errors, zero undefined citations/references, no "??", all figures present (Fig1–6, Fig9 in `figures/`), tables not overflowing the page. Allowed edits: float placement, `\resizebox`, line breaks, package options. Report remaining Overfull/Underfull warnings. Also check `elsarticle-num` style produces all 7 FINEL references correctly (volume, pages, year).
**T2 — FINEL Guide for Authors check.** Open the live guide (sciencedirect.com/journal/finite-elements-in-analysis-and-design → Guide for authors). Check and fix: abstract length, keywords, highlights (3–5 bullets, ≤85 characters incl. spaces; current file has 4 × ≤76), declaration sections required (CRediT, generative-AI statement, data availability, competing interests, funding), figure format/resolution, whether line numbers/review layout is required, reference style. Edit only formatting/structure; leave placeholders for author-only statements. Quote the rules you used with URL.
**T3 — References.** Verify on ScienceDirect/Crossref: Panda 2008 (vol 44, no 8, 493–504), Dash 2009 (vol 45, no 10, 686–694), Zhou 2015 (vol 102–103, 85–94), Palma 2017 (vol 129, 32–41), Hassan (vol 253, 104488; year), Gupta (vol 263, 104681), Rezk (vol 263, 104685). Confirm authors' order. Check that each Introduction sentence about these papers is supported by its abstract; soften any sentence that is not. Report a table.
**T4 — Language pass (Introduction, Section 6 discussion, Conclusions only).** Simple, precise academic English; remove promotional words and filler; keep every claim and number identical; do not add citations. Return as a diff (`git diff`) so the supervisor can verify no technical change. Specific points: (a) say the simplified thermal-stress reduction is an inconsistent reduction, not an alternative model; (b) keep "no experimental or 3D validation" in limitations; (c) do not describe the two co-authored FINEL papers as validation.
**T5 — Consistency sweep.** Check that every number in the text, tables, figure captions, abstract, highlights and cover letter equals the values in `verification/results/*.log|csv` (headline: D −3.43865, A −1.49798, E +0.19346 V; simplified E −0.2156 V; ±1σ range +0.062…+0.325 V; BFS/Q9/classical/all-derivative table values). List each mismatch; fix only text that disagrees with the logs.
**T6 — Cover letter and declarations.** Re-read `cover_letter_FINEL.txt` against the guide; keep it plain and non-promotional; leave the bracketed author-confirmation paragraph as is.
**T7 — Final regression.** `cd verification && python3 unit_tests.py` must exit 0; rerun `run_p2.py`, `run_checks.py`, `conv_stats.py`, `run_alpha_grid.py` and confirm `git diff verification/results` is empty (or explain differences). Rebuild the PDF. Then write an updated decision in `audit/GPT_PROGRESS.md`.

## What only the authors can do (list them in your final report; do not fill)
Archive DOI; Acta Mechanica non-submission confirmation; author list/order, affiliations; CRediT roles; generative-AI use disclosure; funding and competing-interest wording; suggested reviewers; final approval of the redrawn Fig. 1.

## Supervisor acceptance gate (Claude will check each item after your push)
- diff touches only allowed files; no numeric change; `unit_tests.py` exit 0; PDF builds clean; placeholders intact; progress report has evidence for every claim.
Final decision remains NOT READY until the author-only items are filled; GPT may propose CONDITIONALLY READY only if T1–T7 all pass with evidence.
