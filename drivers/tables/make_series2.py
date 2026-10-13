import csv, json
from pathlib import Path
H=Path(__file__).parent
kind={t['id']:t['kind'] for t in json.load(open(H/'tasks.json'))}
def load(s):
    rows=list(csv.DictReader(open(H/f'results/{s}/rows.csv')))
    for r in rows:
        for k in r:
            if k not in('task','arm'): r[k]=float(r[k])
    return rows
R2,R1=load('series2'),load('series1')
def m(rs,k): return sum(r[k] for r in rs)/len(rs) if rs else 0
pc=lambda a,b:'n/a' if not b else f'{100*a/b:.0f}%'
print('| task | kind | arm | correct | calls (devx/shell) | in tok | out tok | bytes | wall s |\n|--|--|--|--|--|--|--|--|--|')
for r in sorted(R2,key=lambda r:(r['task'],r['arm'])):
    print(f"| {r['task']} | {kind[r['task']]} | {r['arm']} | {int(r['correct'])} | {int(r['tool_calls_total'])} ({int(r['tool_calls_devx'])}/{int(r['tool_calls_shell'])}) | {int(r['input_tokens'])} | {int(r['output_tokens'])} | {int(r['result_bytes'])} | {r['wall_seconds']} |")
print('\n| kind | arm | n | correct | calls | in tok | bytes | C/N calls | C/N in tok | C/N bytes | S1 C/N calls | S1 C/N in | S1 C/N bytes |\n|--|--|--|--|--|--|--|--|--|--|--|--|--|')
for kd in ['locate','read','structure','crossref','multihop']:
    sel=lambda R,a:[r for r in R if kind[r['task']]==kd and r['arm']==a]
    c,n=sel(R2,'C'),sel(R2,'N'); c1,n1=sel(R1,'C'),sel(R1,'N')
    for a,rs in(('N',n),('C',c)):
        s=f"| {kd} | {a} | {len(rs)} | {m(rs,'correct'):.2f} | {m(rs,'tool_calls_total'):.1f} | {m(rs,'input_tokens'):.0f} | {m(rs,'result_bytes'):.0f} |"
        if a=='C': s+=f" {pc(m(c,'tool_calls_total'),m(n,'tool_calls_total'))} | {pc(m(c,'input_tokens'),m(n,'input_tokens'))} | {pc(m(c,'result_bytes'),m(n,'result_bytes'))} | {pc(m(c1,'tool_calls_total'),m(n1,'tool_calls_total'))} | {pc(m(c1,'input_tokens'),m(n1,'input_tokens'))} | {pc(m(c1,'result_bytes'),m(n1,'result_bytes'))} |"
        else: s+=' | | | | | |'
        print(s)
print()
for lab,R in(('series2',R2),('series1',R1)):
    c=[r for r in R if r['arm']=='C'];n=[r for r in R if r['arm']=='N']
    for a,rs in(('N',n),('C',c)): print(f"{lab} overall {a}: correct {int(sum(r['correct'] for r in rs))}/12 calls {m(rs,'tool_calls_total'):.2f} in {m(rs,'input_tokens'):.0f} out {m(rs,'output_tokens'):.0f} bytes {m(rs,'result_bytes'):.0f} wall {m(rs,'wall_seconds'):.1f}")
    print(f"{lab} C as % of N: calls",pc(m(c,'tool_calls_total'),m(n,'tool_calls_total')),'in',pc(m(c,'input_tokens'),m(n,'input_tokens')),'bytes',pc(m(c,'result_bytes'),m(n,'result_bytes')))
SESS='--session "<SESSION-F2>" '
print('\ncommands arm C')
for r in sorted([r for r in R2 if r['arm']=='C'],key=lambda r:r['task']):
    print('##',r['task'])
    for cmd,nb,rc in json.load(open(H/f"results/series2/{r['task']}-C-r1.cmds.json")):
        short=cmd.split(' -lc ',1)[-1].replace(SESS,'').replace('--agent codex','')[:150]
        print(f"- {short} | {nb} B | rc={rc}")
