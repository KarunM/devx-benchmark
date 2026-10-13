#!/usr/bin/env python3
"""Series 5 tables from results/series5/rows.csv + hand-check. Prints markdown. Does not touch make_series4.py."""
import csv, json, statistics as st
from pathlib import Path
H = Path(__file__).parent
R = H / 'results' / 'series5'
rows = list(csv.DictReader(open(R / 'rows.csv')))
tasks = {t['id']: t for t in json.load(open(H / 'tasks_heldout.json'))}
# hand-check: (manual_correct, key line <=100 chars)
M = {
 ('H-L1','C'):(1,'`sympy/series/gruntz.py:428` - `def limitinf(e, x):`'),
 ('H-L1','N'):(1,'`sympy/series/gruntz.py:428` defines `limitinf`.'),
 ('H-L2','C'):(1,'`sympy/printing/c.py:637` defines `C99CodePrinter`.'),
 ('H-L2','N'):(1,'`sympy/printing/c.py:637` defines `C99CodePrinter`.'),
 ('H-L3','C'):(1,'`src/DevX.Indexer/DevXCommandConfig.cs:153` defines ...LooksLikeShellCommandLine'),
 ('H-L3','N'):(1,'`src/DevX.Indexer/DevXCommandConfig.cs:153` defines `LooksLikeShellCommandLine`.'),
 ('H-R1','C'):(1,'`ValueError` ... message begins `direction must be one of \'+\', \'-\' or \'+-\', not`'),
 ('H-R1','N'):(1,'`ValueError` ... message begins `direction must be one of \'+\', \'-\' or \'+-\'`'),
 ('H-R2','C'):(1,'cs:18 markdown fence -> "markdown_fence_outside_blocks"; cs:14 empty -> "zero_blocks"'),
 ('H-R2','N'):(1,'cs:20-22 markdown_fence_outside_blocks; cs:14-16 zero_blocks'),
 ('H-R3','C'):(1,'catches `JsonException`, `IOException`, and `UnauthorizedAccessException`; each returns null'),
 ('H-R3','N'):(1,'RipgrepLocator.cs:118-120 catches JsonException, IOException, UnauthorizedAccessException'),
 ('H-S1','C'):(0,'`__init__`, `__repr__`, `__getitem__`, `do_subs`, `meets`, `union`, `copy` (3 underscore names listed)'),
 ('H-S1','N'):(0,'I can\'t access files with shell tools in this read-only environment. (0 calls)'),
 ('H-S2','C'):(1,'CopySourceTree:24, ApplyChanges:32, GetChangedFiles:47, GetUnifiedDiff:72, Dispose:117'),
 ('H-S2','N'):(1,'CopySourceTree:24, ApplyChanges:32, GetChangedFiles:47, GetUnifiedDiff:72, Dispose:117'),
 ('H-X1','C'):(1,'`gruntz.py:421` - `sign`; `:449`, `:451`, `:453` - `limitinf`'),
 ('H-X1','N'):(1,'`sign` - gruntz.py:368; `limitinf` - gruntz.py:428 (definition lines, not call lines)'),
 ('H-X2','C'):(1,'Program.cs:1272 - `Program.DoctorAsync`; RipgrepContentSearcher.cs:42 - `...TrySearch`'),
 ('H-X2','N'):(0,'Program.cs:1272 - "top-level program code"; ...Searcher.cs:42 - TrySearch (DoctorAsync missing)'),
 ('H-M1','C'):(0,'base class: `CCodePrinter`, defined at `sympy/printing/codeprinter.py:24` (0 calls, wrong)'),
 ('H-M1','N'):(1,'C89CodePrinter c.py:637; its base `CodePrinter`, codeprinter.py:53'),
 ('H-M2','C'):(1,'SqliteSessionStore.MarkFileExpandedAsync; ...MarkSymbolExpandedAsync'),
 ('H-M2','N'):(1,'MarkSymbolExpandedAsync (cs:96); MarkFileExpandedAsync (cs:102)'),
}
KINDS = ['locate','read','structure','crossref','multihop']
S4 = {'locate':'100% / 107% / 28%','read':'100% / 102% / 15%','structure':'100% / 106% / 102%','crossref':'100% / 107% / 129%','multihop':'300% / 223% / 167%','ALL':'131% / 124% / 69%'}
D = {}
for r in rows:
    t = tasks[r['task']]
    d = dict(task=r['task'], kind=t['kind'], fx=t['fixture'], arm=r['arm'], sb=r['sandbox'], sc=int(r['correct']),
             man=M[(r['task'], r['arm'])][0], calls=int(r['tool_calls_total'] if 'tool_calls_total' in r else 0),
             dv=int(r['tool_calls_devx']), sh=int(r['tool_calls_shell']), inp=int(r['input_tokens']), by=int(r['result_bytes']), wall=float(r['wall_seconds']),
             rc=int(r['exit_code']), to=int(r['timed_out']))
    d['calls'] = d['dv'] + d['sh'] + int(r['tool_calls_mcp']) + int(r['tool_calls_other'])
    D[(d['task'], d['arm'])] = d
order = [t for t in tasks]
out = ['## Per-run table (24 rows)', '| task | kind | fx | arm | sandbox | scorer | manual | calls (devx/shell) | input tok | result bytes | wall s | key line of answer.txt |', '|--|--|--|--|--|--|--|--|--|--|--|--|']
for tid in order:
    for a in 'CN':
        d = D[(tid, a)]
        out.append(f"| {tid} | {d['kind']} | {d['fx']} | {a} | {d['sb']} | {d['sc']} | {d['man']} | {d['calls']} ({d['dv']}/{d['sh']}) | {d['inp']} | {d['by']} | {d['wall']} | {M[(tid,a)][1].replace('|','/')} |")
dis = [(t,a) for t in order for a in 'CN' if D[(t,a)]['sc'] != D[(t,a)]['man']]
out += ['', 'Scorer vs hand-check disagreements: ' + (', '.join(f'{t}-{a} (scorer {D[(t,a)]["sc"]}, manual {D[(t,a)]["man"]})' for t,a in dis) or 'none')]
def agg(sel):
    res = {}
    for a in 'CN':
        xs = [D[(t, a)] for t in sel]
        res[a] = dict(n=len(xs), ok=sum(x['man'] for x in xs), calls=st.mean(x['calls'] for x in xs), inp=st.mean(x['inp'] for x in xs), by=st.mean(x['by'] for x in xs))
    return res
def pct(r, k): return f"{100*r['C'][k]/r['N'][k]:.0f}%" if r['N'][k] else 'n/a'
def line(label, sel, s4=None):
    r = agg(sel)
    return f"| {label} | {r['C']['ok']}/{r['C']['n']} | {r['N']['ok']}/{r['N']['n']} | {r['C']['calls']:.2f} / {r['N']['calls']:.2f} | {r['C']['inp']:.0f} / {r['N']['inp']:.0f} | {r['C']['by']:.0f} / {r['N']['by']:.0f} | {pct(r,'calls')} / {pct(r,'inp')} / {pct(r,'by')} | {s4 or ''} |"
hdr = ['| group | C correct (hand) | N correct (hand) | calls C / N | input tok C / N | bytes C / N | C%N calls / in / bytes | series-4 C%N |', '|--|--|--|--|--|--|--|--|']
out += ['', '## Per kind (means over tasks: 3 locate, 3 read, 2 each other kind; hand-checked correctness)'] + hdr
for k in KINDS: out.append(line(k, [t for t in order if tasks[t]['kind'] == k], S4[k]))
out.append(line('ALL', order, S4['ALL']))
out += ['', '## Per fixture'] + hdr
for f in ('f2', 'f3'): out.append(line(f, [t for t in order if tasks[t]['fixture'] == f]))
for f in ('f2', 'f3'):
    for k in KINDS: out.append(line(f'{f} {k}', [t for t in order if tasks[t]['fixture'] == f and tasks[t]['kind'] == k]))
both = [t for t in order if D[(t,'C')]['man'] and D[(t,'N')]['man']]
out += ['', f'Both-correct (hand-checked) tasks, n={len(both)}: {", ".join(both)}', '| group | C ok | N ok | calls C / N | input tok C / N | bytes C / N | C%N | |', '|--|--|--|--|--|--|--|--|', line('both-correct', both)]
out += ['', 'Exit codes: ' + ', '.join(f'{k}={sum(1 for d in D.values() if d["rc"]==k)}' for k in sorted({d['rc'] for d in D.values()})) + f'; timeouts={sum(d["to"] for d in D.values())}']
print('\n'.join(out))
