import numpy as np
from sklearn.ensemble import (
    RandomForestRegressor,
    AdaBoostRegressor,
    BaggingRegressor,
    GradientBoostingRegressor,
    HistGradientBoostingRegressor
)


def intrapred(minutes, prices, x):
    """Predict intraday stock prices using multiple ML algorithms"""
    predictions = []
    scores = []
    
    # Random Forest Regressor
    rfc = RandomForestRegressor(n_estimators=100, random_state=42)
    rfc.fit(minutes, prices)
    predictions.append(rfc.predict(x))
    scores.append(rfc.score(minutes, prices))

    # Bagging Regressor
    bgr = BaggingRegressor(n_estimators=100, random_state=42)
    bgr.fit(minutes, prices)
    predictions.append(bgr.predict(x))
    scores.append(bgr.score(minutes, prices))

    # AdaBoost Regressor
    adr = AdaBoostRegressor(n_estimators=100, learning_rate=1, random_state=42)
    adr.fit(minutes, prices)
    predictions.append(adr.predict(x))
    scores.append(adr.score(minutes, prices))

    # Gradient Boosting Regressor
    gbr = GradientBoostingRegressor(n_estimators=100, loss="absolute_error", random_state=42)
    gbr.fit(minutes, prices)
    predictions.append(gbr.predict(x))
    scores.append(gbr.score(minutes, prices))

    # Histogram Gradient Boosting Regressor
    hgbr = HistGradientBoostingRegressor(max_iter=100, loss="absolute_error", random_state=42)
    hgbr.fit(minutes, prices)
    predictions.append(hgbr.predict(x))
    scores.append(hgbr.score(minutes, prices))
    
    return [predictions, scores]
