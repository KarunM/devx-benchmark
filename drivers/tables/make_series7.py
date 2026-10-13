#!/usr/bin/env python3
"""Series 7 analysis: blind pack + SERIES7.md. Working data, not evidence. Corrects calls for the codex 'Model metadata' warning item (counted as 'other' by parse())."""
import csv, json, random, re, shutil
from pathlib import Path
H = Path(__file__).resolve().parent; R = H / 'results'; S = R / 'series7'
KEY = Path('<SCRATCH>/blind7-key')
tasks = {t['id']: t for t in json.load(open(H / 'tasks_heldout.json'))}
rows = list(csv.DictReader(open(S / 'rows.csv')))
for r in rows:
    for k in ('correct','tool_calls_devx','tool_calls_shell','tool_calls_mcp','input_tokens','result_bytes','tool_calls_other'): r[k] = int(r[k])
    r['calls'] = r['tool_calls_devx'] + r['tool_calls_shell'] + r['tool_calls_mcp']
# blind pack
random.seed(7); order = list(range(len(rows))); random.shuffle(order)
(S / 'blind').mkdir(exist_ok=True); KEY.mkdir(parents=True, exist_ok=True)
bi = csv.writer(open(S / 'blind' / 'blind-index.csv', 'w', newline='')); bi.writerow(['blind_id','task','question','expected'])
kc = csv.writer(open(KEY / 'key.csv', 'w', newline='')); kc.writerow(['blind_id','task','arm'])
for n, i in enumerate(order, 1):
    r = rows[i]; b = f'A{n:02d}'; t = tasks[r['task']]
    shutil.copy(S / f"{r['task']}-{r['arm']}-r1.answer.txt", S / 'blind' / f'{b}.answer.txt')
    bi.writerow([b, r['task'], t['prompt'], json.dumps(t['expected'])]); kc.writerow([b, r['task'], r['arm']])
def agg(rs):
    return dict(c=sum(x['calls'] for x in rs), t=sum(x['input_tokens'] for x in rs), b=sum(x['result_bytes'] for x in rs))
def line(name, C, N):
    a, b = agg(C), agg(N); p = lambda x, y: f'{100*x/y:.0f}%' if y else 'n/a'
    return (f"{name} (n={len(C)}): calls C {a['c']} vs N {b['c']} ({p(a['c'],b['c'])} of N); input tokens C {a['t']} vs N {b['t']} ({p(a['t'],b['t'])}); "
            f"result bytes C {a['b']} vs N {b['b']} ({p(a['b'],b['b'])})")
def load(d, rescore):
    rs = list(csv.DictReader(open(R / d / 'rows.csv')))
    for r in rs:
        for k in ('tool_calls_total','input_tokens','result_bytes'): r[k] = int(r[k])
    v = {(x['task'], x['arm']): x['verdict'] for x in csv.DictReader(open(rescore))}
    return rs, v
def prior(tag, d, rescore):
    rs, v = load(d, rescore); by = {(r['task'], r['arm']): r for r in rs}
    def mk(r): return dict(calls=r['tool_calls_total'], input_tokens=r['input_tokens'], result_bytes=r['result_bytes'])
    ts = sorted({r['task'] for r in rs}); allC = [mk(by[(t,'C')]) for t in ts]; allN = [mk(by[(t,'N')]) for t in ts]
    bt = [t for t in ts if v[(t,'C')] == 'correct' and v[(t,'N')] == 'correct']
    nc = sum(v[(t,'C')]=='correct' for t in ts); nn = sum(v[(t,'N')]=='correct' for t in ts)
    return [line(f'{tag} both-correct (verified)', [mk(by[(t,'C')]) for t in bt], [mk(by[(t,'N')]) for t in bt]), line(f'{tag} all {len(ts)}', allC, allN),
            f'{tag} verified correctness: C {nc}/{len(ts)}, N {nn}/{len(ts)}']
ver = {(x['task'], x['arm']): x['verdict'] for x in csv.DictReader(open(S / 'rescore7.csv'))}
byk = {(r['task'], r['arm']): r for r in rows}; ts = [t for t in tasks if (t,'C') in byk]
corr = lambda a: sum(ver[(t,a)] == 'correct' for t in ts)
auto = lambda a: sum(byk[(t,a)]['correct'] for t in ts)
agree = sum((ver[(t,a)] == 'correct') == bool(byk[(t,a)]['correct']) for t in ts for a in 'CN')
both = [t for t in ts if ver[(t,'C')] == 'correct' and ver[(t,'N')] == 'correct']
out = ['# Series 7: held-out 12 tasks on DeepSeek Flash 4.1 via Codex provider', '', 'Working data, not part of the evidence set (maintainer decision 2026-10-12).', '']
out += [line('S7 both-correct (verified)', [byk[(t,'C')] for t in both], [byk[(t,'N')] for t in both]),
        line('S7 all 12', [byk[(t,'C')] for t in ts], [byk[(t,'N')] for t in ts]),
        f'S7 verified correctness (blinded rescore, rescore7.csv): C {corr("C")}/12, N {corr("N")}/12; automated scorer: C {auto("C")}/12, N {auto("N")}/12; agreement {agree}/24', '']
out += prior('S5', 'series5', H / 'rescore.csv') + [''] + prior('S6', 'series6', R / 'series6' / 'rescore6.csv') + ['']
out += ['| task | arm | auto correct | calls (devx/shell) | input tok | result bytes | wall s | exit |', '|--|--|--|--|--|--|--|--|']
for t in ts:
    for a in 'CN':
        r = byk[(t,a)]; out.append(f"| {t} | {a} | {r['correct']} | {r['calls']} ({r['tool_calls_devx']}/{r['tool_calls_shell']}) | {r['input_tokens']} | {r['result_bytes']} | {r['wall_seconds']} | {r['exit_code']} |")
out += ['', 'Zero-tool-call runs: ' + (', '.join(f"{r['task']}-{r['arm']}" for r in rows if r['calls'] == 0) or 'none'), '', 'C used more calls or bytes than N:']
for t in ts:
    c, n = byk[(t,'C')], byk[(t,'N')]
    if c['calls'] > n['calls'] or c['result_bytes'] > n['result_bytes']: out.append(f"- {t}: calls C {c['calls']} vs N {n['calls']}; bytes C {c['result_bytes']} vs N {n['result_bytes']}")
out += ['', 'Arm C devx non-zero exits and grep/sed/cat/find fallbacks (task, command, exit):']
fb = 0
for t in ts:
    for cmd, nb, ec in json.load(open(S / f'{t}-C-r1.cmds.json')):
        inner = cmd.split(' -lc ', 1)[1].strip().strip('\'"') if ' -lc ' in cmd else cmd
        if not inner.lstrip().startswith('devx') or ec not in (0, None): out.append(f'- {t}: {inner[:160]} (exit {ec})'); fb += 1
if not fb: out.append('- none')
open(H / 'SERIES7.md', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
