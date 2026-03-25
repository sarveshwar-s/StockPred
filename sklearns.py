import numpy as np
from sklearn.svm import SVR
from sklearn.ensemble import (
    RandomForestRegressor,
    AdaBoostRegressor,
    BaggingRegressor,
    GradientBoostingRegressor,
    HistGradientBoostingRegressor
)
from sklearn.metrics import explained_variance_score


def prediction_close(dates, prices, prediction_dates):
    """Predict stock closing prices using multiple ML algorithms"""
    predictions = []
    
    # Random Forest Regressor
    rfc = RandomForestRegressor(n_estimators=100, random_state=42)
    rfc.fit(dates, prices)
    predictions.append(rfc.predict(prediction_dates)[0])

    # AdaBoost Regressor
    adr = AdaBoostRegressor(n_estimators=100, learning_rate=1, random_state=42)
    adr.fit(dates, prices)
    predictions.append(adr.predict(prediction_dates)[0])

    # Bagging Regressor
    bgr = BaggingRegressor(n_estimators=100, random_state=42)
    bgr.fit(dates, prices)
    predictions.append(bgr.predict(prediction_dates)[0])

    # Gradient Boosting Regressor
    gbr = GradientBoostingRegressor(n_estimators=100, loss="absolute_error", random_state=42)
    gbr.fit(dates, prices)
    predictions.append(gbr.predict(prediction_dates)[0])

    # Histogram Gradient Boosting Regressor
    hgbr = HistGradientBoostingRegressor(max_iter=100, loss="absolute_error", random_state=42)
    hgbr.fit(dates, prices)
    predictions.append(hgbr.predict(prediction_dates)[0])

    # Support Vector Regression (RBF kernel)
    svr_rbf = SVR(kernel="rbf", C=1e3, gamma=0.1)
    svr_rbf.fit(dates, prices)
    predictions.append(svr_rbf.predict(prediction_dates)[0])
    
    return predictions


def gbr_estimator(dates, prices):
    """Calculate variance scores for different ML algorithms"""
    algorithms = [
        GradientBoostingRegressor(n_estimators=100, loss="absolute_error", random_state=42),
        AdaBoostRegressor(n_estimators=100, learning_rate=1, random_state=42),
        BaggingRegressor(n_estimators=100, random_state=42),
        HistGradientBoostingRegressor(max_iter=100, loss="absolute_error", random_state=42)
    ]
    
    variance_scores = []
    for algorithm in algorithms:
        algorithm.fit(dates, prices)
        predicted_values = algorithm.predict(dates)
        variance_score = explained_variance_score(prices, predicted_values, multioutput="variance_weighted")
        variance_scores.append(variance_score)
    
    return variance_scores


# print(indate)
# print(inprice)
# newdate=[]
# for i in range(len(indate)):
#     newdate.append([int((indate[i]).replace('-',''))])
# print(newdate)
# infypri = prediction_close(newdate,inprice,[[20200101]])
# print(infypri)
####################################################################INFY NSE PRICE PREDICTION CLOSE ###################################################
