#!/usr/bin/env python3
"""agent benchmark driver: Codex (gpt-6-luna) on fixture F2, arm D (DevX MCP) vs arm N (shell only). Stdlib only.

Isolation: Codex runs with CODEX_HOME=./codex_home (symlinked auth, minimal config, NO AGENTS.md; the real
~/.codex/AGENTS.md tells the agent to use the devx CLI, which would contaminate arm N) and a PATH without ~/.dotnet/tools
(no `devx` CLI in either arm). F2 has no AGENTS.md. ~/.codex/config.toml is never touched.

Event stream (codex exec --json, observed in smoke runs, see results/smoke/*.jsonl):
  thread.started / turn.started / turn.completed{usage:{input_tokens,cached_input_tokens,output_tokens,reasoning_output_tokens}}
  item.started + item.completed with item.type:
    agent_message{text}                         -> not a tool call
    mcp_tool_call{server,tool,arguments,result{content[{text}]},error,status} -> counted once on item.completed (mcp)
    command_execution{command,aggregated_output,exit_code,status} -> counted once on item.completed (shell)
    reasoning                                   -> ignored
    any other type (file_change, web_search...) -> counted in tool_calls_total as 'other'
Tokens: sum of turn.completed.usage over turns (input_tokens already includes cached_input_tokens).
result_bytes: UTF-8 bytes of MCP result text + shell aggregated_output returned to the model.
"""
import argparse, csv, json, os, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
F2 = '<F2>'
B = '<DEVX-BIN>/DevX.Cli'
SID = '<SESSION-F2>'
F3 = '<F3>'
SID3 = '<SESSION-F3>'
# per-task fixture: root dir, DevX session id (preamble text), arm-C CODEX_HOME dir (None = the --codex-home-c option)
FIX = {'f2': dict(root=F2, sid=SID, home=None), 'f3': dict(root=F3, sid=SID3, home='codex_home_c3')}
PATHX = '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:<HOME>/.nvm/versions/node/v24.16.0/bin'
TAIL = 'Answer in at most 5 lines, stating file:line or qualified names exactly.'
def pre(arm, sid=SID):
    return {
 'D': f'A DevX MCP server is attached. Use its tools for every search and read (sessionId {sid}, format: agent); do not use shell for searching or reading files. {TAIL}',
 'N': f'Use shell tools (grep, sed, cat, find). {TAIL}',
 'C': ('The `devx` CLI is on PATH and this repository is indexed; your AGENTS.md explains the commands. Use devx for every search and read; '
       'do not use grep, sed, cat, find or python for searching or reading. ' + TAIL),
    }[arm]
CLIBIN = str(HERE / 'clibin')  # contains symlink devx -> B (d9340e9 build)
COLS = ['task', 'arm', 'rep', 'correct', 'tool_calls_total', 'tool_calls_devx', 'tool_calls_shell', 'tool_calls_mcp', 'tool_calls_other',
        'input_tokens', 'output_tokens', 'cached_tokens', 'result_bytes', 'wall_seconds', 'exit_code', 'timed_out', 'sandbox', 'model']

def parse(path):
    r = dict(devx=0, cmds=[], shell=0, mcp=0, other=0, inp=0, out=0, cached=0, nbytes=0, tools={}, errors=[])
    for line in open(path, errors='replace'):
        try: e = json.loads(line)
        except ValueError: continue
        if e.get('type') == 'turn.completed':
            u = e.get('usage') or {}
            r['inp'] += u.get('input_tokens', 0); r['out'] += u.get('output_tokens', 0); r['cached'] += u.get('cached_input_tokens', 0)
        elif e.get('type') == 'item.completed':
            it = e.get('item') or {}; t = it.get('type')
            if t == 'mcp_tool_call':
                r['mcp'] += 1; k = f"{it.get('server')}.{it.get('tool')}"; r['tools'][k] = r['tools'].get(k, 0) + 1
                for c in ((it.get('result') or {}).get('content') or []): r['nbytes'] += len(c.get('text', '').encode())
                if it.get('error'): r['errors'].append(str(it['error'])[:200])
            elif t == 'command_execution':
                nb = len((it.get('aggregated_output') or '').encode()); cmd = it.get('command') or ''
                inner = cmd.split(' -lc ', 1)[1].strip().strip('\'"') if ' -lc ' in cmd else cmd
                k = 'devx' if inner.lstrip().startswith('devx') else 'shell'
                r['devx' if k == 'devx' else 'shell'] += 1; r['tools'][k] = r['tools'].get(k, 0) + 1
                r['nbytes'] += nb; r['cmds'].append((cmd, nb, it.get('exit_code')))
            elif t not in ('agent_message', 'reasoning', None):
                r['other'] += 1; r['tools'][t] = r['tools'].get(t, 0) + 1
            if t == 'error': r['errors'].append(str(it)[:200])
    return r

def run_one(task, arm, rep, series, sandbox='read-only', codex_home_c='codex_home', dry_run=False, model=None, codex_cfg=(), extra_env=None, codex_flags=(), timeout=300):
    fx = FIX[task.get('fixture', 'f2')]
    out = HERE / 'results' / series
    if not dry_run: out.mkdir(parents=True, exist_ok=True)
    stem = f"{task['id']}-{arm}-r{rep}"
    model = model or 'gpt-6-luna'
    cmd = ['codex', 'exec', '-m', model, '--json', '-C', fx['root'], '--skip-git-repo-check', '-s', sandbox, '--ephemeral',
           '-o', str(out / f'{stem}.answer.txt')]
    for kv in (codex_cfg or ()): cmd += ['-c', kv]
    for fl in (codex_flags or ()): cmd += fl.split()
    if arm == 'D':
        cmd += ['-c', f'mcp_servers.devx.command="{B}"', '-c', 'mcp_servers.devx.args=["mcp","serve"]',
                '-c', 'mcp_servers.devx.default_tools_approval_mode="approve"']
    cmd.append(pre(arm, fx['sid']) + ' ' + task['prompt'])
    env = {'HOME': os.environ['HOME'], 'PATH': (CLIBIN + ':' + PATHX) if arm == 'C' else PATHX, 'CODEX_HOME': str(HERE / ((fx['home'] or codex_home_c) if arm == 'C' else 'codex_home'))}
    env.update(extra_env or {})
    if dry_run:
        print(f"DRYRUN {stem} fixture={task.get('fixture', 'f2')} sandbox={sandbox} model={model}\n  argv={cmd}\n  PATH={env['PATH']}\n  CODEX_HOME={env['CODEX_HOME']} extra_env_keys={sorted(extra_env or {})}", flush=True)
        return None
    t0 = time.time(); timed_out = False
    with open(out / f'{stem}.jsonl', 'w') as jf, open(out / f'{stem}.err', 'w') as ef:
        try:
            rc = subprocess.run(cmd, env=env, stdin=subprocess.DEVNULL, stdout=jf, stderr=ef, timeout=timeout).returncode
        except subprocess.TimeoutExpired:
            rc, timed_out = -1, True
    wall = time.time() - t0
    ans = ''
    try: ans = (out / f'{stem}.answer.txt').read_text()
    except OSError: pass
    p = parse(out / f'{stem}.jsonl')
    row = dict(task=task['id'], arm=arm, rep=rep, correct=int(all(x in ans for x in task['expected'])),
               tool_calls_total=p['devx'] + p['shell'] + p['mcp'] + p['other'], tool_calls_devx=p['devx'], tool_calls_shell=p['shell'], tool_calls_mcp=p['mcp'],
               tool_calls_other=p['other'], input_tokens=p['inp'], output_tokens=p['out'], cached_tokens=p['cached'],
               result_bytes=p['nbytes'], wall_seconds=round(wall, 1), exit_code=rc, timed_out=int(timed_out), sandbox=sandbox, model=model)
    json.dump(p['cmds'], open(out / f'{stem}.cmds.json', 'w'), indent=1)
    csv_path = out / 'rows.csv'; new = not csv_path.exists()
    with open(csv_path, 'a', newline='') as f:
        w = csv.DictWriter(f, COLS); 
        if new: w.writeheader()
        w.writerow(row)
    print(f"{stem}: correct={row['correct']} calls={row['tool_calls_total']} (devx {p['devx']}/shell {p['shell']}/mcp {p['mcp']}) "
          f"in={p['inp']} out={p['out']} bytes={p['nbytes']} wall={row['wall_seconds']}s rc={rc} tools={p['tools']}", flush=True)
    return row

def table(rows):
    print('\narm | n | correct | calls (shell/mcp) | input_tokens | output_tokens | result_bytes | wall_seconds')
    m = {}
    for a in 'DNC':
        rs = [r for r in rows if r['arm'] == a]
        if not rs: continue
        n = len(rs); av = lambda k: sum(r[k] for r in rs) / n
        m[a] = dict(calls=av('tool_calls_total'), inp=av('input_tokens'))
        print(f"{a} | {n} | {av('correct'):.2f} | {av('tool_calls_total'):.1f} ({av('tool_calls_shell'):.1f}/{av('tool_calls_mcp'):.1f}) | "
              f"{av('input_tokens'):.0f} | {av('output_tokens'):.0f} | {av('result_bytes'):.0f} | {av('wall_seconds'):.1f}")
    if 'D' in m and 'N' in m:
        pc = lambda a, b: 'n/a' if not b else f'{100 * a / b:.0f}%'
        print(f"savings: arm D calls = {pc(m['D']['calls'], m['N']['calls'])} of arm N; arm D input tokens = {pc(m['D']['inp'], m['N']['inp'])} of arm N")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--series', required=True); ap.add_argument('--tasks', default='trial', help="'trial', 'all' or comma ids")
    ap.add_argument('--arm', default='DN', help="'DN' (paired, default) or 'C'")
    ap.add_argument('--codex-home-c', default='codex_home', help='CODEX_HOME dir (relative to this script) for arm C; series 2 uses codex_home_c (shipped AGENTS.md)')
    ap.add_argument('--reps', type=int, default=1)
    ap.add_argument('--tasks-file', default='tasks.json', help='task list JSON relative to this script; a task may carry "fixture": "f2"|"f3"')
    ap.add_argument('--sandbox-c', default=None, choices=['read-only', 'workspace-write'], help='sandbox for arm C (overrides the CN default of workspace-write)')
    ap.add_argument('--dry-run', action='store_true', help='print the codex exec argv and env per run, execute nothing')
    ap.add_argument('--sandbox', default='read-only', choices=['read-only', 'workspace-write'], help='Codex sandbox mode (default read-only: arms D and N)')
    ap.add_argument('--model', default=None, help='codex model passed as -m to both arms (default gpt-6-luna, the original hardcoded model)')
    ap.add_argument('--codex-config', action='append', default=[], help='key=value passed as -c to codex exec (both arms), repeatable')
    ap.add_argument('--env-file', default=None, help='file of KEY=VALUE lines loaded into the run env (values never logged)')
    ap.add_argument('--codex-flag', action='append', default=[], help='raw flag(s) passed to codex exec (both arms), repeatable; split on spaces')
    ap.add_argument('--timeout', type=int, default=300, help='per-run timeout seconds (default 300)')
    a = ap.parse_args()
    xenv = {}
    if a.env_file:
        for ln in open(os.path.expanduser(a.env_file)):
            if '=' in ln and not ln.lstrip().startswith('#'): k, v = ln.strip().split('=', 1); xenv[k.strip()] = v.strip().strip('\'"')
    tasks = json.load(open(HERE / a.tasks_file))
    sel = [t for t in tasks if t.get('trial')] if a.tasks == 'trial' else tasks if a.tasks == 'all' else [t for t in tasks if t['id'] in a.tasks.split(',')]
    rows = []
    for rep in range(1, a.reps + 1):
        for i, t in enumerate(sel):
            order = ('C', 'N') if (i + rep) % 2 == 1 else ('N', 'C')
            for arm in ((a.arm,) if a.arm == 'C' else order if a.arm == 'CN' else ('D', 'N') if (i + rep) % 2 == 1 else ('N', 'D')):
                # CN: workspace-write applies to arm C only; N stays read-only
                sb = a.sandbox if a.arm != 'CN' else ('workspace-write' if arm == 'C' else 'read-only')
                if arm == 'C' and a.sandbox_c: sb = a.sandbox_c
                r = run_one(t, arm, rep, a.series, sb, a.codex_home_c, a.dry_run, a.model, a.codex_config, xenv, a.codex_flag, a.timeout)
                if r: rows.append(r)
    if not a.dry_run: table(rows)

if __name__ == '__main__':
    main()
