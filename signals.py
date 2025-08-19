from typing import List


def download_csv(timeframes: List[str]) -> None:
    """Download CSV data for each timeframe.

    Currently a stub that prints the requested timeframes.
    """
    for tf in timeframes:
        print(f"Downloading CSV data for {tf}")


def aggregate_signals(timeframes: List[str], target_tf: str) -> None:
    """Aggregate signals from multiple timeframes into a target timeframe.

    Currently a stub that prints the aggregation action.
    """
    print(f"Aggregating signals from {timeframes} into {target_tf}")
