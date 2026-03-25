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


#     response = req.get(api_url)
#     data_30 = response.json()
#     print("The length is ", len(data_30))
#     time.sleep(60)
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
    intratestpred(minute_list[: (len(data_30) - 1)], price_list[: (len(data_30) - 1)], [[(len(data_30) + 15)]])


# intrapred(minute_list[:30],price_list[:30],[[30]])
# returneddata = intratestpred(minute_list,price_list,[[45]])
# print("=================================================================================================")
# print(returneddata[0])
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
