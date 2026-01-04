import argparse
import os
import glob
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="in_dir", required=True, help="input dir with daily_YYYYMMDD.csv")
    ap.add_argument("--out", dest="out_dir", required=True, help="output parquet dir")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    files = sorted(glob.glob(os.path.join(args.in_dir, "daily_*.csv")))
    if not files:
        raise SystemExit(f"No daily_*.csv found in {args.in_dir}")

    dfs = [pd.read_csv(fp, dtype={"ts_code": str, "trade_date": str}) for fp in files]
    df = pd.concat(dfs, ignore_index=True)

    df.rename(columns={"ts_code": "instrument", "trade_date": "date"}, inplace=True)
    out_fp = os.path.join(args.out_dir, "daily.parquet")
    df.to_parquet(out_fp, index=False)
    print(f"Saved: {out_fp} rows={len(df)}")

if __name__ == "__main__":
    main()
