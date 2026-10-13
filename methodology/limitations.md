# Limitations

## Design
- **One run per cell.** Series 5-14 have one run per task and arm; results vary from run to run and no significance test is claimed. Series 4 has 3 reps on the tuned set only.
- **Same 12 tasks across all nine configurations.** After series 5 the held-out tasks are a regression set, not a generalisation set. Per-task wording problems (H-M1) were left in place.
- **One repository pair.** One Python repository (sympy) and one C# repository (DevX's own source, which the DevX authors know well). Neither is representative of arbitrary codebases.
- **Read-only question answering only.** No editing, building or testing workflow was measured.
- **Author-run, not independent.** The same people built DevX, wrote the tasks and references, ran the series and (through a separate session) graded the answers. The blinded rescore is blinded but not independent.
- **Tuned set is tuned.** DevX guidance and features (builds CS24-CS26) were developed against the series 1-4 tasks; their numbers are not evidence of generalisation.

## Harnesses and models
- **Harness differences.** Codex CLI returns whatever a shell command prints; Claude Code's Read and Grep tools bound their output. This is why result bytes favour DevX on Codex (3.6-79%) and native on Claude Code (156-172%). Do not average bytes across harnesses.
- **Reasoning effort is not controlled.** Codex runs print `medium` from config; for DeepSeek and Qwen it is unknown whether the setting is honoured; Claude Code runs used the default and the harness did not record it.
- **Model availability.** `gpt-6.1-sol` was rejected by the account (HTTP 400), so `gpt-6-sol` was used. Model identifiers are as the providers reported them on the run dates (2026-10-12); some may no longer resolve.
- **Token accounting.** Each run carries a fixed input of about 26,000 tokens (prompt plus guidance), which dominates token totals. DeepSeek input tokens include about 73k uncached baseline per run, so series 7 tokens are not comparable with series 5-6 in absolute terms. The Codex "Model metadata not found" warning is subtracted from call counts in series 7 and 14 (otherwise series 14 reads 62% / 70% instead of 48% / 58% on all 12 tasks). Cached tokens are included in `input_tokens`.
- **Wall time** is reported in the write-ups but is not a headline metric; it depends on provider load.

## The measured build
The build 1.6.14+04a02ef (release 1.7.0) contains known defects that the numbers include:
- C# `callers` on an overloaded method fails ("matched multiple implementations" or "not found"), seen on H-X2 in four of five early configurations; the agent recovered with `search text` each time. Fixed in 1.7.1.
- Python text-backed `callers` counts module-docstring lines (and doctest `>>>` lines) as call sites; it caused the one traceable DevX-wrong answer (series 14 H-X1). Present in 1.7.1; fix scheduled for 1.7.2.
- Single-line locate returns 383-1,762 B where grep returns 53-813 B; the `--full` wording invites listing every site.
- Reruns on 1.7.1 or later are therefore not comparable on H-X1 and H-X2.

## Published files
- Fixtures are not included (licences and size); see `reproducibility/environment.md`.
- Per-run `.err` files of series 14 and of the DeepInfra trial were left out: they contain the provider's model catalogue (model descriptions and terms text) printed by a cosmetic Codex "failed to refresh available models" error. One further transcript (`series9/H-R2-N-r1.jsonl`) was left out because it lists directory names of unrelated local projects. Their rows in `rows.csv` and verdicts are included. See `checksums/ORIGINAL-SHA256SUMS` for the files that exist in the original.
- The Ollama (local Qwen) trial is excluded: it was stopped after 4 of 6 runs and is not evidence.
- Charts are not included (data tables are: `chart1-ratios.csv`, `per-configuration.csv`, `all-runs.csv`, `CHARTS.md`).
- Redaction replaced only paths, session and conversation ids, maintainer e-mail addresses and internal process terms (see the README); third-party e-mail addresses inside fixture text echoed by tools (sympy source headers) are kept so transcripts stay byte-faithful to the recorded `result_bytes`, and only the maintainer's own addresses were redacted; transcripts otherwise contain the model's output verbatim, including fixture source text whose code comments contain ordinary words such as role names.

## Licences and rights (open for the maintainer)
- Fixture F2 is sympy 1.13.3 (BSD-3-Clause); fixture F3 is DevX source at commit 04a02ef (MIT). Neither is redistributed here; transcripts quote fragments of both.
- Model outputs in transcripts come from OpenAI (via Codex CLI, ChatGPT account), Anthropic (via Claude Code), DeepSeek (API) and DeepInfra (Qwen). Whether republishing those outputs for research and benchmark documentation is permitted under each provider's terms has not been checked; this is the maintainer's decision and is not asserted here.
- Provider names and model names are used descriptively only.
