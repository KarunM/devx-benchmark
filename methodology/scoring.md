# Scoring

## 1. Automated check
A run is automatically correct if every string in the task's `expected` list is a substring of the final answer text (`tasks_heldout.json`). This is the `correct` column of `rows.csv` and the "auto" column of the series tables.

## 2. Blinded rescore (authoritative from series 6 on)
For each held-out series the 24 final answers were shuffled and renamed A01..A24 (`results/scored/seriesN/blind/`). `blind-index.csv` maps each id to its task and question but not to the arm; the key that maps ids back to arms was kept outside the repository. A separate grader session judged each answer against the reference, without knowing the arm. The verdicts were joined back through the key into `rescoreN.csv` (columns `task,arm,verdict,reason`) and `rescore-blindN.csv` (blind id, task, verdict, reason). `rescoreN.csv` is the verified result used for every correctness figure. Series 5 predates this format: its blinded rescore is `rescore-blind.csv` (20/24 correct, arm hidden), the unblinded hand-checked verdicts are `rescore.csv`, and `verify-results.py` takes series 5 verdicts from the per-run table in `results/summaries/SERIES5.md`.

"Blinded but not independent": the grader was blinded to the arm but is another session of the same author-run process, and the reference answers and derivations were written by the same people who built DevX.

## 3. Adjudication rules
- The blinded verdict stands unless a documented ruling overrides it; every override is listed in the series write-up and in the `reason` column.
- **H-M1 ruling.** H-M1 ("Name that class") asks for CodePrinter at `codeprinter.py:53`. An answer that names the intermediate class `C89CodePrinter` but gives CodePrinter only as chain context is incorrect (upheld in series 8, 10, 11, consistent with series 6). In series 9 one such native answer was overridden to correct because the asked elements (CodePrinter and `codeprinter.py:53`) were right and the wrong line on an unasked intermediate class was immaterial. The question wording is loose; it is to be tightened in a future task set, not retroactively. Correctness is shown with and without H-M1 in the series 10 and 11 write-ups.
- **Series 14 H-X1 (DevX arm).** Automated scorer: correct. Blinded grader: incorrect ("extra wrong caller `limit`"). Final classification: INCORRECT, because the blinded rescore is authoritative. The answer listed a non-existent caller `limit` after DevX's text-backed `callers` reported four module-docstring lines (gruntz.py:78,102,108,111) as module-level call sites. The published 11/12 versus 9/12 uses the adjudicated result (automated would read 12/12). This is the only disagreement of 24 in that series.
- Series 9 H-X1 (native) incorrect upheld (swapped callers, mid-answer retraction); series 9 H-R2 (native) incorrect upheld (the final message was a background-search status line; kept as a failed row, not rerun).
- Zero-call runs (series 5 H-M1 DevX, H-S1 native) are kept as incorrect.

## 4. Agreement
Automated check versus final verdicts: series 5 23/24 (H-S1 DevX differs), 6 24/24, 7 24/24, 8 23/24, 9 23/24 after rulings, 10 22/24 (the two H-M1 answers), 11 23/24, 13 24/24, 14 23/24.

## 5. No reruns
Nothing was rerun or deleted to improve a result; favourable and unfavourable rows are both kept.
