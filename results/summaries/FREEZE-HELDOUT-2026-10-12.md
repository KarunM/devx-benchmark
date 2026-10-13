# Freeze manifest: held-out benchmark, series 5-9 (2026-10-12)

Record of build, harness, tasks, scoring and per-run outputs. Favourable and unfavourable results are both preserved; nothing was rerun or deleted. Checksums of the original files were recorded at freeze time (`shasum -a 256 -c` all OK); in this package see `checksums/ORIGINAL-SHA256SUMS`.

## 1. DevX build
- `clibin/devx` is a symlink to a local build of commit 04a02ef (`DevX.Cli`).
- `devx version`: `1.6.14+04a02ef444bf66e639c4a6afc5ef3524e5a19f04`.
- sha256 of that DevX.Cli (apphost): `b035879a34a9dc6555f6887a1acca769e4e739ce54f2d13dd33bef9922cd33c7` (identical to a second copy of the same build). `DevX.Cli.dll` is also in the sha file.
- Source commit 04a02ef is the public v1.7.0 code; only the version string differs (1.6.14 development build vs 1.7.0 release).

## 2. Harness versions
| item | seen |
|--|--|
| codex | codex-cli 0.155.1 |
| claude | 2.1.296 (Claude Code) |
| python3 | 3.9.6 (drivers run with /usr/bin/python3) |
| macOS | 26.5.1 |
| rg | ripgrep 14.1.1 (rev eecfd55deb); in this shell `rg` is a function wrapping the claude binary; there is no rg in `clibin` |

## 3. Models and invocation
- Series 5: Codex, `gpt-6-luna` (driver default), `run_series5.sh`: `run_bench.py --series series5 --tasks-file tasks_heldout.json --arm CN --codex-home-c codex_home_c --sandbox-c read-only --tasks all --reps 1`. Per run `codex exec -m <model> --json -C <fixture> --skip-git-repo-check -s read-only --ephemeral -o <answer>`; arm C PATH has `clibin`, `codex_home_c` (f2) or `codex_home_c3` (f3) AGENTS.md.
- Series 6: same plus `--model gpt-5.6-luna` (`run_series6.sh`).
- Series 7: `deepseek-flash` through Codex provider overrides (`ds_flags.sh`: model_provider deepseek, base_url https://api.deepseek.com, env_key DEEPSEEK_API_KEY, wire_api responses). Key file path only: `<HOME>/.config/devx-bench/deepseek.env` (content never recorded).
- Series 8: Claude Code, `claude-sonnet-5-5`. Series 9: Claude Code, `claude-sonnet-5`. Argv for both: `claude -p --output-format stream-json --verbose --no-session-persistence --setting-sources project,local --permission-mode acceptEdits --allowedTools Bash Read Grep Glob --disallowedTools Edit Write NotebookEdit --model <m> [arm C: --append-system-prompt-file claude_guidance_c_f2.md|claude_guidance_c_f3.md] "<prompt>"`, cwd fixture root, 600 s timeout, 1 rep, 24 runs. Isolation: `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`, parent CLAUDE*/ANTHROPIC* env dropped; native-arm probe answered `NONE`.
- Series 10: Claude Code, `claude-opus-5-5`; series 13: Claude Code, `claude-fable-5-1`; argv and isolation as series 8/9, 24 runs each (`SERIES10.md`, `SERIES13.md`).
- Series 11: Codex CLI 0.155.1, `gpt-6-sol` (`gpt-6.1-sol` rejected by the account), same `run_bench.py` invocation as series 6 with `--model gpt-6-sol`, reasoning effort `medium` from config (`SERIES11.md`).
- Series 14: Codex CLI 0.155.1, `Qwen/Qwen3.6-27B` (fp8, DeepInfra) via `-c` overrides `model_provider="deepinfra"`, `base_url="https://api.deepinfra.com/v1/openai"`, `env_key="DEEPINFRA_API_KEY"`, `wire_api="responses"`; key loaded with `--env-file` from outside the repo (path `~/.config/devx-bench/deepinfra.env`, content never recorded); `run_series14.sh` (`SERIES14.md`).

## 4. Task set (`tasks_heldout.json`, 12 tasks; answers in `HELDOUT-ANSWERS.md`)
| id | kind | fixture |
|--|--|--|
| H-L1 | locate | f2 |
| H-L2 | locate | f2 |
| H-R1 | read | f2 |
| H-S1 | structure | f2 |
| H-X1 | crossref | f2 |
| H-M1 | multihop | f2 |
| H-L3 | locate | f3 |
| H-R2 | read | f3 |
| H-R3 | read | f3 |
| H-S2 | structure | f3 |
| H-X2 | crossref | f3 |
| H-M2 | multihop | f3 |

Fixtures: f2 = sympy checkout, `sympy/release.py` `__version__ = "1.13.3"`, 2529 listed files; f3 = DevX C# source at 04a02ef, 241 files. Proof of no change: `results/f2-before-seriesN.txt` vs `f2-after-seriesN.txt` and the f3 pair, N = 5..9, are byte-identical (`cmp`, checked at freeze; `.devx/` excluded). All are in the sha file.

## 5. Scoring
- Automated: correct = every string in the task's `expected` list is a substring of the final answer text.
- Blinded rescore: answers shuffled to A01..A24, `blind/blind-index.csv` maps id to task and question without arm, key kept outside the repo, a second agent judged each, maintainer rulings applied where noted, then joined to `rescoreN.csv`.
- Agreement automated vs blinded rescore: S5 hand-check (rescore.csv): one disagreement, H-S1 arm C (scorer 1, manual 0); S6 24/24; S7 24/24; S8 23/24 (A23 H-M1 arm N, ruling upheld incorrect); S9 23/24 after rulings (22/24 before; A14 H-X1 arm N upheld incorrect, A22 H-M1 arm N overridden to correct).
- Verified correctness C/N: S5 10/12, 10/12; S6 12/12, 12/12; S7 12/12, 12/12; S8 12/12, 11/12; S9 12/12, 10/12.

## 6. Metric definitions (drivers)
- `tool_calls_total` = devx + shell + mcp + other (Claude driver: devx + shell + other, mcp 0). `tool_calls_devx`/`_shell`: Codex counts command_execution items; Claude counts Bash tool_use, devx when the command starts with `devx`. `tool_calls_other`: any other item type (Claude: Grep, Read, Glob).
- `input_tokens`: Codex, sum of turn.completed usage input_tokens (already includes cached_input_tokens). Claude, sum over distinct API messages of input + cache_read + cache_creation.
- `result_bytes`: UTF-8 bytes of tool result text returned to the model (Codex: MCP text plus shell aggregated_output).
- `wall_seconds`: wall clock of the subprocess, rounded to 0.1 s.

## 7. Per-run artifacts (`results/seriesN/`)
Each run: `<task>-<arm>-r1.jsonl`, `.answer.txt`, `.cmds.json`, `.err` (24 each) plus the files below.
| series | total files | other files |
|--|--|--|
| 5 | 99 | rows.csv, tables.md, series5.log |
| 6 | 126 | rows.csv, tables.txt, series6.log, rescore6.csv, rescore-blind6.csv, blind/ (25) |
| 7 | 128 | rows.csv, series7.log, mtimes-before.txt, probe1.txt, probe2.txt, rescore7.csv, rescore-blind7.csv, blind/ (25) |
| 8 | 126 | rows.csv, tables.txt, series8.log, rescore8.csv, rescore-blind8.csv, blind/ (25) |
| 9 | 126 | rows.csv, tables.txt, series9.log, rescore9.csv, rescore-blind9.csv, blind/ (25) |

Series 5 rescore files are `rescore.csv` and `rescore-blind.csv` in the bench root. Also frozen: drivers, `codex_home_c*/AGENTS.md`, Claude guidance files.

## 8. Known defects and anomalies kept
- H-X2 `devx callers "…RipgrepLocator.Locate"` failed in arm C: series 5 (rc 1, "matched multiple implementations"), series 7 (rc 1, "not found"), series 8 and 9 (devx error, method not found). Series 6 arm C had no devx error. Runs still answered via search.
- Series 9 H-R2 arm N: final result text was a background-search status message; kept as a failed row, not rerun.
- Series 7: parser counts the codex "Model metadata … not found" warning as an `other` item (rows.csv totals 1 higher per run), and two `cd <fixture> && devx …` calls in H-R2 arm C are counted as shell; input tokens include a ~73k baseline, so not comparable to S5/S6.
- Series 5: H-R2 arm N 358,121 B outlier (`rg -C 5` including a tracked `Program.cs.bak`); zero-call runs H-S1-N (refusal) and H-M1-C (wrong class).
- H-M1 wording ("Name that class") is loose; reference is CodePrinter at codeprinter.py:53, rulings differ in effect between S8 (upheld) and S9 (overridden).
- Series 14 H-X1 arm C (and F-FM-10): Python text-backed `callers mrv_leadterm` reports four module-docstring lines (gruntz.py:78,102,108,111) as `<module>` call sites; the Qwen answer invented a caller `limit`; blind verdict incorrect; open in 1.7.1.
- `run_bench.py` was modified on 2026-10-12 at 22:23: added `--codex-flag` and `--timeout`. Old sha256 3bfd09edc22cfed60d617d12c0bd36a7f6f3f1562336d5523a6a8605f3121b04 (series 5-13 ran on this content); new sha256 2f62769e0b59a9cb85a8cfcb8f9849eea157a2fa508f24c3018911494881dead (used by series 14 and `results/trial-qwen-di/`); the pin line now holds the new hash.
