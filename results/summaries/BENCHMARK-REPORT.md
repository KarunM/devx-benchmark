# DevX agent benchmark: method, results, limitations

Prepared 2026-10-12 for a technical reviewer who has not seen this work. No model runs and no code changes were made to produce it; every number below is recomputed from the CSVs named under each table (`results/series{1..5}/rows.csv`, and `rescore.csv` for series 5 correctness).

## 1. Summary

In a 12-task held-out, read-only repository benchmark using one coding model, DevX and native grep workflows each completed 10 tasks correctly. On the eight tasks both completed correctly, DevX required 25% fewer tool calls, 12% fewer model input tokens, and 47% fewer tool-result bytes.

The eight exclude task H-R2, where the grep arm returned 358,121 B (a `rg -C 5` over a tree containing a tracked `.bak` file). With H-R2 included (nine tasks) the figures are 27%, 15% and 95% fewer.

Qualifiers: one repetition per task; one model (gpt-6-luna through Codex CLI); manual blinded scoring; read-only workflows; the C# fixture is DevX's own source. This report does not claim lower cost, general engineering superiority, or statistical significance. The tuned Series 4 result is less favourable on calls and tokens (arm C at 131% / 124% of native calls / input tokens over all 12 tasks, bytes 69%) and is given equal prominence in section 5.

Table 1.1 (source: series5 rows.csv + rescore.csv; series4 rows.csv; metric order: correctness, calls, input tokens, result bytes).

| scope | correct C / N | calls C vs N | input tokens C vs N | result bytes C vs N | C saving vs native (calls / input / bytes) |
|--|--|--|--|--|--|
| Series 5 held-out, both-correct n=8 (excl. H-R2) | 8/8 each | 9 vs 12 | 240,425 vs 271,897 | 12,701 vs 24,152 | 25.0% / 11.6% / 47.4% |
| Series 5, both-correct n=9 (incl. H-R2) | 9/9 each | 11 vs 15 | 283,601 vs 333,473 | 17,251 vs 382,273 | 26.7% / 15.0% / 95.5% |
| Series 5, all 12 tasks | 10/12 vs 10/12 | 16 vs 17 | 405,003 vs 399,597 | 31,958 vs 385,283 | 5.9% / -1.4% / 91.7% |
| Series 4 tuned, all 12 (medians, 3 reps) | 36/36 vs 33/36 | C = 131% of N | C = 124% | C = 69% | -31% / -24% / 31% |
| Series 4 tuned, both-correct n=10 | all reps | C = 120% | C = 116% | C = 48% | -20% / -16% / 52% |

A negative saving means arm C used more than native. Wall time is not reported as a headline metric.

## 2. What was measured

Arms. Arm C: the model (Codex CLI, `gpt-6-luna`) has the `devx` CLI on PATH and DevX's shipped guidance (`devx init --agents codex`, a 2,893-3,001 B AGENTS.md block, one edit: the session id) in its own CODEX_HOME. Arm N: the same model with shell only (grep/rg/sed/cat), no DevX on PATH, a CODEX_HOME without DevX guidance. Same prompt wording, same fixtures, tasks written by the project team with fixed expected strings (`tasks.json`, `tasks_heldout.json`).

Driver. `run_bench.py` drives `codex exec --json` once per (task, arm, rep) and counts tool calls from event items (`tool_calls_total` = devx + shell + mcp + other), `input_tokens` from the `turn.completed` usage, and `result_bytes` from the aggregated tool output.

Metric order everywhere: correctness, tool calls, input tokens, result bytes. Savings are quoted as a share of the native arm.

Scoring. A substring scorer produced the `correct` column in rows.csv. Series 1-4 were then hand-checked by the agent that ran them. Series 5 was additionally rescored blind (arm hidden, a separate grader session, `rescore-blind.csv`, 20/24 correct), then unblinded by the maintainer (`rescore.csv`), which overrides the scorer column. The one scorer/hand disagreement in series 5 was H-S1 arm C (scorer 1, hand and blind 0).

Sandbox history. Series 1-4: arm C ran `workspace-write` because DevX wrote search/read history to `.devx/devx.db`; arm N ran read-only. Under `-s read-only` the first arm-C trial failed 3 of 3 (exit 134, `SQLite Error 8: attempt to write a readonly database`). CS23 made history writing best-effort (diagnostic `history not recorded: ...`), after which series 5 ran both arms read-only.

Arm D dropped. An MCP arm (D) was trialled first. It used about 2.3x the input tokens of arm N (74,215 vs 31,433 mean over the 3 trial tasks). Isolation runs (`ISOLATION.md`: A0 no MCP 13,474 input tokens; with 15 MCP tools 12,971; with 1 dummy tool 12,971) showed the tool list itself adds no tokens. The doubling is inferred (not proven) to be extra model requests per MCP call (about 4-5 requests for one tool call). Arm D was dropped; its overhead belongs to the Codex MCP path, not to DevX.

## 3. Product changes (internal change-set labels CS21-CS26, one per commit)

The development branch has five commits on `f318c56`: `d9340e9`, `33b9ddf`, `df25de6`, `2f2c19d`, `04a02ef` (49 files, 5,827 insertions, 275 deletions). CS24, CS25 and CS26 guidance and features were tuned on the same 12 tasks that series 1-4 measure; series 5 is the only untouched set (section 8).

Table 3.1 (source: the maintainer's per-change implementation notes, not published).

| step | commit | motivated by | change | tests after | F2 (sympy) byte check |
|--|--|--|--|--|--|
| CS21 | d9340e9 | correctness findings from the review of an earlier candidate build | absolute in-root patch path normalised; ripgrep invoked with explicit path and closed stdin; MCP `test` forwards testFiles; one tautological test fixed | 522 | MCP text search on a copy: 20 s timeout (earlier build) to 120 ms |
| CS23 | 33b9ddf | arm-C trial: multi-hop lost on a 7,404 B whole-class read; read-only sandbox killed every `devx` call | `read type` returns an outline by default (`--full` gives the body); read guidance; best-effort history write | 531 | `read type Symbol` 7,404 to 1,216 B; Basic 9,025 to 4,288 B; M1 replay 9,596 to 3,408 B; read-only DB exit 134 to exit 0 |
| CS24 | df25de6 | series 1: agent searched before almost every `read type`, never used `callers` | shipped AGENTS.md block, `--help` and MCP descriptions teach bare names, outlines, cross-reference commands | 534 | rules block 2,342 to 2,942 B; tools/list 6,343 to 6,664 B; reads byte-identical |
| CS25 | 2f2c19d | series 2: all four `callers`/`references` calls on Python failed | text-backed Python `references`/`callers` with enclosing symbol; unindexed ripgrep hits no longer counted as unsafe paths; ripgrep killed at its 5,000-match ceiling | 548 | `references _factorint_small` 345 B; `callers _symbol` 4,923 B (44 sites); ceiling case 30 s/0 hits to 1.3 s |
| CS26 | 04a02ef | series 3: multi-hop costs one outline per hop; `callers` of a common helper is 4.9 KB | resolved `bases:` line in the outline; grouped `callers` by enclosing symbol (top 10), `--full` lists every site | 561 | Symbol outline 1,216 to 1,302 B; `callers _symbol` 4,923 to 1,068 B; `--full` byte-identical to old |

CS21 was not driven by a benchmark loss. CS23 was motivated by the arm-C trial (section 4). CS24 to CS26 each answered the previous series' largest loss. Note the cost of the CS26 bases line: +86 B on the Symbol outline.

## 4. Series 1-3 (n=1 per cell, 24 runs each)

Builds: series 1 on 33b9ddf (CS23), series 2 on df25de6 (CS24), series 3 on 2f2c19d (CS25). Fixture F2: a sympy copy (1,605 files). Source: `results/series{1,2,3}/rows.csv`; correctness is the scorer column confirmed by hand-check in each SERIESn.md (not blind-rescored).

Table 4.1, overall, C as % of N.

| series | correct C / N | calls C / N | input tok C / N | bytes C / N | C%N calls / input / bytes | both-correct subset |
|--|--|--|--|--|--|--|
| 1 | 11/12 / 11/12 | 2.17 / 1.58 | 45,066 / 34,783 | 2,308 / 2,340 | 137% / 130% / 99% | n=10: 94% / 99% / 48% |
| 2 | 12/12 / 10/12 | 1.92 / 1.17 | 42,830 / 29,480 | 2,788 / 2,237 | 164% / 145% / 125% | n=10: 131% / 124% / 97% |
| 3 | 11/12 / 10/12 | 1.50 / 1.17 | 36,622 / 29,531 | 2,118 / 3,175 | 129% / 124% / 67% | n=9: 100% / 104% / 31% |

Table 4.2, per kind, C%N (calls / input / bytes) and correct C / N.

| kind | series 1 | series 2 | series 3 |
|--|--|--|--|
| locate (3) | 100% / 103% / 35%; 3/3, 3/3 | 100% / 104% / 35%; 3/3, 3/3 | 100% / 108% / 35%; 3/3, 3/3 |
| read (3) | 60% / 76% / 17%; 3/3, 3/3 | 150% / 124% / 23%; 3/3, 2/3 | 75% / 83% / 7%; 3/3, 3/3 |
| structure (2) | 133% / 126% / 253%; 2/2, 2/2 | 100% / 113% / 591%; 2/2, 2/2 | 100% / 108% / 98%; 2/2, 2/2 |
| crossref (2) | 175% / 159% / 129%; 1/2, 2/2 | 200% / 180% / 150%; 2/2, 2/2 | 150% / 137% / 374%; 2/2, 1/2 |
| multihop (2) | 225% / 200% / 227%; 2/2, 1/2 | 233% / 199% / 151%; 2/2, 1/2 | 233% / 208% / 479%; 1/2, 1/2 |

What each series changed. Series 1 (CS23 build, no guidance): arm C searched before nearly every read and lost on structure, crossref and multihop. Series 2 (shipped guidance): the search-before-read pattern fell to 1 of 8 `read type` calls, structure ties on calls, but all four `callers`/`references` calls on Python failed, so crossref cost 4 calls against 2 and `read type --full` on Sieve returned 10,564 B. Series 3 (Python callers/references): X1 fell to 1 call and was right where N was wrong; X2 needed 2 calls (bare name ambiguous, then 4,923 B); M1 arm C was wrong after reading Boolean with `--full` (answered `to_nnf` at boolalg.py:118, expected :131). Multihop stayed the weakest kind in all three series. Over series 1-3 the arm-C losses are on calls and tokens; the byte advantage holds where grep output is wide (read, locate).

Arm-C trial (n=3, CS21 build, `TRIAL-C.md`): 3/3 correct, 125% calls, 122% input tokens, 158% bytes of N. The authors read this as mixed at best.

## 5. Series 4: tuned (CS26 build 04a02ef, 12 tasks x 2 arms x 3 reps = 72 runs)

Arm C ran workspace-write, N read-only. All 72 rows exit 0, none timed out. Source: `results/series4/rows.csv` (medians over three reps). This series is tuned: CS24-CS26 guidance and features were developed against these same tasks.

Table 5.1, per task (median calls / input tokens / result bytes; correct reps out of 3).

| task | kind | C correct | N correct | C | N |
|--|--|--|--|--|--|
| L1 | locate | 3/3 | 3/3 | 1 / 28,368 / 383 | 1 / 26,178 / 105 |
| L2 | locate | 3/3 | 3/3 | 1 / 28,297 / 287 | 1 / 27,421 / 5,810 |
| L3 | locate | 3/3 | 3/3 | 1 / 28,490 / 1,023 | 1 / 26,114 / 53 |
| R1 | read | 3/3 | 3/3 | 1 / 28,399 / 628 | 1 / 28,268 / 3,370 |
| R2 | read | 3/3 | 3/3 | 1 / 28,470 / 867 | 1 / 26,559 / 1,336 |
| R3 | read | 3/3 | 3/3 | 1 / 28,386 / 416 | 1 / 28,354 / 7,843 |
| S1 | structure | 3/3 | 3/3 | 1 / 28,639 / 1,302 | 1 / 27,579 / 1,490 |
| S2 | structure | 3/3 | 3/3 | 1 / 28,484 / 728 | 1 / 26,304 / 502 |
| X1 | crossref | 3/3 | 2/3 | 1 / 28,390 / 384 | 2 / 40,468 / 2,776 |
| X2 | crossref | 3/3 | 3/3 | 2 / 43,152 / 4,923 | 1 / 26,480 / 1,332 |
| M1 | multihop | 3/3 | 3/3 | 2 / 43,649 / 2,080 | 1 / 27,695 / 4,233 |
| M2 | multihop | 3/3 | 1/3 | 4 / 77,569 / 7,989 | 1 / 26,690 / 1,810 |

Table 5.2, per kind (mean of per-task medians).

| kind | correct C / N | calls C / N | input tok C / N | bytes C / N | C%N calls / input / bytes |
|--|--|--|--|--|--|
| locate | 9/9, 9/9 | 1.00 / 1.00 | 28,385 / 26,571 | 564 / 1,989 | 100% / 107% / 28% |
| read | 9/9, 9/9 | 1.00 / 1.00 | 28,418 / 27,727 | 637 / 4,183 | 100% / 102% / 15% |
| structure | 6/6, 6/6 | 1.00 / 1.00 | 28,562 / 26,942 | 1,015 / 996 | 100% / 106% / 102% |
| crossref | 6/6, 5/6 | 1.50 / 1.50 | 35,771 / 33,474 | 2,654 / 2,054 | 100% / 107% / 129% |
| multihop | 6/6, 4/6 | 3.00 / 1.00 | 60,609 / 27,192 | 5,034 / 3,022 | 300% / 223% / 167% |
| ALL | 36/36, 33/36 | 1.42 / 1.08 | 35,024 / 28,176 | 1,751 / 2,555 | 131% / 124% / 69% |

Both-correct lines. All three reps correct in both arms (n=10: L1 L2 L3 M1 R1 R2 R3 S1 S2 X2): calls 120%, input 116%, bytes 48% of N. Majority-of-reps both-correct (n=11, adds X1): 108% / 110% / 45%. These are the less favourable figures and they stand next to the held-out figures: arm C used more calls and more input tokens than native in this tuned series, and fewer result bytes.

Stability. Correctness did not flip in 22 of 24 (task, arm) cells. Flips were native only: M2 [0,0,1] and X1 [1,0,1]. Arm C was correct in every one of its 36 runs. Arm C's result bytes were exactly constant across reps in 7 of 12 tasks; native bytes varied widely (L2 4,617-18,679; S1 1,490-10,067). Correctness differences are 3 runs out of 36 and are not significant.

X2 and `--full`. X2 arm C's median 4,923 B is the full 44-site list for a bare name `_symbol`. The bare name is ambiguous (three definitions, rc 2, 428 B), costing one call; the agent then used the qualified name. Reps 1 and 3 added `--full`, which lists every site; the default grouped output for the same call is 1,068 B. The guidance line invited this ("pass `--full` for every site", read literally); it is a wording defect carried to the backlog.

Reviewer pushbacks recorded by the authors (SERIES4.md section 7): (1) sandbox asymmetry; (2) n=3 per cell; (3) one fixture, tasks written by the team; (4) one model; (5) `callers` is text-backed and name-based, not a resolved call graph (the 44 sites include docstring examples); (6) arm C is told which commands to use, arm N is not told to avoid anything; (7) guidance edited between series and tuned on these tasks.

## 6. Series 5: held-out (CS26 build 04a02ef, 12 unseen tasks x 2 arms x 1 rep = 24 runs, both arms read-only)

Fixtures: f2 sympy (6 tasks), f3 a copy of DevX's own C# source at 04a02ef (6 tasks, 222 indexed files). 3 locate, 3 read, 2 each of structure, crossref, multihop. Pre-flight proved arm C works with `.devx` 0555 and `devx.db` 0444 on both fixtures. All 24 rows exit 0, none timed out; fixture listings were identical before and after. Answer keys with two-way derivations: `HELDOUT-ANSWERS.md`. Source: `results/series5/rows.csv`, verdicts from `rescore.csv`.

Table 6.1, per run (calls, input tokens, result bytes; verdict is the blinded-then-unblinded rescoring).

| task | kind | fx | arm | verdict | calls | input tok | bytes |
|--|--|--|--|--|--|--|--|
| H-L1 | locate | f2 | C | correct | 1 | 28,345 | 1,762 |
| H-L1 | locate | f2 | N | correct | 1 | 27,442 | 813 |
| H-L2 | locate | f2 | C | correct | 1 | 28,072 | 982 |
| H-L2 | locate | f2 | N | correct | 1 | 26,122 | 64 |
| H-L3 | locate | f3 | C | correct | 1 | 27,955 | 724 |
| H-L3 | locate | f3 | N | correct | 1 | 26,188 | 304 |
| H-R1 | read | f2 | C | correct | 1 | 28,185 | 1,150 |
| H-R1 | read | f2 | N | correct | 1 | 26,747 | 1,808 |
| H-R2 | read | f3 | C | correct | 2 | 43,176 | 4,550 |
| H-R2 | read | f3 | N | correct | 3 | 61,576 | 358,121 |
| H-R3 | read | f3 | C | correct | 1 | 28,140 | 1,494 |
| H-R3 | read | f3 | N | correct | 2 | 41,926 | 3,572 |
| H-S1 | structure | f2 | C | incorrect | 1 | 27,957 | 468 |
| H-S1 | structure | f2 | N | incorrect | 0 | 13,018 | 0 |
| H-S2 | structure | f3 | C | correct | 1 | 28,041 | 942 |
| H-S2 | structure | f3 | N | correct | 1 | 26,226 | 403 |
| H-X1 | crossref | f2 | C | correct | 1 | 28,470 | 1,772 |
| H-X1 | crossref | f2 | N | correct | 3 | 54,704 | 2,636 |
| H-X2 | crossref | f3 | C | correct | 4 | 79,587 | 14,239 |
| H-X2 | crossref | f3 | N | incorrect | 1 | 26,793 | 2,555 |
| H-M1 | multihop | f2 | C | incorrect | 0 | 13,858 | 0 |
| H-M1 | multihop | f2 | N | correct | 1 | 26,313 | 455 |
| H-M2 | multihop | f3 | C | correct | 2 | 43,217 | 3,875 |
| H-M2 | multihop | f3 | N | correct | 2 | 42,542 | 14,552 |

Table 6.2, per kind (3 locate, 3 read, 2 each other).

| kind | correct C / N | calls C / N | input tok C / N | bytes C / N | C%N calls / input / bytes | series 4 C%N |
|--|--|--|--|--|--|--|
| locate | 3/3, 3/3 | 1.00 / 1.00 | 28,124 / 26,584 | 1,156 / 394 | 100% / 106% / 294% | 100% / 107% / 28% |
| read | 3/3, 3/3 | 1.33 / 2.00 | 33,167 / 43,416 | 2,398 / 121,167 | 67% / 76% / 2% | 100% / 102% / 15% |
| structure | 1/2, 1/2 | 1.00 / 0.50 | 27,999 / 19,622 | 705 / 202 | 200% / 143% / 350% | 100% / 106% / 102% |
| crossref | 2/2, 1/2 | 2.50 / 2.00 | 54,028 / 40,748 | 8,006 / 2,596 | 125% / 133% / 308% | 100% / 107% / 129% |
| multihop | 1/2, 2/2 | 1.00 / 1.50 | 28,538 / 34,428 | 1,938 / 7,504 | 67% / 83% / 26% | 300% / 223% / 167% |
| ALL | 10/12, 10/12 | 1.33 / 1.42 | 33,750 / 33,300 | 2,663 / 32,107 | 94% / 101% / 8% | 131% / 124% / 69% |

Table 6.3, per fixture.

| fixture | correct C / N | calls C vs N | input tok C vs N | bytes C vs N | C%N calls / input / bytes |
|--|--|--|--|--|--|
| f2 sympy | 4/6, 5/6 | 5 vs 7 | 154,887 vs 174,346 | 6,134 vs 5,776 | 71% / 89% / 106% |
| f3 C# | 6/6, 5/6 | 11 vs 10 | 250,116 vs 225,251 | 25,824 vs 379,507 | 110% / 111% / 7% |

Both-correct subsets are in Table 1.1 (n=9: H-L1 H-L2 H-L3 H-M2 H-R1 H-R2 H-R3 H-S2 H-X1; n=8 removes H-R2).

The four wrong answers (`rescore.csv`). H-M1 arm C: answered with no tool call and named `CCodePrinter` at codeprinter.py:24; the real base is `CodePrinter` at :53. H-S1 arm C: listed `__init__`, `__repr__`, `__getitem__`, violating the "no underscore names" constraint (scorer said correct; hand and blind said incorrect). H-S1 arm N: stated it could not access files with shell tools and made no call, no answer. H-X2 arm N: labelled Program.cs:1272 "top-level program code"; the site is inside `DoctorAsync`, which it did not name. Two of the four are zero-tool-call runs (H-M1 C, H-S1 N): model behaviour, not tool effect. A minor note: H-M2 arm N's two names were right but its link line numbers were off (96/102 vs 101/107); lines were not asked.

C# `callers` failure and fallback. On H-X2 arm C, `callers "DevX.Infrastructure.Storage.SQLite.RipgrepLocator.Locate" --full` failed rc 1: `error: Method '...' matched multiple implementations.` The agent had already run `references` (11,883 B), then used `search symbol` and `search text`, and answered correctly. Cost: 4 calls and 14,239 B against native's 1 call and 2,555 B, the clearest arm-C loss in the series (400% calls). Separately, C# `callers` over-reports: for `RequireSessionAsync` it returned all 15 methods of `SqliteSessionStore` (2,127 B) where 6 are real callers; the agent filtered by name, hiding the effect. This also occurs on the pre-branch binary.

The grep outlier. H-R2 arm N returned 358,121 B from one `rg -C 5` run over `.` including a tracked `Program.cs.bak`. That single result is why read-kind bytes are 2% of N and why the all-12 byte saving is 91.7%. It is excluded from the headline for that reason; Table 1.1 gives both with and without it.

Where arm C was not better here: input tokens over all 12 tasks (101% of native), single-line locate bytes (294%), structure and crossref calls, and the f3 fixture on calls and input tokens (110% / 111%). The series-4 call and token deficit did not reproduce on calls (94%), but with n=2-3 per kind and two zero-call runs the per-kind figures are noise.

## 7. Failures and known defects

- C# `callers` on an overloaded method fails with `matched multiple implementations` (rc 1; `ProtocolEngine.cs:322`, matches at `:265`). Observed in series 5 H-X2. Pre-existing; not fixed.
- C# `callers` over-reports (every method of a file listed as caller). Pre-existing: identical on the d9340e9 binary. Not fixed.
- Python text-backed `callers` counts doctest `>>>` lines as calls, and does not detect `#` inside strings or multi-line docstring bodies (CS25 change notes). The 44 sites for `_symbol` in series 3 and 4 include these.
- `--full` guidance wording read literally leads the agent to list every site (series 4 X2, 2 of 3 reps; series 5 H-X1 used `callers --full` and was correct in 1 call at 1,772 B). Backlog item.
- Locate and structure byte losses: `search symbol` returns 383-1,762 B where `grep -n` returns 53-813 B for a single-line locate question (series 4 L1 383 vs 105, L3 1,023 vs 53; series 5 H-L2 982 vs 64). Backlog item: exact-match-first, cap candidates.
- Multihop in the tuned series: 300% calls, 223% input tokens, 167% bytes of native (one outline per hop; CS26 added `bases:` to reduce this, and series 4 still shows M2 at 4 calls against 1).
- The CS25 tests were not strictly red-first (the pre-change behaviour was shown by the baseline binary), as recorded in the unpublished change notes.
- Codex harness limits that shaped the method: the sandbox used for development kills commands over about 2-3 minutes and denies process listing, so long runs were driven from a separate session; `--model gpt-6-luna` must be passed; under `-s read-only` early DevX builds crashed on history writes (fixed in CS23).
- Packaging item: the tracked `src/DevX.Cli/Program.cs.bak` had to be excluded from packaging.

## 8. Limitations and what would strengthen the evidence

- Repetitions: series 5 is one run per cell. Differences of one or two tasks (10 vs 10) carry no significance; series 4 with three reps shows native flipping on 2 of 12 tasks.
- One model. A second model, and a second agent harness, would test whether the effect is DevX or this model's particular tool habits (two zero-call runs show how much model behaviour moves a cell).
- Fixtures. Six of the twelve held-out tasks use DevX's own C# source, which DevX indexes and its authors know; a neutral third-party C# repository is needed. Series 1-4 use one Python fixture.
- Authorship. Tasks, answer keys, scorer strings and the guidance under test were written by the same team; independent task authorship, and independent blind scoring beyond series 5, are missing.
- Scoring. Series 1-4 correctness is substring plus same-agent hand-check, not blind.
- Cost. Tokens and bytes are proxies; no price accounting, cached-token adjustment, or wall time is reported. Fixed input of about 26,000 tokens per run (prompt and guidance) dominates the token totals, so byte savings barely move them.
- Read-only workflows only: no editing, patching or build tasks were measured.
- Held-out status. Series 5 was held-out only for the CS26 build. The product is now frozen at 04a02ef; any rerun of `tasks_heldout.json` after later product changes (backlog: the C# overload and over-reporting defects, `search symbol` result size, `--full` wording, doctest lines) is a regression set, not held-out. A new task set is required for a further held-out claim.

## 9. Multi-model held-out comparison (series 6-9)

Same 12 held-out tasks, same DevX build (1.7.0 = 04a02ef), read-only workflows, one repetition per cell, 24 runs per series. Figures recomputed from `results/series{5,6,7,8,9}/rows.csv` joined with the verified verdicts `rescore.csv`, `results/series6/rescore6.csv`, `rescore7.csv`, `rescore8.csv`, `rescore9.csv`. Ratios are DevX divided by native on tasks both arms answered correctly (below 100% means DevX used less). Facts anchored as F-MM-1 to F-MM-13 in `FACTS.md`. Per-series notes: `SERIES6.md`, `SERIES7.md`, `SERIES8.md`, `SERIES9.md`.

| Series | Model, harness | Correct C / N | n | Calls | Input tokens | Result bytes |
|--|--|--|--|--|--|--|
| 5 | gpt-6-luna, Codex CLI 0.155.1 | 10/12 · 10/12 | 9 (incl. outlier) | 11 vs 15 (73%) | 283,601 vs 333,473 (85%) | 17,251 vs 382,273 (5%) |
| 6 | gpt-5.6-luna, Codex CLI | 12/12 · 12/12 | 12 | 22 vs 20 (110%) | 438,875 vs 423,045 (104%) | 42,090 vs 1,167,598 (4%) |
| 7 | deepseek-flash (DeepSeek-V4.1-Flash), Codex CLI via provider overrides | 12/12 · 12/12 | 12 | 19 vs 34 (56%) | 1,097,629 vs 1,599,417 (69%) | 26,768 vs 33,848 (79%) |
| 8 | claude-sonnet-5-5, Claude Code 2.1.296 | 12/12 · 11/12 | 11 | 16 vs 18 (89%) | 539,293 vs 537,944 (100%) | 22,630 vs 14,550 (156%) |
| 9 | claude-sonnet-5, Claude Code 2.1.296 | 12/12 · 10/12 | 10 | 17 vs 29 (59%) | 774,121 vs 1,052,377 (74%) | 31,743 vs 18,509 (172%) |

All-12 lines (calls, tokens, bytes as C vs N percentage): series 5 94% / 101% / 8%; series 6 110% / 104% / 4%; series 7 56% / 69% / 79%; series 8 95% / 104% / 160%; series 9 53% / 67% / 138%. Series 7 calls exclude the "Model metadata not found" pseudo-call the parser counts once per run (SERIES7.md).

Verified lines and agreement between the automated scorer and the blinded rescore: series 6, 24/24 agree; series 7, 24/24; series 8, 23/24 after rulings; series 9, 23/24 after rulings (series 5: 23/24, H-S1 arm C).

Rulings: series 8 H-M1 arm N, rescorer "incorrect" upheld (answers C89CodePrinter as the class, CodePrinter only as chain context). Series 9 H-M1 arm N overridden to correct (asked elements right; wrong line on the unasked intermediate class immaterial); H-X1 arm N incorrect upheld (swapped callers, mid-answer retraction); H-R2 arm N incorrect upheld (final message was a background-search status line; kept as a failed row, not rerun).

Aggregate verified correctness, series 5-9: DevX 58/60, native 55/60. DevX misses: series 5 H-M1 (zero calls), series 5 H-S1. Native misses: series 5 H-S1 (refused, zero calls), series 5 H-X2, series 8 H-M1, series 9 H-R2, series 9 H-X1.

Harness and isolation: series 5-7 use Codex CLI 0.155.1 with reasoning effort `medium` in force (for deepseek-flash the provider lists low/high/max, so whether `medium` is honoured is unknown); series 8-9 use Claude Code 2.1.296 headless with Bash/Read/Grep/Glob allowed and Edit/Write/NotebookEdit disallowed, effort left at the default. `--setting-sources project,local` alone did not exclude the global instructions that mention DevX; with CLAUDE_CODE_DISABLE_CLAUDE_MDS=1, CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 and CLAUDE*/ANTHROPIC* environment variables dropped, the native-arm probe answered NONE. Fixture listings with checksums were identical before and after every series.

Caveats: one repetition per cell; the twelve tasks are reused across all five series (a regression set, not a generalisation set); harness differs for series 8-9; DeepSeek input tokens carry about 73k uncached baseline per run; reasoning effort is not controlled across models; Claude Code Read and Grep return bounded output; the C# `callers` defect on `RipgrepLocator.Locate` (H-X2) failed in arm C in series 5, 7, 8 and 9 and was recovered by `search text` each time (a product defect, not a failed task); the series 9 native H-R2 final message was a background-search status line.

Paid and plan-run accounting: 238 runs on the Codex path in total; Claude Code 48 benchmark runs plus 4 probes.

What changed in the interpretation: the calls win depends on the model's native search style. Models that navigate through several small searches (deepseek-flash, claude-sonnet-5) gave DevX the largest call and token reductions; gpt-5.6-luna, which usually answers in one shell command, made DevX cost slightly more calls and tokens. The bytes win depends on the harness: on the Codex shell native commands print whatever they match (up to about 1 MB), so DevX returned a few percent of the bytes, while Claude Code's Read and Grep already return bounded output and DevX returned more bytes (156% and 172%). Correctness is the consistent result: DevX matched or exceeded the native arm in every configuration (58/60 against 55/60).

## 10. Appendix

Paid run accounting (Codex runs): 8 (trial 6 + 2 smoke) + 4 (isolation) + 3 (arm-C trial attempt 1, blocked by read-only sandbox, unusable) + 3 (arm-C trial attempt 2) + 24 (series 1) + 24 (series 2) + 24 (series 3) + 72 (series 4) + 24 (series 5) = 186.

Test suite per commit (with and without ripgrep, both green): d9340e9 522; 33b9ddf 531; df25de6 534; 2f2c19d 548; 04a02ef 561. Both CS26 TRX files report 561 results and zero failed.

File index (paths relative to the original working tree):
- Per-series reports: `SERIES1.md`, `SERIES2.md`, `SERIES3.md`, `SERIES4.md`, `SERIES5.md`; trials `TRIAL.md`, `TRIAL-C.md`; `ISOLATION.md`.
- Data: `results/series1..5/rows.csv`; `rescore.csv` (unblinded), `rescore-blind.csv` (blind, 20/24); per-run command lists `results/seriesN/tables.txt`, `*.cmds.json`, `*.answer.txt`.
- Tasks and keys: `tasks.json`, `tasks_heldout.json`, `HELDOUT-ANSWERS.md`; driver `run_bench.py`, `run_series4.sh`, `run_series5.sh`, `make_series{,2,3,4,5}.py`, `make_heldout.py`, `iso_run.py`.
- Guidance under test: `codex_home_c/AGENTS.md`, `codex_home_c3/AGENTS.md`.
- Product changes: per-change implementation notes and test result files exist in the maintainer's working tree and are not published.

Self-review of the summary numbers (least certain three). (1) 11.6% and 47.4% against the maintainer's 12% and 47%: recomputed from rows.csv for the eight both-correct tasks with the rescore.csv verdicts (calls 9 vs 12, input 240,425 vs 271,897, bytes 12,701 vs 24,152); rounding to whole percent matches the sentence. (2) Series 4 both-correct n=10 at 120% / 116% / 48%: recomputed from per-task medians in rows.csv and equal to SERIES4.md. (3) The 186 run total: summed from the per-step run-count records (6+2, 4, 3, 3, 24x3, 72, 24).
