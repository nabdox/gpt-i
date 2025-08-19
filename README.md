# gpt-i

## Dashboard

The Streamlit dashboard downloads market data automatically via `yfinance`.

Install dependencies and run:

```bash
pip install -r requirements.txt
streamlit run ui/dashboard.py
```

Enter a ticker symbol and select time intervals to view candlestick charts and
generate a simple Buy/Sell signal with stop and target levels.
