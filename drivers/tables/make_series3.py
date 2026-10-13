import csv, json
from pathlib import Path
H=Path(__file__).parent
T=json.load(open(H/'tasks.json')); kind={t['id']:t['kind'] for t in T}
def load(s):
    rows=list(csv.DictReader(open(H/f'results/{s}/rows.csv')))
    for r in rows:
        for k in r:
            if k not in('task','arm'): r[k]=float(r[k])
    return {(r['task'],r['arm']):r for r in rows}
S={1:load('series1'),2:load('series2'),3:load('series3')}
ids=sorted(kind)
def m(rs,k): return sum(r[k] for r in rs)/len(rs) if rs else 0
pc=lambda a,b:'n/a' if not b else f'{100*a/b:.0f}%'
print('| task | kind | arm | correct | calls (devx/shell) | in tok | out tok | bytes | wall s |\n|--|--|--|--|--|--|--|--|--|')
for t in ids:
    for a in 'CN':
        r=S[3][(t,a)]
        print(f"| {t} | {kind[t]} | {a} | {int(r['correct'])} | {int(r['tool_calls_total'])} ({int(r['tool_calls_devx'])}/{int(r['tool_calls_shell'])}) | {int(r['input_tokens'])} | {int(r['output_tokens'])} | {int(r['result_bytes'])} | {r['wall_seconds']} |")
def sel(s,a,f=lambda t:True): return [S[s][(t,a)] for t in ids if f(t)]
def ratio(s,f=lambda t:True):
    c,n=sel(s,'C',f),sel(s,'N',f)
    return [pc(m(c,k),m(n,k)) for k in('tool_calls_total','input_tokens','result_bytes')]
print('\n| kind | C/N calls S3/S2/S1 | C/N in tok S3/S2/S1 | C/N bytes S3/S2/S1 | correct C N (S3) | (S2) | (S1) |\n|--|--|--|--|--|--|--|')
for kd in ['locate','read','structure','crossref','multihop']:
    f=lambda t,kd=kd:kind[t]==kd
    R={s:ratio(s,f) for s in(3,2,1)}
    cor=lambda s:f"{m(sel(s,'C',f),'correct'):.2f} / {m(sel(s,'N',f),'correct'):.2f}"
    print(f"| {kd} | {R[3][0]} / {R[2][0]} / {R[1][0]} | {R[3][1]} / {R[2][1]} / {R[1][1]} | {R[3][2]} / {R[2][2]} / {R[1][2]} | {cor(3)} | {cor(2)} | {cor(1)} |")
print()
for s in(3,2,1):
    for a in 'NC':
        rs=sel(s,a); print(f"series{s} {a}: correct {int(sum(r['correct'] for r in rs))}/12 calls {m(rs,'tool_calls_total'):.2f} in {m(rs,'input_tokens'):.0f} bytes {m(rs,'result_bytes'):.0f} wall {m(rs,'wall_seconds'):.1f}")
    print(f"series{s} C%N all12: calls/in/bytes", ' / '.join(ratio(s)))
    both=[t for t in ids if S[s][(t,'C')]['correct'] and S[s][(t,'N')]['correct']]
    print(f"series{s} both-correct n={len(both)} ({','.join(both)}): calls/in/bytes", ' / '.join(ratio(s,lambda t:t in both)))
print('\nper-task calls/bytes C vs N, series3 (and S2, S1 C calls)')
for t in ids:
    c,n=S[3][(t,'C')],S[3][(t,'N')]
    print(t,kind[t],f"C {int(c['tool_calls_total'])}c/{int(c['result_bytes'])}B  N {int(n['tool_calls_total'])}c/{int(n['result_bytes'])}B  | S2 C {int(S[2][(t,'C')]['tool_calls_total'])}c/{int(S[2][(t,'C')]['result_bytes'])}B N {int(S[2][(t,'N')]['tool_calls_total'])}c/{int(S[2][(t,'N')]['result_bytes'])}B | S1 C {int(S[1][(t,'C')]['tool_calls_total'])}c N {int(S[1][(t,'N')]['tool_calls_total'])}c",'FLAG' if c['tool_calls_total']>n['tool_calls_total'] or c['result_bytes']>n['result_bytes'] else '')
SESS='--session "<SESSION-F2>" '
print('\ncommands arm C')
for t in ids:
    print('##',t)
    for cmd,nb,rc in json.load(open(H/f"results/series3/{t}-C-r1.cmds.json")):
        print(f"- {cmd.split(' -lc ',1)[-1].replace(SESS,'').replace('--agent codex','')[:170]} | {nb} B | rc={rc}")
