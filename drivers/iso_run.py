#!/usr/bin/env python3
"""Isolation: 4 single-request Codex runs (trivial prompt)."""
import json, os, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
F2 = '<F2>'
B = '<DEVX-BIN>/DevX.Cli'
PATHX = '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:<HOME>/.nvm/versions/node/v24.16.0/bin'
dev = ['-c', f'mcp_servers.devx.command="{B}"', '-c', 'mcp_servers.devx.args=["mcp","serve"]',
       '-c', 'mcp_servers.devx.default_tools_approval_mode="approve"']
dum = ['-c', 'mcp_servers.dummy.command="python3"', '-c', f'mcp_servers.dummy.args=["{HERE}/dummy_mcp.py"]',
       '-c', 'mcp_servers.dummy.default_tools_approval_mode="approve"']
RUNS = {'A0': [], 'A1': dev, 'A2': dum, 'A3': dev + ['-c', 'mcp_servers.devx.enabled_tools=["search","read"]']}
name = sys.argv[1]
out = HERE / 'results' / 'iso'; out.mkdir(parents=True, exist_ok=True)
cmd = ['codex', 'exec', '-m', 'gpt-6-luna', '--json', '-C', F2, '--skip-git-repo-check', '-s', 'read-only', '--ephemeral',
       '-o', str(out / f'{name}.answer.txt')] + RUNS[name] + ['Reply with the single word OK and nothing else.']
env = {'HOME': os.environ['HOME'], 'PATH': PATHX, 'CODEX_HOME': str(HERE / 'codex_home')}
with open(out / f'{name}.jsonl', 'w') as jf, open(out / f'{name}.err', 'w') as ef:
    rc = subprocess.run(cmd, env=env, stdin=subprocess.DEVNULL, stdout=jf, stderr=ef, timeout=200).returncode
u = [json.loads(l).get('usage') for l in open(out / f'{name}.jsonl') if '"turn.completed"' in l]
print(name, rc, u)
