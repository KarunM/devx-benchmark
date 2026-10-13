# SERIES5 - held-out run: 12 unseen tasks x arms C and N x 1 rep (24 paid Codex runs, gpt-6-luna), CS26 build 1.6.14+04a02ef

Both arms read-only (`-s read-only`). Arm C: `clibin` on PATH, `codex_home_c` (f2) / `codex_home_c3` (f3) AGENTS.md, reduced preamble. Fixtures f2 = sympy (6 tasks), f3 = DevX C# copy at 04a02ef (6 tasks). Pre-flight: arm C read-only viability proven first (with `.devx` 0555 and `devx.db` 0444, `devx read method` exited 0 with the body on stdout on f2 and f3; stderr: `history not recorded: SQLite Error 8: 'attempt to write a readonly database'`); modes restored to 0755/0644. `devx index status` Current on both (f2 1605 files, f3 222). All 24 rows exit 0, 0 timeouts. F2/F3 file listings before/after identical (`.devx/` excluded). Raw data: `results/series5/rows.csv`, `*.cmds.json`, `*.answer.txt`, `tables.md`. Deviation from the planned command: `--codex-home-c codex_home_c` was added (without it arm C on f2 would have run with `codex_home`, which has no AGENTS.md; series 4 used it). n=1 per cell; every ratio below uses HAND-CHECKED correctness (scorer is substring-based).

## Per-run table (24 rows)
| task | kind | fx | arm | sandbox | scorer | manual | calls (devx/shell) | input tok | result bytes | wall s | key line of answer.txt |
|--|--|--|--|--|--|--|--|--|--|--|--|
| H-L1 | locate | f2 | C | read-only | 1 | 1 | 1 (1/0) | 28345 | 1762 | 12.7 | `sympy/series/gruntz.py:428` - `def limitinf(e, x):` |
| H-L1 | locate | f2 | N | read-only | 1 | 1 | 1 (0/1) | 27442 | 813 | 9.7 | `sympy/series/gruntz.py:428` defines `limitinf`. |
| H-L2 | locate | f2 | C | read-only | 1 | 1 | 1 (1/0) | 28072 | 982 | 5.5 | `sympy/printing/c.py:637` defines `C99CodePrinter`. |
| H-L2 | locate | f2 | N | read-only | 1 | 1 | 1 (0/1) | 26122 | 64 | 5.0 | `sympy/printing/c.py:637` defines `C99CodePrinter`. |
| H-R1 | read | f2 | C | read-only | 1 | 1 | 1 (1/0) | 28185 | 1150 | 13.6 | `ValueError` ... message begins `direction must be one of '+', '-' or '+-', not` |
| H-R1 | read | f2 | N | read-only | 1 | 1 | 1 (0/1) | 26747 | 1808 | 8.1 | `ValueError` ... message begins `direction must be one of '+', '-' or '+-'` |
| H-S1 | structure | f2 | C | read-only | 1 | 0 | 1 (1/0) | 27957 | 468 | 6.7 | `__init__`, `__repr__`, `__getitem__`, `do_subs`, `meets`, `union`, `copy` (3 underscore names listed) |
| H-S1 | structure | f2 | N | read-only | 0 | 0 | 0 (0/0) | 13018 | 0 | 3.8 | I can't access files with shell tools in this read-only environment. (0 calls) |
| H-X1 | crossref | f2 | C | read-only | 1 | 1 | 1 (1/0) | 28470 | 1772 | 8.3 | `gruntz.py:421` - `sign`; `:449`, `:451`, `:453` - `limitinf` |
| H-X1 | crossref | f2 | N | read-only | 1 | 1 | 3 (0/3) | 54704 | 2636 | 16.0 | `sign` - gruntz.py:368; `limitinf` - gruntz.py:428 (definition lines, not call lines) |
| H-M1 | multihop | f2 | C | read-only | 0 | 0 | 0 (0/0) | 13858 | 0 | 3.6 | base class: `CCodePrinter`, defined at `sympy/printing/codeprinter.py:24` (0 calls, wrong) |
| H-M1 | multihop | f2 | N | read-only | 1 | 1 | 1 (0/1) | 26313 | 455 | 9.4 | C89CodePrinter c.py:637; its base `CodePrinter`, codeprinter.py:53 |
| H-L3 | locate | f3 | C | read-only | 1 | 1 | 1 (1/0) | 27955 | 724 | 7.7 | `src/DevX.Indexer/DevXCommandConfig.cs:153` defines ...LooksLikeShellCommandLine |
| H-L3 | locate | f3 | N | read-only | 1 | 1 | 1 (0/1) | 26188 | 304 | 7.6 | `src/DevX.Indexer/DevXCommandConfig.cs:153` defines `LooksLikeShellCommandLine`. |
| H-R2 | read | f3 | C | read-only | 1 | 1 | 2 (2/0) | 43176 | 4550 | 13.5 | cs:18 markdown fence -> "markdown_fence_outside_blocks"; cs:14 empty -> "zero_blocks" |
| H-R2 | read | f3 | N | read-only | 1 | 1 | 3 (0/3) | 61576 | 358121 | 10.5 | cs:20-22 markdown_fence_outside_blocks; cs:14-16 zero_blocks |
| H-R3 | read | f3 | C | read-only | 1 | 1 | 1 (1/0) | 28140 | 1494 | 7.4 | catches `JsonException`, `IOException`, and `UnauthorizedAccessException`; each returns null |
| H-R3 | read | f3 | N | read-only | 1 | 1 | 2 (0/2) | 41926 | 3572 | 8.9 | RipgrepLocator.cs:118-120 catches JsonException, IOException, UnauthorizedAccessException |
| H-S2 | structure | f3 | C | read-only | 1 | 1 | 1 (1/0) | 28041 | 942 | 10.2 | CopySourceTree:24, ApplyChanges:32, GetChangedFiles:47, GetUnifiedDiff:72, Dispose:117 |
| H-S2 | structure | f3 | N | read-only | 1 | 1 | 1 (0/1) | 26226 | 403 | 9.5 | CopySourceTree:24, ApplyChanges:32, GetChangedFiles:47, GetUnifiedDiff:72, Dispose:117 |
| H-X2 | crossref | f3 | C | read-only | 1 | 1 | 4 (4/0) | 79587 | 14239 | 12.2 | Program.cs:1272 - `Program.DoctorAsync`; RipgrepContentSearcher.cs:42 - `...TrySearch` |
| H-X2 | crossref | f3 | N | read-only | 0 | 0 | 1 (0/1) | 26793 | 2555 | 7.1 | Program.cs:1272 - "top-level program code"; ...Searcher.cs:42 - TrySearch (DoctorAsync missing) |
| H-M2 | multihop | f3 | C | read-only | 1 | 1 | 2 (2/0) | 43217 | 3875 | 7.3 | SqliteSessionStore.MarkFileExpandedAsync; ...MarkSymbolExpandedAsync |
| H-M2 | multihop | f3 | N | read-only | 1 | 1 | 2 (0/2) | 42542 | 14552 | 10.2 | MarkSymbolExpandedAsync (cs:96); MarkFileExpandedAsync (cs:102) |

Scorer vs hand-check disagreements: H-S1-C (scorer 1, manual 0)

## Per kind (means over tasks: 3 locate, 3 read, 2 each other kind; hand-checked correctness)
| group | C correct (hand) | N correct (hand) | calls C / N | input tok C / N | bytes C / N | C%N calls / in / bytes | series-4 C%N |
|--|--|--|--|--|--|--|--|
| locate | 3/3 | 3/3 | 1.00 / 1.00 | 28124 / 26584 | 1156 / 394 | 100% / 106% / 294% | 100% / 107% / 28% |
| read | 3/3 | 3/3 | 1.33 / 2.00 | 33167 / 43416 | 2398 / 121167 | 67% / 76% / 2% | 100% / 102% / 15% |
| structure | 1/2 | 1/2 | 1.00 / 0.50 | 27999 / 19622 | 705 / 202 | 200% / 143% / 350% | 100% / 106% / 102% |
| crossref | 2/2 | 1/2 | 2.50 / 2.00 | 54028 / 40748 | 8006 / 2596 | 125% / 133% / 308% | 100% / 107% / 129% |
| multihop | 1/2 | 2/2 | 1.00 / 1.50 | 28538 / 34428 | 1938 / 7504 | 67% / 83% / 26% | 300% / 223% / 167% |
| ALL | 10/12 | 10/12 | 1.33 / 1.42 | 33750 / 33300 | 2663 / 32107 | 94% / 101% / 8% | 131% / 124% / 69% |

## Per fixture
| group | C correct (hand) | N correct (hand) | calls C / N | input tok C / N | bytes C / N | C%N calls / in / bytes | series-4 C%N |
|--|--|--|--|--|--|--|--|
| f2 | 4/6 | 5/6 | 0.83 / 1.17 | 25814 / 29058 | 1022 / 963 | 71% / 89% / 106% |  |
| f3 | 6/6 | 5/6 | 1.83 / 1.67 | 41686 / 37542 | 4304 / 63251 | 110% / 111% / 7% |  |
| f2 locate | 2/2 | 2/2 | 1.00 / 1.00 | 28208 / 26782 | 1372 / 438 | 100% / 105% / 313% |  |
| f2 read | 1/1 | 1/1 | 1.00 / 1.00 | 28185 / 26747 | 1150 / 1808 | 100% / 105% / 64% |  |
| f2 structure | 0/1 | 0/1 | 1.00 / 0.00 | 27957 / 13018 | 468 / 0 | n/a / 215% / n/a |  |
| f2 crossref | 1/1 | 1/1 | 1.00 / 3.00 | 28470 / 54704 | 1772 / 2636 | 33% / 52% / 67% |  |
| f2 multihop | 0/1 | 1/1 | 0.00 / 1.00 | 13858 / 26313 | 0 / 455 | 0% / 53% / 0% |  |
| f3 locate | 1/1 | 1/1 | 1.00 / 1.00 | 27955 / 26188 | 724 / 304 | 100% / 107% / 238% |  |
| f3 read | 2/2 | 2/2 | 1.50 / 2.50 | 35658 / 51751 | 3022 / 180846 | 60% / 69% / 2% |  |
| f3 structure | 1/1 | 1/1 | 1.00 / 1.00 | 28041 / 26226 | 942 / 403 | 100% / 107% / 234% |  |
| f3 crossref | 1/1 | 0/1 | 4.00 / 1.00 | 79587 / 26793 | 14239 / 2555 | 400% / 297% / 557% |  |
| f3 multihop | 1/1 | 1/1 | 2.00 / 2.00 | 43217 / 42542 | 3875 / 14552 | 100% / 102% / 27% |  |

Both-correct (hand-checked) tasks, n=9: H-L1, H-L2, H-R1, H-X1, H-L3, H-R2, H-R3, H-S2, H-M2
| group | C ok | N ok | calls C / N | input tok C / N | bytes C / N | C%N | |
|--|--|--|--|--|--|--|--|
| both-correct | 9/9 | 9/9 | 1.22 / 1.67 | 31511 / 37053 | 1917 / 42475 | 73% / 85% / 5% |  |

Exit codes: 0=24; timeouts=0

## Arm C command patterns (12 runs)
- `search symbol` then read: L1, L2, L3 (search only, 1 call each); R1 (`search symbol "Limit.__new__"` alone, body not read, answer from search output); R2 (`search symbol "Parse"` then `read method`); R3 (`search symbol` alone). `read type` used directly without `search symbol`: S1, S2.
- `callers`: X1 `callers "mrv_leadterm" --full` succeeded (1 call, correct); M2 `callers ...RequireSessionAsync` succeeded, agent filtered the `Mark*` names itself (correct); X2 `callers "DevX.Infrastructure.Storage.SQLite.RipgrepLocator.Locate" --full` FAILED rc 1, verbatim: `error: Method 'DevX.Infrastructure.Storage.SQLite.RipgrepLocator.Locate' matched multiple implementations.` Coping: it had already run `references` (11,883 B), then ran `search symbol` and `search text "RipgrepLocator.Locate("`, answered correctly from the text hits.
- `references`: X2 only (succeeded). `--full`: X1 (succeeded), X2 (failed as above).
- grep/sed/cat fallbacks: 0 in all 12 runs (0 shell calls). No stated reasons. Zero-call run: M1 answered with no tool call and was wrong (`CCodePrinter`, `codeprinter.py:24`).
- C# `callers` over-reporting: the M2 `callers` output was 2,127 B for a method with 6 true callers; the agent's filter by name hid the effect.

## Where C's calls or bytes exceed N's
- Calls: S1 (1 vs 0; N refused to run any command) and X2 (4 vs 1; `references` was large, `callers` hit the multiple-implementations defect, then two more searches; N did one `rg`).
- Bytes: L1 1762 vs 813, L2 982 vs 64, L3 724 vs 304, S2 942 vs 403 (devx search/read output carries a header and signature lines; N's grep line is minimal), S1 468 vs 0 (N did nothing), X2 14,239 vs 2,555.
- N's R-kind bytes are dominated by R2 (358,121 B: `rg -C 5` over `.` including a tracked `Program.cs.bak`); read-kind C%N bytes of 2% is that outlier, not a typical ratio.

## Verdict (held-out vs tuned)
- Correctness (hand): C 10/12, N 10/12. Misses: C = S1 (listed `__init__`, `__repr__`, `__getitem__` as public, so scorer 1 / hand 0) and M1 (no tool call, wrong class); N = S1 (refused, 0 calls) and X2 (named Program.cs:1272 as "top-level program code", DoctorAsync missing). Scorer-vs-hand disagreement: only H-S1-C. H-X1-N's `sign`/`limitinf` are right names (it gave definition lines, not call lines); H-M1-N's `CodePrinter` came with the correct `codeprinter.py:53`.
- Ratios, overall: calls 94%, input 101%, bytes 8% (series 4: 131% / 124% / 69%). Both-correct (n=9): 73% / 85% / 5%. The series-4 ratios were NOT reproduced: here C is cheaper on calls, but with n=2-3 per kind the per-kind figures are noisy (single zero-call runs move a kind: M1-C 0 calls, S1-N 0 calls). Locate reproduced (100% calls, ~106% input; bytes C higher than N, 294% vs 28% before, because N's grep one-liners were tiny). Read: C fewer calls here (67%) vs 100% before, driven by R2-N/R3-N using 2-3 greps; bytes inflated by the 358 KB outlier. Structure, crossref, multihop do not support a pattern at n=1-2.
- By fixture: f2 calls 71%, input 89%, bytes 106%; f3 calls 110%, input 111%, bytes 7%. On f3, X2 (crossref) is the clear loss for C (4 vs 1 calls, 400% calls); C did get X2 right where N missed DoctorAsync.
- C# defects: `callers` multiple-implementations failure cost X2-C 3 extra calls; over-reporting did not change an answer in this run. Both are DevX defects, build frozen.
- Where DevX wins here: R2/R3/M2 bytes and calls on f3, X1 (1 vs 3 calls, `callers --full`). Where not: single-line locate bytes, S1/X2 call counts, M1 (agent skipped the tool).
- Reviewer pushback: n=1 per cell; two runs without any tool call (S1-N refusal, M1-C guess) are model behaviour, not tool effect; f3 is DevX indexing its own source; one model (gpt-6-luna); N allowed `rg` across the whole tree incl. a `.bak`; hand-check by the same agent that ran the series.
