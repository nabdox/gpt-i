from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression


@dataclass
class DataConfig:
    """Configuration des données.

    Attributes:
        symbol: Nom de la paire (ex: "XAUUSD").
        timeframes: Liste de timeframes à agréger (ex: ["M1", "M15", "H1"]).
        data_path: Dossier contenant les fichiers CSV "<symbol>_<timeframe>.csv".
    """

    symbol: str
    timeframes: List[str]
    data_path: Path = Path("data")


def load_data(symbol: str, timeframe: str, base_path: Path) -> pd.DataFrame:
    """Charge un fichier CSV OHLC pour un symbole et un timeframe donnés."""
    file = base_path / f"{symbol}_{timeframe}.csv"
    df = pd.read_csv(file, parse_dates=["Date"], index_col="Date")
    return df


def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calcule un RSI simple."""
    delta = series.diff()
    up = delta.clip(lower=0)
    down = (-delta).clip(lower=0)
    roll_up = up.ewm(com=period - 1, adjust=False).mean()
    roll_down = down.ewm(com=period - 1, adjust=False).mean()
    rs = roll_up / roll_down
    return 100 - (100 / (1 + rs))


def compute_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calcule un Average True Range basique."""
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift()).abs()
    low_close = (df["Low"] - df["Close"].shift()).abs()
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    return true_range.rolling(period).mean()


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """Génère quelques indicateurs simples."""
    out = pd.DataFrame(index=df.index)
    out["return"] = df["Close"].pct_change()
    out["sma"] = df["Close"].rolling(14).mean()
    out["rsi"] = compute_rsi(df["Close"])
    out["atr"] = compute_atr(df)
    return out.dropna()


def align_timeframes(features: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Aligne les features de différentes TF sur l'index commun."""
    frames = [f.add_prefix(f"{tf}_") for tf, f in features.items()]
    return pd.concat(frames, axis=1, join="inner")


class Aggregator:
    """Agrégateur probabiliste via régression logistique."""

    def __init__(self) -> None:
        self.model = LogisticRegression(max_iter=1000, class_weight="balanced")

    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        self.model.fit(X, y)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict_proba(X)[:, 1]


class MoneyManager:
    """Gestion basique du risque basée sur l'ATR."""

    def __init__(self, risk_perc: float = 1.0) -> None:
        self.risk_perc = risk_perc

    def position_size(self, capital: float, atr: float, price: float) -> float:
        risk_amount = capital * self.risk_perc / 100
        units = risk_amount / atr
        return units / price


def run_workflow(cfg: DataConfig) -> pd.DataFrame:
    """Pipeline complet : chargement, features, apprentissage, prévisions."""
    feats: Dict[str, pd.DataFrame] = {}
    for tf in cfg.timeframes:
        raw = load_data(cfg.symbol, tf, cfg.data_path)
        feats[tf] = compute_features(raw)

    dataset = align_timeframes({tf: f[["return", "sma", "rsi", "atr"]] for tf, f in feats.items()})
    # Cible : retour positif sur le plus petit timeframe
    smallest_tf = cfg.timeframes[0]
    dataset["target"] = (dataset[f"{smallest_tf}_return"].shift(-1) > 0).astype(int)
    dataset = dataset.dropna()

    train = dataset.iloc[:-100]
    test = dataset.iloc[-100:]

    agg = Aggregator()
    agg.train(train.drop(columns="target"), train["target"])
    probs = agg.predict_proba(test.drop(columns="target"))

    out = test.copy()
    out["prob"] = probs
    return out[["prob"]]


if __name__ == "__main__":
    cfg = DataConfig(symbol="XAUUSD", timeframes=["M1", "M15", "H1"], data_path=Path("data"))
    try:
        result = run_workflow(cfg)
        print(result.tail())
    except FileNotFoundError:
        print("⚠️ CSV introuvable. Placez vos données dans le dossier 'data'.")
