import argparse
import subprocess
import sys
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="yaml config path")
    args = ap.parse_args()

    cfg = Path(args.config)
    if not cfg.exists():
        raise SystemExit(f"Config not found: {cfg}")

    cmd = ["qrun", str(cfg)]
    print("Running:", " ".join(cmd))
    r = subprocess.run(cmd)
    sys.exit(r.returncode)

if __name__ == "__main__":
    main()
