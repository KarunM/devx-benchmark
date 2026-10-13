#!/bin/zsh
cd <BENCH>
/usr/bin/python3 run_bench.py --series series5 --tasks-file tasks_heldout.json --arm CN --codex-home-c codex_home_c --sandbox-c read-only --tasks all --reps 1
echo "SERIES_DONE rc=$?"
