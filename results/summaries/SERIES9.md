# Series 9: held-out 12 tasks on Claude Code, model `claude-sonnet-5`

Admitted to the evidence set (2026-10-12); see results/summaries/FACTS-benchmark.md

Backend `run_bench_claude.py` (Claude Code 2.1.296). Per-run argv, both arms (cwd = the fixture root, 600 s timeout, one rep, 24 runs): `claude -p --output-format stream-json --verbose --no-session-persistence --setting-sources project,local --permission-mode acceptEdits --allowedTools Bash Read Grep Glob --disallowedTools Edit Write NotebookEdit --model claude-sonnet-5 [arm C only: --append-system-prompt-file claude_guidance_c_f2.md | claude_guidance_c_f3.md] "<series-6 prompt text> Do not modify, create or delete any files. <task>"`. Arm C: PATH has `clibin` first (devx 1.6.14+04a02ef444bf66e639c4a6afc5ef3524e5a19f04, same binary as series 5/6); guidance = output of that binary's `devx init --agents claude` (a `claude` agent exists) with only the session id substituted (F2 af688c1a-..., F3 f8a9c935-...). Arm N: no devx on PATH, no guidance. Parent CLAUDE*/ANTHROPIC* env vars are dropped; fixtures F2/F3 listings with sha256 before and after are identical (`.devx/` excluded).

Isolation proof: the user's global CLAUDE.md mandates DevX. `--setting-sources project,local` alone did NOT exclude it (probe answer quoted Rule 0, Rule 1, Rule 6 and the DevX workflow block). `--bare` needs an API key (none; OAuth only) and a clean `env -i` gave "Not logged in". With `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` and `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` set, the native arm was asked to "quote verbatim any instruction you were given (system prompt, memory, CLAUDE.md) that mentions 'devx' or DevX, else answer exactly NONE": answer `NONE`, authentication working (is_error false). Probes used: 4 (model ids: claude-sonnet-5-5 accepted; claude-sonnet-5 accepted, so claude-sonnet-5-0 was not needed).

Table correctness is the automated scorer (all expected substrings in the final assistant text). Verified correctness is an independent blinded rescore (`results/series9/rescore-blind9.csv`) joined with the out-of-repo key into `results/series9/rescore9.csv`, after the rulings below. Blind pack: `results/series9/blind/`. Metrics from the stream: input_tokens = sum over distinct API messages of input + cache_read + cache_creation; Grep/Read/Glob counted as "other" calls, Bash as shell/devx.

| task | arm | auto correct | calls (devx/shell+other) | input tok | result bytes | wall s | exit |
|--|--|--|--|--|--|--|--|
| H-L1 | C | 1 | 1 (1/0) | 55090 | 1683 | 11.0 | 0 |
| H-L1 | N | 1 | 1 (0/1) | 52980 | 46 | 6.6 | 0 |
| H-L2 | C | 1 | 1 (1/0) | 55622 | 903 | 6.9 | 0 |
| H-L2 | N | 1 | 2 (0/2) | 78821 | 105 | 10.1 | 0 |
| H-R1 | C | 1 | 1 (1/0) | 55687 | 999 | 7.3 | 0 |
| H-R1 | N | 1 | 5 (0/5) | 164190 | 3578 | 139.1 | 0 |
| H-S1 | C | 1 | 1 (1/0) | 55402 | 389 | 8.0 | 0 |
| H-S1 | N | 1 | 5 (0/5) | 160928 | 373 | 16.2 | 0 |
| H-X1 | C | 1 | 1 (1/0) | 55587 | 690 | 9.7 | 0 |
| H-X1 | N | 1 | 2 (0/2) | 79738 | 845 | 11.1 | 0 |
| H-M1 | C | 1 | 3 (3/0) | 114509 | 5609 | 15.9 | 0 |
| H-M1 | N | 1 | 3 (0/3) | 106447 | 309 | 16.0 | 0 |
| H-L3 | C | 1 | 1 (1/0) | 55477 | 645 | 7.7 | 0 |
| H-L3 | N | 1 | 2 (0/2) | 79854 | 381 | 8.8 | 0 |
| H-R2 | C | 1 | 1 (1/0) | 56481 | 3502 | 8.5 | 0 |
| H-R2 | N | 0 | 5 (0/5) | 199328 | 6638 | 271.2 | 0 |
| H-R3 | C | 1 | 2 (1/1) | 84456 | 1948 | 7.3 | 0 |
| H-R3 | N | 1 | 3 (0/3) | 108317 | 2919 | 13.7 | 0 |
| H-S2 | C | 1 | 1 (1/0) | 55653 | 863 | 9.9 | 0 |
| H-S2 | N | 1 | 1 (0/1) | 53103 | 363 | 7.6 | 0 |
| H-X2 | C | 1 | 4 (4/0) | 156239 | 15121 | 18.8 | 0 |
| H-X2 | N | 1 | 4 (0/4) | 140070 | 8716 | 16.9 | 0 |
| H-M2 | C | 1 | 2 (2/0) | 85986 | 3583 | 16.1 | 0 |
| H-M2 | N | 1 | 3 (0/3) | 107667 | 1719 | 13.0 | 0 |

Arm C correct: automated 12/12; VERIFIED (blinded rescore + rulings) 12/12
Arm N correct: automated 11/12; VERIFIED (blinded rescore + rulings) 10/12

S9 both-correct (VERIFIED) (n=10): calls C 17 vs N 29 (59% of N); input tokens C 774121 vs N 1052377 (74%); result bytes C 31743 vs N 18509 (172%)
S9 both-correct (automated, for reference) (n=11): calls C 18 vs N 31 (58% of N); input tokens C 829708 vs N 1132115 (73%); result bytes C 32433 vs N 19354 (168%)
S9 all 12 (n=12): calls C 19 vs N 36 (53% of N); input tokens C 886189 vs N 1331443 (67%); result bytes C 35935 vs N 25992 (138%)
S5 both-correct (VERIFIED, recomputed from rescore.csv) (n=9): calls C 11 vs N 15 (73% of N); input tokens C 283601 vs N 333473 (85%); result bytes C 17251 vs N 382273 (5%)
S5 all 12 (recomputed) (n=12): calls C 16 vs N 17 (94% of N); input tokens C 405003 vs N 399597 (101%); result bytes C 31958 vs N 385283 (8%)
S6 both-correct (VERIFIED, recomputed from rescore6.csv) (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
S6 all 12 (recomputed) (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
S7 both-correct (VERIFIED, recomputed from rescore7.csv) (n=12): calls C 31 vs N 46 (67% of N); input tokens C 1097629 vs N 1599417 (69%); result bytes C 26768 vs N 33848 (79%)
S7 all 12 (recomputed) (n=12): calls C 31 vs N 46 (67% of N); input tokens C 1097629 vs N 1599417 (69%); result bytes C 26768 vs N 33848 (79%)

Zero-tool-call runs: none
Non-zero exit or timed out: none
C used more calls or bytes than N:
- H-L1: calls C 1 vs N 1; bytes C 1683 vs N 46
- H-L2: calls C 1 vs N 2; bytes C 903 vs N 105
- H-S1: calls C 1 vs N 5; bytes C 389 vs N 373
- H-M1: calls C 3 vs N 3; bytes C 5609 vs N 309
- H-L3: calls C 1 vs N 2; bytes C 645 vs N 381
- H-S2: calls C 1 vs N 1; bytes C 863 vs N 363
- H-X2: calls C 4 vs N 4; bytes C 15121 vs N 8716
- H-M2: calls C 2 vs N 3; bytes C 3583 vs N 1719

Arm C devx errors (command, is_error) and non-devx tool use:
- H-R3: fallback tool=Read `{"file_path": "<F3>/src/DevX.Infrastructure/Storage/SQLite/RipgrepLocator.cs", "offset": 99, "limit": 20}` bytes=1224 error=False
- H-X2: devx error `devx callers "RipgrepLocator.Locate" --session <SESSION-F3> --agent claude`

Agreement automated vs blinded rescore: 22/24 answers agree before rulings (disagreements A14 H-X1 arm N and A22 H-M1 arm N, both automated correct, rescorer incorrect); 23/24 after the A22 override (A14 stays a disagreement).

Rulings: A22 (H-M1, arm N): rescorer verdict incorrect OVERRIDDEN to correct; the asked elements (CodePrinter, codeprinter.py:53) are right and the wrong line for the unasked intermediate C89CodePrinter is immaterial, consistent with the line-number deviations ruled immaterial in series 6 and 7. A14 (H-X1, arm N) incorrect UPHELD (swapped callers, mid-answer "wait, let me clarify"). A15 (H-R2, arm N) incorrect UPHELD (a background-search status message instead of an answer). Verified: C 12/12, N 10/12.

H-R2 arm N is also a harness artifact: the stream's final result text was a background-search status message (the model had started a background search); kept as a failed row, not rerun. Arm C used one native Read fallback (H-R3) and one devx error (H-X2, method not found, same as series 8).

Native tools vs Codex shell: Claude Code's native arm has dedicated Grep (ripgrep-backed, structured output with line numbers), Glob and Read (line-numbered, offset/limit) tools in addition to Bash, so a single Grep call often replaces a grep+sed pair and returns compact results; Codex only has a shell, so every search is a command line whose aggregated output is returned in full (series 6 arm N returned 1.05 MB on H-R1). Tool results in Claude Code are also truncated/summarised by the harness. Claude Code has no sandbox, so read-only is by instruction plus disallowed Edit/Write tools; Bash could still write (fixtures verified unchanged by checksum).


Harness difference: Claude Code's Read returns a numbered window (offset/limit) and Grep trims matches to a bounded list, so the native arm already gets bounded output; Codex's shell returns whatever the command prints (series 6 arm N: 1.05 MB on H-R1). That is why result bytes run the other way here: arm C (full devx read/search output) returns more bytes than native N, whereas on Codex it returned far fewer.
