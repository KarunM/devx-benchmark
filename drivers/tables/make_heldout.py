#!/usr/bin/env python3
"""phase A: write tasks_heldout.json + HELDOUT-ANSWERS.md, running every derivation command live (output capped at 5 lines)."""
import json, subprocess
from pathlib import Path
H = Path(__file__).resolve().parent
FX = {'f2': ('<F2>', '<SESSION-F2>'),
      'f3': ('<F3>', '<SESSION-F3>')}
DX = str(H / 'clibin' / 'devx')
AST_METHODS = """python3 -c "
import ast,sys
t=ast.parse(open('sympy/series/gruntz.py').read())
c=[n for n in ast.walk(t) if isinstance(n,ast.ClassDef) and n.name=='SubsSet'][0]
print([m.name for m in c.body if isinstance(m,ast.FunctionDef) and not m.name.startswith('_')])"
"""
AST_CALLERS = """python3 -c "
import ast
t=ast.parse(open('sympy/series/gruntz.py').read())
print(sorted({(n.name,c.lineno) for n in t.body if isinstance(n,ast.FunctionDef) for c in ast.walk(n) if isinstance(c,ast.Call) and isinstance(c.func,ast.Name) and c.func.id=='mrv_leadterm'}))"
"""
AST_BASES = """python3 -c "
import ast
for f,n in (('sympy/printing/c.py','C99CodePrinter'),('sympy/printing/c.py','C89CodePrinter'),('sympy/printing/codeprinter.py','CodePrinter')):
    c=[x for x in ast.walk(ast.parse(open(f).read())) if isinstance(x,ast.ClassDef) and x.name==n][0]
    print(f,n,c.lineno,[ast.unparse(b) for b in c.bases])"
"""
T = [
 dict(id='H-L1', kind='locate', fixture='f2', prompt='Which file and line defines the function `limitinf` (not the tests)?', expected=['series/gruntz.py:428'],
      a='grep -rn "^def limitinf" sympy', b=f'{DX} search symbol limitinf --session {{S}} | sed -n 1,2p', why='Plain definition lookup of a unique module-level function.'),
 dict(id='H-L2', kind='locate', fixture='f2', prompt='Which file and line defines the class `C99CodePrinter` (not the tests)?', expected=['printing/c.py:637'],
      a='grep -rn "^class C99CodePrinter" sympy', b=f'{DX} search symbol C99CodePrinter --session {{S}} | sed -n 1p', why='Plain definition lookup of a unique class.'),
 dict(id='H-R1', kind='read', fixture='f2', prompt='In sympy.series.limits.Limit.__new__, what exception type is raised when `dir` is a string or Symbol that is not one of the allowed directions, and how does its message begin?',
      expected=['ValueError', 'direction must be one of'], a='sed -n 161,165p sympy/series/limits.py',
      b=f'{DX} read method sympy.series.limits.Limit.__new__ --session {{S}} | grep -n "ValueError\\|direction must be one"', why='Answerable only from the method body: the exception type and message of the last validation branch.'),
 dict(id='H-S1', kind='structure', fixture='f2', prompt='List the public methods (names not starting with an underscore) defined directly in class SubsSet in sympy/series/gruntz.py.',
      expected=['do_subs', 'meets', 'union', 'copy'], a=AST_METHODS, b=f'{DX} read type sympy.series.gruntz.SubsSet --session {{S}} | grep "^method"', why='Member listing of one class, as S1/S2 of the originals.'),
 dict(id='H-X1', kind='crossref', fixture='f2', prompt='Which functions in sympy/series/gruntz.py call `mrv_leadterm` (ignore docstrings and tests)?',
      expected=['sign', 'limitinf'], a=AST_CALLERS, b=f'{DX} callers sympy.series.gruntz.mrv_leadterm --session {{S}} | grep -v "tests\\|<module>  "', why='Call sites of one function resolved to enclosing functions (two distinct callers).'),
 dict(id='H-M1', kind='multihop', fixture='f2', prompt='Class C99CodePrinter (sympy/printing/c.py) has a base class whose own base is defined in sympy/printing/codeprinter.py. Name that class and give its definition file:line.',
      expected=['CodePrinter', 'sympy/printing/codeprinter.py:53'], a=AST_BASES,
      b=f'{DX} read type sympy.printing.c.C89CodePrinter --session {{S}} | sed -n 1,2p; {DX} read type sympy.printing.codeprinter.CodePrinter --session {{S}} | sed -n 1p', why='Three hops: C99CodePrinter -> C89CodePrinter -> CodePrinter, then its definition line.'),
 dict(id='H-L3', kind='locate', fixture='f3', prompt='Which file and line defines the method `LooksLikeShellCommandLine` (not the tests)?', expected=['DevXCommandConfig.cs:153'],
      a='grep -rn "bool LooksLikeShellCommandLine" src', b=f'{DX} search symbol LooksLikeShellCommandLine --session {{S}} | sed -n 1,2p', why='Plain definition lookup of a unique method.'),
 dict(id='H-R2', kind='read', fixture='f3', prompt='In DevX.Cli.SearchReplaceBlockParser.Parse, what error message is returned when the response contains a markdown code fence (```), and what message is returned when the response is empty or whitespace?',
      expected=['markdown_fence_outside_blocks', 'zero_blocks'], a='grep -n "zero_blocks\\|markdown_fence" src/DevX.Cli/SearchReplaceBlockParser.cs',
      b=f'{DX} read method DevX.Cli.SearchReplaceBlockParser.Parse --session {{S}} | grep -n "zero_blocks\\|markdown_fence" ', why='Answerable only from the first two early returns of the method body.'),
 dict(id='H-R3', kind='read', fixture='f3', prompt='In DevX.Infrastructure.Storage.SQLite.RipgrepLocator.ConfiguredPath, which exception types are caught (each making the method return null)?',
      expected=['JsonException', 'IOException', 'UnauthorizedAccessException'], a='sed -n 99p\\;115,117p src/DevX.Infrastructure/Storage/SQLite/RipgrepLocator.cs',
      b=f'{DX} read method DevX.Infrastructure.Storage.SQLite.RipgrepLocator.ConfiguredPath --session {{S}} | grep -n "catch"', why='Answerable only from the catch clauses of one method body.'),
 dict(id='H-S2', kind='structure', fixture='f3', prompt='List the public methods (excluding the constructor) defined directly in class SandboxManager (src/DevX.Cli/SandboxManager.cs).',
      expected=['CopySourceTree', 'ApplyChanges', 'GetChangedFiles', 'GetUnifiedDiff', 'Dispose'], a='grep -n "^    public .*(" src/DevX.Cli/SandboxManager.cs',
      b=f'{DX} read type DevX.Cli.SandboxManager --session {{S}} | grep "^method .*public"', why='Member listing of one class.'),
 dict(id='H-X2', kind='crossref', fixture='f3', prompt='Which methods in src (not tests, and not inside RipgrepLocator itself) call `RipgrepLocator.Locate`?',
      expected=['TrySearch', 'DoctorAsync'], a='grep -rn "RipgrepLocator.Locate" src --include=*.cs',
      b=f'{DX} search text "RipgrepLocator.Locate" --session {{S}} | grep -v tests', why='Call sites resolved to their enclosing methods (two distinct callers in different projects).'),
 dict(id='H-M2', kind='multihop', fixture='f3', prompt='SqliteSessionStore has a private helper that throws InvalidOperationException("Session not found."). Which of that helper\'s callers have a name starting with `Mark`?',
      expected=['MarkSymbolExpandedAsync', 'MarkFileExpandedAsync'], a='awk \'/^    (public|private) /{m=$0} /Session not found/{print NR": throw in: "m} /await RequireSessionAsync/{print NR": caller: "m}\' src/DevX.Infrastructure/Storage/SQLite/SqliteSessionStore.cs',
      b=f'{DX} search text "RequireSessionAsync" --session {{S}} | grep -o "SqliteSessionStore\\.[A-Za-z]*Async\\]"', why='Two hops: find the method that throws the message, then its callers filtered by name.'),
]
def run(cmd, root, S):
    p = subprocess.run(cmd.replace('{S}', S), shell=True, cwd=root, capture_output=True, text=True)
    lines = (p.stdout + p.stderr).splitlines()
    return [l[:230] for l in lines[:5]] + ([f'... ({len(lines)-5} more lines)'] if len(lines) > 5 else [])
tasks = [{k: t[k] for k in ('id', 'kind', 'prompt', 'expected', 'fixture')} for t in T]
json.dump(tasks, open(H / 'tasks_heldout.json', 'w'), indent=1); open(H / 'tasks_heldout.json', 'a').write('\n')
md = ['# Held-out answers (phase A)', '',
      'Fixtures: f2 = sympy (session <SESSION-F2>), f3 = DevX C# copy at 04a02ef (session <SESSION-F3>). Binary: clibin/devx (1.6.14+04a02ef). Outputs capped at 5 lines, produced by `make_heldout.py`.', '',
      'f2 modules excluded (named in tasks.json prompts or expected): sympy/ntheory/factor_.py, sympy/ntheory/generate.py, sympy/core/symbol.py, sympy/core/numbers.py, sympy/core/expr.py, sympy/logic/boolalg.py (also sympy.core.symbol.{Symbol,Dummy,Wild}). Held-out f2 tasks use sympy/series/gruntz.py, sympy/series/limits.py, sympy/printing/c.py, sympy/printing/codeprinter.py only.', '',
      'f3 tasks avoid the tuned features (outline bases, grouped callers, text references, guidance): they use storage, CLI parsing, patch/sandbox, ripgrep location, session store. Note src/DevX.Cli/Program.cs.bak is tracked at 04a02ef and is kept in F3.', '']
for t in T:
    root, S = FX[t['fixture']]
    md += [f"## {t['id']} ({t['kind']}, {t['fixture']})", f"- prompt: {t['prompt']}", f"- expected (all must appear): {json.dumps(t['expected'])}", f"- kind: {t['why']}",
           '- derivation A (shell/ast):', '```', '$ ' + t['a'].strip().replace('\n', ' '), *run(t['a'], root, S), '```',
           '- derivation B (devx):', '```', '$ ' + t['b'].replace('{S}', S), *run(t['b'], root, S), '```', '']
open(H / 'HELDOUT-ANSWERS.md', 'w').write('\n'.join(md))
