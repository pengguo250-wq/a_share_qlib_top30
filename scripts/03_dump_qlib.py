import argparse
import os
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parquet", required=True, help="parquet dir containing daily.parquet")
    ap.add_argument("--qlib_dir", required=True, help="output qlib dir, e.g. data/qlib_cn")
    args = ap.parse_args()

    parquet_fp = os.path.join(args.parquet, "daily.parquet")
    if not os.path.exists(parquet_fp):
        raise SystemExit(f"Missing {parquet_fp}. Run 02_to_parquet.py first.")

    os.makedirs(args.qlib_dir, exist_ok=True)
    df = pd.read_parquet(parquet_fp)

    tmp = df.copy()
    tmp.rename(columns={"instrument": "symbol", "vol": "volume"}, inplace=True)
    tmp["date"] = tmp["date"].astype(str)
    tmp["date"] = tmp["date"].str.slice(0,4) + "-" + tmp["date"].str.slice(4,6) + "-" + tmp["date"].str.slice(6,8)
    keep = ["symbol","date","open","high","low","close","volume","amount"]
    tmp = tmp[keep]
    tmp_csv = os.path.join(args.qlib_dir, "_tmp_daily.csv")
    tmp.to_csv(tmp_csv, index=False)

    from qlib.data.dump_bin import DumpDataAll
    dumper = DumpDataAll(
        csv_path=tmp_csv,
        qlib_dir=args.qlib_dir,
        include_fields=keep[2:],
        symbol_field_name="symbol",
        date_field_name="date",
        freq="day",
    )
    dumper.dump()
    print(f"Dumped qlib data to: {args.qlib_dir}")

if __name__ == "__main__":
    main()
