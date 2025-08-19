import pandas as pd

def detect_trend(df: pd.DataFrame) -> str:
    """Detects overall trend based on moving averages.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing a ``price`` column representing sequential price
        data.

    Returns
    -------
    str
        One of ``"uptrend"``, ``"downtrend"`` or ``"sideways"`` depending on
        the final relation of short and long moving averages.
    """
    if "price" not in df.columns:
        raise ValueError("DataFrame must contain a 'price' column")

    short_window, long_window = 3, 5
    if len(df) < long_window:
        raise ValueError("DataFrame must contain at least 5 rows for trend detection")

    short_ma = df["price"].rolling(window=short_window).mean().iloc[-1]
    long_ma = df["price"].rolling(window=long_window).mean().iloc[-1]

    diff = short_ma - long_ma
    threshold = 1e-9
    if diff > threshold:
        return "uptrend"
    if diff < -threshold:
        return "downtrend"
    return "sideways"
