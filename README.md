# a_share_qlib_top30

TuShare 拉取 → 落 parquet → 转 Qlib bin → qrun 跑 Alpha158 + LightGBM（最小可跑通骨架）

## Quick start (WSL Ubuntu)

1) Create venv
- python3 -m venv .venv
- source .venv/bin/activate
- pip install -U pip wheel setuptools
- pip install -r requirements.txt

2) Export TuShare token
- export TUSHARE_TOKEN="YOUR_TOKEN"

3) Smoke test (short range)
- python scripts/01_tushare_fetch.py --start 20250101 --end 20250110 --out data/raw/daily_by_date
- python scripts/02_to_parquet.py --in data/raw/daily_by_date --out data/parquet
- python scripts/03_dump_qlib.py --parquet data/parquet --qlib_dir data/qlib_cn
- python scripts/04_qrun.py --config configs/workflow_allA_k30.yaml

Notes:
- Research/demo only. Not investment advice.
- Large data folders are gitignored by default.
