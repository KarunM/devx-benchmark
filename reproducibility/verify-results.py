#!/usr/bin/env python3
"""Recompute every published number of the DevX benchmark from the recorded raw and scored files.

Mode A of reproducibility/environment.md: no accounts, no network, Python 3 standard library only.
Run from anywhere:  python3 reproducibility/verify-results.py      (exit 0 = every check matches, 1 = mismatch)

Inputs
  results/raw/series<N>/rows.csv             per-run counts (tool calls, input tokens, result bytes)
  results/scored/series<N>/rescore<N>.csv    verified verdicts, series 6-14 (blinded rescore after adjudication)
  results/summaries/SERIES5.md               series 5 per-run table (hand-checked verdict + call count); series 5 has
                                             no rescore<N>.csv in the verdict format, so the table is the source
  results/raw/series7|14/<task>-<arm>-r1.jsonl   the Codex "Model metadata not found" warning that the parser
                                             recorded as one extra tool call per run is subtracted (series 7 and 14)
Compared against
  results/summaries/per-configuration.csv, README.md, results/summaries/FACTS-benchmark.md
"""
import csv, os, re, statistics, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "results", "raw")
SCORED = os.path.join(ROOT, "results", "scored")
SUMM = os.path.join(ROOT, "results", "summaries")

CONFIGS = [(5, "gpt-6-luna", "Codex"), (6, "gpt-5.6-luna", "Codex"), (7, "DeepSeek Flash 4.1", "Codex"),
           (8, "Sonnet 5.5", "Claude Code"), (9, "Sonnet 5", "Claude Code"), (10, "Opus 5.5", "Claude Code"),
           (11, "gpt-6-sol", "Codex"), (13, "Fable 5.1", "Claude Code"), (14, "Qwen3.6-27B fp8", "Codex")]
FAILS = []
ROWS = []


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def check(label, computed, expected):
    ok = computed == expected
    ROWS.append((label, str(computed), str(expected), "OK" if ok else "MISMATCH"))
    if not ok:
        FAILS.append(label)


def claim(label, text, doc, doc_text):
    """A published claim: the exact string must occur in the named document."""
    ok = text in doc_text
    ROWS.append((label, text, "in " + doc, "OK" if ok else "MISSING"))
    if not ok:
        FAILS.append(label)


def fmt(n):
    return "{:,}".format(n)


def series5_table():
    ver = {}
    pat = re.compile(r"\|\s*(H-\w+)\s*\|\s*\w+\s*\|\s*f\d\s*\|\s*([CN])\s*\|\s*[\w-]+\s*\|\s*(\d)\s*\|\s*(\d)\s*\|\s*(\d+) \(")
    for line in read_text(os.path.join(SUMM, "SERIES5.md")).splitlines():
        m = pat.match(line)
        if m:
            ver[(m.group(1), m.group(2))] = (int(m.group(4)) == 1, int(m.group(5)))
    if len(ver) != 24:
        raise SystemExit("SERIES5.md per-run table: expected 24 rows, found %d" % len(ver))
    return ver


def pseudo(series, task, arm):
    path = os.path.join(RAW, "series%d" % series, "%s-%s-r1.jsonl" % (task, arm))
    return 1 if "Model metadata" in read_text(path) else 0


def load(series):
    rows = read_csv(os.path.join(RAW, "series%d" % series, "rows.csv"))
    if series == 5:
        ver = series5_table()
        verdict = {k: v[0] for k, v in ver.items()}
        for r in rows:
            if int(r["tool_calls_total"]) != ver[(r["task"], r["arm"])][1]:
                raise SystemExit("series 5 call count differs between rows.csv and SERIES5.md for %s" % ((r["task"], r["arm"]),))
    else:
        verdict = {(r["task"], r["arm"]): r["verdict"] == "correct"
                   for r in read_csv(os.path.join(SCORED, "series%d" % series, "rescore%d.csv" % series))}
    d = {}
    for r in rows:
        k = (r["task"], r["arm"])
        calls = int(r["tool_calls_total"]) - (pseudo(series, *k) if series in (7, 14) else 0)
        d[k] = dict(calls=calls, tokens=int(r["input_tokens"]), bytes=int(r["result_bytes"]), ok=verdict[k])
    if len(d) != 24:
        raise SystemExit("series %d: expected 24 runs, found %d" % (series, len(d)))
    return d


def basis(d, tasks):
    return {a: {m: sum(d[(t, a)][m] for t in tasks) for m in ("calls", "tokens", "bytes")} for a in "CN"}


def both_correct(d):
    return sorted(t for t in {k[0] for k in d} if d[(t, "C")]["ok"] and d[(t, "N")]["ok"])


def pct(a, b):
    return round(100.0 * a / b, 1)


def main():
    readme = read_text(os.path.join(ROOT, "README.md"))
    facts = read_text(os.path.join(SUMM, "FACTS-benchmark.md"))
    pc = {int(r["series"]): r for r in read_csv(os.path.join(SUMM, "per-configuration.csv"))}
    tot_c = tot_n = 0
    fewer_calls = fewer_tok = fewer_bytes = 0
    s5 = {}
    for s, label, harness in CONFIGS:
        d = load(s)
        bc = both_correct(d)
        if s == 5:
            n9 = basis(d, bc)
            s5["n9"] = (len(bc), n9)
            bc = [t for t in bc if t != "H-R2"]   # the published series-5 line drops the H-R2 outlier (n=8)
            s5["n8"] = (len(bc), basis(d, bc))
        b = basis(d, bc)
        cor_c = sum(d[(t, "C")]["ok"] for t in {k[0] for k in d})
        cor_n = sum(d[(t, "N")]["ok"] for t in {k[0] for k in d})
        tot_c += cor_c
        tot_n += cor_n
        row = pc[s]
        tag = "series %d %s" % (s, label)
        check(tag + " n both-correct", len(bc), int(row["n_both_correct"]))
        check(tag + " calls DevX/native", "%d/%d" % (b["C"]["calls"], b["N"]["calls"]), "%s/%s" % (row["calls_devx"], row["calls_native"]))
        check(tag + " input tokens DevX/native", "%d/%d" % (b["C"]["tokens"], b["N"]["tokens"]), "%s/%s" % (row["input_tokens_devx"], row["input_tokens_native"]))
        check(tag + " result bytes DevX/native", "%d/%d" % (b["C"]["bytes"], b["N"]["bytes"]), "%s/%s" % (row["result_bytes_devx"], row["result_bytes_native"]))
        pcts = tuple(pct(b["C"][m], b["N"][m]) for m in ("calls", "tokens", "bytes"))
        check(tag + " calls/tokens/bytes %", pcts, (float(row["calls_pct"]), float(row["tokens_pct"]), float(row["bytes_pct"])))
        check(tag + " verified correct DevX/native", "%d/%d" % (cor_c, cor_n), "%s/%s" % (row["correct_devx"], row["correct_native"]))
        fewer_calls += pcts[0] < 100.0
        fewer_tok += pcts[1] < 100.0
        fewer_bytes += pcts[2] < 100.0
        # README headline row for this configuration
        prefix = "| %d | %s | %s |" % (s, label, harness)
        line = next((l for l in readme.splitlines() if l.startswith(prefix)), None)
        if line is None:
            check(tag + " README row present", False, True)
        else:
            want = "%d/12 vs %d/12" % (cor_c, cor_n)
            check(tag + " README correct", want in line, True)
            check(tag + " README ratios", all(x in line for x in ("%.1f%%" % pcts[0], "%.1f%%" % pcts[1], "%.1f%%" % pcts[2])), True)
    check("nine-configuration verified correct DevX/native", "%d/108 vs %d/108" % (tot_c, tot_n), "104/108 vs 98/108")
    check("DevX fewer calls (of 9)", fewer_calls, 8)
    check("DevX fewer input tokens (of 9)", fewer_tok, 7)
    check("DevX fewer result bytes (of 9)", fewer_bytes, 5)
    claim("README totals", "104/108", "README.md", readme)
    claim("README totals native", "98/108", "README.md", readme)
    claim("FACTS F-FM-6 totals", "verified correct DevX 104/108 versus native 98/108", "FACTS-benchmark.md", facts)
    claim("FACTS F-FM-6 calls 8 of 9", "DevX used fewer calls in 8 of 9 configurations", "FACTS-benchmark.md", facts)
    claim("FACTS F-FM-6 tokens 7 of 9", "fewer input tokens in 7 of 9", "FACTS-benchmark.md", facts)
    claim("FACTS F-FM-6 bytes 5 of 9", "fewer result bytes in 5 of 9", "FACTS-benchmark.md", facts)
    claim("README 8 of 9 calls", "8 of 9", "README.md", readme)
    claim("README 7 of 9 tokens", "7 of 9", "README.md", readme)
    claim("README 5 of 9 bytes", "5 of 9", "README.md", readme)

    # series 5 n=9 and n=8 lines
    n9, b9 = s5["n9"]
    n8, b8 = s5["n8"]
    check("series 5 n=9 count", n9, 9)
    check("series 5 n=9 calls", (b9["C"]["calls"], b9["N"]["calls"]), (11, 15))
    check("series 5 n=9 tokens", (b9["C"]["tokens"], b9["N"]["tokens"]), (283601, 333473))
    check("series 5 n=9 bytes", (b9["C"]["bytes"], b9["N"]["bytes"]), (17251, 382273))
    claim("FACTS series 5 n=9", "calls C 11 vs N 15 (73%); input tokens 283,601 vs 333,473 (85%); result bytes 17,251 vs 382,273 (5%)", "FACTS-benchmark.md", facts)
    check("series 5 n=8 count", n8, 8)
    claim("FACTS series 5 n=8 calls", "calls 9 vs 12 (25.0% fewer)", "FACTS-benchmark.md", facts)
    claim("FACTS series 5 n=8 tokens", "input tokens %s vs %s (11.6%% fewer)" % (fmt(b8["C"]["tokens"]), fmt(b8["N"]["tokens"])), "FACTS-benchmark.md", facts)
    claim("FACTS series 5 n=8 bytes", "result bytes %s vs %s (47.4%% fewer)" % (fmt(b8["C"]["bytes"]), fmt(b8["N"]["bytes"])), "FACTS-benchmark.md", facts)
    check("series 5 n=8 calls/tokens/bytes", (b8["C"]["calls"], b8["N"]["calls"], b8["C"]["tokens"], b8["N"]["tokens"], b8["C"]["bytes"], b8["N"]["bytes"]),
          (9, 12, 240425, 271897, 12701, 24152))
    d5 = load(5)
    all_c = basis(d5, sorted({k[0] for k in d5}))
    claim("FACTS series 5 all 12 tasks", "calls 16 vs 17, input tokens 101%% of native (%s vs %s)" % (fmt(all_c["C"]["tokens"]), fmt(all_c["N"]["tokens"])), "FACTS-benchmark.md", facts)
    check("series 5 all-12 calls", (all_c["C"]["calls"], all_c["N"]["calls"]), (16, 17))

    # tuned series 4: sum of per-task medians, all 12 tasks x 3 reps
    rows4 = read_csv(os.path.join(RAW, "series4", "rows.csv"))
    tasks = sorted({r["task"] for r in rows4})
    check("series 4 rows / tasks", (len(rows4), len(tasks)), (72, 12))
    sm = {}
    for m, col in (("calls", "tool_calls_total"), ("tokens", "input_tokens"), ("bytes", "result_bytes")):
        sm[m] = {a: sum(statistics.median(int(r[col]) for r in rows4 if r["task"] == t and r["arm"] == a) for t in tasks) for a in "CN"}
    med = tuple(int(round(100.0 * sm[m]["C"] / sm[m]["N"])) for m in ("calls", "tokens", "bytes"))
    check("series 4 tuned medians calls/tokens/bytes % (C as share of N)", med, (131, 124, 69))
    claim("FACTS series 4 medians", "calls 131%, input tokens 124%, result bytes 69%", "FACTS-benchmark.md", facts)
    claim("README series 4 medians", "131% / 124% / 69%", "README.md", readme)
    corr4 = (sum(int(r["correct"]) for r in rows4 if r["arm"] == "C"), sum(int(r["correct"]) for r in rows4 if r["arm"] == "N"))
    check("series 4 scorer-correct C/N of 36", corr4, (36, 33))

    w = max(len(r[0]) for r in ROWS)
    print("%-*s  %-34s %-34s %s" % (w, "check", "recomputed", "published", "result"))
    for r in ROWS:
        print("%-*s  %-34s %-34s %s" % (w, r[0], r[1][:34], r[2][:34], r[3]))
    print("\n%d checks, %d failed" % (len(ROWS), len(FAILS)))
    if FAILS:
        print("MISMATCH: " + "; ".join(FAILS))
        return 1
    print("ALL CHECKS MATCH")
    return 0


if __name__ == "__main__":
    sys.exit(main())
