import os
import argparse
from tqdm import tqdm

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", default=os.getenv("TUSHARE_TOKEN", ""), help="TuShare token (or env TUSHARE_TOKEN)")
    ap.add_argument("--start", required=True, help="YYYYMMDD")
    ap.add_argument("--end", required=True, help="YYYYMMDD")
    ap.add_argument("--out", required=True, help="output dir, e.g. data/raw/daily_by_date")
    args = ap.parse_args()

    if not args.token:
        raise SystemExit("TuShare token missing. Use --token or export TUSHARE_TOKEN=...")

    import tushare as ts
    ts.set_token(args.token)
    pro = ts.pro_api()

    os.makedirs(args.out, exist_ok=True)

    cal = pro.trade_cal(exchange="SSE", start_date=args.start, end_date=args.end, fields="cal_date,is_open")
    dates = cal.loc[cal["is_open"] == 1, "cal_date"].tolist()

    for d in tqdm(dates, desc="Fetching daily"):
        df = pro.daily(trade_date=d, fields="ts_code,trade_date,open,high,low,close,vol,amount")
        if df is None or df.empty:
            continue
        df.to_csv(os.path.join(args.out, f"daily_{d}.csv"), index=False)

    sb = pro.stock_basic(exchange="", list_status="L", fields="ts_code,name,industry,market,list_date")
    sb.to_csv(os.path.join(args.out, "stock_basic.csv"), index=False)

    print(f"Done. Saved to: {args.out}")

if __name__ == "__main__":
    main()
