# Configurations

Guidance files under test (arm C only):
- `claude_guidance_c_f2.md`, `claude_guidance_c_f3.md`: Claude Code (`--append-system-prompt-file`), F2 and F3 variants.
- `codex_agents_c_f2.md`, `codex_agents_c_f3.md`: Codex CLI `AGENTS.md` (originally `codex_home_c/AGENTS.md` and `codex_home_c3/AGENTS.md`). They are the text DevX ships (`devx init --agents codex`) with the session id replaced by a placeholder (`<SESSION-F2>`, `<SESSION-F3>`). The text says "the session ID your brief gives you"; it is the shipped wording, kept verbatim. Only these four files were taken from the Codex home directories; nothing else from them (credentials, caches, databases) is published.

## Versions
| item | value |
|--|--|
| DevX build | commit 04a02ef, `devx version` = `1.6.14+04a02ef444bf66e639c4a6afc5ef3524e5a19f04`; this commit is the public v1.7.0 code (only the version string differs) |
| DevX.Cli apphost sha256 | `b035879a34a9dc6555f6887a1acca769e4e739ce54f2d13dd33bef9922cd33c7` |
| Codex CLI | codex-cli 0.155.1 |
| Claude Code | 2.1.296 (headless `-p`, stream-json) |
| ripgrep | 14.1.1 |
| Python | 3.9.6 (`/usr/bin/python3`) |
| OS | macOS 26.5.1, arm64 |
| .NET (to build DevX) | .NET 10 |

## Per-series invocation and model
| series | model id | harness and provider | invocation |
|--|--|--|--|
| 1-4 | gpt-6-luna | Codex CLI, ChatGPT account | `run_bench.py` default model; `codex exec -m <model> --json -C <fixture> --skip-git-repo-check --ephemeral -o <answer>`; arm C `workspace-write`, arm N `read-only` (series 1-4) |
| 5 | gpt-6-luna | Codex CLI, ChatGPT account | `run_bench.py --series series5 --tasks-file tasks_heldout.json --arm CN --codex-home-c codex_home_c --sandbox-c read-only --tasks all --reps 1` |
| 6 | gpt-5.6-luna | Codex CLI, ChatGPT account | as series 5 plus `--model gpt-5.6-luna`; reasoning effort `medium` (config) |
| 7 | deepseek-flash (metadata: DeepSeek-V4.1-Flash) | Codex CLI with `-c` provider overrides, DeepSeek API | `ds_flags.sh`: `model_provider=deepseek`, base URL `https://api.deepseek.com`, `env_key=DEEPSEEK_API_KEY`, `wire_api=responses`; effort printed `medium`, honoured or not is unknown |
| 8 | claude-sonnet-5-5 | Claude Code, subscription | `claude -p --output-format stream-json --verbose --no-session-persistence --setting-sources project,local --permission-mode acceptEdits --allowedTools Bash Read Grep Glob --disallowedTools Edit Write NotebookEdit --model <m> [arm C: --append-system-prompt-file claude_guidance_c_f2.md or _f3.md] "<prompt>"`, cwd = fixture root, 600 s timeout; environment `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`, parent `CLAUDE*`/`ANTHROPIC*` variables dropped |
| 9 | claude-sonnet-5 | as series 8 | as series 8 |
| 10 | claude-opus-5-5 | as series 8 | as series 8 |
| 11 | gpt-6-sol | Codex CLI, ChatGPT account | as series 6 with `--model gpt-6-sol`; `gpt-6.1-sol` was rejected (HTTP 400); effort `medium` |
| 13 | claude-fable-5-1 | as series 8 | as series 8 |
| 14 | Qwen/Qwen3.6-27B (fp8, 262k context) | Codex CLI with `-c` provider overrides, DeepInfra API | `run_series14.sh`: `model_provider=deepinfra`, base URL `https://api.deepinfra.com/v1/openai`, `env_key=DEEPINFRA_API_KEY`, `wire_api=responses`; effort `medium` from config, usage reports 0 reasoning tokens |

Per-series details (probes, rulings, per-run tables): `results/summaries/SERIES<N>.md`. The `run_bench.py` driver was edited once during the project (added `--codex-flag` and `--timeout`, 2026-10-12): series 5-13 ran on the version with sha256 `3bfd09edc22cfed60d617d12c0bd36a7f6f3f1562336d5523a6a8605f3121b04`, series 14 on the published version (sha256 of the original file `2f62769e0b59a9cb85a8cfcb8f9849eea157a2fa508f24c3018911494881dead`; the published copy differs only by redaction, see `checksums/ORIGINAL-SHA256SUMS`).
