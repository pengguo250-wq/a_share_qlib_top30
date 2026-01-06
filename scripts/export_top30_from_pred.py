import argparse
from pathlib import Path
import yaml
import pandas as pd

import qlib
from qlib.constant import REG_CN
from qlib.utils.mod import init_instance_by_config


def ensure_inst_dt_order(s: pd.Series) -> pd.Series:
    if not isinstance(s.index, pd.MultiIndex) or s.index.nlevels != 2:
        raise ValueError(f"pred index is not 2-level MultiIndex: {type(s.index)}")

    lv0 = s.index.get_level_values(0)
    lv1 = s.index.get_level_values(1)

    is_dt0 = pd.api.types.is_datetime64_any_dtype(lv0) or isinstance(lv0[0], pd.Timestamp)
    is_dt1 = pd.api.types.is_datetime64_any_dtype(lv1) or isinstance(lv1[0], pd.Timestamp)

    if is_dt0 and not is_dt1:
        s = s.copy()
        s.index = pd.MultiIndex.from_arrays([lv1, lv0], names=["instrument", "datetime"])
        return s

    names = list(s.index.names)
    if names[0] is None:
        names[0] = "instrument"
    if names[1] is None:
        names[1] = "datetime"
    s.index = s.index.set_names(names)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out_csv", default="outputs/top30_latest.csv")
    ap.add_argument("--segment", default="test", choices=["train", "valid", "test"])
    ap.add_argument("--topk", type=int, default=30)
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))

    qlib.init(provider_uri=cfg["qlib_init"]["provider_uri"], region=REG_CN)

    task = cfg["task"]
    model = init_instance_by_config(task["model"])
    dataset = init_instance_by_config(task["dataset"])

    model.fit(dataset)
    pred = model.predict(dataset, segment=args.segment)

    if isinstance(pred, pd.DataFrame):
        s = pred.iloc[:, 0]
    elif isinstance(pred, pd.Series):
        s = pred
    else:
        raise ValueError(f"Unexpected pred type: {type(pred)}")

    s = ensure_inst_dt_order(s)
    dts = sorted(set(s.index.get_level_values(1)))
    last_dt = dts[-1]
    top = s.xs(last_dt, level=1).sort_values(ascending=False).head(args.topk)

    out = top.reset_index()
    out.columns = ["instrument", "score"]
    out.insert(1, "date", str(last_dt))

    out_csv = Path(args.out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_csv, index=False, encoding="utf-8-sig")

    print("Wrote:", out_csv)
    print(out.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
