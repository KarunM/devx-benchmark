import csv, json, re, statistics as st
from pathlib import Path
H=Path(__file__).parent
T=json.load(open(H/'tasks.json')); kind={t['id']:t['kind'] for t in T}; ids=sorted(kind)
KINDS=['locate','read','structure','crossref','multihop']
def load(s):
    rows=list(csv.DictReader(open(H/f'results/{s}/rows.csv')))
    for r in rows:
        for k in r:
            if k not in('task','arm'): r[k]=float(r[k])
    return rows
R4=load('series4')
G={}
for r in R4: G.setdefault((r['task'],r['arm']),[]).append(r)
def med(t,a,k): return st.median([r[k] for r in G[(t,a)]])
def old(s):
    d={}
    for r in load(f'series{s}'): d[(r['task'],r['arm'])]=r
    return d
S={1:old(1),2:old(2),3:old(3)}
pc=lambda a,b:'n/a' if not b else f'{100*a/b:.0f}%'
mean=lambda xs:sum(xs)/len(xs) if xs else 0
M=('tool_calls_total','input_tokens','result_bytes')
print(f'rows: {len(R4)}')
print('## per-task\n| task | kind | arm | correct | med calls | med in tok | med bytes | bytes min-max | med wall s |\n|--|--|--|--|--|--|--|--|--|')
for t in ids:
    for a in 'CN':
        rs=G[(t,a)]; b=[r['result_bytes'] for r in rs]
        print(f"| {t} | {kind[t]} | {a} | {int(sum(r['correct'] for r in rs))}/{len(rs)} | {med(t,a,M[0]):g} | {med(t,a,M[1]):.0f} | {med(t,a,M[2]):.0f} | {int(min(b))}-{int(max(b))} | {med(t,a,'wall_seconds'):.1f} |")
def agg(a,f): 
    return {k:mean([med(t,a,k) for t in ids if f(t)]) for k in M}
def corr(a,f): 
    rs=[r for t in ids if f(t) for r in G[(t,a)]]; return f"{int(sum(r['correct'] for r in rs))}/{len(rs)}"
def old_ratio(s,f):
    c=[S[s][(t,'C')] for t in ids if f(t)]; n=[S[s][(t,'N')] for t in ids if f(t)]
    return [pc(mean([r[k] for r in c]),mean([r[k] for r in n])) for k in M]
print('\n## per-kind (mean of per-task medians)\n| kind | arm | calls | in tok | bytes | correct | C%N calls/in/bytes S4 | S3 | S2 | S1 |\n|--|--|--|--|--|--|--|--|--|--|')
for kd in KINDS+['ALL']:
    f=(lambda t:True) if kd=='ALL' else (lambda t,kd=kd:kind[t]==kd)
    c,n=agg('C',f),agg('N',f)
    rat=[pc(c[k],n[k]) for k in M]
    for a,x in(('N',n),('C',c)):
        extra=f"{' / '.join(rat)} | {' / '.join(old_ratio(3,f))} | {' / '.join(old_ratio(2,f))} | {' / '.join(old_ratio(1,f))}" if a=='C' else ' | | |'
        print(f"| {kd} | {a} | {x[M[0]]:.2f} | {x[M[1]]:.0f} | {x[M[2]]:.0f} | {corr(a,f)} | {extra} |")
def allcorrect(t,a): return all(r['correct'] for r in G[(t,a)])
def maj(t,a): return sum(r['correct'] for r in G[(t,a)])>len(G[(t,a)])/2
for name,fn in(('ALL 3 reps',lambda t:allcorrect(t,'C') and allcorrect(t,'N')),('majority of reps',lambda t:maj(t,'C') and maj(t,'N'))):
    b=[t for t in ids if fn(t)]; c,n=agg('C',lambda t:t in b),agg('N',lambda t:t in b)
    print(f"\nboth-correct ({name}): n={len(b)} ({','.join(b)}): C%N calls/in/bytes", ' / '.join(pc(c[k],n[k]) for k in M), f"| N means {n[M[0]]:.2f}/{n[M[1]]:.0f}/{n[M[2]]:.0f} C means {c[M[0]]:.2f}/{c[M[1]]:.0f}/{c[M[2]]:.0f}")
print('\n## stability')
stable=0
for t in ids:
    line=[]
    for a in 'CN':
        cs=[int(r['correct']) for r in sorted(G[(t,a)],key=lambda r:r['rep'])]; b=[r['result_bytes'] for r in G[(t,a)]]
        flip=len(set(cs))>1; stable+=not flip
        line.append(f"{a}: correct {cs} {'FLIP' if flip else 'stable'} bytes {int(min(b))}-{int(max(b))}")
    print(t,' | '.join(line))
print('stable cells (no correctness flip):',stable,'of 24')
print('\n## C vs N flags (median calls or bytes of C > N)')
for t in ids:
    c=[med(t,'C',k) for k in M]; n=[med(t,'N',k) for k in M]
    if c[0]>n[0] or c[2]>n[2]: print(t,kind[t],f"C {c[0]:g}c/{c[1]:.0f}tok/{c[2]:.0f}B  N {n[0]:g}c/{n[1]:.0f}tok/{n[2]:.0f}B", 'CALLS' if c[0]>n[0] else '', 'BYTES' if c[2]>n[2] else '')
print('\n## arm C commands (36 runs)')
SESS=re.compile(r'\s*--session "[^"]+"|\s*--agent codex')
def inner(cmd):
    c=cmd.split(' -lc ',1)[-1].strip().strip('\'"'); return SESS.sub('',c).replace('\\"','"')
runs=[]
for t in ids:
    for rep in(1,2,3):
        cm=json.load(open(H/f'results/series4/{t}-C-r{rep}.cmds.json'))
        out={}
        for line in open(H/f'results/series4/{t}-C-r{rep}.jsonl',errors='replace'):
            try:e=json.loads(line)
            except ValueError: continue
            it=e.get('item') or {}
            if e.get('type')=='item.completed' and it.get('type')=='command_execution': out.setdefault(it.get('command'),[]).append(it.get('aggregated_output') or '')
        runs.append((t,rep,[(inner(c),nb,rc,(out.get(c) or [''])[0]) for c,nb,rc in cm]))
ss_rt=0; walks=[]; callers=[0,0]; refs=[0,0]; full=[]; shells=[]; errs=[]
for t,rep,cs in runs:
    ks=[]
    for c,nb,rc,o in cs:
        m=re.match(r'devx\s+(\S+)(?:\s+(\S+))?',c)
        k=(m.group(1)+((' '+m.group(2)) if m.group(1) in('search','read') and m.group(2) else '')) if m and c.startswith('devx') else 'SHELL'
        ks.append(k)
        if '--full' in c and c.startswith('devx'): full.append((t,rep,c[:120]))
        if k=='callers': callers[0]+=1; callers[1]+=(rc==0 and nb>0)
        if k=='references': refs[0]+=1; refs[1]+=(rc==0 and nb>0)
        if k=='SHELL': shells.append((t,rep,c[:160],nb,rc))
        if c.startswith('devx') and rc not in(0,None): errs.append((t,rep,c[:120],o[:200].replace('\n',' / ')))
        elif c.startswith('devx') and re.search(r'(?i)\berror\b|not found|ambiguous',o[:300]): errs.append((t,rep,c[:120],'rc=0: '+o[:200].replace('\n',' / ')))
    ss_rt+=sum(1 for a,b in zip(ks,ks[1:]) if a=='search symbol' and b=='read type')
    i=0
    while i<len(ks):
        if ks[i]=='read type':
            j=i
            while j<len(ks) and ks[j]=='read type': j+=1
            if j-i>=2: walks.append((t,rep,j-i))
            i=j
        else: i+=1
print('runs with >=1 call:',sum(1 for r in runs if r[2]),'of',len(runs))
print('search symbol immediately before read type (pairs):',ss_rt)
print('read type total:',sum(1 for r in runs for c in r[2] if c[0].startswith('devx read type')),'| hierarchy walks (>=2 consecutive read type):',len(walks),walks)
print('callers used/succeeded(rc0,nonempty):',callers,'| references:',refs)
print('--full uses:',len(full),full)
print('shell fallbacks:',len(shells))
for s in shells: print('  ',s)
print('devx errors:',len(errs))
for e in errs: print('  ',e)
print('\nall C commands'); 
for t,rep,cs in runs:
    print('##',t,rep)
    for c,nb,rc,o in cs: print(f'- {c[:170]} | {nb} B | rc={rc}')
