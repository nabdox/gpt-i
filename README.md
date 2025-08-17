# gpt-i

Prototype de stratégie de trading IA multi-timeframe.

Le module principal est `strategy.py`, qui illustre :

- agrégation de données multi-échelles,
- régression logistique pour générer une probabilité,
- gestion simple du risque via ATR.

Pour exécuter un exemple :

```bash
pip install -r requirements.txt  # si nécessaire
python strategy.py
```

Les fichiers CSV `XAUUSD_<TF>.csv` doivent se trouver dans le dossier `data/`.
