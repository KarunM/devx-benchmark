<!-- DEVX RULES START -->
## DevX code workflow

Use DevX (`devx`) as the primary code-intelligence tool in this workspace.

Use the session ID your brief gives you; create one only if none was given:
```bash
SESSION_ID=<SESSION-F3>
```

`--agent <label>`: use the label your brief gives you (for example, `deepseek`); default to `claude`.

```bash
devx search symbol "<name>" --session "$SESSION_ID" --agent claude
devx search text "<text>" --session "$SESSION_ID" --agent claude
devx read method "<symbol>" "<another symbol>" --session "$SESSION_ID" --agent claude   # up to 10 targets; preserves order and reports each failure
devx read method "<symbol>" --context --session "$SESSION_ID" --agent claude   # bounded test/name candidates when related code needs discovery
devx read section 'path/to/file.md#Heading' --session "$SESSION_ID" --agent claude
devx replace <file> --old "<text>" --new "<text>" --verify --session "$SESSION_ID" --agent claude   # edit + build + tests, ONE call
devx patch create <out.json> --op ReplaceMethod --path <file> --session "$SESSION_ID" --agent claude
devx verify [build|test|both] --session "$SESSION_ID" --agent claude   # check without editing; `verify build` is build-only
```

The four steps are: find it (`search`), read just it (`read`), change it (`replace` or `patch`), then check it. Make your edits, add `--verify` to the LAST one (or run `devx verify` once) -- one check for the batch, not one per edit.

A `devx search` that matches exactly one symbol returns its source with it (a symbol hit shows the declaration line, with bases for a class), so go straight to the edit; a `devx search text` result already carries the matching line, so read the file only when you need the lines around it.

`devx read type "<Class>"` gives the declaration line with bases plus a member outline: `read type` (outline) answers 'which methods/fields does X have' -- use `--full` only when you need bodies. `bases:` gives paths: follow a hierarchy one `read type` per level, no search between. Bare or `Class.member` names resolve when unique, so do not search first. For who-calls / calls-what / where-used use `devx callers|callees "<Qualified.method>"` and `devx references "<Qualified.Name>"` before any `search text`; `callers`/`references` work for Python too (text-backed); `callees` does not -- read the body instead. `callers` groups by function; `--full` lists every site. `devx snapshot <file>` outlines a file; `devx read file <path> --range a:b` reads lines around a hit.

`read method --context` adds bounded test-name and same-file name candidates. Treat them as navigation hints, not confirmed caller or test relations.

Every edit re-indexes the files it touches by itself -- never run `index update` after a write (`--no-index` opts out, and you almost never want that). Use `search text` before grep for repository content. Prefer narrow symbol, method, section, and line-range reads over whole-file reads.
<!-- DEVX RULES END -->
