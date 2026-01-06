#!/usr/bin/env bash
set -euo pipefail

ROOT="$HOME/projects/a_share_qlib_top30"
cd "$ROOT"

mkdir -p logs outputs

LOG="logs/run_$(date +%F)_1700_bjt.log"
exec > >(tee -a "$LOG") 2>&1

echo "[START] $(date)"
source .venv/bin/activate

# 仅当工作区干净时才 pull，避免 rebase 报错
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if git diff --quiet && git diff --cached --quiet; then
    echo "[GIT] Clean working tree, pulling..."
    git pull --rebase || true
  else
    echo "[GIT] Working tree not clean, skip pull."
  fi
fi

python scripts/export_top30_from_pred.py --config configs/workflow_allA_k30.yaml --topk 30 --segment test

echo "[DONE] wrote outputs/top30_latest.csv"
echo "[END] $(date)"
