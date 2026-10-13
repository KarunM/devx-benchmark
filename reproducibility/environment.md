# Reproducing the benchmark

Two modes. Mode A needs nothing but Python 3. Mode B repeats the live agent runs and needs accounts.

## Mode A: verify the recorded results
    python3 reproducibility/verify-results.py
Standard library only, no network, no accounts. It recomputes from `results/raw/*/rows.csv` and `results/scored/*/rescore*.csv` (series 5 from the per-run table in `results/summaries/SERIES5.md`; series 7 and 14 also read the run `.jsonl` to subtract the Codex "Model metadata not found" pseudo-call): per-configuration both-correct sums and percentages, per-arm verified correctness, the nine-configuration totals (104/108 vs 98/108; DevX fewer calls in 8 of 9, fewer input tokens in 7 of 9, fewer result bytes in 5 of 9), the tuned series 4 medians (131% / 124% / 69%) and the series 5 n=9 and n=8 lines. It compares them with `results/summaries/per-configuration.csv`, `README.md` and `results/summaries/FACTS-benchmark.md`, prints a table and exits non-zero on any mismatch.

## Mode B: rerun the runs
Fixtures are not included. Fetch them yourself:
- **F2**: `pip download sympy==1.13.3 --no-binary :all:` or `git clone https://github.com/sympy/sympy && git checkout sympy-1.13.3` (tag `sympy-1.13.3`; `sympy/release.py` must read `__version__ = "1.13.3"`). sympy is BSD-3-Clause. The original F2 listing had 2,529 files (1,605 indexed by DevX); a different checkout may differ in untracked files.
- **F3**: the DevX source at commit `04a02ef` (MIT, public; this commit is the v1.7.0 code). Build `DevX.Cli` from that commit with the .NET 10 SDK and put it on PATH as `devx` for arm C. Use 1.7.0 = 04a02ef: 1.7.1 and 1.7.2 changed `callers` behaviour, so reruns on newer builds are not comparable on H-X1 and H-X2.
- Index each fixture with `devx index`, create a DevX session for each (the guidance files contain `<SESSION-F2>` / `<SESSION-F3>` placeholders; put your own session id there).
- Drivers: `drivers/run_bench.py` (Codex) and `drivers/run_bench_claude.py` (Claude Code), launched by `drivers/run_series*.sh`. They contain paths of the original working tree (`<BENCH>`, `<F2>`, `<F3>`, `<HOME>` placeholders in this copy); edit the constants at the top. The table and blind-pack scripts in `drivers/tables/` are provenance and expect the original layout.
- Arm N needs a Codex home (or Claude Code configuration) with no DevX instructions; check with the "answer exactly NONE" probe described in `results/summaries/ISOLATION.md`.

### Accounts and keys per harness
| harness | needs | notes |
|--|--|--|
| Codex CLI 0.155.1 + OpenAI models (series 5, 6, 11) | ChatGPT account signed in to Codex | ran on a subscription plan |
| Claude Code 2.1.296 (series 8, 9, 10, 13) | Anthropic account signed in to Claude Code | ran on a subscription plan |
| Codex CLI + DeepSeek (series 7) | a DeepSeek API key in `DEEPSEEK_API_KEY`, passed through `--env-file` | model `deepseek-flash`; spend not recorded |
| Codex CLI + DeepInfra (series 14) | a DeepInfra API key in `DEEPINFRA_API_KEY`, passed through `--env-file` | about $0.75 |

Keep keys outside the repository and never log them.

### Approximate cost per 24-run series (recorded totals, both arms, all 24 runs)
| series | input tokens | output tokens | billing |
|--|--|--|--|
| 5 | 804,600 | 4,810 | subscription |
| 6 | 861,920 | 9,160 | subscription |
| 7 | 2,697,046 | 7,336 | DeepSeek API, not recorded |
| 8 | 1,174,042 | 4,712 | subscription |
| 9 | 2,217,632 | 625 | subscription |
| 10 | 1,316,062 | 2,756 | subscription |
| 11 | 915,446 | 6,484 | subscription |
| 13 | 1,313,415 | 3,516 | subscription |
| 14 | 2,075,598 | 10,245 | DeepInfra: 2,075,598 x $0.32/M + 10,245 x $3.20/M = $0.697; trial and probes add about $0.05, so about $0.75 in total |

Input tokens include cached input. Claude Code and Codex consumption on subscription plans counts against plan limits, not dollars; DeepInfra prices are those quoted on 2026-10-12.

### Nondeterminism
One run per task and arm. Model output and tool choices vary between runs, so a rerun will not reproduce individual rows; expect differences of a call or two per task and an occasional different verdict. Compare totals and ratios, not rows.

### Machine and software used
macOS 26.5.1 (arm64), .NET 10 SDK, Codex CLI 0.155.1, Claude Code 2.1.296, ripgrep 14.1.1, Python 3.9.6 (`/usr/bin/python3`), DevX 1.7.0 = commit 04a02ef (`devx version` printed `1.6.14+04a02ef444bf66e639c4a6afc5ef3524e5a19f04`). Timeout 600 s per run for Claude Code.

## Licences and rights
- F2 sympy 1.13.3: BSD-3-Clause. F3 DevX at 04a02ef: MIT. Transcripts quote fragments of both.
- Model outputs in the transcripts come from OpenAI (Codex CLI with a ChatGPT account), Anthropic (Claude Code), DeepSeek (API) and DeepInfra (Qwen). Whether republishing these outputs for research and benchmark documentation is allowed under each provider's terms has not been checked and is the maintainer's decision; nothing here asserts those rights.
- The local Ollama Qwen trial is excluded (stopped after 4 of 6 runs, parked, not evidence).
