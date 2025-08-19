import argparse
from typing import List

from signals import download_csv, aggregate_signals


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download data and aggregate signals")
    parser.add_argument(
        "--timeframes",
        nargs="+",
        required=True,
        help="List of timeframes to download (e.g., 15m 30m 1h)",
    )
    parser.add_argument(
        "--target-tf",
        required=True,
        help="Target timeframe for aggregation (e.g., 1h)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    download_csv(args.timeframes)
    aggregate_signals(args.timeframes, args.target_tf)


if __name__ == "__main__":
    main()
