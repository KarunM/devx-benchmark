#!/usr/bin/env python3
"""Series 6 working-data tables + blind pack. Automated scorer only. Key goes to the scratchpad, never the repo."""
import csv, json, random, shutil, re
from pathlib import Path
H = Path(__file__).parent; R = H/'results'/'series6'
KEYD = Path('<SCRATCH>/blind6-key')
tasks = {t['id']: t for t in json.load(open(H/'tasks_heldout.json'))}
def load(s):
    D = {}
    for r in csv.DictReader(open(H/'results'/s/'rows.csv')):
        d = dict(task=r['task'], arm=r['arm'], ok=int(r['correct']), calls=sum(int(r[k]) for k in ('tool_calls_devx','tool_calls_shell','tool_calls_mcp','tool_calls_other')),
                 dv=int(r['tool_calls_devx']), sh=int(r['tool_calls_shell']), inp=int(r['input_tokens']), by=int(r['result_bytes']), wall=float(r['wall_seconds']), rc=int(r['exit_code']))
        D[(d['task'], d['arm'])] = d
    return D
def ratios(D, sel):
    out = {}
    for k in ('calls','inp','by'):
        c = sum(D[(t,'C')][k] for t in sel); n = sum(D[(t,'N')][k] for t in sel)
        out[k] = (c, n, f'{100*c/n:.0f}%' if n else 'n/a')
    return out
def line(D, sel, lab):
    r = ratios(D, sel)
    return f"{lab} (n={len(sel)}): calls C {r['calls'][0]} vs N {r['calls'][1]} ({r['calls'][2]} of N); input tokens C {r['inp'][0]} vs N {r['inp'][1]} ({r['inp'][2]}); result bytes C {r['by'][0]} vs N {r['by'][1]} ({r['by'][2]})"
D6 = load('series6'); D5 = load('series5'); ids = list(tasks)
out = ['| task | arm | auto correct | calls (devx/shell) | input tok | result bytes | wall s | exit |', '|--|--|--|--|--|--|--|--|']
for t in ids:
    for a in 'CN':
        d = D6[(t,a)]; out.append(f"| {t} | {a} | {d['ok']} | {d['calls']} ({d['dv']}/{d['sh']}) | {d['inp']} | {d['by']} | {d['wall']} | {d['rc']} |")
out += ['']
for a in 'CN': out.append(f"Arm {a} automated correct: {sum(D6[(t,a)]['ok'] for t in ids)}/12 (pending blinded rescore)")
bc6 = [t for t in ids if D6[(t,'C')]['ok'] and D6[(t,'N')]['ok']]; bc5 = [t for t in ids if D5[(t,'C')]['ok'] and D5[(t,'N')]['ok']]
out += ['', line(D6, bc6, 'S6 both-correct (automated)'), line(D6, ids, 'S6 all 12'), line(D5, bc5, 'S5 both-correct (automated, recomputed)'), line(D5, ids, 'S5 all 12 (recomputed)')]
for s, D in (('S5', D5), ('S6', D6)): out.append(f"{s} arm correctness (automated): C {sum(D[(t,'C')]['ok'] for t in ids)}/12, N {sum(D[(t,'N')]['ok'] for t in ids)}/12")
out += ['', 'Zero-tool-call runs: ' + (', '.join(f'{t}-{a}' for t in ids for a in 'CN' if D6[(t,a)]['calls'] == 0) or 'none')]
out += ['C used more calls or bytes than N:'] + [f"- {t}: calls C {D6[(t,'C')]['calls']} vs N {D6[(t,'N')]['calls']}; bytes C {D6[(t,'C')]['by']} vs N {D6[(t,'N')]['by']}" for t in ids if D6[(t,'C')]['calls'] > D6[(t,'N')]['calls'] or D6[(t,'C')]['by'] > D6[(t,'N')]['by']]
out += ['', 'Arm C grep/sed/cat/find fallbacks and devx non-zero exits (command, exit):']
pat = re.compile(r'\b(grep|sed|cat|find|rg|python3?|awk)\b')
for t in ids:
    for cmd, nb, ec in json.load(open(R/f'{t}-C-r1.cmds.json')):
        inner = cmd.split(' -lc ', 1)[1].strip().strip('\'"') if ' -lc ' in cmd else cmd
        if not inner.lstrip().startswith('devx') and pat.search(inner) or (inner.lstrip().startswith('devx') and ec not in (0, None)):
            out.append(f"- {t}: `{inner[:160]}` exit={ec}")
open(R/'tables.txt', 'w').write('\n'.join(out)); print('\n'.join(out))
# blind pack
random.seed(6); order = [(t,a) for t in ids for a in 'CN']; random.shuffle(order)
(R/'blind').mkdir(exist_ok=True); KEYD.mkdir(parents=True, exist_ok=True)
with open(R/'blind'/'blind-index.csv','w',newline='') as f, open(KEYD/'key.csv','w',newline='') as k:
    w = csv.writer(f); w.writerow(['blind_id','task','question','expected']); kw = csv.writer(k); kw.writerow(['blind_id','task','arm'])
    for i,(t,a) in enumerate(order,1):
        b = f'A{i:02d}'; src = R/f'{t}-{a}-r1.answer.txt'
        (R/'blind'/f'{b}.answer.txt').write_text(src.read_text() if src.exists() else '')
        w.writerow([b,t,tasks[t]['prompt'],json.dumps(tasks[t]['expected'])]); kw.writerow([b,t,a])
