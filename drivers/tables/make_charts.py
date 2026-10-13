#!/usr/bin/env python3
"""Regenerate the five article charts from results/series<N>/rows.csv joined with verified verdicts.
Run: python3 make_charts.py   (no network; deterministic).  Writes article/charts/*.png|svg and CHARTS.md.
Every figure is recomputed and checked against FACTS values before drawing; a mismatch skips that chart."""
import csv, json, os, re, statistics, sys, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
OUT = os.path.join(HERE, "article", "charts")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "axes.titlesize": 15, "axes.labelsize": 12, "svg.fonttype": "none",
                     "axes.spines.top": False, "axes.spines.right": False})
CB = {"calls": "#0072B2", "tokens": "#E69F00", "bytes": "#009E73", "devx": "#0072B2", "native": "#D55E00"}

CONFIGS = [  # series, label, harness
    (5, "gpt-6-luna", "Codex"), (6, "gpt-5.6-luna", "Codex"), (7, "DeepSeek Flash 4.1", "Codex"),
    (8, "Sonnet 5.5", "Claude Code"), (9, "Sonnet 5", "Claude Code"), (10, "Opus 5.5", "Claude Code"),
    (11, "gpt-6-sol", "Codex"), (13, "Fable 5.1", "Claude Code"), (14, "Qwen3.6-27B fp8", "Codex"),
]
# FACTS expectations: (calls C, calls N, tok C, tok N, bytes C, bytes N) raw where FACTS gives them, else None; plus rounded %
EXP = {
 5: dict(n=8, raw=(9, 12, 240425, 271897, 12701, 24152), pct=(75, 88, 53), ids="F-LA-3, F-MM-1"),
 6: dict(n=12, raw=(22, 20, 438875, 423045, 42090, 1167598), pct=(110, 104, 4), ids="F-MM-2"),
 7: dict(n=12, raw=(19, 34, 1097629, 1599417, 26768, 33848), pct=(56, 69, 79), ids="F-MM-3"),
 8: dict(n=11, raw=(16, 18, 539293, 537944, 22630, 14550), pct=(89, 100, 156), ids="F-MM-4"),
 9: dict(n=10, raw=(17, 29, 774121, 1052377, 31743, 18509), pct=(59, 74, 172), ids="F-MM-6"),
 10: dict(n=11, raw=(18, 23, 584399, 635280, 23973, 14826), pct=(78, 92, 162), ids="F-FM-1"),
 11: dict(n=11, raw=(17, 19, 405640, 422764, 22448, 76422), pct=(89, 96, 29), ids="F-FM-2"),
 13: dict(n=12, raw=(16, 22, 610717, 702698, 20850, 13020), pct=(73, 87, 160), ids="F-FM-3"),
 14: dict(n=None, raw=None, pct=(48, 65, 45), ids="F-FM-4"),
}
EXP_CORRECT = {5: (10, 10), 6: (12, 12), 7: (12, 12), 8: (12, 11), 9: (12, 10), 10: (11, 11), 11: (12, 11), 13: (12, 12), 14: (11, None)}
FACTS_TOTAL = (104, 98)  # F-FM-6 nine-configuration totals

def read_csv(p):
    with open(p, newline="") as f:
        return list(csv.DictReader(f))

def pseudo(series, task, arm):
    """1 if the run's jsonl carries the Codex 'Model metadata ... not found' warning counted as an 'other' call."""
    p = os.path.join(RES, "series%d" % series, "%s-%s-r1.jsonl" % (task, arm))
    with open(p, errors="replace") as f:
        return 1 if "Model metadata" in f.read() else 0

def load_series5():
    ver = {}
    with open(os.path.join(HERE, "SERIES5.md")) as f:
        for line in f:
            m = re.match(r"\|\s*(H-\w+)\s*\|\s*\w+\s*\|\s*f\d\s*\|\s*([CN])\s*\|\s*[\w-]+\s*\|\s*(\d)\s*\|\s*(\d)\s*\|\s*(\d+) \(", line)
            if m:
                ver[(m.group(1), m.group(2))] = (int(m.group(4)) == 1, int(m.group(5)))
    assert len(ver) == 24, len(ver)
    return ver

def load(series):
    rows = read_csv(os.path.join(RES, "series%d" % series, "rows.csv"))
    if series == 5:
        ver = load_series5(); chk = {(r["task"], r["arm"]): int(r["tool_calls_total"]) for r in rows}
        for k, (ok, calls) in ver.items():
            assert chk[k] == calls, ("series5 calls vs SERIES5.md", k)
        verdict = {k: v[0] for k, v in ver.items()}
    else:
        verdict = {(r["task"], r["arm"]): r["verdict"] == "correct"
                   for r in read_csv(os.path.join(RES, "series%d" % series, "rescore%d.csv" % series))}
    d = {}
    for r in rows:
        k = (r["task"], r["arm"])
        calls = int(r["tool_calls_total"])
        if series in (7, 14):
            calls -= pseudo(series, r["task"], r["arm"])
        d[k] = dict(calls=calls, tokens=int(r["input_tokens"]), bytes=int(r["result_bytes"]), ok=verdict[k])
    assert len(d) == 24
    return d

def basis(d, tasks):
    s = {a: {m: sum(d[(t, a)][m] for t in tasks) for m in ("calls", "tokens", "bytes")} for a in "CN"}
    return s

def both_correct(d):
    tasks = sorted({t for t, _ in d})
    return [t for t in tasks if d[(t, "C")]["ok"] and d[(t, "N")]["ok"]]

DATA, TABLE, STATUS, LOG = {}, {}, {}, []
def log(s):
    print(s); LOG.append(s)

for s, label, harness in CONFIGS:
    d = load(s); DATA[s] = d
    bc = both_correct(d)
    if s == 5:
        log("series 5: both-correct n=%d (%s); outlier H-R2 excluded for chart: n=8" % (len(bc), ",".join(bc)))
        n9 = basis(d, bc)
        e9 = (11, 15, 283601, 333473, 17251, 382273)
        got9 = (n9["C"]["calls"], n9["N"]["calls"], n9["C"]["tokens"], n9["N"]["tokens"], n9["C"]["bytes"], n9["N"]["bytes"])
        log("  S5 n=9 raw %s vs FACTS %s -> %s" % (got9, e9, "MATCH" if got9 == e9 else "MISMATCH"))
        if got9 != e9: STATUS[s] = "MISMATCH n=9"
        bc = [t for t in bc if t != "H-R2"]
    b = basis(d, bc)
    raw = (b["C"]["calls"], b["N"]["calls"], b["C"]["tokens"], b["N"]["tokens"], b["C"]["bytes"], b["N"]["bytes"])
    pct = tuple(100.0 * b["C"][m] / b["N"][m] for m in ("calls", "tokens", "bytes"))
    cor = (sum(d[k]["ok"] for k in d if k[1] == "C"), sum(d[k]["ok"] for k in d if k[1] == "N"))
    e = EXP[s]
    problems = []
    if e["raw"] is not None and raw != e["raw"]: problems.append("raw %s != FACTS %s" % (raw, e["raw"]))
    if e["n"] is not None and len(bc) != e["n"]: problems.append("n %d != %d" % (len(bc), e["n"]))
    if tuple(int(round(p)) for p in pct) != e["pct"]: problems.append("pct %s != FACTS %s" % (tuple(round(p, 1) for p in pct), e["pct"]))
    ec = EXP_CORRECT[s]
    if cor[0] != ec[0] or (ec[1] is not None and cor[1] != ec[1]): problems.append("correct %s != FACTS %s" % (cor, ec))
    STATUS[s] = ("MISMATCH: " + "; ".join(problems)) if problems else STATUS.get(s, "MATCH")
    TABLE[s] = dict(label=label, harness=harness, n=len(bc), raw=raw, pct=pct, cor=cor, ids=e["ids"], tasks=bc)
    log("series %d %-18s n=%d calls %d/%d tok %d/%d bytes %d/%d -> %.1f%% %.1f%% %.1f%% | correct C %d N %d | %s"
        % (s, label, len(bc), raw[0], raw[1], raw[2], raw[3], raw[4], raw[5], pct[0], pct[1], pct[2], cor[0], cor[1], STATUS[s]))

totC = sum(TABLE[s]["cor"][0] for s in TABLE); totN = sum(TABLE[s]["cor"][1] for s in TABLE)
tot_ok = (totC, totN) == FACTS_TOTAL
log("nine-configuration correct totals DevX %d native %d vs FACTS F-FM-6 %s -> %s" % (totC, totN, FACTS_TOTAL, "MATCH" if tot_ok else "MISMATCH"))
good = [s for s, *_ in CONFIGS if STATUS[s].startswith("MATCH")]
bad = [s for s, *_ in CONFIGS if not STATUS[s].startswith("MATCH")]

CAP_PATH = {}
def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, name + "." + ext), dpi=200)
    plt.close(fig)

def cap(fig, text, width=120):
    fig.text(0.5, 0.012, textwrap.fill(text, width), ha="center", va="bottom", fontsize=9)

def newfig():
    return plt.subplots(figsize=(8, 4.5))  # 1600x900 at 200 dpi

CAPTIONS = {}
def chart1():
    fig, ax = newfig()
    x = list(range(len(CONFIGS))); w = 0.27
    for i, (m, c, nm) in enumerate((("calls", CB["calls"], "tool calls"), ("tokens", CB["tokens"], "input tokens"), ("bytes", CB["bytes"], "result bytes"))):
        vals = [TABLE[s]["pct"][i] for s, *_ in CONFIGS]
        ax.bar([xi + (i - 1) * w for xi in x], vals, w, label=nm, color=c)
    ax.axhline(100, ls="--", color="black", lw=1)
    ax.set_xticks(x)
    ax.set_xticklabels(["%s\nn=%d" % (TABLE[s]["label"].replace(" ", "\n", 1), TABLE[s]["n"]) for s, *_ in CONFIGS], fontsize=8)
    ax.set_ylabel("DevX as % of native")
    ax.set_title("DevX relative to native, nine configurations (100% = same as native)")
    ax.legend(fontsize=10, loc="upper left", frameon=False, ncol=3)
    ax.set_ylim(0, max(TABLE[s]["pct"][2] for s in TABLE) * 1.12)
    cap(fig, "12 held-out tasks, one run per task, both-correct basis (n per configuration shown; series 5 n=8, outlier H-R2 excluded). Below 100% = DevX used less.")
    fig.tight_layout(rect=(0, 0.08, 1, 1)); save(fig, "01-ratios-by-configuration")
    CAPTIONS[1] = "DevX as a share of native on the tasks both arms answered correctly, nine configurations (12 held-out tasks, one run per task; series 5 shown at n=8 without the H-R2 outlier). Dashed line = parity."

def chart2():
    fig, ax = newfig(); x = list(range(len(CONFIGS))); w = 0.38
    c = [TABLE[s]["cor"][0] for s, *_ in CONFIGS]; n = [TABLE[s]["cor"][1] for s, *_ in CONFIGS]
    b1 = ax.bar([xi - w / 2 for xi in x], c, w, label="DevX", color=CB["devx"])
    b2 = ax.bar([xi + w / 2 for xi in x], n, w, label="native", color=CB["native"], hatch="//")
    for b in list(b1) + list(b2):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.15, "%d" % b.get_height(), ha="center", fontsize=10)
    ax.axhline(12, ls="--", color="black", lw=1)
    ax.set_xticks(x); ax.set_xticklabels([TABLE[s]["label"].replace(" ", "\n", 1) for s, *_ in CONFIGS], fontsize=8)
    ax.set_ylim(0, 13.5); ax.set_ylabel("verified correct, out of 12")
    ax.set_title("Verified correct answers per configuration (out of 12)", pad=28)
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=10)
    cap(fig, "One run per task; blinded rescore (series 5 hand-checked). 12 tasks per configuration, 24 runs each.")
    fig.tight_layout(rect=(0, 0.08, 1, 1)); save(fig, "02-correctness-by-configuration")
    CAPTIONS[2] = "Verified correct answers out of 12 for DevX and native in each configuration. One run per task; blinded rescore (series 5 hand-checked). Totals: DevX %d/108, native %d/108." % (totC, totN)

def chart3():
    tasks = json.load(open(os.path.join(HERE, "tasks_heldout.json")))
    order = ["locate", "read", "structure", "crossref", "multihop"]
    tasks = sorted(tasks, key=lambda t: (order.index(t["kind"]), t["id"]))
    d = DATA[5]; fig, ax = newfig(); w = 0.38
    rows3 = []
    for i, t in enumerate(tasks):
        c, nn = d[(t["id"], "C")], d[(t["id"], "N")]
        wrong = not (c["ok"] and nn["ok"])
        ax.bar(i - w / 2, c["calls"], w, color=CB["devx"], hatch="xx" if not c["ok"] else None, edgecolor="black" if not c["ok"] else CB["devx"], label="DevX" if i == 0 else None)
        ax.bar(i + w / 2, nn["calls"], w, color=CB["native"], hatch="xx" if not nn["ok"] else None, edgecolor="black" if not nn["ok"] else CB["native"], label="native" if i == 0 else None)
        if wrong:
            ax.text(i, max(c["calls"], nn["calls"]) + 0.15, "wrong:" + ("C" if not c["ok"] else "") + ("N" if not nn["ok"] else ""), ha="center", fontsize=8)
        rows3.append((t["id"], t["kind"], c["calls"], nn["calls"], c["ok"], nn["ok"]))
    ax.set_xticks(range(len(tasks))); ax.set_xticklabels(["%s\n%s" % (t["id"], t["kind"]) for t in tasks], fontsize=8)
    ax.set_ylabel("tool calls"); ax.set_ylim(0, 4.9)
    ax.set_title("Series 5: tool calls per task, DevX vs native (hatched = wrong answer)")
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    cap(fig, "gpt-6-luna via Codex CLI, 12 held-out tasks, one run per task, 24 runs; hatched bars mark a wrong (hand-checked) answer.")
    fig.tight_layout(rect=(0, 0.08, 1, 1)); save(fig, "03-heldout-per-task-calls")
    CAPTIONS[3] = "Series 5, tool calls per task grouped by kind (gpt-6-luna, Codex CLI, 12 tasks, one run each). Hatched bars are wrong answers (hand-checked); the task kind 'structure' is the held-out set's name for the structure/summary questions."
    return rows3

def chart4():
    fig, axes = plt.subplots(1, 2, figsize=(8, 4.5), sharey=True, gridspec_kw={"width_ratios": [5, 4]})
    rows4 = []
    for ax, harness in zip(axes, ("Codex", "Claude Code")):
        cfg = [(s, l) for s, l, h in CONFIGS if h == harness]; w = 0.38
        for i, (s, l) in enumerate(cfg):
            r = TABLE[s]["raw"]
            ax.bar(i - w / 2, r[4], w, color=CB["devx"], label="DevX" if i == 0 else None)
            ax.bar(i + w / 2, r[5], w, color=CB["native"], hatch="//", label="native" if i == 0 else None)
            rows4.append((s, l, harness, r[4], r[5]))
        ax.set_yscale("log"); ax.set_xticks(range(len(cfg)))
        ax.set_xticklabels(["%s\nn=%d" % (l.replace(" ", "\n", 1), TABLE[s]["n"]) for s, l in cfg], fontsize=7)
        ax.set_title(harness + " harness", fontsize=12)
    axes[0].set_ylabel("result bytes, both-correct tasks (log)")
    axes[0].legend(frameon=False, fontsize=10, loc="upper right")
    fig.suptitle("Result bytes: DevX vs native by harness", fontsize=15)
    cap(fig, "Same 12 held-out tasks, one run per task, both-correct basis (series 5 n=8). Log scale. Codex shell returns whatever a command prints; Claude Code tools bound their output.")
    fig.tight_layout(rect=(0, 0.09, 1, 0.95)); save(fig, "04-bytes-by-harness")
    CAPTIONS[4] = "Tool-result bytes, DevX vs native, summed over the both-correct tasks (log scale). On the Codex shell, native commands print unbounded output and DevX returns less; on Claude Code, native Read/Grep are bounded and DevX returns more."
    return rows4

def chart5():
    rows = read_csv(os.path.join(RES, "series4", "rows.csv"))
    tasks = sorted({r["task"] for r in rows})
    assert len(rows) == 72 and len(tasks) == 12
    sm = {}
    for m, col in (("calls", "tool_calls_total"), ("tokens", "input_tokens"), ("bytes", "result_bytes")):
        sm[m] = {a: sum(statistics.median(int(r[col]) for r in rows if r["task"] == t and r["arm"] == a) for t in tasks) for a in "CN"}
    tuned = tuple(100.0 * sm[m]["C"] / sm[m]["N"] for m in ("calls", "tokens", "bytes"))
    ok = tuple(int(round(v)) for v in tuned) == (131, 124, 69)
    corr = (sum(int(r["correct"]) for r in rows if r["arm"] == "C"), sum(int(r["correct"]) for r in rows if r["arm"] == "N"))
    log("series 4 sum of per-task medians C%%N calls/tokens/bytes %.1f %.1f %.1f vs FACTS F-LA-7 131/124/69 -> %s; automated correct C %d N %d (FACTS 36/33)"
        % (tuned + (("MATCH" if ok else "MISMATCH"), corr[0], corr[1])))
    held = TABLE[5]["pct"]
    if not ok or 5 in bad:
        log("chart 5 skipped"); return None
    fig, ax = newfig(); w = 0.35
    for j, (nm, vals, col) in enumerate((("tuned set (series 4, 12 tasks x 3 reps)", tuned[:2], CB["native"]), ("held-out (series 5, n=8)", held[:2], CB["devx"]))):
        b = ax.bar([0 + (j - 0.5) * w * 1.1, 1 + (j - 0.5) * w * 1.1], vals, w, label=nm, color=col)
        for r in b: ax.text(r.get_x() + r.get_width() / 2, r.get_height() + 2, "%.0f%%" % r.get_height(), ha="center", fontsize=11)
    ax.axhline(100, ls="--", color="black", lw=1)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["tool calls", "input tokens"]); ax.set_ylim(0, 160)
    ax.set_ylabel("DevX as % of native"); ax.set_title("Tuned set vs held-out set (100% = same as native)")
    ax.legend(frameon=False, fontsize=10, loc="upper right")
    cap(fig, "Tuned: sum of per-task medians, 3 reps, Codex CLI, one model. Held-out: n=8 both-correct tasks, one run each, same model.")
    fig.tight_layout(rect=(0, 0.08, 1, 1)); save(fig, "05-tuned-vs-heldout")
    CAPTIONS[5] = "DevX as a share of native on the set it was tuned against (series 4, sum of per-task medians over 12 tasks x 3 reps) and on the held-out set (series 5, n=8 both-correct, one run each); same model and harness. Dashed line = parity."
    return tuned, held, sm

if 1 not in [] and not bad:
    chart1(); chart2(); r3 = chart3(); r4 = chart4(); r5 = chart5()
else:
    log("MISMATCH in series %s: charts 1, 2, 4 skipped; chart 3 needs series 5 only" % bad)
    r3 = r4 = r5 = None
    if 5 not in bad: r3 = chart3()
    sys.exit(1)

# CHARTS.md
L = ["# Article charts (generated by make_charts.py; do not edit by hand)", "",
     "Regenerate: `cd <BENCH> && python3 make_charts.py` (matplotlib Agg, no network). Every figure is recomputed from `results/series<N>/rows.csv` joined with the verified verdicts and checked against FACTS before drawing. Series 7 and 14: the Codex \"Model metadata not found\" warning (counted as an `other` call) is detected by that phrase in the run's jsonl and subtracted once per run, as SERIES7.md and SERIES14.md do. Series 5 verdicts come from the hand-checked `manual` column of the SERIES5.md per-run table.", ""]
L += ["## 01-ratios-by-configuration", "Files: `01-ratios-by-configuration.png`, `.svg`. FACTS: F-LA-3, F-MM-1..4, F-MM-6, F-FM-1..4.", "",
      "| series | configuration | harness | n | calls C/N | input tokens C/N | bytes C/N | calls % | tokens % | bytes % | FACTS check |", "|--|--|--|--|--|--|--|--|--|--|--|"]
for s, l, h in CONFIGS:
    t = TABLE[s]; r = t["raw"]
    L.append("| %d | %s | %s | %d | %d/%d | %d/%d | %d/%d | %.1f | %.1f | %.1f | %s (%s) |" % (s, l, h, t["n"], r[0], r[1], r[2], r[3], r[4], r[5], t["pct"][0], t["pct"][1], t["pct"][2], STATUS[s], t["ids"]))
L += ["", "Caption: " + CAPTIONS[1], ""]
L += ["## 02-correctness-by-configuration", "Files: `02-correctness-by-configuration.png`, `.svg`. FACTS: F-MM-1..4, F-MM-6, F-FM-1..4, F-FM-6 (totals 104/108 vs 98/108).", "",
      "| series | configuration | DevX correct /12 | native correct /12 |", "|--|--|--|--|"]
for s, l, h in CONFIGS:
    L.append("| %d | %s | %d | %d |" % (s, l, TABLE[s]["cor"][0], TABLE[s]["cor"][1]))
L += ["", "Totals: DevX %d, native %d (F-FM-6: 104 vs 98)." % (totC, totN), "", "Caption: " + CAPTIONS[2], ""]
L += ["## 03-heldout-per-task-calls", "Files: `03-heldout-per-task-calls.png`, `.svg`. FACTS: F-LA-2, F-LA-5, F-LA-9, F-LA-10, F-MM-1. Kinds are the `kind` field of `tasks_heldout.json` (locate, read, structure, crossref, multihop; there is no separate search or summary kind).", "",
      "| task | kind | DevX calls | native calls | DevX correct | native correct |", "|--|--|--|--|--|--|"]
for t in r3:
    L.append("| %s | %s | %d | %d | %s | %s |" % (t[0], t[1], t[2], t[3], "yes" if t[4] else "NO", "yes" if t[5] else "NO"))
L += ["", "Caption: " + CAPTIONS[3], ""]
L += ["## 04-bytes-by-harness", "Files: `04-bytes-by-harness.png`, `.svg`. FACTS: F-MM-10 and the per-series byte figures in chart 1.", "",
      "| series | configuration | harness | DevX bytes | native bytes |", "|--|--|--|--|--|"]
for r in r4:
    L.append("| %d | %s | %s | %d | %d |" % r)
L += ["", "Caption: " + CAPTIONS[4], ""]
if r5:
    tuned, held, sm = r5
    L += ["## 05-tuned-vs-heldout", "Files: `05-tuned-vs-heldout.png`, `.svg`. FACTS: F-LA-6, F-LA-7 (131/124/69), F-LA-3. Tuned figures are recomputed from `results/series4/rows.csv` (sum of per-task medians over 12 tasks x 3 reps, all tasks, as the article section 2 states); series 3 is not drawn.", "",
          "| set | calls C/N | input tokens C/N | bytes C/N | calls % | tokens % | bytes % |", "|--|--|--|--|--|--|--|",
          "| tuned (series 4) | %d/%d | %d/%d | %d/%d | %.1f | %.1f | %.1f |" % (sm["calls"]["C"], sm["calls"]["N"], sm["tokens"]["C"], sm["tokens"]["N"], sm["bytes"]["C"], sm["bytes"]["N"], tuned[0], tuned[1], tuned[2]),
          "| held-out (series 5, n=8) | %d/%d | %d/%d | %d/%d | %.1f | %.1f | %.1f |" % (TABLE[5]["raw"] + held), "", "Caption: " + CAPTIONS[5], ""]
with open(os.path.join(OUT, "CHARTS.md"), "w") as f:
    f.write("\n".join(L))
print("wrote", OUT)
