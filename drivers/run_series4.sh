#!/bin/zsh
cd <BENCH>
lst(){ (cd <F2> && find . -type f -not -path './.devx/*' -not -path './.git/*' -exec stat -f '%N %z %m' {} + | LC_ALL=C sort) > $1; }
lst results/f2-before-series4.txt
/usr/bin/python3 run_bench.py --series series4 --arm CN --tasks all --reps 3 --codex-home-c codex_home_c --sandbox workspace-write
echo "SERIES_DONE rc=$?"
lst results/f2-after-series4.txt
echo LISTED
