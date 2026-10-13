# Held-out answers (phase A)

Fixtures: f2 = sympy (session <SESSION-F2>), f3 = DevX C# copy at 04a02ef (session <SESSION-F3>). Binary: clibin/devx (1.6.14+04a02ef). Outputs capped at 5 lines, produced by `make_heldout.py`.

f2 modules excluded (named in tasks.json prompts or expected): sympy/ntheory/factor_.py, sympy/ntheory/generate.py, sympy/core/symbol.py, sympy/core/numbers.py, sympy/core/expr.py, sympy/logic/boolalg.py (also sympy.core.symbol.{Symbol,Dummy,Wild}). Held-out f2 tasks use sympy/series/gruntz.py, sympy/series/limits.py, sympy/printing/c.py, sympy/printing/codeprinter.py only.

f3 tasks avoid the tuned features (outline bases, grouped callers, text references, guidance): they use storage, CLI parsing, patch/sandbox, ripgrep location, session store. Note src/DevX.Cli/Program.cs.bak is tracked at 04a02ef and is kept in F3.

## H-L1 (locate, f2)
- prompt: Which file and line defines the function `limitinf` (not the tests)?
- expected (all must appear): ["series/gruntz.py:428"]
- kind: Plain definition lookup of a unique module-level function.
- derivation A (shell/ast):
```
$ grep -rn "^def limitinf" sympy
sympy/series/gruntz.py:428:def limitinf(e, x):
```
- derivation B (devx):
```
$ <BENCH>/clibin/devx search symbol limitinf --session <SESSION-F2> | sed -n 1,2p
method sympy.series.gruntz.<module>.limitinf sympy/series/gruntz.py:428-470
sympy/series/gruntz.py:428-470 sympy.series.gruntz.<module>.limitinf [method]
```

## H-L2 (locate, f2)
- prompt: Which file and line defines the class `C99CodePrinter` (not the tests)?
- expected (all must appear): ["printing/c.py:637"]
- kind: Plain definition lookup of a unique class.
- derivation A (shell/ast):
```
$ grep -rn "^class C99CodePrinter" sympy
sympy/printing/c.py:637:class C99CodePrinter(C89CodePrinter):
```
- derivation B (devx):
```
$ <BENCH>/clibin/devx search symbol C99CodePrinter --session <SESSION-F2> | sed -n 1p
class sympy.printing.c.C99CodePrinter sympy/printing/c.py:637-729
```

## H-R1 (read, f2)
- prompt: In sympy.series.limits.Limit.__new__, what exception type is raised when `dir` is a string or Symbol that is not one of the allowed directions, and how does its message begin?
- expected (all must appear): ["ValueError", "direction must be one of"]
- kind: Answerable only from the method body: the exception type and message of the last validation branch.
- derivation A (shell/ast):
```
$ sed -n 161,165p sympy/series/limits.py
            raise TypeError("direction must be of type basestring or "
                    "Symbol, not %s" % type(dir))
        if str(dir) not in ('+', '-', '+-'):
            raise ValueError("direction must be one of '+', '-' "
                    "or '+-', not %s" % dir)
```
- derivation B (devx):
```
$ <BENCH>/clibin/devx read method sympy.series.limits.Limit.__new__ --session <SESSION-F2> | grep -n "ValueError\|direction must be one"
21:            raise ValueError("direction must be one of '+', '-' "
```

## H-S1 (structure, f2)
- prompt: List the public methods (names not starting with an underscore) defined directly in class SubsSet in sympy/series/gruntz.py.
- expected (all must appear): ["do_subs", "meets", "union", "copy"]
- kind: Member listing of one class, as S1/S2 of the originals.
- derivation A (shell/ast):
```
$ python3 -c " import ast,sys t=ast.parse(open('sympy/series/gruntz.py').read()) c=[n for n in ast.walk(t) if isinstance(n,ast.ClassDef) and n.name=='SubsSet'][0] print([m.name for m in c.body if isinstance(m,ast.FunctionDef) and not m.name.startswith('_')])"
['do_subs', 'meets', 'union', 'copy']
```
- derivation B (devx):
```
$ <BENCH>/clibin/devx read type sympy.series.gruntz.SubsSet --session <SESSION-F2> | grep "^method"
method __repr__ 205-206 __repr__(self)
method __getitem__ 208-211 __getitem__(self, key)
method do_subs 213-217 do_subs(self, e)
method meets 219-221 meets(self, s2)
method union 223-236 union(self, s2, exps=None)
... (1 more lines)
```

## H-X1 (crossref, f2)
- prompt: Which functions in sympy/series/gruntz.py call `mrv_leadterm` (ignore docstrings and tests)?
- expected (all must appear): ["sign", "limitinf"]
- kind: Call sites of one function resolved to enclosing functions (two distinct callers).
- derivation A (shell/ast):
```
$ python3 -c " import ast t=ast.parse(open('sympy/series/gruntz.py').read()) print(sorted({(n.name,c.lineno) for n in t.body if isinstance(n,ast.FunctionDef) for c in ast.walk(n) if isinstance(c,ast.Call) and isinstance(c.func,ast.Name) and c.func.id=='mrv_leadterm'}))"
[('limitinf', 449), ('limitinf', 451), ('limitinf', 453), ('sign', 421)]
```
- derivation B (devx):
```
$ <BENCH>/clibin/devx callers sympy.series.gruntz.mrv_leadterm --session <SESSION-F2> | grep -v "tests\|<module>  "
sympy.series.gruntz.<module>.limitinf  3 calls  sympy/series/gruntz.py:449,451,453
sympy.series.gruntz.<module>.sign  1 call  sympy/series/gruntz.py:421
13 call sites in 6 functions; target sympy/series/gruntz.py:530; text-backed: call sites by name, not a resolved call graph; pass --full for every site
```

## H-M1 (multihop, f2)
- prompt: Class C99CodePrinter (sympy/printing/c.py) has a base class whose own base is defined in sympy/printing/codeprinter.py. Name that class and give its definition file:line.
- expected (all must appear): ["CodePrinter", "sympy/printing/codeprinter.py:53"]
- kind: Three hops: C99CodePrinter -> C89CodePrinter -> CodePrinter, then its definition line.
- derivation A (shell/ast):
```
$ python3 -c " import ast for f,n in (('sympy/printing/c.py','C99CodePrinter'),('sympy/printing/c.py','C89CodePrinter'),('sympy/printing/codeprinter.py','CodePrinter')):     c=[x for x in ast.walk(ast.parse(open(f).read())) if isinstance(x,ast.ClassDef) and x.name==n][0]     print(f,n,c.lineno,[ast.unparse(b) for b in c.bases])"
sympy/printing/c.py C99CodePrinter 637 ['C89CodePrinter']
sympy/printing/c.py C89CodePrinter 147 ['CodePrinter']
sympy/printing/codeprinter.py CodePrinter 53 ['StrPrinter']
```
- derivation B (devx):
```
$ <BENCH>/clibin/devx read type sympy.printing.c.C89CodePrinter --session <SESSION-F2> | sed -n 1,2p; <BENCH>/clibin/devx read type sympy.printing.codeprinter.CodePrinter --session <SESSION-F2> | sed -n 1p
sympy/printing/c.py:147-635 sympy.printing.c.C89CodePrinter [type]
class C89CodePrinter(CodePrinter):
sympy/printing/codeprinter.py:53-614 sympy.printing.codeprinter.CodePrinter [type]
```

## H-L3 (locate, f3)
- prompt: Which file and line defines the method `LooksLikeShellCommandLine` (not the tests)?
- expected (all must appear): ["DevXCommandConfig.cs:153"]
- kind: Plain definition lookup of a unique method.
- derivation A (shell/ast):
```
$ grep -rn "bool LooksLikeShellCommandLine" src
src/DevX.Indexer/DevXCommandConfig.cs:153:    public static bool LooksLikeShellCommandLine(string command)
```
- derivation B (devx):
```
$ <BENCH>/clibin/devx search symbol LooksLikeShellCommandLine --session <SESSION-F3> | sed -n 1,2p
method DevX.Indexer.DevXCommandConfig.LooksLikeShellCommandLine src/DevX.Indexer/DevXCommandConfig.cs:153-161
src/DevX.Indexer/DevXCommandConfig.cs:153-161 DevX.Indexer.DevXCommandConfig.LooksLikeShellCommandLine [method]
```

## H-R2 (read, f3)
- prompt: In DevX.Cli.SearchReplaceBlockParser.Parse, what error message is returned when the response contains a markdown code fence (```), and what message is returned when the response is empty or whitespace?
- expected (all must appear): ["markdown_fence_outside_blocks", "zero_blocks"]
- kind: Answerable only from the first two early returns of the method body.
- derivation A (shell/ast):
```
$ grep -n "zero_blocks\|markdown_fence" src/DevX.Cli/SearchReplaceBlockParser.cs
16:            return new SearchReplaceParseResult(false, "zero_blocks", []);
22:            return new SearchReplaceParseResult(false, "markdown_fence_outside_blocks", []);
110:            return new SearchReplaceParseResult(false, "zero_blocks", []);
```
- derivation B (devx):
```
$ <BENCH>/clibin/devx read method DevX.Cli.SearchReplaceBlockParser.Parse --session <SESSION-F3> | grep -n "zero_blocks\|markdown_fence" 
6:            return new SearchReplaceParseResult(false, "zero_blocks", []);
12:            return new SearchReplaceParseResult(false, "markdown_fence_outside_blocks", []);
100:            return new SearchReplaceParseResult(false, "zero_blocks", []);
```

## H-R3 (read, f3)
- prompt: In DevX.Infrastructure.Storage.SQLite.RipgrepLocator.ConfiguredPath, which exception types are caught (each making the method return null)?
- expected (all must appear): ["JsonException", "IOException", "UnauthorizedAccessException"]
- kind: Answerable only from the catch clauses of one method body.
- derivation A (shell/ast):
```
$ sed -n 99p\;115,117p src/DevX.Infrastructure/Storage/SQLite/RipgrepLocator.cs
    public static string? ConfiguredPath(string? repositoryRoot)
        catch (JsonException) { return null; }
        catch (IOException) { return null; }
        catch (UnauthorizedAccessException) { return null; }
```
- derivation B (devx):
```
$ <BENCH>/clibin/devx read method DevX.Infrastructure.Storage.SQLite.RipgrepLocator.ConfiguredPath --session <SESSION-F3> | grep -n "catch"
18:        catch (JsonException) { return null; }
19:        catch (IOException) { return null; }
20:        catch (UnauthorizedAccessException) { return null; }
```

## H-S2 (structure, f3)
- prompt: List the public methods (excluding the constructor) defined directly in class SandboxManager (src/DevX.Cli/SandboxManager.cs).
- expected (all must appear): ["CopySourceTree", "ApplyChanges", "GetChangedFiles", "GetUnifiedDiff", "Dispose"]
- kind: Member listing of one class.
- derivation A (shell/ast):
```
$ grep -n "^    public .*(" src/DevX.Cli/SandboxManager.cs
14:    public SandboxManager(string originalRoot)
24:    public void CopySourceTree()
32:    public void ApplyChanges()
47:    public IReadOnlyList<string> GetChangedFiles()
72:    public string GetUnifiedDiff(int contextLines = 3)
... (1 more lines)
```
- derivation B (devx):
```
$ <BENCH>/clibin/devx read type DevX.Cli.SandboxManager --session <SESSION-F3> | grep "^method .*public"
method CopySourceTree 24-27 public void CopySourceTree()
method ApplyChanges 32-42 public void ApplyChanges()
method GetChangedFiles 47-67 public IReadOnlyList<string> GetChangedFiles()
method GetUnifiedDiff 72-115 public string GetUnifiedDiff(int contextLines = 3)
method Dispose 117-132 public void Dispose()
```

## H-X2 (crossref, f3)
- prompt: Which methods in src (not tests, and not inside RipgrepLocator itself) call `RipgrepLocator.Locate`?
- expected (all must appear): ["TrySearch", "DoctorAsync"]
- kind: Call sites resolved to their enclosing methods (two distinct callers in different projects).
- derivation A (shell/ast):
```
$ grep -rn "RipgrepLocator.Locate" src --include=*.cs
src/DevX.Infrastructure/Storage/SQLite/RipgrepContentSearcher.cs:42:        => TrySearch(rootPath, query, RipgrepLocator.Locate(rootPath).Executable, out hits, out scanCapped, cancellationToken);
src/DevX.Cli/Program.cs:1272:    var searchEngine = DevX.Infrastructure.Storage.SQLite.RipgrepLocator.Locate(repositoryRoot);
```
- derivation B (devx):
```
$ <BENCH>/clibin/devx search text "RipgrepLocator.Locate" --session <SESSION-F3> | grep -v tests
src/DevX.Cli/Program.cs:1272: var searchEngine = DevX.Infrastructure.Storage.SQLite.RipgrepLocator.Locate(repositoryRoot); [Program.DoctorAsync]
src/DevX.Infrastructure/Storage/SQLite/RipgrepContentSearcher.cs:42: => TrySearch(rootPath, query, RipgrepLocator.Locate(rootPath).Executable, out hits, out scanCapped, cancellationToken); [DevX.Infrastructure.Storage.SQLite.Ripgr
```

## H-M2 (multihop, f3)
- prompt: SqliteSessionStore has a private helper that throws InvalidOperationException("Session not found."). Which of that helper's callers have a name starting with `Mark`?
- expected (all must appear): ["MarkSymbolExpandedAsync", "MarkFileExpandedAsync"]
- kind: Two hops: find the method that throws the message, then its callers filtered by name.
- derivation A (shell/ast):
```
$ awk '/^    (public|private) /{m=$0} /Session not found/{print NR": throw in: "m} /await RequireSessionAsync/{print NR": caller: "m}' src/DevX.Infrastructure/Storage/SQLite/SqliteSessionStore.cs
89: caller:     public async Task SaveSearchAsync(SaveSearchRequest request, CancellationToken cancellationToken = default)
96: caller:     public async Task AddWorkingSetItemAsync(AddWorkingSetItemRequest request, CancellationToken cancellationToken = default)
103: caller:     public async Task MarkSymbolExpandedAsync(MarkSymbolExpandedRequest request, CancellationToken cancellationToken = default)
109: caller:     public async Task MarkFileExpandedAsync(MarkFileExpandedRequest request, CancellationToken cancellationToken = default)
115: caller:     public async Task AddDiagnosticAsync(AddDiagnosticRequest request, CancellationToken cancellationToken = default)
... (2 more lines)
```
- derivation B (devx):
```
$ <BENCH>/clibin/devx search text "RequireSessionAsync" --session <SESSION-F3> | grep -o "SqliteSessionStore\.[A-Za-z]*Async\]"
SqliteSessionStore.SaveSearchAsync]
SqliteSessionStore.AddWorkingSetItemAsync]
SqliteSessionStore.MarkSymbolExpandedAsync]
SqliteSessionStore.MarkFileExpandedAsync]
SqliteSessionStore.AddDiagnosticAsync]
... (2 more lines)
```
