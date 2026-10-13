#!/bin/zsh
cd <BENCH>
. ./ds_flags.sh
/usr/bin/python3 run_bench.py --series series7 --tasks-file tasks_heldout.json --arm CN --codex-home-c codex_home_c --sandbox-c read-only --tasks all --reps 1 "${DSFLAGS[@]}"
echo "SERIES_DONE rc=$?"
