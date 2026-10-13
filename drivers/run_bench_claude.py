#!/usr/bin/env python3
"""Claude Code backend for the held-out benchmark (arm C = DevX CLI + shipped guidance, arm N = native tools). Stdlib only.

Imports prompt text, fixtures, CLIBIN and PATH from run_bench.py (not modified). Isolation: the user's global CLAUDE.md is
excluded with CLAUDE_CODE_DISABLE_CLAUDE_MDS=1 + CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 (auth kept: no --bare, no CLAUDE_CONFIG_DIR) and
--setting-sources project,local; all CLAUDE* env vars of the parent session are dropped. Guidance for arm C is delivered with
--append-system-prompt-file. Stream: claude -p --output-format stream-json --verbose (assistant/user/result events).
"""
import argparse, csv, hashlib, json, os, subprocess, sys, time
from pathlib import Path
import run_bench as rb

HERE = rb.HERE
RO = ' Do not modify, create or delete any files.'
COLS = ['task', 'arm', 'rep', 'correct', 'tool_calls_total', 'tool_calls_devx', 'tool_calls_shell', 'tool_calls_mcp', 'tool_calls_other',
        'input_tokens', 'output_tokens', 'cached_tokens', 'result_bytes', 'wall_seconds', 'exit_code', 'timed_out', 'sandbox', 'model', 'backend']
BASE = ['claude', '-p', '--output-format', 'stream-json', '--verbose', '--no-session-persistence', '--setting-sources', 'project,local',
        '--permission-mode', 'acceptEdits', '--allowedTools', 'Bash', 'Read', 'Grep', 'Glob', '--disallowedTools', 'Edit', 'Write', 'NotebookEdit']

def env_for(arm):
    env = {k: v for k, v in os.environ.items() if not k.startswith(('CLAUDE', 'ANTHROPIC'))}
    env['PATH'] = (rb.CLIBIN + ':' + rb.PATHX) if arm == 'C' else rb.PATHX
    env['CLAUDE_CODE_DISABLE_CLAUDE_MDS'] = '1'; env['CLAUDE_CODE_DISABLE_AUTO_MEMORY'] = '1'
    return env

def build_cmd(task, arm, model):
    fx = rb.FIX[task.get('fixture', 'f2')]
    cmd = BASE + ['--model', model]
    if arm == 'C': cmd += ['--append-system-prompt-file', str(HERE / f"claude_guidance_c_{task.get('fixture', 'f2')}.md")]
    cmd.append(rb.pre(arm, fx['sid']) + RO + ' ' + task['prompt'])
    return cmd

def parse(path):
    r = dict(devx=0, shell=0, other=0, inp=0, out=0, cached=0, nbytes=0, cmds=[], tools={}, answer='', errors=[])
    uses = {}; usage = {}
    for line in open(path, errors='replace'):
        try: e = json.loads(line)
        except ValueError: continue
        t = e.get('type')
        if t == 'assistant' and not e.get('parent_tool_use_id'):
            m = e.get('message') or {}
            if m.get('id') and m.get('usage'): usage[m['id']] = m['usage']
            for b in m.get('content') or []:
                if b.get('type') == 'tool_use':
                    inp = b.get('input') or {}; name = b.get('name')
                    cmd = inp.get('command') if name == 'Bash' else None
                    k = ('devx' if (cmd or '').lstrip().startswith('devx') else 'shell') if name == 'Bash' else 'other'
                    r['devx' if k == 'devx' else 'shell' if k == 'shell' else 'other'] += 1
                    r['tools'][name if k == 'other' else k] = r['tools'].get(name if k == 'other' else k, 0) + 1
                    uses[b['id']] = dict(tool=name, kind=k, command=cmd if cmd is not None else json.dumps(inp)[:300], bytes=0, is_error=False)
        elif t == 'user' and not e.get('parent_tool_use_id'):
            c = (e.get('message') or {}).get('content')
            if isinstance(c, list):
                for b in c:
                    if b.get('type') == 'tool_result':
                        x = b.get('content'); s = x if isinstance(x, str) else ''.join(i.get('text', '') for i in (x or []) if isinstance(i, dict))
                        nb = len((s or '').encode()); r['nbytes'] += nb
                        u = uses.get(b.get('tool_use_id'))
                        if u: u['bytes'] = nb; u['is_error'] = bool(b.get('is_error'))
        elif t == 'result':
            r['answer'] = e.get('result') or ''
            if e.get('is_error'): r['errors'].append(str(e.get('result'))[:300])
    for u in usage.values():
        r['inp'] += u.get('input_tokens', 0) + u.get('cache_read_input_tokens', 0) + u.get('cache_creation_input_tokens', 0)
        r['out'] += u.get('output_tokens', 0); r['cached'] += u.get('cache_read_input_tokens', 0)
    r['cmds'] = list(uses.values())
    return r

def listing(root):
    lines = []
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x != '.devx')
        for f in sorted(files):
            p = Path(d) / f
            try: lines.append(f"./{p.relative_to(root)} {p.stat().st_size} {int(p.stat().st_mtime)} {hashlib.sha256(p.read_bytes()).hexdigest()}")
            except OSError: lines.append(f"./{p.relative_to(root)} UNREADABLE")
    return '\n'.join(sorted(lines)) + '\n'

def run_one(task, arm, rep, series, model, dry_run=False):
    out = HERE / 'results' / series; stem = f"{task['id']}-{arm}-r{rep}"; cmd = build_cmd(task, arm, model); fx = rb.FIX[task.get('fixture', 'f2')]
    if dry_run:
        print(f"DRYRUN {stem} cwd={fx['root']}\n  argv={cmd}\n  PATH={env_for(arm)['PATH']}", flush=True); return None
    out.mkdir(parents=True, exist_ok=True); t0 = time.time(); timed_out = False
    with open(out / f'{stem}.jsonl', 'w') as jf, open(out / f'{stem}.err', 'w') as ef:
        try: rc = subprocess.run(cmd, cwd=fx['root'], env=env_for(arm), stdin=subprocess.DEVNULL, stdout=jf, stderr=ef, timeout=600).returncode
        except subprocess.TimeoutExpired: rc, timed_out = -1, True
    wall = time.time() - t0; p = parse(out / f'{stem}.jsonl')
    (out / f'{stem}.answer.txt').write_text(p['answer'])
    json.dump(p['cmds'], open(out / f'{stem}.cmds.json', 'w'), indent=1)
    row = dict(task=task['id'], arm=arm, rep=rep, correct=int(all(x in p['answer'] for x in task['expected'])),
               tool_calls_total=p['devx'] + p['shell'] + p['other'], tool_calls_devx=p['devx'], tool_calls_shell=p['shell'], tool_calls_mcp=0,
               tool_calls_other=p['other'], input_tokens=p['inp'], output_tokens=p['out'], cached_tokens=p['cached'], result_bytes=p['nbytes'],
               wall_seconds=round(wall, 1), exit_code=rc, timed_out=int(timed_out), sandbox='instruction', model=model, backend='claude')
    cp = out / 'rows.csv'; new = not cp.exists()
    with open(cp, 'a', newline='') as f:
        w = csv.DictWriter(f, COLS)
        if new: w.writeheader()
        w.writerow(row)
    print(f"{stem}: correct={row['correct']} calls={row['tool_calls_total']} in={p['inp']} out={p['out']} bytes={p['nbytes']} wall={row['wall_seconds']}s rc={rc} tools={p['tools']}", flush=True)
    return row

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--series', required=True); ap.add_argument('--model', required=True); ap.add_argument('--tasks', default='all')
    ap.add_argument('--tasks-file', default='tasks_heldout.json'); ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    tasks = json.load(open(HERE / a.tasks_file))
    sel = tasks if a.tasks == 'all' else [t for t in tasks if t['id'] in a.tasks.split(',')]
    R = HERE / 'results'
    if not a.dry_run:
        R.mkdir(exist_ok=True)
        for k in ('f2', 'f3'): (R / f'{k}-before-{a.series}.txt').write_text(listing(rb.FIX[k]['root']))
    for i, t in enumerate(sel):
        for arm in (('C', 'N') if (i + 1) % 2 == 1 else ('N', 'C')):
            run_one(t, arm, 1, a.series, a.model, a.dry_run)
    if not a.dry_run:
        for k in ('f2', 'f3'): (R / f'{k}-after-{a.series}.txt').write_text(listing(rb.FIX[k]['root']))
        same = all((R / f'{k}-before-{a.series}.txt').read_text() == (R / f'{k}-after-{a.series}.txt').read_text() for k in ('f2', 'f3'))
        print(f"LISTINGS_IDENTICAL={same}", flush=True)

if __name__ == '__main__':
    main()
