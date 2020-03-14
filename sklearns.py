# from sklearn import datasets
# iris = datasets.load_iris()
# digits = datasets.load_digits()
# # print("IRIS DATA" ,iris)
# print("DIGITS DATA", digits.data)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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


def prediction_close(dates,prices,x):
    svr_lin = SVR(kernel="poly", C=1e3, degree=5)
    svr_rbf = SVR(kernel="rbf", C=1e3, gamma=0.1)
    
    # lab_enc = preprocessing.LabelEncoder()
    # encoded_prices = lab_enc.fit_transform(prices)

    # lr = LogisticRegression(random_state=0).fit(dates,encoded_prices)
    # print("Logistic Regression:",lr.predict(dates))
    result_list = []
    rfc = RandomForestRegressor(n_estimators=100)
    rfc.fit(dates,prices)
    rfc_prob = []
    rfc_predicted_values = rfc.predict(dates)
    for i in range(len(rfc_predicted_values)):
        min_dev = prices[i]-0.05
        max_dev = prices[i]+0.05
        if((rfc_predicted_values[i]<= min_dev) or (rfc_predicted_values[i]>max_dev)):
            rfc_prob.append(False)
        else:
            rfc_prob.append(True)
    print("TOTAL TRUES", rfc_prob.count(True))
    print("TOTAL FALSES", rfc_prob.count(False))
    print("RELIABILITY FACTOR RFC:",rfc_prob.count(True)/len(rfc_prob))
    print("RFC SCORE:" , rfc.score(dates,prices),"RFC PREDICTION:" ,rfc.predict(x))
    result_list.append(rfc.predict(x)[0])

    adr = AdaBoostRegressor(n_estimators=100,learning_rate=1)
    adr.fit(dates,prices)
    print("ADR SCORE", adr.score(dates,prices),"ADR PREDICTION:", adr.predict(x))
    adrvalues = adr.predict(x)
    result_list.append(adr.predict(x)[0])

    bgr = BaggingRegressor(n_estimators=100)
    bgr.fit(dates,prices)
    print("BGR VALUE:", bgr.predict(x), "BGR SCORE:", bgr.score(dates,prices))
    result_list.append(bgr.predict(x)[0])

    gbr = GradientBoostingRegressor(n_estimators=100,loss='lad')
    gbr.fit(dates,prices)
    # print(gbr.predict(dates))
    print("GBR VALUE:", gbr.predict(x), "GBR SCORE:", gbr.score(dates,prices))
    result_list.append( gbr.predict(x)[0])

    #in hgbr n_estimator is replaced by max_iter, controls the number of iteration of the boosting process
    hgbr = HistGradientBoostingRegressor(max_iter=100,loss='least_absolute_deviation',warm_start=True)
    hgbr.fit(dates,prices)
    print("HGBR VALUE:", hgbr.predict(x), "HGBR SCORE:", hgbr.score(dates,prices))
    result_list.append(hgbr.predict(x)[0])

    # svr_lin.fit(dates,prices)
    # svr_rbf.fit(dates,prices)
    # # print(svr_rbf.predict(dates))
    # print("RBF PREDICTION:",svr_rbf.predict(x), "POLY PREDICTION",svr_lin.predict(x))
    # print("RBF SCORE: ",svr_rbf.score(dates,prices))
    # result_list.append(svr_rbf.predict(x)[0])
    return result_list

def gbr_estimator(dates,prices):
    variance_list = []
    gbr = GradientBoostingRegressor(n_estimators=100,loss='lad')
    gbr.fit(dates,prices)
    adr = AdaBoostRegressor(n_estimators=100,learning_rate=1)
    adr.fit(dates,prices)
    bgr = BaggingRegressor(n_estimators=100)
    bgr.fit(dates,prices)
    hgbr = HistGradientBoostingRegressor(max_iter=100,loss='least_absolute_deviation',warm_start=True)
    hgbr.fit(dates,prices)
    variance_gbr = explained_variance_score(prices,gbr.predict(dates), multioutput='variance_weighted')
    variance_adr = explained_variance_score(prices,adr.predict(dates),multioutput='variance_weighted')
    variance_bgr = explained_variance_score(prices,bgr.predict(dates),multioutput='variance_weighted')
    variance_hgbr= explained_variance_score(prices,hgbr.predict(dates),multioutput='variance_weighted')
    variance_list.append(variance_gbr)
    variance_list.append(variance_adr)
    variance_list.append(variance_bgr)
    variance_list.append(variance_hgbr)
    # knn = neighbors.KNeighborsRegressor(n_neighbors=5,weights='distance')
    # knn.fit(dates,prices)
    # print(knn.predict([[20200101]]))
    return variance_list
    



dates = []
prices = []
api_url = "https://financialmodelingprep.com/api/v3/historical-price-full/aapl?from=2019-03-04&to=2020-03-04"
response = req.get(api_url)
data_30 = response.json()
for i in range(len(data_30["historical"])-1):
    # print((data_30["historical"][i]["date"]).split('-')[2])
    dates.append([int((data_30["historical"][i]["date"]).replace('-',''))])
    prices.append(data_30["historical"][i]["close"])
print(dates)
# print(prices)
estimation = gbr_estimator(dates,prices)
print(estimation)
algo_name=["RFC","ADR","BGR","GBR","HGBR","RBF"]
yes_pred = prediction_close(dates,prices,[[20200305]])
print("30-12-2019 PREDICTION", yes_pred)
print("actual close data:", prices[len(prices)-1])
org = prices[len(prices)-1]
diff = []
for i in range(len(yes_pred)):
    diff.append(abs(yes_pred[i]-org))
print(diff)
print(min(diff))
print(algo_name[diff.index(min(diff))])
# new_prediction = prediction_close(dates,prices,[[20191231]])
# prices.append(new_prediction[0])
# dates.append([20191231])
# jan_prediction = prediction_close(dates,prices,[[20200101]])
# print("december:",new_prediction,"january:",jan_prediction)



########################################################################## INFY NSE PRICE PREDICTION ##################################################
# df = pd.read_csv('infy1.csv')
# # print(df["date"][0])
# infydate = []
# indate=[]
# infyprice = []
# inprice = []
# for i in range(len(df["date"])):
#     infydate.append(df["date"][i])
# for i in range(len(df["close"])):
#     infyprice.append(df["close"][i])
# lens = len(infydate)-1
# for i in range(len(infydate)):
#     indate.append(infydate[lens])
#     inprice.append(infyprice[lens])
#     lens-=1
# print(indate)
# print(inprice)
# newdate=[]
# for i in range(len(indate)):
#     newdate.append([int((indate[i]).replace('-',''))])
# print(newdate)
# infypri = prediction_close(newdate,inprice,[[20200101]])
# print(infypri)
####################################################################INFY NSE PRICE PREDICTION CLOSE ###################################################