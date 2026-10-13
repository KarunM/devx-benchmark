#!/usr/bin/env python3
"""Export per-run and per-configuration data for the nine admitted series. Deterministic, no network.
Run: python3 export_runs.py   -> article/data/all-runs.csv, article/data/per-configuration.csv
Join/adjustment logic copied from make_charts.py (verdicts, series 5 from SERIES5.md, 'Model metadata' pseudo-call for 7/14)."""
import csv, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
OUT = os.path.join(HERE, "article", "data")
CONFIGS = [(5, "gpt-6-luna", "Codex"), (6, "gpt-5.6-luna", "Codex"), (7, "DeepSeek Flash 4.1", "Codex"),
           (8, "Sonnet 5.5", "Claude Code"), (9, "Sonnet 5", "Claude Code"), (10, "Opus 5.5", "Claude Code"),
           (11, "gpt-6-sol", "Codex"), (13, "Fable 5.1", "Claude Code"), (14, "Qwen3.6-27B fp8", "Codex")]
EXCLUDED_CHART = {5: {"H-R2"}}  # chart-1 basis drops the series 5 outlier

def read_csv(p):
    with open(p, newline="") as f:
        return list(csv.DictReader(f))

def pseudo(series, task, arm):
    with open(os.path.join(RES, "series%d" % series, "%s-%s-r1.jsonl" % (task, arm)), errors="replace") as f:
        return 1 if "Model metadata" in f.read() else 0

def load_series5():
    ver = {}
    with open(os.path.join(HERE, "SERIES5.md")) as f:
        for line in f:
            m = re.match(r"\|\s*(H-\w+)\s*\|\s*\w+\s*\|\s*f\d\s*\|\s*([CN])\s*\|\s*[\w-]+\s*\|\s*(\d)\s*\|\s*(\d)\s*\|\s*(\d+) \(", line)
            if m:
                ver[(m.group(1), m.group(2))] = (int(m.group(4)) == 1, int(m.group(5)))
    assert len(ver) == 24
    return ver

def verdicts(series, rows):
    if series == 5:
        ver = load_series5()
        for r in rows:
            assert int(r["tool_calls_total"]) == ver[(r["task"], r["arm"])][1]
        return {k: v[0] for k, v in ver.items()}
    return {(r["task"], r["arm"]): r["verdict"] == "correct"
            for r in read_csv(os.path.join(RES, "series%d" % series, "rescore%d.csv" % series))}

tasks = {t["id"]: t for t in json.load(open(os.path.join(HERE, "tasks_heldout.json")))}
runs, cfg = [], []
for s, label, harness in CONFIGS:
    rows = read_csv(os.path.join(RES, "series%d" % s, "rows.csv"))
    ver = verdicts(s, rows)
    assert len(rows) == 24
    recs = {}
    for r in rows:
        k = (r["task"], r["arm"])
        calls = int(r["tool_calls_total"]) - (pseudo(s, *k) if s in (7, 14) else 0)
        recs[k] = dict(series=s, model=label, harness=harness, task=r["task"], kind=tasks[r["task"]]["kind"],
                       fixture=tasks[r["task"]]["fixture"], arm="DevX" if r["arm"] == "C" else "native",
                       verified_correct=int(ver[k]), tool_calls=calls, tool_calls_devx=int(r["tool_calls_devx"]),
                       tool_calls_shell=int(r["tool_calls_shell"]), input_tokens=int(r["input_tokens"]),
                       cached_tokens=int(r["cached_tokens"]) if r.get("cached_tokens") != "" else "",
                       output_tokens=int(r["output_tokens"]), result_bytes=int(r["result_bytes"]),
                       wall_seconds=float(r["wall_seconds"]))
    ids = sorted({t for t, _ in recs})
    bc = [t for t in ids if ver[(t, "C")] and ver[(t, "N")]]
    for (t, a), rec in sorted(recs.items(), key=lambda kv: (kv[0][0], kv[0][1] != "C")):
        rec["both_correct"] = int(t in bc)
        runs.append(rec)
    basis = [t for t in bc if t not in EXCLUDED_CHART.get(s, ())]
    sm = lambda a, m: sum(recs[(t, a)][m] for t in basis)
    c = dict(series=s, model=label, harness=harness, n_both_correct=len(basis), n_both_correct_all=len(bc))
    for a, nm in (("C", "devx"), ("N", "native")):
        c["calls_" + nm] = sm(a, "tool_calls"); c["input_tokens_" + nm] = sm(a, "input_tokens"); c["result_bytes_" + nm] = sm(a, "result_bytes")
    c["calls_pct"] = round(100.0 * c["calls_devx"] / c["calls_native"], 1)
    c["tokens_pct"] = round(100.0 * c["input_tokens_devx"] / c["input_tokens_native"], 1)
    c["bytes_pct"] = round(100.0 * c["result_bytes_devx"] / c["result_bytes_native"], 1)
    c["correct_devx"] = sum(ver[(t, "C")] for t in ids); c["correct_native"] = sum(ver[(t, "N")] for t in ids)
    cfg.append(c)

os.makedirs(OUT, exist_ok=True)
for name, rows in (("all-runs.csv", runs), ("per-configuration.csv", cfg)):
    with open(os.path.join(OUT, name), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n"); w.writeheader(); w.writerows(rows)
print("all-runs rows", len(runs), "per-configuration rows", len(cfg))
for c in cfg:
    print(c["series"], c["n_both_correct"], c["calls_devx"], c["calls_native"], c["calls_pct"], c["tokens_pct"], c["bytes_pct"], c["correct_devx"], c["correct_native"])
