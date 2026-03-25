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

api_url = "https://cloud.iexapis.com/stable/stock/aapl/intraday-prices?token=pk_16f5315051b240f5a1d5058dd880179b"
response = req.get(api_url)
data_30 = response.json()
print("The length is ", len(data_30))
print(data_30[0])
minute_list = []
price_list = []
for i in range(1, (len(data_30) + 1)):
    minute_list.append([i])
    if data_30[i - 1]["open"] == None:
        print("NULL at", i - 1)
        price_list.append(data_30[i - 2]["open"])
    else:
        price_list.append(data_30[i - 1]["open"])
# print(minute_list)
# print(price_list)
def tobedone(x):
    api_url = "https://cloud.iexapis.com/stable/stock/aapl/intraday-prices?token=pk_16f5315051b240f5a1d5058dd880179b"
    response = req.get(api_url)
    data_30 = response.json()
    print("The length is ", len(data_30))
    intrapred(minute_list[: (len(data_30) - 1)], price_list[: (len(data_30) - 1)], [[(len(data_30) + 15)]])


# intrapred(minute_list[:31],price_list[:31],[[32]])
print("ORIGINAL PRICE AT 45st MINUTE", price_list[45])
buy_value = data_30[1]["open"]
profit_value = buy_value * 0.01
min_sell_value = buy_value + profit_value
print("EXPECTED SELL VALUE", min_sell_value)


# schedule.every(1).minutes.do(tobedone,"intraday")
# # schedule.every().day.at("20:00").do(tobedone,"automation")
# while True:
#     schedule.run_pending()
#     time.sleep(1)
