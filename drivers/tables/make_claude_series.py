#!/usr/bin/env python3
"""tables + blind pack for a Claude series. usage: make_claude_series.py <N>. Key goes to the scratchpad only."""
import csv, json, random, re, sys
from pathlib import Path
H = Path(__file__).parent; N = sys.argv[1]; S = f'series{N}'; R = H/'results'/S
KEYD = Path(f'<SCRATCH>/blind{N}-key')
tasks = {t['id']: t for t in json.load(open(H/'tasks_heldout.json'))}; ids = list(tasks)
def load(path, ver=None):
    D = {}
    for r in csv.DictReader(open(path)):
        ok = int(r['correct']) if ver is None else int(ver[(r['task'], r['arm'])])
        D[(r['task'], r['arm'])] = dict(ok=ok, calls=sum(int(r[k]) for k in ('tool_calls_devx','tool_calls_shell','tool_calls_mcp','tool_calls_other')), dv=int(r['tool_calls_devx']),
            sh=int(r['tool_calls_shell']), inp=int(r['input_tokens']), by=int(r['result_bytes']), wall=float(r['wall_seconds']), rc=int(r['exit_code']), to=int(r['timed_out']))
    return D
def verdicts(p): return {(r['task'], r['arm']): r['verdict'] == 'correct' for r in csv.DictReader(open(p))}
def line(D, sel, lab):
    f = lambda k: (sum(D[(t,'C')][k] for t in sel), sum(D[(t,'N')][k] for t in sel))
    p = lambda c, n: f'{100*c/n:.0f}%' if n else 'n/a'
    (c1,n1),(c2,n2),(c3,n3) = f('calls'), f('inp'), f('by')
    return f"{lab} (n={len(sel)}): calls C {c1} vs N {n1} ({p(c1,n1)} of N); input tokens C {c2} vs N {n2} ({p(c2,n2)}); result bytes C {c3} vs N {n3} ({p(c3,n3)})"
D = load(R/'rows.csv'); DV = load(R/'rows.csv', verdicts(R/f'rescore{N}.csv')); D7 = load(H/'results'/'series7'/'rows.csv', verdicts(H/'results'/'series7'/'rescore7.csv')); D5 = load(H/'results'/'series5'/'rows.csv', verdicts(H/'rescore.csv')); D6 = load(H/'results'/'series6'/'rows.csv', verdicts(H/'results'/'series6'/'rescore6.csv'))
out = ['| task | arm | auto correct | calls (devx/shell+other) | input tok | result bytes | wall s | exit |', '|--|--|--|--|--|--|--|--|']
for t in ids:
    for a in 'CN':
        d = D[(t,a)]; out.append(f"| {t} | {a} | {d['ok']} | {d['calls']} ({d['dv']}/{d['calls']-d['dv']}) | {d['inp']} | {d['by']} | {d['wall']} | {d['rc']} |")
out.append('')
for a in 'CN': out.append(f"Arm {a} correct: automated {sum(D[(t,a)]['ok'] for t in ids)}/12; VERIFIED (blinded rescore + rulings) {sum(DV[(t,a)]['ok'] for t in ids)}/12")
bc = [t for t in ids if D[(t,'C')]['ok'] and D[(t,'N')]['ok']]; bv = [t for t in ids if DV[(t,'C')]['ok'] and DV[(t,'N')]['ok']]; b7 = [t for t in ids if D7[(t,'C')]['ok'] and D7[(t,'N')]['ok']]
b5 = [t for t in ids if D5[(t,'C')]['ok'] and D5[(t,'N')]['ok']]; b6 = [t for t in ids if D6[(t,'C')]['ok'] and D6[(t,'N')]['ok']]
out += ['', line(DV, bv, f'S{N} both-correct (VERIFIED)'), line(D, bc, f'S{N} both-correct (automated, for reference)'), line(D, ids, f'S{N} all 12'),
        line(D5, b5, 'S5 both-correct (VERIFIED, recomputed from rescore.csv)'), line(D5, ids, 'S5 all 12 (recomputed)'),
        line(D6, b6, 'S6 both-correct (VERIFIED, recomputed from rescore6.csv)'), line(D6, ids, 'S6 all 12 (recomputed)'),
        line(D7, b7, 'S7 both-correct (VERIFIED, recomputed from rescore7.csv)'), line(D7, ids, 'S7 all 12 (recomputed)')]
out += ['', 'Zero-tool-call runs: ' + (', '.join(f'{t}-{a}' for t in ids for a in 'CN' if D[(t,a)]['calls'] == 0) or 'none'),
        'Non-zero exit or timed out: ' + (', '.join(f'{t}-{a}' for t in ids for a in 'CN' if D[(t,a)]['rc'] or D[(t,a)]['to']) or 'none'),
        'C used more calls or bytes than N:'] + [f"- {t}: calls C {D[(t,'C')]['calls']} vs N {D[(t,'N')]['calls']}; bytes C {D[(t,'C')]['by']} vs N {D[(t,'N')]['by']}" for t in ids if D[(t,'C')]['calls'] > D[(t,'N')]['calls'] or D[(t,'C')]['by'] > D[(t,'N')]['by']]
out += ['', 'Arm C devx errors (command, is_error) and non-devx tool use:']
pat = re.compile(r'\b(grep|sed|cat|find|rg|python3?|awk)\b')
for t in ids:
    for c in json.load(open(R/f'{t}-C-r1.cmds.json')):
        cmd = c['command']
        if c['kind'] == 'devx' and c['is_error']: out.append(f"- {t}: devx error `{cmd[:200]}`")
        elif c['kind'] != 'devx': out.append(f"- {t}: fallback tool={c['tool']} `{cmd[:160]}` bytes={c['bytes']} error={c['is_error']}")
open(R/'tables.txt', 'w').write('\n'.join(out)); print('\n'.join(out))
if (R/'blind'/'blind-index.csv').exists(): sys.exit(0)
random.seed(int(N)); order = [(t,a) for t in ids for a in 'CN']; random.shuffle(order)
(R/'blind').mkdir(exist_ok=True); KEYD.mkdir(parents=True, exist_ok=True)
with open(R/'blind'/'blind-index.csv','w',newline='') as f, open(KEYD/'key.csv','w',newline='') as k:
    w = csv.writer(f); w.writerow(['blind_id','task','question','expected']); kw = csv.writer(k); kw.writerow(['blind_id','task','arm'])
    for i,(t,a) in enumerate(order,1):
        b = f'A{i:02d}'; src = R/f'{t}-{a}-r1.answer.txt'
        (R/'blind'/f'{b}.answer.txt').write_text(src.read_text() if src.exists() else '')
        w.writerow([b,t,tasks[t]['prompt'],json.dumps(tasks[t]['expected'])]); kw.writerow([b,t,a])
