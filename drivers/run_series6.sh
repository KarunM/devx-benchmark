#!/bin/zsh
cd <BENCH>
/usr/bin/python3 run_bench.py --series series6 --tasks-file tasks_heldout.json --arm CN --codex-home-c codex_home_c --sandbox-c read-only --tasks all --reps 1 --model gpt-5.6-luna
echo "SERIES_DONE rc=$?"
