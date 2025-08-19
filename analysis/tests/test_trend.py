import pandas as pd

from ..trend import detect_trend


def test_uptrend():
    df = pd.DataFrame({"price": range(1, 21)})
    assert detect_trend(df) == "uptrend"


def test_downtrend():
    df = pd.DataFrame({"price": range(20, 0, -1)})
    assert detect_trend(df) == "downtrend"


def test_sideways():
    df = pd.DataFrame({"price": [1] * 20})
    assert detect_trend(df) == "sideways"

