# devx-benchmark

Recorded data, scripts and write-ups from a live-agent benchmark of the DevX code-navigation CLI (`devx`, build = commit `04a02ef`, released as 1.7.0). A coding agent answers read-only questions about two repositories either with DevX on its PATH plus DevX's shipped guidance (arm C, "DevX") or with the shell only (arm N, "native"). The package holds every task, driver, run transcript and score, plus a script that recomputes every number below from the recorded files.

Author and copyright holder: Karuna Prasad Madu. Licence: see `LICENSE` (CC-BY-4.0 for data and documents, MIT for scripts).

## What was measured

- 12 held-out tasks (`tasks/held-out/`): locate, read, structure, crossref and multi-hop questions, 6 on a Python repository (sympy 1.13.3) and 6 on DevX's own C# source. Fixed expected strings; answers in `tasks/held-out/HELDOUT-ANSWERS.md`.
- Nine configurations (model plus agent harness), one run per task and arm: 108 evaluations per arm. Same 12 tasks and same DevX build in every configuration.
- Counted: tool calls, model input tokens, tool-result bytes, and verified correctness (automated check, then a blinded rescore by a separate grader session; see `methodology/scoring.md`).
- Ratios below are DevX as a share of native on the tasks both arms answered correctly. Below 100% means DevX used less.

## Headline (nine configurations)

| series | configuration | harness | correct (DevX vs native, of 12) | both-correct n | calls DevX/native | input tokens DevX/native | result bytes DevX/native | note |
|--|--|--|--|--|--|--|--|--|
| 5 | gpt-6-luna | Codex | 10/12 vs 10/12 | 8 | 75.0% | 88.4% | 52.6% | baseline; n=8 excludes H-R2 native outlier (358,121 B); 2 wrong answers per arm |
| 6 | gpt-5.6-luna | Codex | 12/12 vs 12/12 | 12 | 110.0% | 103.7% | 3.6% | DevX used more calls and tokens; native H-R1 returned 1,051,628 B in one command |
| 7 | DeepSeek Flash 4.1 | Codex | 12/12 vs 12/12 | 12 | 55.9% | 68.6% | 79.1% | DeepSeek tokens include ~73k uncached baseline per run; effort setting unverified |
| 8 | Sonnet 5.5 | Claude Code | 12/12 vs 11/12 | 11 | 88.9% | 100.3% | 155.5% | Claude Code tools bound output, so DevX returns more bytes |
| 9 | Sonnet 5 | Claude Code | 12/12 vs 10/12 | 10 | 58.6% | 73.6% | 171.5% | native: 2 wrong answers (H-X1, H-R2) |
| 10 | Opus 5.5 | Claude Code | 11/12 vs 11/12 | 11 | 78.3% | 92.0% | 161.7% | both arms missed H-M1 |
| 11 | gpt-6-sol | Codex | 12/12 vs 11/12 | 11 | 89.5% | 95.9% | 29.4% | DevX slower in wall time (125 s vs 105 s) |
| 13 | Fable 5.1 | Claude Code | 12/12 vs 12/12 | 12 | 72.7% | 86.9% | 160.1% | both arms answered all 12 correctly |
| 14 | Qwen3.6-27B fp8 | Codex | 11/12 vs 9/12 | 8 | 47.6% | 64.5% | 44.6% | DevX wrong on H-X1 (docstring-line `callers` defect); native wrong on 3 |

Totals: verified correct DevX 104/108 versus native 98/108 (four wrong DevX answers, ten wrong native answers). On both-correct tasks DevX used fewer calls in 8 of 9 configurations, fewer input tokens in 7 of 9, and fewer result bytes in 5 of 9; the four Claude Code series return more bytes with DevX because Claude Code's native Read and Grep are bounded. Series 5 is shown at n=8 (without the H-R2 native outlier); the n=9 line is in `results/summaries/FACTS-benchmark.md`. The tuned set (series 4, 12 tasks x 3 reps, tuned against by the DevX authors) reads 131% / 124% / 69% (calls / input tokens / result bytes, sum of per-task medians); on that set DevX used more calls and input tokens than native and fewer result bytes.

## Read this before quoting the numbers

- One run per task and arm; nothing is statistically significant. The same 12 tasks are reused in all nine configurations, so they are now a regression set.
- Author-run and not independent. The blinded rescore is blinded but not independent (`methodology/limitations.md`).
- The measured build still has two `callers` defects (fixed in 1.7.1 and 1.7.2); reruns on newer builds are not comparable on H-X1 and H-X2.
- No claim of lower cost, general superiority or statistical significance is made.

## Layout

- `methodology/`: `experimental-design.md`, `scoring.md`, `limitations.md`
- `tasks/`: tuned and held-out task files and answer key
- `drivers/`: benchmark drivers and series launchers; `drivers/tables/` has the table and blind-pack scripts (provenance only; they refer to the original working tree)
- `configurations/`: guidance files under test and a table of model, harness, invocation and versions
- `results/raw/seriesN/`: `rows.csv` and per-run files (`.jsonl` transcript, `.answer.txt`, `.cmds.json`); `results/scored/seriesN/`: rescore CSVs and blind packs; `results/summaries/`: write-ups, `FACTS-benchmark.md`, `per-configuration.csv`, `all-runs.csv`, `chart1-ratios.csv`, `CHARTS.md`
- `reproducibility/`: `verify-results.py` and `environment.md`
- `checksums/`: `SHA256SUMS` (every published file) and `ORIGINAL-SHA256SUMS` (hash of the original source file for each published path, so a reader can see which files were changed by redaction)

## Verify the recorded results (no accounts, no network)

    python3 reproducibility/verify-results.py

It recomputes every row above, the 104/108 vs 98/108 totals, the 8/7/5-of-9 counts, the series 4 medians (131% / 124% / 69%) and the series 5 n=9 and n=8 lines, compares them with `results/summaries/per-configuration.csv`, this README and `FACTS-benchmark.md`, prints a table and exits non-zero on any mismatch. `reproducibility/environment.md` explains how to rerun the benchmark itself.

## What was removed

Local paths, DevX session ids, conversation ids and e-mail addresses were replaced by placeholders such as `<F2>`, `<F3>`, `<BENCH>`, `<HOME>`, `<SESSION-F2>`, `<THREAD-n>`. Scores, answers, numbers and task text were not changed. Some per-run files were left out; see `methodology/limitations.md` ("Published files"). Internal change-set labels `CSnn` in the write-ups name successive DevX builds (CS21 = commit d9340e9, CS23 = 33b9ddf, CS24 = df25de6, CS25 = 2f2c19d, CS26 = 04a02ef). `F-LA-n` in write-ups is the live-agent fact id (`F-OSS22-n` in the original FACTS file).
