#!/usr/bin/env bash
set -euo pipefail

ROOT="$HOME/projects/a_share_qlib_top30"
cd "$ROOT"

mkdir -p logs outputs

LOG="logs/run_$(date +%F)_1700_bjt.log"
exec > >(tee -a "$LOG") 2>&1

echo "[START] $(date)"
source .venv/bin/activate

# git pull 不阻塞（有改动就 stash）
STASHED=0
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if ! git diff --quiet || ! git diff --cached --quiet; then
    echo "[GIT] Unstaged changes detected, stashing..."
    git stash push -u -m "auto-stash before cron run" || true
    STASHED=1
  fi
  echo "[GIT] Pull latest..."
  git pull --rebase || true
fi

python scripts/export_top30_from_pred.py --config configs/workflow_allA_k30.yaml --topk 30 --segment test

echo "[DONE] wrote outputs/top30_latest.csv"

if [ "$STASHED" = "1" ]; then
  echo "[GIT] Restoring stashed changes..."
  git stash pop || true
fi

echo "[END] $(date)"
