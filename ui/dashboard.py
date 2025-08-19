import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf


def download_csv(symbol: str, interval: str) -> pd.DataFrame:
    """Download data for the given symbol and interval using yfinance."""
    interval_map = {
        "15m": "15m",
        "30m": "30m",
        "1h": "1h",
        "4h": "1h",  # download hourly data then resample
        "1D": "1d",
    }
    yf_interval = interval_map.get(interval)
    if yf_interval is None:
        raise ValueError(f"Unsupported interval: {interval}")

    df = yf.download(symbol, interval=yf_interval, period="60d", progress=False)
    if df.empty:
        raise ValueError("No data returned")

    if interval == "4h":
        df = (
            df.resample("4H")
            .agg({"Open": "first", "High": "max", "Low": "min", "Close": "last"})
            .dropna()
        )

    df = df.reset_index()
    df.columns = [col[0] for col in df.columns]
    df = df.drop(columns=[c for c in ["Adj Close"] if c in df.columns])
    return df


def generate_signal(df: pd.DataFrame) -> tuple[str, float, float]:
    """Very simple strategy: direction based on last candle, with basic stop/target."""
    last = df.iloc[-1]
    direction = "Buy" if last["Close"] > last["Open"] else "Sell"
    price = last["Close"]
    if direction == "Buy":
        stop, target = price * 0.99, price * 1.01
    else:
        stop, target = price * 1.01, price * 0.99
    return direction, round(stop, 2), round(target, 2)


def main() -> None:
    st.title("Trading Dashboard")

    symbol = st.text_input("Symbol", "AAPL").upper()

    st.sidebar.header("Intervals")
    interval_options = ["15m", "30m", "1h", "4h", "1D"]
    selected_intervals = [
        interval for interval in interval_options if st.sidebar.checkbox(interval, True)
    ]

    for interval in selected_intervals:
        try:
            df = download_csv(symbol, interval)
        except Exception as e:
            st.warning(f"Could not load data for {symbol} at {interval}: {e}")
            continue

        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=pd.to_datetime(df["Date"]),
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                )
            ]
        )
        fig.update_layout(title=f"{symbol} - {interval}")
        st.plotly_chart(fig, use_container_width=True)

    if st.button("Generate Signal"):
        try:
            df = download_csv(symbol, selected_intervals[0])
        except (Exception, IndexError) as e:
            st.error(f"No data available to generate a signal: {e}")
        else:
            direction, stop, target = generate_signal(df)
            st.success(f"Signal: {direction}")
            st.write(f"Stop: {stop}")
            st.write(f"Target: {target}")


if __name__ == "__main__":
    main()
