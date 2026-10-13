# Series 13: held-out 12 tasks on Claude Code, model `claude-fable-5-1`

Admitted to the evidence set (maintainer decision 2026-10-12); see FACTS.md F-FM-*.

Model id `claude-fable-5-1` accepted (run 1 jsonl and all 24 rows.csv rows carry `claude-fable-5-1`). Harness `run_bench_claude.py` unchanged: `python3 run_bench_claude.py --series series13 --model claude-fable-5-1`. Per-run argv identical to series 10 except the model: `claude -p --output-format stream-json --verbose --no-session-persistence --setting-sources project,local --permission-mode acceptEdits --allowedTools Bash Read Grep Glob --disallowedTools Edit Write NotebookEdit --model claude-fable-5-1 [arm C: --append-system-prompt-file claude_guidance_c_f2.md|f3.md] "<prompt>"`. Reasoning effort: not set by the harness (Claude Code default for the model). DevX via clibin: same as series 5-11 (1.6.14+04a02ef). Fixture listings with sha256 before/after identical (f2 and f3 byte-identical). 1 rep, 24 runs, all exit 0.

Isolation proof: with CLAUDE_CODE_DISABLE_CLAUDE_MDS=1, CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 and CLAUDE*/ANTHROPIC* parent env dropped, model claude-fable-5-1, the question "Quote verbatim any instruction you were given (system prompt, memory, CLAUDE.md) that mentions 'devx' or DevX, else answer exactly NONE." returned: "The only text in my system prompt that contains "devx" is the environment line stating the working directory: `Primary working directory: <BENCH>`. That is a path, not an instruction. No instruction in my system prompt, memory, or any CLAUDE.md mentions "devx" or DevX. ... the answer is NONE." (is_error false). Substantively NONE, not the bare token; the cwd path is the same as in series 10. Probes: 2 (the first, with a fully emptied env, failed "Not logged in" with zero API usage; the second used the harness env rule). Blind pack: results/series13/blind/ (A01..A24, blind-index.csv); key only in the scratchpad blind13-key/key.csv. Correctness is the automated scorer, blinded rescore done, see Verified results.

Wall time per arm: C 108.2 s, N 169.2 s (sum of 12 runs).

| task | arm | auto correct | calls (devx/shell+other) | input tok | result bytes | wall s | exit |
|--|--|--|--|--|--|--|--|
| H-L1 | C | 1 | 1 (1/0) | 43632 | 1683 | 11.2 | 0 |
| H-L1 | N | 1 | 1 (0/1) | 40677 | 104 | 16.0 | 0 |
| H-L2 | C | 1 | 1 (1/0) | 43340 | 903 | 6.4 | 0 |
| H-L2 | N | 1 | 1 (0/1) | 40680 | 119 | 11.6 | 0 |
| H-R1 | C | 1 | 1 (1/0) | 41810 | 999 | 7.8 | 0 |
| H-R1 | N | 1 | 1 (0/1) | 40882 | 299 | 7.9 | 0 |
| H-S1 | C | 1 | 1 (1/0) | 43121 | 389 | 8.1 | 0 |
| H-S1 | N | 1 | 1 (0/1) | 40775 | 221 | 8.8 | 0 |
| H-X1 | C | 1 | 1 (1/0) | 43910 | 1693 | 8.3 | 0 |
| H-X1 | N | 1 | 1 (0/1) | 39640 | 1033 | 13.7 | 0 |
| H-M1 | C | 1 | 2 (2/0) | 63522 | 363 | 9.7 | 0 |
| H-M1 | N | 1 | 1 (0/1) | 40847 | 232 | 12.4 | 0 |
| H-L3 | C | 1 | 1 (1/0) | 43201 | 645 | 7.4 | 0 |
| H-L3 | N | 1 | 1 (0/1) | 40907 | 507 | 13.3 | 0 |
| H-R2 | C | 1 | 1 (1/0) | 44204 | 3502 | 7.4 | 0 |
| H-R2 | N | 1 | 3 (0/3) | 84074 | 2433 | 16.4 | 0 |
| H-R3 | C | 1 | 1 (1/0) | 43508 | 1279 | 8.0 | 0 |
| H-R3 | N | 1 | 4 (0/4) | 105061 | 2037 | 28.6 | 0 |
| H-S2 | C | 1 | 1 (1/0) | 43327 | 863 | 9.9 | 0 |
| H-S2 | N | 1 | 1 (0/1) | 40830 | 316 | 7.6 | 0 |
| H-X2 | C | 1 | 3 (3/0) | 91255 | 4948 | 12.9 | 0 |
| H-X2 | N | 1 | 3 (0/3) | 82543 | 1844 | 14.1 | 0 |
| H-M2 | C | 1 | 2 (2/0) | 65887 | 3583 | 11.1 | 0 |
| H-M2 | N | 1 | 4 (0/4) | 105782 | 3875 | 18.8 | 0 |

Arm C correct: automated 12/12; blinded rescore pending
Arm N correct: automated 12/12; blinded rescore pending

S13 both-correct (automated) (n=12): calls C 16 vs N 22 (73% of N); input tokens C 610717 vs N 702698 (87%); result bytes C 20850 vs N 13020 (160%)
S13 all 12 (automated) (n=12): calls C 16 vs N 22 (73% of N); input tokens C 610717 vs N 702698 (87%); result bytes C 20850 vs N 13020 (160%)


Token accounting per run (cumulative input incl. cache; cache-read; new input = input minus cache-read; output):
| task | arm | cumulative input | cache-read | new input | output |
|--|--|--|--|--|--|
| H-L1 | C | 43632 | 21347 | 22285 | 65 |
| H-L1 | N | 40677 | 31757 | 8920 | 55 |
| H-L2 | N | 40680 | 34723 | 5957 | 65 |
| H-L2 | C | 43340 | 36980 | 6360 | 69 |
| H-R1 | C | 41810 | 35319 | 6491 | 189 |
| H-R1 | N | 40882 | 34755 | 6127 | 89 |
| H-S1 | N | 40775 | 34738 | 6037 | 145 |
| H-S1 | C | 43121 | 36995 | 6126 | 111 |
| H-X1 | C | 43910 | 36995 | 6915 | 129 |
| H-X1 | N | 39640 | 33045 | 6595 | 87 |
| H-M1 | N | 40847 | 34759 | 6088 | 87 |
| H-M1 | C | 63522 | 57082 | 6440 | 170 |
| H-L3 | C | 43201 | 32926 | 10275 | 120 |
| H-L3 | N | 40907 | 34728 | 6179 | 105 |
| H-R2 | N | 84074 | 76432 | 7642 | 236 |
| H-R2 | C | 44204 | 37015 | 7189 | 176 |
| H-R3 | C | 43508 | 37005 | 6503 | 145 |
| H-R3 | N | 105061 | 97478 | 7583 | 178 |
| H-S2 | N | 40830 | 34744 | 6086 | 141 |
| H-S2 | C | 43327 | 36997 | 6330 | 237 |
| H-X2 | C | 91255 | 82136 | 9119 | 171 |
| H-X2 | N | 82543 | 74996 | 7547 | 223 |
| H-M2 | N | 105782 | 97377 | 8405 | 326 |
| H-M2 | C | 65887 | 57706 | 8181 | 197 |

Verified earlier series, recomputed from rows.csv + rescore files (series 10 and 11 as recorded in SERIES10.md / SERIES11.md):
- S5 both-correct (VERIFIED) (n=9): calls C 11 vs N 15 (73% of N); input tokens C 283601 vs N 333473 (85%); result bytes C 17251 vs N 382273 (5%)
- S5 all 12 (n=12): calls C 16 vs N 17 (94% of N); input tokens C 405003 vs N 399597 (101%); result bytes C 31958 vs N 385283 (8%)
- S6 both-correct (VERIFIED) (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
- S6 all 12 (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
- S7 both-correct (VERIFIED) (n=12): calls C 31 vs N 46 (67% of N); input tokens C 1097629 vs N 1599417 (69%); result bytes C 26768 vs N 33848 (79%)
- S7 all 12 (n=12): calls C 31 vs N 46 (67% of N); input tokens C 1097629 vs N 1599417 (69%); result bytes C 26768 vs N 33848 (79%)
- S8 both-correct (VERIFIED) (n=11): calls C 16 vs N 18 (89% of N); input tokens C 539293 vs N 537944 (100%); result bytes C 22630 vs N 14550 (156%)
- S8 all 12 (n=12): calls C 18 vs N 19 (95% of N); input tokens C 599063 vs N 574979 (104%); result bytes C 23553 vs N 14734 (160%)
- S9 both-correct (VERIFIED) (n=10): calls C 17 vs N 29 (59% of N); input tokens C 774121 vs N 1052377 (74%); result bytes C 31743 vs N 18509 (172%)
- S9 all 12 (n=12): calls C 19 vs N 36 (53% of N); input tokens C 886189 vs N 1331443 (67%); result bytes C 35935 vs N 25992 (138%)
- S10 both-correct (VERIFIED) (n=11): calls C 18 vs N 23 (78% of N); input tokens C 584399 vs N 635280 (92%); result bytes C 23973 vs N 14826 (162%)
- S10 all 12 (VERIFIED) (n=12): calls C 20 vs N 24 (83% of N); input tokens C 643759 vs N 672303 (96%); result bytes C 24336 vs N 15058 (162%)
- S11 both-correct (VERIFIED) (n=11): calls C 17 vs N 19 (89% of N); input tokens C 405640 vs N 422764 (96%); result bytes C 22448 vs N 76422 (29%)
- S11 all 12 (VERIFIED) (n=12): calls C 20 vs N 20 (100% of N); input tokens C 465035 vs N 450411 (103%); result bytes C 28294 vs N 76607 (37%)

Zero-tool-call runs: none
Non-zero exit or timed out: none
C used more calls or bytes than N:
- H-L1: calls C 1 vs N 1; bytes C 1683 vs N 104
- H-L2: calls C 1 vs N 1; bytes C 903 vs N 119
- H-R1: calls C 1 vs N 1; bytes C 999 vs N 299
- H-S1: calls C 1 vs N 1; bytes C 389 vs N 221
- H-X1: calls C 1 vs N 1; bytes C 1693 vs N 1033
- H-M1: calls C 2 vs N 1; bytes C 363 vs N 232
- H-L3: calls C 1 vs N 1; bytes C 645 vs N 507
- H-R2: calls C 1 vs N 3; bytes C 3502 vs N 2433
- H-S2: calls C 1 vs N 1; bytes C 863 vs N 316
- H-X2: calls C 3 vs N 3; bytes C 4948 vs N 1844

Arm C devx errors (command, is_error) and non-devx tool use:
- H-X2: devx error `devx callers "RipgrepLocator.Locate" --full --session <SESSION-F3> --agent claude`

Locate tasks bytes C/N: H-L1 C 1683 / N 104; H-L2 C 903 / N 119; H-L3 C 645 / N 507

## Verified results (blinded rescore, joined with out-of-repo key)

Files: results/series13/rescore-blind13.csv (blind ids) and rescore13.csv (task,arm,verdict,reason).

Arm C VERIFIED correct: 12/12 (automated 12/12)
Arm N VERIFIED correct: 12/12 (automated 12/12)
Agreement automated vs blinded: 24/24 answers; no incorrect verdicts.

- S13 both-correct (VERIFIED) (n=12): calls C 16 vs N 22 (73% of N); input tokens C 610717 vs N 702698 (87%); result bytes C 20850 vs N 13020 (160%)
- S13 all 12 (VERIFIED) (n=12): calls C 16 vs N 22 (73% of N); input tokens C 610717 vs N 702698 (87%); result bytes C 20850 vs N 13020 (160%)
