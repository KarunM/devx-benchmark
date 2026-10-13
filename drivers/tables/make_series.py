import csv, json
from pathlib import Path
H=Path(__file__).parent; R=H/'results/series1'
kind={t['id']:t['kind'].replace('read','read-and-answer') if t['kind']=='read' else t['kind'] for t in json.load(open(H/'tasks.json'))}
rows=list(csv.DictReader(open(R/'rows.csv')))
for r in rows:
    for k in r:
        if k not in('task','arm'): r[k]=float(r[k])
print('| task | kind | arm | correct | calls (devx/shell) | in tok | out tok | bytes | wall s |\n|--|--|--|--|--|--|--|--|--|')
for r in sorted(rows,key=lambda r:(r['task'],r['arm'])):
    print(f"| {r['task']} | {kind[r['task']]} | {r['arm']} | {int(r['correct'])} | {int(r['tool_calls_total'])} ({int(r['tool_calls_devx'])}/{int(r['tool_calls_shell'])}) | {int(r['input_tokens'])} | {int(r['output_tokens'])} | {int(r['result_bytes'])} | {r['wall_seconds']} |")
def m(rs,k): return sum(r[k] for r in rs)/len(rs) if rs else 0
pc=lambda a,b:'n/a' if not b else f'{100*a/b:.0f}%'
print('\n| kind | arm | n | correct | calls | in tok | bytes | C/N calls | C/N in tok | C/N bytes |\n|--|--|--|--|--|--|--|--|--|--|')
for kd in ['locate','read','structure','crossref','multihop']:
    sel=lambda a:[r for r in rows if kd==[t for t in [kind[r['task']]]][0].replace('-and-answer','') and r['arm']==a]
    c,n=sel('C'),sel('N')
    for a,rs in(('N',n),('C',c)):
        s=f"| {kd} | {a} | {len(rs)} | {m(rs,'correct'):.2f} | {m(rs,'tool_calls_total'):.1f} | {m(rs,'input_tokens'):.0f} | {m(rs,'result_bytes'):.0f} |"
        if a=='C': s+=f" {pc(m(c,'tool_calls_total'),m(n,'tool_calls_total'))} | {pc(m(c,'input_tokens'),m(n,'input_tokens'))} | {pc(m(c,'result_bytes'),m(n,'result_bytes'))} |"
        else: s+=' | | |'
        print(s)
c=[r for r in rows if r['arm']=='C'];n=[r for r in rows if r['arm']=='N']
for a,rs in(('N',n),('C',c)): print(f"overall {a}: correct {int(sum(r['correct'] for r in rs))}/12 calls {m(rs,'tool_calls_total'):.2f} in {m(rs,'input_tokens'):.0f} bytes {m(rs,'result_bytes'):.0f} wall {m(rs,'wall_seconds'):.1f}")
print('C as % of N: calls',pc(m(c,'tool_calls_total'),m(n,'tool_calls_total')),'in',pc(m(c,'input_tokens'),m(n,'input_tokens')),'bytes',pc(m(c,'result_bytes'),m(n,'result_bytes')))
print('\ncommands arm C')
for r in sorted(c,key=lambda r:r['task']):
    print('##',r['task'])
    for cmd,nb,rc in json.load(open(R/f"{r['task']}-C-r1.cmds.json")):
        print(f"- {cmd.split(' -lc ',1)[-1][:170]} | {nb} B | rc={rc}")
