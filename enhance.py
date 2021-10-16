import datetime
import schedule
import time
import requests as req
x = datetime.datetime.now()
print(x.hour)
print(x.minute)
hour = x.strftime("%H")
minute = x.strftime("%M")
print(type(x.strftime("%m")))
# print(x.year)
# print(x.month)
# print(x.day)
year=x.strftime("%Y")
month = x.strftime("%m")
dayss=x.strftime("%d")
print(year+month+dayss)

def tobedone(x):
    print("my job is",x)
    api_url = "https://cloud.iexapis.com/stable/stock/aapl/intraday-prices?token=YOUR_API_KEY"
    response = req.get(api_url)
    data_30 = response.json()
    print("The length is ", len(data_30),"The highvalue is ", data_30[len(data_30)-1]["high"])

schedule.every(1).minutes.do(tobedone,"intraday")
# schedule.every().day.at("20:00").do(tobedone,"automation")
while True:
    schedule.run_pending()
    time.sleep(1)
