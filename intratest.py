import numpy as np
from sklearn.ensemble import (
    RandomForestRegressor,
    AdaBoostRegressor,
    BaggingRegressor,
    GradientBoostingRegressor,
    HistGradientBoostingRegressor
)


def intratestpred(minutes, prices, prediction_point):
    """Test intraday predictions and return the best performing algorithm's results"""
    algorithms = {
        'RFC': RandomForestRegressor(n_estimators=100, random_state=42),
        'BGR': BaggingRegressor(n_estimators=100, random_state=42),
        'ADR': AdaBoostRegressor(n_estimators=100, learning_rate=1, random_state=42),
        'GBR': GradientBoostingRegressor(n_estimators=100, loss="absolute_error", random_state=42),
        'HGBR': HistGradientBoostingRegressor(max_iter=100, loss="absolute_error", random_state=42)
    }
    
    scores = {}
    predictions = {}
    
    # Train each algorithm and collect scores
    for name, algorithm in algorithms.items():
        algorithm.fit(minutes, prices)
        score = algorithm.score(minutes, prices)
        scores[name] = score
        predictions[name] = algorithm.predict(minutes)
    
    # Find the best performing algorithm
    best_algo = max(scores, key=scores.get)
    
    return predictions[best_algo].tolist()
