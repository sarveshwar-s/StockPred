# import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import time
from sklearn.svm import SVR
import requests as req
# from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import GradientBoostingRegressor
 # explicitly require this experimental feature for histgradientboostingRegressor as it is still in experimental stage
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingRegressor

from sklearn.metrics import explained_variance_score
from sklearn import neighbors

from sklearn import preprocessing
from sklearn import utils
import schedule

def intratestpred(minutes,prices,x):
    returnprice = []
    returnscore = []
    rfcl=[]
    bgrl=[]
    adrl=[]
    gbrl=[]
    hgbrl=[]
    rfc = RandomForestRegressor(n_estimators=100)
    rfc.fit(minutes,prices)
    rfc_predicted = rfc.predict(x)
    rfcp = rfc.predict(minutes)
    for i in range(0, len(rfcp)):
        rfcl.append(rfcp[i])
    # print("PREDICTED RFC VALUE FOR",x,"MINUTE IS", rfc_predicted,"THE SCORE IS", rfc.score(minutes,prices))
    returnprice.append(rfc_predicted)
    returnscore.append(rfc.score(minutes,prices))

    bgr =  BaggingRegressor(n_estimators=100)
    bgr.fit(minutes,prices)
    bgr_predicted = bgr.predict(x)
    bgrp = bgr.predict(minutes)
    for i in range(0, len(bgrp)):
        bgrl.append(bgrp)
    print("BGR PREDICTED",bgr_predicted , bgr.score(minutes,prices))
    returnprice.append(bgr_predicted)
    returnscore.append(bgr.score(minutes,prices))

    adr = AdaBoostRegressor(n_estimators=100,learning_rate=1)
    adr.fit(minutes,prices)
    adr_predicted = adr.predict(x)
    adrp = adr.predict(minutes)
    for i in range(0, len(adrp)):
        adrl.append(adrp)
    print("ADR PREDICTED", adr_predicted, adr.score(minutes,prices))
    returnprice.append(adr_predicted)
    returnscore.append(adr.score(minutes,prices))

    gbr = GradientBoostingRegressor(n_estimators=100,loss='lad')
    gbr.fit(minutes,prices)
    gbr_predicted = gbr.predict(x)
    gbrp = gbr.predict(minutes)
    for i in range(0, len(gbrp)):
        gbrl.append(gbrp)
    print("GBR PREDICTED", gbr_predicted, gbr.score(minutes,prices))
    returnprice.append(gbr_predicted)
    returnscore.append(gbr.score(minutes,prices))

    hgbr = HistGradientBoostingRegressor(max_iter=100,loss='least_absolute_deviation',warm_start=True)
    hgbr.fit(minutes,prices)
    hgbr_predicted = hgbr.predict(x)
    hgbrp = hgbr.predict(minutes)
    for i in range(0, len(hgbrp)):
        hgbrl.append(hgbrp)
    print("HGBR predicted", hgbr_predicted, hgbr.score(minutes,prices))
    returnprice.append(hgbr_predicted)
    returnscore.append(hgbr.score(minutes,prices))
    algo_name=["RFC","BGR","ADR","GBR","HGBR"]
    finalalgo = algo_name[returnscore.index(max(returnscore))]
    finalreturn = rfcl
    print(finalalgo)
    if(finalalgo=="RFC"):
        print("print rfc")
        print(rfcl)
        finalreturn = rfcl
    elif(finalalgo=="BGR"):
        print("print bgr")
        print(bgrl)
        finalreturn = bgrl
    elif(finalalgo=="GBR"):
        print("print GBR")
        print(gbrl)
        finalreturn = gbrl
    elif(finalalgo=="ADR"):
        print("printing ADR")
        print(adrl)
        finalreturn = adrl
    else:
        print("print HGBR")
        print(hgbrl)
        finalreturn = hgbrl
    return rfcl


dates = []
prices = []
# for i in range(1,5):
#     api_url = "https://cloud.iexapis.com/stable/stock/aapl/intraday-prices?token=pk_16f5315051b240f5a1d5058dd880179b"
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
for i in range(1,(len(data_30)+1)):
    minute_list.append([i])
    if(data_30[i-1]["open"]==None):
        print("NULL at", i-1)
        price_list.append(data_30[i-2]["open"])
    else:
        price_list.append(data_30[i-1]["open"])
print(minute_list)
print(price_list)
def tobedone(x):
    api_url = "https://cloud.iexapis.com/stable/stock/aapl/intraday-prices?token=pk_16f5315051b240f5a1d5058dd880179b"
    response = req.get(api_url)
    data_30 = response.json()
    print("The length is ", len(data_30))
    intratestpred(minute_list[:(len(data_30)-1)],price_list[:(len(data_30)-1)],[[(len(data_30)+15)]])

# intrapred(minute_list[:30],price_list[:30],[[30]])
# returneddata = intratestpred(minute_list,price_list,[[45]])
# print("=================================================================================================")
# print(returneddata[0])
print("ORIGINAL PRICE AT 45st MINUTE", price_list[45])
buy_value = data_30[1]["open"]
profit_value = (buy_value * 0.01)
min_sell_value = buy_value + profit_value
print("EXPECTED SELL VALUE", min_sell_value)


# schedule.every(1).minutes.do(tobedone,"intraday")
# # schedule.every().day.at("20:00").do(tobedone,"automation")
# while True:
#     schedule.run_pending()
#     time.sleep(1)
    