# Series 7: held-out 12 tasks on DeepSeek Flash 4.1 via Codex provider

Admitted to the evidence set (2026-10-12); see results/summaries/FACTS-benchmark.md

Model: `deepseek-flash` (api.deepseek.com/models listed `deepseek-flash`, `deepseek-v4-pro`; metadata names it DeepSeek-V4.1-Flash), passed with `-m` to both arms. Provider via `-c` overrides only: `model_provider="deepseek"`, base_url `https://api.deepseek.com`, `env_key="DEEPSEEK_API_KEY"`, `wire_api="responses"` (`chat` is rejected by codex 0.155.1; probe 1 failed locally with no API call, probe 2 returned "ok", rc 0). Key read from the env file at run time, never written here. Reasoning effort: codex printed `medium` (from config.toml), but DeepSeek lists supported levels low/high/max, so whether `medium` is honoured is unknown. Run 1 jsonl and stderr name `deepseek-flash`, not gpt-6-luna. Same DevX binary and guidance as series 5/6. 24 runs, all exit 0. F2/F3 listings before/after identical. Blind pack: `results/series7/blind/`; key outside the repo. Verified correctness comes from an independent blinded rescore (`results/series7/rescore-blind7.csv`, joined with the out-of-repo key into `results/series7/rescore7.csv`): 24/24 correct, agreement with the automated scorer 24/24. Rescorer's immaterial deviations (all rated correct): A04 (H-R2, arm C) fence/zero_blocks line numbers slightly off; A03 (H-M2, arm N) and A07 (H-M2, arm C) RequireSessionAsync line 181 vs 182; A18 (H-R3, arm N) catch lines 119-121 vs derivation 115-117 (maintainer note: H-R3 asks only for exception types, so line numbers do not affect the verdict).

Calls here exclude the codex "Model metadata for deepseek-flash not found" warning, which parse() counts as an `other` item in tool_calls_total (rows.csv totals are 1 higher per run; input tokens include a ~73k baseline per run, so S7 token figures are not comparable to S5/S6).

Provider-specific tool-call failures: none (no malformed calls, no refusals). Stderr carries a repeated "failed to refresh available models" decode error (cosmetic). H-R2 arm C's two `cd <fixture> && devx ...` commands are counted as shell by the parser although they are devx calls.

S7 both-correct (verified) (n=12): calls C 19 vs N 34 (56% of N); input tokens C 1097629 vs N 1599417 (69%); result bytes C 26768 vs N 33848 (79%)
S7 all 12 (n=12): calls C 19 vs N 34 (56% of N); input tokens C 1097629 vs N 1599417 (69%); result bytes C 26768 vs N 33848 (79%)
S7 verified correctness (blinded rescore, rescore7.csv): C 12/12, N 12/12; automated scorer: C 12/12, N 12/12; agreement 24/24

S5 both-correct (verified) (n=9): calls C 11 vs N 15 (73% of N); input tokens C 283601 vs N 333473 (85%); result bytes C 17251 vs N 382273 (5%)
S5 all 12 (n=12): calls C 16 vs N 17 (94% of N); input tokens C 405003 vs N 399597 (101%); result bytes C 31958 vs N 385283 (8%)
S5 verified correctness: C 10/12, N 10/12

S6 both-correct (verified) (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
S6 all 12 (n=12): calls C 22 vs N 20 (110% of N); input tokens C 438875 vs N 423045 (104%); result bytes C 42090 vs N 1167598 (4%)
S6 verified correctness: C 12/12, N 12/12

| task | arm | auto correct | calls (devx/shell) | input tok | result bytes | wall s | exit |
|--|--|--|--|--|--|--|--|
| H-L1 | C | 1 | 1 (1/0) | 75482 | 1762 | 12.1 | 0 |
| H-L1 | N | 1 | 1 (0/1) | 73607 | 902 | 4.6 | 0 |
| H-L2 | C | 1 | 1 (1/0) | 75252 | 982 | 5.0 | 0 |
| H-L2 | N | 1 | 1 (0/1) | 73275 | 64 | 6.3 | 0 |
| H-R1 | C | 1 | 1 (1/0) | 75294 | 1078 | 4.8 | 0 |
| H-R1 | N | 1 | 3 (0/3) | 111686 | 3806 | 16.6 | 0 |
| H-S1 | C | 1 | 1 (1/0) | 75125 | 468 | 4.5 | 0 |
| H-S1 | N | 1 | 3 (0/3) | 149508 | 2671 | 7.3 | 0 |
| H-X1 | C | 1 | 1 (1/0) | 75729 | 1884 | 5.5 | 0 |
| H-X1 | N | 1 | 5 (0/5) | 224673 | 2532 | 11.7 | 0 |
| H-M1 | C | 1 | 2 (2/0) | 114560 | 4864 | 7.2 | 0 |
| H-M1 | N | 1 | 2 (0/2) | 110364 | 145 | 6.1 | 0 |
| H-L3 | C | 1 | 1 (1/0) | 75129 | 724 | 5.2 | 0 |
| H-L3 | N | 1 | 2 (0/2) | 110170 | 345 | 5.5 | 0 |
| H-R2 | C | 1 | 2 (0/2) | 114452 | 4272 | 8.0 | 0 |
| H-R2 | N | 1 | 4 (0/4) | 148442 | 2992 | 8.1 | 0 |
| H-R3 | C | 1 | 1 (1/0) | 75311 | 1358 | 4.5 | 0 |
| H-R3 | N | 1 | 2 (0/2) | 111232 | 3097 | 6.0 | 0 |
| H-S2 | C | 1 | 1 (1/0) | 73705 | 942 | 4.5 | 0 |
| H-S2 | N | 1 | 2 (0/2) | 75261 | 7864 | 4.8 | 0 |
| H-X2 | C | 1 | 3 (3/0) | 113890 | 3361 | 7.1 | 0 |
| H-X2 | N | 1 | 5 (0/5) | 224972 | 3891 | 12.9 | 0 |
| H-M2 | C | 1 | 4 (4/0) | 153700 | 5073 | 9.5 | 0 |
| H-M2 | N | 1 | 4 (0/4) | 186227 | 5539 | 10.2 | 0 |

Zero-tool-call runs: none

C used more calls or bytes than N:
- H-L1: calls C 1 vs N 1; bytes C 1762 vs N 902
- H-L2: calls C 1 vs N 1; bytes C 982 vs N 64
- H-M1: calls C 2 vs N 2; bytes C 4864 vs N 145
- H-L3: calls C 1 vs N 2; bytes C 724 vs N 345
- H-R2: calls C 2 vs N 4; bytes C 4272 vs N 2992

Arm C devx non-zero exits and grep/sed/cat/find fallbacks (task, command, exit); H-X2 `devx callers` exit 1 was 'Method RipgrepLocator.Locate was not found' (devx error), the agent then used search text; every devx call also printed 'history not recorded: SQLite readonly':
- H-R2: cd <F3> && devx read method "SearchReplaceBlockParser.Parse" --session <SESSION-F3> (exit 0)
- H-R2: cd <F3> && devx search text "zero_blocks" --session <SESSION-F3> --agent codex (exit 0)
- H-X2: devx callers "RipgrepLocator.Locate" --session <SESSION-F3> --agent codex (exit 1)
