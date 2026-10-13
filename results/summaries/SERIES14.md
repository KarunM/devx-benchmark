# Series 14: held-out 12 tasks on Qwen3.6-27B (fp8) via DeepInfra through Codex

Admitted to the evidence set (maintainer decision 2026-10-12); see FACTS.md F-FM-*.

Model `Qwen/Qwen3.6-27B` (DeepInfra, fp8, 262k context, $0.32/M in, $3.20/M out), passed with `-m` to both arms; run-1 jsonl/rows.csv carry that id. Provider via `-c` overrides only: `model_provider="deepinfra"`, `model_providers.deepinfra.name="DeepInfra"`, `.base_url="https://api.deepinfra.com/v1/openai"`, `.env_key="DEEPINFRA_API_KEY"`, `.wire_api="responses"`; key loaded by `--env-file` from outside the repo, never logged. Per-run argv: `codex exec -m Qwen/Qwen3.6-27B --json -C <fixture> --skip-git-repo-check -s read-only --ephemeral -o <answer> -c ... <prompt>`; arm C CODEX_HOME=codex_home_c (shipped AGENTS.md, clibin on PATH), arm N codex_home. Driver: `run_bench.py --series series14 --tasks all --tasks-file tasks_heldout.json --arm CN --codex-home-c codex_home_c --sandbox-c read-only --env-file ... --model Qwen/Qwen3.6-27B --timeout 300 --codex-config ...` (script run_series14.sh). Reasoning effort: codex config `medium` (not sent as a provider-tuned setting; thinking mode untouched; usage reports reasoning_output_tokens 0 in every probe). DevX: clibin, same as series 5-13 (1.6.14+04a02ef). Fixture listings with sha256 before/after identical (f2, f3). Blind pack: results/series14/blind/ (A01..A24, blind-index.csv); key only in scratchpad blind14-key. Correctness below is the automated scorer, blinded rescore pending.

Probes (2 of 3 allowed): (1) "Reply with the single word ok." rc 0, text "ok", usage 25308 in / 19 out; (2) "Run `ls` and report the first entry." rc 0, one command_execution, answer "The first entry is `R.md`.", 51174 in / 76 out. Both emit a "Model metadata for `Qwen/Qwen3.6-27B` not found" warning (counted by parse() as an `other` item, excluded from calls here) and a cosmetic "failed to refresh available models" decode error.

Trial (6 runs, tasks H-L1,H-R1,H-S2 both arms, gate: >=4/6 automated-correct and <=1 harness failure): 6/6 correct, 0 harness failures, gate PASS.

| run | correct | calls | input tok | wall s |
|--|--|--|--|--|
| H-L1-C-r1 | 1 | 1 | 52949 | 15.9 |
| H-L1-N-r1 | 1 | 1 | 51360 | 9.4 |
| H-R1-N-r1 | 1 | 6 | 227341 | 52.8 |
| H-R1-C-r1 | 1 | 1 | 52768 | 8.9 |
| H-S2-C-r1 | 1 | 1 | 53794 | 10.2 |
| H-S2-N-r1 | 1 | 1 | 51995 | 9.7 |

Wall time arm C: 136.7 s (sum of 12 runs)
Arm C correct: automated 12/12; blinded rescore pending
Wall time arm N: 198.6 s (sum of 12 runs)
Arm N correct: automated 9/12; blinded rescore pending

| task | arm | auto correct | calls (devx/shell) | input tok | result bytes | wall s | exit |
|--|--|--|--|--|--|--|--|
| H-L1 | C | 1 | 1 (1/0) | 52932 | 1762 | 13.8 | 0 |
| H-L1 | N | 1 | 1 (0/1) | 51202 | 1323 | 7.0 | 0 |
| H-L2 | C | 1 | 1 (1/0) | 52714 | 982 | 6.6 | 0 |
| H-L2 | N | 1 | 1 (0/1) | 50719 | 120 | 6.4 | 0 |
| H-R1 | C | 1 | 1 (1/0) | 52737 | 1078 | 8.5 | 0 |
| H-R1 | N | 1 | 2 (0/2) | 79085 | 5229 | 10.4 | 0 |
| H-S1 | C | 1 | 1 (1/0) | 53350 | 3181 | 9.7 | 0 |
| H-S1 | N | 0 | 0 (0/0) | 76169 | 0 | 29.7 | 0 |
| H-X1 | C | 1 | 1 (1/0) | 52688 | 769 | 11.4 | 0 |
| H-X1 | N | 1 | 4 (0/4) | 128767 | 780 | 17.6 | 0 |
| H-M1 | C | 1 | 2 (2/0) | 81099 | 4864 | 11.9 | 0 |
| H-M1 | N | 0 | 0 (0/0) | 50706 | 0 | 17.7 | 0 |
| H-L3 | C | 1 | 1 (1/0) | 52598 | 724 | 7.3 | 0 |
| H-L3 | N | 1 | 3 (0/3) | 101997 | 508 | 13.7 | 0 |
| H-R2 | C | 1 | 2 (2/0) | 106828 | 4790 | 13.4 | 0 |
| H-R2 | N | 1 | 3 (0/3) | 130342 | 6490 | 28.2 | 0 |
| H-R3 | C | 1 | 1 (1/0) | 52723 | 1358 | 7.8 | 0 |
| H-R3 | N | 1 | 3 (0/3) | 106580 | 11302 | 12.3 | 0 |
| H-S2 | C | 1 | 1 (1/0) | 52689 | 942 | 10.1 | 0 |
| H-S2 | N | 1 | 2 (0/2) | 78369 | 7239 | 11.3 | 0 |
| H-X2 | C | 1 | 4 (4/0) | 166012 | 15244 | 23.1 | 0 |
| H-X2 | N | 0 | 6 (0/6) | 183215 | 6072 | 19.7 | 0 |
| H-M2 | C | 1 | 2 (2/0) | 80220 | 3875 | 13.1 | 0 |
| H-M2 | N | 1 | 6 (0/6) | 181857 | 2529 | 24.6 | 0 |

S14 both-correct (automated) (n=9): calls C 11 vs N 25 (44% of N); input tokens C 556129 vs N 908918 (61%); result bytes C 16280 vs N 35520 (46%)
S14 all 12 (automated) (n=12): calls C 18 vs N 31 (58% of N); input tokens C 856590 vs N 1219008 (70%); result bytes C 39569 vs N 41592 (95%)

Token accounting per run (DeepInfra reports no cached tokens: cache-read 0, so new input = cumulative input; output):
| task | arm | cumulative input | cache-read | new input | output |
|--|--|--|--|--|--|
| H-L1 | C | 52932 | 0 | 52932 | 163 |
| H-L1 | N | 51202 | 0 | 51202 | 162 |
| H-L2 | C | 52714 | 0 | 52714 | 164 |
| H-L2 | N | 50719 | 0 | 50719 | 134 |
| H-R1 | C | 52737 | 0 | 52737 | 307 |
| H-R1 | N | 79085 | 0 | 79085 | 388 |
| H-S1 | C | 53350 | 0 | 53350 | 389 |
| H-S1 | N | 76169 | 0 | 76169 | 358 |
| H-X1 | C | 52688 | 0 | 52688 | 533 |
| H-X1 | N | 128767 | 0 | 128767 | 738 |
| H-M1 | C | 81099 | 0 | 81099 | 382 |
| H-M1 | N | 50706 | 0 | 50706 | 273 |
| H-L3 | C | 52598 | 0 | 52598 | 172 |
| H-L3 | N | 101997 | 0 | 101997 | 317 |
| H-R2 | C | 106828 | 0 | 106828 | 384 |
| H-R2 | N | 130342 | 0 | 130342 | 807 |
| H-R3 | C | 52723 | 0 | 52723 | 269 |
| H-R3 | N | 106580 | 0 | 106580 | 454 |
| H-S2 | C | 52689 | 0 | 52689 | 283 |
| H-S2 | N | 78369 | 0 | 78369 | 432 |
| H-X2 | C | 166012 | 0 | 166012 | 1002 |
| H-X2 | N | 183215 | 0 | 183215 | 689 |
| H-M2 | C | 80220 | 0 | 80220 | 418 |
| H-M2 | N | 181857 | 0 | 181857 | 1027 |

Verified earlier series (copied from SERIES13.md):
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
- S13 both-correct (VERIFIED) (n=12): calls C 16 vs N 22 (73% of N); input tokens C 610717 vs N 702698 (87%); result bytes C 20850 vs N 13020 (160%)
- S13 all 12 (VERIFIED) (n=12): calls C 16 vs N 22 (73% of N); input tokens C 610717 vs N 702698 (87%); result bytes C 20850 vs N 13020 (160%)

Zero-tool-call (zero counted calls) runs: H-S1-N, H-M1-N
- H-S1-N: a command was started (`/bin/zsh -lc 'find / -path "*/sympy/series/gruntz.py" 2>/dev/null'`, no completion event, so the parser counted 0 calls and 0 bytes) and the model then answered from memory without file evidence; automated correct=0
- H-M1-N: a command was started (`/bin/zsh -lc 'find / -path "*/sympy/printing/c.py" 2>/dev/null'`, no completion event, so the parser counted 0 calls and 0 bytes) and the model then answered from memory without file evidence; automated correct=0
Empty-answer runs: none
Non-zero exit or timed out: none

C used more calls or bytes than N:
- H-L1: calls C 1 vs N 1; bytes C 1762 vs N 1323
- H-L2: calls C 1 vs N 1; bytes C 982 vs N 120
- H-S1: calls C 1 vs N 0; bytes C 3181 vs N 0
- H-M1: calls C 2 vs N 0; bytes C 4864 vs N 0
- H-L3: calls C 1 vs N 3; bytes C 724 vs N 508
- H-X2: calls C 4 vs N 6; bytes C 15244 vs N 6072
- H-M2: calls C 2 vs N 6; bytes C 3875 vs N 2529

Arm C devx non-zero exits and non-devx shell fallbacks (task, command, exit):
- H-X2: devx callers "RipgrepLocator.Locate" --session <SESSION-F3> --agent codex --full' (exit 1)

Locate tasks bytes C/N: H-L1 C 1762 / N 1323; H-L2 C 982 / N 120; H-L3 C 724 / N 508

Approximate spend (series): 2075598 input tok x $0.32/M + 10245 output tok x $3.20/M = $0.697 (trial + 2 probes add roughly $0.05).

## Verified results (blinded rescore, joined with out-of-repo key)

Files: results/series14/rescore-blind14.csv (blind ids) and rescore14.csv (task,arm,verdict,reason).

Arm C VERIFIED correct: 11/12 (automated 12/12)
Arm N VERIFIED correct: 9/12 (automated 9/12)
Agreement automated vs blinded: 23/24 answers.
- Disagreement H-X1 arm C: automated correct, blind incorrect
- Final classification (R-1): H-X1 arm C is INCORRECT. The blinded rescore is the authoritative scorer (FREEZE section 5); the answer lists a non-existent function `limit` as a caller because DevX's text-backed `callers` reported four module-docstring lines (gruntz.py:78,102,108,111) as module-level call sites. The 11/12 vs 9/12 above already uses this adjudicated result.
Incorrect (blind): H-S1 N, H-X1 C, H-M1 N, H-X2 N

- S14 both-correct (VERIFIED) (n=8): calls C 10 vs N 21 (48% of N); input tokens C 503441 vs N 780151 (65%); result bytes C 15511 vs N 34740 (45%)
- S14 all 12 (VERIFIED) (n=12): calls C 18 vs N 31 (58% of N); input tokens C 856590 vs N 1219008 (70%); result bytes C 39569 vs N 41592 (95%)
