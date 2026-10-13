#!/bin/zsh
cd <BENCH>
. <SCRATCH>/difl.sh
lst(){ (cd <FIXTURES>/$1 && find . -type f -not -path './.devx/*' -not -path './.git/*' -exec sh -c 'for f; do printf "%s %s %s %s\n" "$f" "$(stat -f %z "$f")" "$(stat -f %m "$f")" "$(shasum -a 256 "$f" | cut -d" " -f1)"; done' sh {} + | LC_ALL=C sort) > $2; }
mkdir -p results/series14
lst f2 results/f2-before-series14.txt
lst f3 results/f3-before-series14.txt
/usr/bin/python3 run_bench.py --series series14 --tasks all --tasks-file tasks_heldout.json --arm CN --codex-home-c codex_home_c --sandbox-c read-only "${DIFLAGS[@]}"
echo "SERIES_RC=$?"
lst f2 results/f2-after-series14.txt
lst f3 results/f3-after-series14.txt
echo "SERIES_DONE"
