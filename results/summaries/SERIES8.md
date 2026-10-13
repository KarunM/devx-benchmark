# Series 8: held-out 12 tasks on Claude Code, model `claude-sonnet-5-5`

Admitted to the evidence set (2026-10-12); see results/summaries/FACTS-benchmark.md

Backend `run_bench_claude.py` (Claude Code 2.1.296). Per-run argv, both arms (cwd = the fixture root, 600 s timeout, one rep, 24 runs): `claude -p --output-format stream-json --verbose --no-session-persistence --setting-sources project,local --permission-mode acceptEdits --allowedTools Bash Read Grep Glob --disallowedTools Edit Write NotebookEdit --model claude-sonnet-5-5 [arm C only: --append-system-prompt-file claude_guidance_c_f2.md | claude_guidance_c_f3.md] "<series-6 prompt text> Do not modify, create or delete any files. <task>"`. Arm C: PATH has `clibin` first (devx 1.6.14+04a02ef444bf66e639c4a6afc5ef3524e5a19f04, same binary as series 5/6); guidance = output of that binary's `devx init --agents claude` (a `claude` agent exists) with only the session id substituted (F2 af688c1a-..., F3 f8a9c935-...). Arm N: no devx on PATH, no guidance. Parent CLAUDE*/ANTHROPIC* env vars are dropped; fixtures F2/F3 listings with sha256 before and after are identical (`.devx/` excluded).

Isolation proof: the user's global CLAUDE.md mandates DevX. `--setting-sources project,local` alone did NOT exclude it (probe answer quoted Rule 0, Rule 1, Rule 6 and the DevX workflow block). `--bare` needs an API key (none; OAuth only) and a clean `env -i` gave "Not logged in". With `CLAUDE_CODE_DISABLE_CLAUDE_MDS=1` and `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` set, the native arm was asked to "quote verbatim any instruction you were given (system prompt, memory, CLAUDE.md) that mentions 'devx' or DevX, else answer exactly NONE": answer `NONE`, authentication working (is_error false). Probes used: 4 (model ids: claude-sonnet-5-5 accepted; claude-sonnet-5 accepted, so claude-sonnet-5-0 was not needed).

Table correctness is the automated scorer (all expected substrings in the final assistant text). Verified correctness is an independent blinded rescore (`results/series8/rescore-blind8.csv`) joined with the out-of-repo key into `results/series8/rescore8.csv`, after the rulings below. Blind pack: `results/series8/blind/`. Metrics from the stream: input_tokens = sum over distinct API messages of input + cache_read + cache_creation; Grep/Read/Glob counted as "other" calls, Bash as shell/devx.

| task | arm | auto correct | calls (devx/shell+other) | input tok | result bytes | wall s | exit |
|--|--|--|--|--|--|--|--|
| H-L1 | C | 1 | 1 (1/0) | 38240 | 1683 | 11.2 | 0 |
| H-L1 | N | 1 | 1 (0/1) | 36839 | 46 | 5.4 | 0 |
| H-L2 | C | 1 | 1 (1/0) | 39556 | 903 | 6.4 | 0 |
| H-L2 | N | 1 | 1 (0/1) | 36865 | 61 | 5.3 | 0 |
| H-R1 | C | 1 | 1 (1/0) | 38003 | 999 | 11.7 | 0 |
| H-R1 | N | 1 | 2 (0/2) | 56497 | 1342 | 78.7 | 0 |
| H-S1 | C | 1 | 1 (1/0) | 39336 | 389 | 7.4 | 0 |
| H-S1 | N | 1 | 1 (0/1) | 35377 | 151 | 6.7 | 0 |
| H-X1 | C | 1 | 1 (1/0) | 41194 | 3499 | 9.4 | 0 |
| H-X1 | N | 1 | 1 (0/1) | 35599 | 524 | 7.2 | 0 |
| H-M1 | C | 1 | 2 (2/0) | 59770 | 923 | 9.6 | 0 |
| H-M1 | N | 1 | 1 (0/1) | 37035 | 184 | 6.9 | 0 |
| H-L3 | C | 1 | 1 (1/0) | 39411 | 645 | 6.7 | 0 |
| H-L3 | N | 1 | 1 (0/1) | 35342 | 299 | 5.2 | 0 |
| H-R2 | C | 1 | 1 (1/0) | 38798 | 3502 | 6.0 | 0 |
| H-R2 | N | 1 | 2 (0/2) | 56166 | 1410 | 9.0 | 0 |
| H-R3 | C | 1 | 1 (1/0) | 39721 | 1279 | 6.4 | 0 |
| H-R3 | N | 1 | 2 (0/2) | 57738 | 3791 | 7.6 | 0 |
| H-S2 | C | 1 | 1 (1/0) | 37932 | 863 | 6.2 | 0 |
| H-S2 | N | 1 | 1 (0/1) | 35513 | 674 | 6.1 | 0 |
| H-X2 | C | 1 | 4 (4/0) | 102947 | 4138 | 15.0 | 0 |
| H-X2 | N | 1 | 3 (0/3) | 76079 | 2908 | 13.5 | 0 |
| H-M2 | C | 1 | 3 (3/0) | 84155 | 4730 | 11.6 | 0 |
| H-M2 | N | 1 | 3 (0/3) | 75929 | 3344 | 8.9 | 0 |

Arm C correct: automated 12/12; VERIFIED (blinded rescore + rulings) 12/12
Arm N correct: automated 12/12; VERIFIED (blinded rescore + rulings) 11/12

S8 both-correct (VERIFIED) (n=11): calls C 16 vs N 18 (89% of N); input tokens C 539293 vs N 537944 (100%); result bytes C 22630 vs N 14550 (156%)
S8 both-correct (automated, for reference) (n=12): calls C 18 vs N 19 (95% of N); input tokens C 599063 vs N 574979 (104%); result bytes C 23553 vs N 14734 (160%)
S8 all 12 (n=12): calls C 18 vs N 19 (95% of N); input tokens C 599063 vs N 574979 (104%); result bytes C 23553 vs N 14734 (160%)
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
- H-L2: calls C 1 vs N 1; bytes C 903 vs N 61
- H-S1: calls C 1 vs N 1; bytes C 389 vs N 151
- H-X1: calls C 1 vs N 1; bytes C 3499 vs N 524
- H-M1: calls C 2 vs N 1; bytes C 923 vs N 184
- H-L3: calls C 1 vs N 1; bytes C 645 vs N 299
- H-R2: calls C 1 vs N 2; bytes C 3502 vs N 1410
- H-S2: calls C 1 vs N 1; bytes C 863 vs N 674
- H-X2: calls C 4 vs N 3; bytes C 4138 vs N 2908
- H-M2: calls C 3 vs N 3; bytes C 4730 vs N 3344

Arm C devx errors (command, is_error) and non-devx tool use:
- H-X2: devx error `devx callers "RipgrepLocator.Locate" --full --session <SESSION-F3> --agent claude`

Agreement automated vs blinded rescore: 23/24 answers agree before and after rulings (sole disagreement A23, H-M1 arm N: automated correct, rescorer incorrect, upheld).

Rulings: A23 (H-M1, arm N): rescorer verdict incorrect UPHELD. It states "The class is C89CodePrinter" and gives CodePrinter only as chain context; the reference asks for CodePrinter at codeprinter.py:53. H-M1's wording ("Name that class") is loose and a reader could take it as the intermediate base; the fixed reference and the HELDOUT-ANSWERS derivation define it as CodePrinter, and the same rule was applied in series 6. Verified: C 12/12, N 11/12.

Zero-tool-call runs and devx fallbacks are listed above. The one arm-C devx error (H-X2) was `devx callers` on a method name that does not resolve; the run still answered correctly via later devx calls.

Native tools vs Codex shell: Claude Code's native arm has dedicated Grep (ripgrep-backed, structured output with line numbers), Glob and Read (line-numbered, offset/limit) tools in addition to Bash, so a single Grep call often replaces a grep+sed pair and returns compact results; Codex only has a shell, so every search is a command line whose aggregated output is returned in full (series 6 arm N returned 1.05 MB on H-R1). Tool results in Claude Code are also truncated/summarised by the harness. Claude Code has no sandbox, so read-only is by instruction plus disallowed Edit/Write tools; Bash could still write (fixtures verified unchanged by checksum).


Harness difference: Claude Code's Read returns a numbered window (offset/limit) and Grep trims matches to a bounded list, so the native arm already gets bounded output; Codex's shell returns whatever the command prints (series 6 arm N: 1.05 MB on H-R1). That is why result bytes run the other way here: arm C (full devx read/search output) returns more bytes than native N, whereas on Codex it returned far fewer.
