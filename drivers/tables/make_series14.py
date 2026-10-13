import csv, json, random, re, shutil, os, collections
R = 'results/series14'
KEY = '<SCRATCH>/blind14-key/key.csv'
rows = list(csv.DictReader(open(f'{R}/rows.csv')))
tasks = {t['id']: t for t in json.load(open('tasks_heldout.json'))}
order = [t for t in tasks]
if os.path.exists('results/series14.log') and not os.path.exists(f'{R}/series14.log'):
    shutil.copy('results/series14.log', f'{R}/series14.log')
for r in rows:
    for k in ('correct', 'tool_calls_devx', 'tool_calls_shell', 'tool_calls_mcp', 'tool_calls_other', 'input_tokens', 'output_tokens', 'result_bytes', 'exit_code', 'timed_out'):
        r[k] = int(r[k])
    r['wall'] = float(r['wall_seconds'])
    r['calls'] = r['tool_calls_devx'] + r['tool_calls_shell'] + r['tool_calls_mcp']  # excludes the 'Model metadata not found' error item
by = {(r['task'], r['arm']): r for r in rows}
# blind pack
os.makedirs(f'{R}/blind', exist_ok=True); os.makedirs(os.path.dirname(KEY), exist_ok=True)
if not os.path.exists(KEY):
    pairs = [(t, a) for t in order for a in 'CN']
    random.Random(14).shuffle(pairs)
    with open(KEY, 'w', newline='') as kf, open(f'{R}/blind/blind-index.csv', 'w', newline='') as bf:
        kw = csv.writer(kf); bw = csv.writer(bf); kw.writerow(['blind_id', 'task', 'arm']); bw.writerow(['blind_id', 'task', 'question', 'expected'])
        for i, (t, a) in enumerate(pairs, 1):
            b = f'A{i:02d}'
            shutil.copy(f'{R}/{t}-{a}-r1.answer.txt', f'{R}/blind/{b}.answer.txt')
            kw.writerow([b, t, a]); bw.writerow([b, t, tasks[t]['prompt'], tasks[t]['expected']])
def agg(ts):
    o = {}
    for a in 'CN':
        rs = [by[(t, a)] for t in ts]
        o[a] = (sum(r['calls'] for r in rs), sum(r['input_tokens'] for r in rs), sum(r['result_bytes'] for r in rs))
    return o
def line(name, ts):
    o = agg(ts); c, n = o['C'], o['N']
    p = lambda x, y: f'{round(100*x/y)}%' if y else 'n/a'
    return f'{name} (n={len(ts)}): calls C {c[0]} vs N {n[0]} ({p(c[0],n[0])} of N); input tokens C {c[1]} vs N {n[1]} ({p(c[1],n[1])}); result bytes C {c[2]} vs N {n[2]} ({p(c[2],n[2])})'
both = [t for t in order if by[(t, 'C')]['correct'] and by[(t, 'N')]['correct']]
out = []
w = out.append
w('# Series 14: held-out 12 tasks on Qwen3.6-27B (fp8) via DeepInfra through Codex\n')
w('Working data, not part of the evidence set (maintainer decision 2026-10-12).\n')
w('Model `Qwen/Qwen3.6-27B` (DeepInfra, fp8, 262k context, $0.32/M in, $3.20/M out), passed with `-m` to both arms; run-1 jsonl/rows.csv carry that id. Provider via `-c` overrides only: `model_provider="deepinfra"`, `model_providers.deepinfra.name="DeepInfra"`, `.base_url="https://api.deepinfra.com/v1/openai"`, `.env_key="DEEPINFRA_API_KEY"`, `.wire_api="responses"`; key loaded by `--env-file` from outside the repo, never logged. Per-run argv: `codex exec -m Qwen/Qwen3.6-27B --json -C <fixture> --skip-git-repo-check -s read-only --ephemeral -o <answer> -c ... <prompt>`; arm C CODEX_HOME=codex_home_c (shipped AGENTS.md, clibin on PATH), arm N codex_home. Driver: `run_bench.py --series series14 --tasks all --tasks-file tasks_heldout.json --arm CN --codex-home-c codex_home_c --sandbox-c read-only --env-file ... --model Qwen/Qwen3.6-27B --timeout 300 --codex-config ...` (script run_series14.sh). Reasoning effort: codex config `medium` (not sent as a provider-tuned setting; thinking mode untouched; usage reports reasoning_output_tokens 0 in every probe). DevX: clibin, same as series 5-13 (1.6.14+04a02ef). Fixture listings with sha256 before/after identical (f2, f3). Blind pack: results/series14/blind/ (A01..A24, blind-index.csv); key only in scratchpad blind14-key. Correctness below is the automated scorer, blinded rescore pending.\n')
w('Probes (2 of 3 allowed): (1) "Reply with the single word ok." rc 0, text "ok", usage 25308 in / 19 out; (2) "Run `ls` and report the first entry." rc 0, one command_execution, answer "The first entry is `R.md`.", 51174 in / 76 out. Both emit a "Model metadata for `Qwen/Qwen3.6-27B` not found" warning (counted by parse() as an `other` item, excluded from calls here) and a cosmetic "failed to refresh available models" decode error.\n')
tl = open('results/trial-qwen-di/trial.log').read().splitlines()
w('Trial (6 runs, tasks H-L1,H-R1,H-S2 both arms, gate: >=4/6 automated-correct and <=1 harness failure): 6/6 correct, 0 harness failures, gate PASS.\n')
w('| run | correct | calls | input tok | wall s |\n|--|--|--|--|--|')
for l in tl:
    m = re.match(r'(\S+-r1): correct=(\d) calls=(\d+) \(devx (\d+)/shell (\d+)/mcp (\d+)\) in=(\d+).*wall=([\d.]+)s', l)
    if m: w(f'| {m[1]} | {m[2]} | {int(m[4])+int(m[5])+int(m[6])} | {m[7]} | {m[8]} |')
w('')
for a in 'CN':
    rs = [by[(t, a)] for t in order]
    w(f'Wall time arm {a}: {sum(r["wall"] for r in rs):.1f} s (sum of 12 runs)')
    w(f'Arm {a} correct: automated {sum(r["correct"] for r in rs)}/12; blinded rescore pending')
w('')
w('| task | arm | auto correct | calls (devx/shell) | input tok | result bytes | wall s | exit |\n|--|--|--|--|--|--|--|--|')
for t in order:
    for a in 'CN':
        r = by[(t, a)]
        w(f'| {t} | {a} | {r["correct"]} | {r["calls"]} ({r["tool_calls_devx"]}/{r["tool_calls_shell"]+r["tool_calls_mcp"]}) | {r["input_tokens"]} | {r["result_bytes"]} | {r["wall"]} | {r["exit_code"]} |')
w('')
w('S14 both-correct (automated) ' + line('', both).lstrip())
w('S14 all 12 (automated) ' + line('', order).lstrip())
w('')
w('Token accounting per run (DeepInfra reports no cached tokens: cache-read 0, so new input = cumulative input; output):\n| task | arm | cumulative input | cache-read | new input | output |\n|--|--|--|--|--|--|')
for t in order:
    for a in 'CN':
        r = by[(t, a)]; w(f'| {t} | {a} | {r["input_tokens"]} | 0 | {r["input_tokens"]} | {r["output_tokens"]} |')
w('')
w('Verified earlier series (copied from SERIES13.md):')
for l in open('SERIES13.md'):
    if re.match(r'- S(5|6|7|8|9|10|11|13) ', l) and 'VERIFIED' in l or re.match(r'- S(5|6) all', l) or re.match(r'- S(7|8|9|10|11) all', l):
        w(l.rstrip())
w('')
zero = [f'{r["task"]}-{r["arm"]}' for r in rows if r['calls'] == 0]
w('Zero-tool-call (zero counted calls) runs: ' + (', '.join(zero) if zero else 'none'))
for z in zero:
    t, a = z.rsplit('-', 1)
    jl = open(f'{R}/{t}-{a}-r1.jsonl').read()
    cm = [json.loads('"'+x+'"') for x in re.findall(r'"command":"((?:[^"\\]|\\.)*)"', jl)]
    w(f'- {z}: a command was started (`{cm[0] if cm else "?"}`, no completion event, so the parser counted 0 calls and 0 bytes) and the model then answered from memory without file evidence; automated correct={by[(t,a)]["correct"]}')
emp = [f'{r["task"]}-{r["arm"]}' for r in rows if os.path.getsize(f'{R}/{r["task"]}-{r["arm"]}-r1.answer.txt') < 5]
w('Empty-answer runs: ' + (', '.join(emp) if emp else 'none'))
bad = [f'{r["task"]}-{r["arm"]}' for r in rows if r['exit_code'] or r['timed_out']]
w('Non-zero exit or timed out: ' + (', '.join(bad) if bad else 'none'))
w('')
w('C used more calls or bytes than N:')
for t in order:
    c, n = by[(t, 'C')], by[(t, 'N')]
    if c['calls'] > n['calls'] or c['result_bytes'] > n['result_bytes']:
        w(f'- {t}: calls C {c["calls"]} vs N {n["calls"]}; bytes C {c["result_bytes"]} vs N {n["result_bytes"]}')
w('')
w('Arm C devx non-zero exits and non-devx shell fallbacks (task, command, exit):')
any_ = False
for t in order:
    for cmd, nb, ex in json.load(open(f'{R}/{t}-C-r1.cmds.json')):
        inner = re.sub(r"^/bin/zsh -lc ['\"]?", '', cmd)
        isdevx = bool(re.match(r'(cd \S+ && )?devx ', inner))
        if ex not in (0, None) or not isdevx:
            any_ = True; w(f'- {t}: {inner[:160]} (exit {ex})')
if not any_: w('- none')
w('')
w('Locate tasks bytes C/N: ' + '; '.join(f'{t} C {by[(t,"C")]["result_bytes"]} / N {by[(t,"N")]["result_bytes"]}' for t in ('H-L1', 'H-L2', 'H-L3')))
ti = sum(r['input_tokens'] for r in rows); to = sum(r['output_tokens'] for r in rows)
w(f'\nApproximate spend (series): {ti} input tok x $0.32/M + {to} output tok x $3.20/M = ${ti*0.32/1e6 + to*3.2/1e6:.3f} (trial + 2 probes add roughly $0.05).')
open('SERIES14.md', 'w').write('\n'.join(out) + '\n')
print(line('both', both)); print(line('all12', order)); print(len(both), 'both-correct')
for a in 'CN': print(a, sum(by[(t,a)]['correct'] for t in order), round(sum(by[(t,a)]['wall'] for t in order),1))
print(f'spend ${ti*0.32/1e6 + to*3.2/1e6:.3f}', ti, to)
