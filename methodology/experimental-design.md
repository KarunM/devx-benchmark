# Experimental design

## Question
Does giving a coding agent the DevX CLI (`devx search|read|callers|references|snapshot`) and DevX's shipped guidance reduce the tool calls, model input tokens and tool-result bytes needed to answer read-only code questions correctly, compared with the same agent using the shell only (grep, rg, sed, cat)?

## Arms
- **Arm C ("DevX")**: the `devx` CLI on PATH (build 1.6.14+04a02ef = release 1.7.0) and DevX's shipped guidance block (about 2.9-3.0 KB, `devx init --agents codex`; for Claude Code the same text via `--append-system-prompt-file`), with one edit: the DevX session id. Files: `configurations/`.
- **Arm N ("native")**: the same model and prompt wording with shell tools only, no DevX on PATH, and a home/config directory without DevX guidance. For Claude Code the isolation settings of `results/summaries/ISOLATION.md` and the per-series probe ("answer exactly NONE") confirm no DevX instruction reached the native arm.

## Sandbox
Series 1-4 arm C ran `workspace-write` because early builds wrote search/read history to `.devx/devx.db`; arm N ran read-only. From series 5 (held-out) both arms ran read-only (`-s read-only` for Codex; Claude Code with Edit, Write and NotebookEdit disallowed). Fixture listings with checksums before and after a series (`results/raw/fixture-listings/`) are byte-identical wherever both exist (F2: series 2-10, 13, 14; F3: series 5-10, 13, 14), so no run in those series changed a fixture. Series 1 and 11 have no matching before/after pair (`f2-before.txt` and `f2-after.txt` differ; the reason is not documented in the source write-ups), and `.devx/` is excluded from the listings.

## Fixtures (not included; see `reproducibility/environment.md`)
- **F2**: sympy 1.13.3 checkout (Python, BSD-3-Clause), about 1,605 indexed files.
- **F3**: DevX's own C# source at commit 04a02ef (MIT), about 222-241 files.

## Task sets
- **Tuned set** (`tasks/tuned/tasks.json`): 12 tasks, kinds locate (L), read (R), structure (S), crossref (X), multihop (M), 2-3 per kind, on F2. DevX guidance and features were developed against these tasks (builds CS23 to CS26), so results on this set are not a generalisation test. Series 1-3 are 1 rep; series 4 is 3 reps (72 runs).
- **Held-out set** (`tasks/held-out/tasks_heldout.json`): 12 tasks written after the DevX build was frozen: H-L1, H-L2, H-R1, H-S1, H-X1, H-M1 on F2 and H-L3, H-R2, H-R3, H-S2, H-X2, H-M2 on F3, with fixed expected strings and the derivation commands in `HELDOUT-ANSWERS.md`. Series 5 is the only series for which the set was untouched. From series 6 on, the same 12 tasks were reused for other models, so the set is a regression set from then on.

## Series
| series | what | model | harness | DevX build | runs |
|--|--|--|--|--|--|
| 1 | tuned tasks, no guidance | gpt-6-luna | Codex CLI | 1.6.14+33b9ddf | 24 |
| 2 | tuned tasks, shipped guidance | gpt-6-luna | Codex CLI | 1.6.14+df25de6 | 24 |
| 3 | tuned tasks, regenerated guidance | gpt-6-luna | Codex CLI | 1.6.14+2f2c19d | 24 |
| 4 | tuned tasks, 3 reps | gpt-6-luna | Codex CLI | 1.6.14+04a02ef | 72 |
| 5 | held-out | gpt-6-luna | Codex CLI | 1.6.14+04a02ef | 24 |
| 6 | held-out | gpt-5.6-luna | Codex CLI | 04a02ef | 24 |
| 7 | held-out | deepseek-flash (DeepSeek Flash 4.1) | Codex CLI, provider overrides | 04a02ef | 24 |
| 8 | held-out | claude-sonnet-5-5 | Claude Code 2.1.296 | 04a02ef | 24 |
| 9 | held-out | claude-sonnet-5 | Claude Code 2.1.296 | 04a02ef | 24 |
| 10 | held-out | claude-opus-5-5 | Claude Code 2.1.296 | 04a02ef | 24 |
| 11 | held-out | gpt-6-sol | Codex CLI 0.155.1 | 04a02ef | 24 |
| 13 | held-out | claude-fable-5-1 | Claude Code 2.1.296 | 04a02ef | 24 |
| 14 | held-out | Qwen/Qwen3.6-27B fp8 (DeepInfra) | Codex CLI, provider overrides | 04a02ef | 24 |

Series 12 does not exist in this package (the number was skipped). The nine configurations of the headline table are series 5, 6, 7, 8, 9, 10, 11, 13 and 14. Series 1-4 are the tuning history; the preliminary trials (`results/raw/preliminary/`: MCP arm trial, DevX-arm trials, isolation, smoke) are kept as records and are not counted in any figure. A local Ollama trial was stopped after 4 of 6 runs because of stream disconnects; it is parked, is not evidence and is excluded from this package.

## What was counted
Per run (`rows.csv`): `tool_calls_total` = devx + shell + mcp + other (Claude driver: devx + shell + other); `input_tokens` (Codex: sum of `turn.completed` input tokens including cached; Claude: sum over distinct API messages of input + cache read + cache creation); `result_bytes` = UTF-8 bytes of tool-result text returned to the model; `wall_seconds`. For series 7 and 14 the Codex warning "Model metadata for `<model>` not found" is recorded by the parser as one `other` item per run; it is subtracted once per run (detected by that phrase in the run's `.jsonl`), as in the series write-ups.

## Derived figures
Ratios are DevX divided by native, summed over the tasks both arms answered correctly (verified verdicts). Series 5 is published at n=8 (H-R2 excluded: the native `rg -C 5` printed 358,121 B because the fixture tree contained a tracked `.bak` file); the n=9 line is in `FACTS-benchmark.md`. Correctness totals use all 12 tasks per arm. `reproducibility/verify-results.py` recomputes all of it.

## Guidance, prompts, drivers
The prompt text and run commands are in `drivers/` (`run_bench.py` for Codex, `run_bench_claude.py` for Claude Code, `run_series*.sh`, `ds_flags.sh` for DeepSeek provider flags). Per-series invocations are in `configurations/configurations.md` and the series write-ups.
