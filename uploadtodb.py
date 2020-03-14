
import requests as req
import mysql.connector

api_url = "https://financialmodelingprep.com/api/v3/company/stock/list"
response = req.get(api_url)
data = response.json()

# db=mysql.connector.connect(host="localhost", user="root", passwd="",database="stock")
# mycursor = db.cursor()
# name = "aapll"
# insertquery = "INSERT INTO `intrasymbols`(`company_name`,`price`,`stock_symbol`,`exchange`) VALUES (%s,%s,%s,%s)"
# for i in range(8808,13000):
#     # print(data["symbolsList"][i])
#     mycursor.execute(insertquery,params=(data["symbolsList"][i]["name"],data["symbolsList"][i]["price"],data["symbolsList"][i]["symbol"],data["symbolsList"][i]["exchange"]))

# db.commit()
# print(mycursor.rowcount)
db=mysql.connector.connect(host="stock.crne5vznig3b.ap-south-1.rds.amazonaws.com", user="admin", passwd="testingalgos",database="trading")
mycursor = db.cursor()
selectquery="SELECT * FROM intrasymbols where id=11"
# insertquery = "INSERT INTO `intrasymbols`(`company_name`,`price`,`stock_symbol`,`exchange`) VALUES (%s,%s,%s,%s)"
mycursor.execute(selectquery)
results = mycursor.fetchall()
for row in results:
    print("==================================================================================================")
    print(row[0])
    print(row[1])

db.commit()
print(mycursor.rowcount)