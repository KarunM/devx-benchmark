#!/bin/zsh
cd <BENCH>
. <SCRATCH>/difl.sh
/usr/bin/python3 run_bench.py --series trial-qwen-di --tasks H-L1,H-R1,H-S2 --tasks-file tasks_heldout.json --arm CN --codex-home-c codex_home_c --sandbox-c read-only "${DIFLAGS[@]}"
echo "TRIAL_DONE rc=$?"
