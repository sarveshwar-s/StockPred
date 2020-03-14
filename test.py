from flask import Flask
from flask import render_template
from flask import request
from textblob import TextBlob
import requests as req
import mysql.connector
from intra import intrapred
from sklearns import prediction_close
from news import news_analysis
from tweets import twitter_analysis
from intratest import intratestpred

app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)
db=mysql.connector.connect(host="stock.crne5vznig3b.ap-south-1.rds.amazonaws.com", user="admin", passwd="testingalgos",database="trading")


@app.route("/")
def hello_world():
    api_url = "https://financialmodelingprep.com/api/v3/historical-price-full/infy?from=2018-12-01&to=2019-12-31"
    response = req.get(api_url)
    data = response.json()
    return render_template('login.html', hist=data)

@app.route("/user/<username>")
def show_user_name(username): 
    strs = "Username is:" + username
    print(strs)
    return strs

@app.route("/investment/complist")
def list_company():
    list_api = "https://financialmodelingprep.com/api/v3/stock/actives"
    list_response = req.get(list_api)
    list_data = list_response.json()
    return render_template('complist.html', clist=list_data)

@app.route("/investment/compdetails", methods=['POST','GET'])
def details_company():
    if request.method == 'POST':
        cname = request.form.get('companyname')
    rating_api = "https://financialmodelingprep.com/api/v3/company/rating/" + cname
    print(rating_api)
    dcf_api = "https://financialmodelingprep.com/api/v3/company/discounted-cash-flow/" + cname.upper()
    profile_api = "https://financialmodelingprep.com/api/v3/company/profile/" + cname
    profile_response = req.get(profile_api)
    profile_data = profile_response.json()
    rating_response = req.get(rating_api)
    dcf_response = req.get(dcf_api)
    rating_data = rating_response.json()
    print(rating_data)
    dcf_data = dcf_response.json()
    return render_template('compdetails.html', data=cname, rating=rating_data,dcf=dcf_data,profile=profile_data)

# @app.route("/investment/profile/<companyname>")
# def show_profile_details(companyname):
#     profile_api = "https://financialmodelingprep.com/api/v3/company/profile/" + companyname
#     profile_response = req.get(profile_api)
#     profile_data = profile_response.json()
#     return render_template('compprofile.html', profile=profile_data)

@app.route("/investment/enterprise/<enterprisename>")
def show_enterprise_details(enterprisename):
    eapi_annual = "https://financialmodelingprep.com/api/v3/enterprise-value/" + enterprisename
    eapi_quarter = "https://financialmodelingprep.com/api/v3/enterprise-value/" + enterprisename + "?period=quarter"
    eres_annual = req.get(eapi_annual)
    eres_quarter = req.get(eapi_quarter)
    edata_annual = eres_annual.json()
    edata_quarter = eres_quarter.json()
    return render_template('enterprisedetails.html', enterpriseannual=edata_annual, enterprisequarter=edata_quarter)

@app.route("/investment/finstatement/<financename>")
def show_finance_details(financename):
    finance_state_api = "https://financialmodelingprep.com/api/v3/financial-statement-growth/" + financename
    financestate_response = req.get(finance_state_api)
    financestate_data = financestate_response.json()
    return render_template('fingrowth.html', financestate=financestate_data)


@app.route("/investment/finstate/<fincompanyname>")
def show_financial_state(fincompanyname):
    # gets finance data of company (annual and quarterly)
    finance_api = "https://financialmodelingprep.com/api/v3/financials/income-statement/" + fincompanyname
    finance_quarter_api = "https://financialmodelingprep.com/api/v3/financials/income-statement/" + fincompanyname + "?period=quarter"
    balance_sheet_annual = "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/" + fincompanyname
    balance_sheet_quarterly = "https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/" + fincompanyname + "?period=quarter"
    cashflow_annual = "https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/" + fincompanyname
    cashflow_quarterly = "https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/" + fincompanyname + "?period=quarter"
    balance_sheet_annual_response = req.get(balance_sheet_annual)
    balance_sheet_quarterly_response = req.get(balance_sheet_quarterly)
    cashflow_annual_response = req.get(cashflow_annual)
    cashflow_quarterly_response = req.get(cashflow_quarterly)
    finance_quarter_response = req.get(finance_quarter_api)
    balance_sheet_annual_data = balance_sheet_annual_response.json()
    balance_sheet_quarterly_data = balance_sheet_quarterly_response.json()
    cashflow_annual_data = cashflow_annual_response.json()
    cashflow_quarterly_data = cashflow_quarterly_response.json()
    finance_quarter_data = finance_quarter_response.json()
    finance_response = req.get(finance_api)
    finance_data = finance_response.json()
    return render_template('financestate.html', companynames=fincompanyname,
     finance_annual=finance_data, finance_quarter=finance_quarter_data,
     balancesheetannual= balance_sheet_annual_data, balancesheetquarter= balance_sheet_quarterly_data,
     cashflowannual= cashflow_annual_data, cashflowquarter = cashflow_quarterly_data)

# @app.route("/investment/")

# db=mysql.connector.connect(host="localhost", user="root", passwd="",database="stock")
# mycursor = db.cursor()
# mycursor.execute("INSERT INTO `users`(`username`, `password`) VALUES ('user1','google')")
# db.commit()
# print(mycursor.rowcount)

@app.route("/longterm/search")
def longterm_search():
    # db=mysql.connector.connect(host="localhost", user="root", passwd="",database="stock")
    mycursor = db.cursor()
    selectquery="SELECT * FROM intrasymbols"
    # insertquery = "INSERT INTO `intrasymbols`(`company_name`,`price`,`stock_symbol`,`exchange`) VALUES (%s,%s,%s,%s)"
    mycursor.execute(selectquery)
    results = mycursor.fetchall()
    comname=[]
    compprice=[]
    comexchange=[]
    comsymbol=[]
    for row in results:
        comname.append(row[1])
        compprice.append(row[2])
        comexchange.append(row[4])
        comsymbol.append(row[3])

    db.commit()
    print(mycursor.rowcount)
    return render_template("longtermsearch.html",compname=comname,comprice=compprice, comexchange=comexchange, compsymbol=comsymbol)

@app.route("/longterm/<longtermname>/index")
def longterm_prediction(longtermname):
    dates = []
    prices = []
    api_url = "https://financialmodelingprep.com/api/v3/historical-price-full/" +longtermname+"?from=2019-03-04&to=2020-03-04"
    response = req.get(api_url)
    data_30 = response.json()
    for i in range(len(data_30["historical"])-1):
        # print((data_30["historical"][i]["date"]).split('-')[2])
        dates.append([int((data_30["historical"][i]["date"]).replace('-',''))])
        prices.append(data_30["historical"][i]["close"])
    print(dates)
    print(prices)
    # estimation = gbr_estimator(dates,prices)
    # print(estimation)
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
    confirmation = yes_pred[diff.index(min(diff))]
    # db=mysql.connector.connect(host="localhost", user="root", passwd="",database="stock")
    mycursor = db.cursor()
    selectquery="SELECT * FROM intrasymbols where stock_symbol='" + longtermname + "'"
    # insertquery = "INSERT INTO `intrasymbols`(`company_name`,`price`,`stock_symbol`,`exchange`) VALUES (%s,%s,%s,%s)"
    mycursor.execute(selectquery)
    results = mycursor.fetchall()
    for row in results:
        compnames  = row[1]

    db.commit()
    print(mycursor.rowcount)
    news_result = news_analysis(compnames)
    twitter_result = twitter_analysis(compnames)
    return render_template("longterm.html",comnames=compnames,newsapi=news_result,twitterapi=twitter_result,sdates=dates,sprices=prices,alogsresult=yes_pred, confirmed=confirmation)

@app.route("/intraday/search")
def intraday_search():
    # db=mysql.connector.connect(host="localhost", user="root", passwd="",database="stock")
    mycursor = db.cursor()
    selectquery="SELECT * FROM intrasymbols"
    # insertquery = "INSERT INTO `intrasymbols`(`company_name`,`price`,`stock_symbol`,`exchange`) VALUES (%s,%s,%s,%s)"
    mycursor.execute(selectquery)
    results = mycursor.fetchall()
    comname=[]
    compprice=[]
    comexchange=[]
    comsymbol=[]
    for row in results:
        comname.append(row[1])
        compprice.append(row[2])
        comexchange.append(row[4])
        comsymbol.append(row[3])

    db.commit()
    print(mycursor.rowcount)
    return render_template("intradaysearch.html",compname=comname,comprice=compprice, comexchange=comexchange, compsymbol=comsymbol)

@app.route("/intraday/<intracomp>/index")
def intraday_prediction(intracomp):
    comppname = intracomp.lower()
    print(comppname)
    api_url = "https://cloud.iexapis.com/stable/stock/" + comppname +"/intraday-prices?token=pk_16f5315051b240f5a1d5058dd880179b"
    response = req.get(api_url)
    data_30 = response.json()
    # print("The length is ", len(data_30))
    # print(data_30[0])
    minute_list = []
    price_list = []
    for i in range(1,(len(data_30)+1)):
        minute_list.append([i])
        if(data_30[i-1]["open"]==None):
            print("NULL at", i-1)
            price_list.append(data_30[1]["open"])
        else:
            price_list.append(data_30[i-1]["open"])
    # api_url = "https://cloud.iexapis.com/stable/stock/aapl/intraday-prices?token=pk_16f5315051b240f5a1d5058dd880179b"
    # response = req.get(api_url)
    # data_30 = response.json()
    print("The length is ", len(data_30))
    # returndata = intrapred(minute_list[:(len(data_30)-1)],price_list[:(len(data_30)-1)],[[(len(data_30)+15)]])
    returndata = intrapred(minute_list[:45],price_list[:45],[[60]])
    intratestreturn = intratestpred(minute_list, price_list,[[45]])
    # intratestlist = []
    # for i in range(0, 389):
    #     intratestlist.append(intratestreturn[0][i])
    #     if(i<389):
    #         intratestlist.append(",")
    # print("======================================================================================")
    # print(intratestlist)
    print(returndata)  
    new_minutes = []
    for i in range(0, len(minute_list)):
        new_minutes.append(i)
    # db=mysql.connector.connect(host="localhost", user="root", passwd="",database="stock")
    mycursor = db.cursor()
    selectquery="SELECT * FROM intrasymbols where stock_symbol='" + intracomp + "'"
    # insertquery = "INSERT INTO `intrasymbols`(`company_name`,`price`,`stock_symbol`,`exchange`) VALUES (%s,%s,%s,%s)"
    mycursor.execute(selectquery)
    results = mycursor.fetchall()
    for row in results:
        compnames  = row[1]

    db.commit()
    print(mycursor.rowcount)
    news_result = news_analysis(compnames)
    twitter_result = twitter_analysis(compnames)
    return render_template("intra.html",companyname=compnames,newsapi=news_result,twitterapi=twitter_result,times=new_minutes,intratest=intratestreturn,pricelist=price_list, predictions=returndata[0], accuracy=returndata[1])

@app.route("/videos")
def making_video():
    return render_template("videos.html")
