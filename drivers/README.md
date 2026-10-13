# Drivers

- `run_bench.py` (Codex CLI) and `run_bench_claude.py` (Claude Code): one agent run per (task, arm, rep); write `rows.csv` and per-run `.jsonl`, `.answer.txt`, `.cmds.json`, `.err`.
- `run_series4.sh`, `run_series5.sh`, `run_series6.sh`, `run_series7.sh`, `run_series14.sh`, `run_series14_trial.sh`: the series launchers as run. `ds_flags.sh`: DeepSeek provider overrides. `iso_run.py`, `dummy_mcp.py`: fixed-cost isolation runs.
- `tables/`: scripts that built the per-series tables, blind packs and exports (`make_series*.py`, `make_claude_series.py`, `make_heldout.py`, `export_runs.py`, `make_charts.py`). Provenance only: they point at the original working tree and at a private key directory, and `make_charts.py` needs matplotlib.

Paths were replaced by placeholders (`<BENCH>`, `<F2>`, `<F3>`, `<FIXTURES>`, `<DEVX-BIN>`, `<HOME>`, `<SCRATCH>`); set them to your own locations before running. Environment variable names for provider keys (`DEEPSEEK_API_KEY`, `DEEPINFRA_API_KEY`) appear as names only; no key value was ever stored in the repository.
