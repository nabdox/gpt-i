# gpt-i

## Trend Detection

The `analysis.detect_trend` function determines whether a time series of
prices is in an uptrend, downtrend, or moving sideways. Supply a
`pandas.DataFrame` with a `price` column representing sequential prices:

```python
import pandas as pd
from analysis import detect_trend

df = pd.DataFrame({"price": [1, 2, 3, 4, 5]})
trend = detect_trend(df)
print(trend)
```
