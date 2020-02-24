# app/robo_advisor.py
import csv
import json
import os

import requests



# Convert float or integer to usd formatting string
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#
# Info Inputs
#
request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

response = requests.get(request_url)

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())

latest_day = dates[0]

latest_close = tsd[latest_day]["4. close"]

#get high price from each day
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

#max of all prices
recent_high = max(high_prices)
recent_low = min(low_prices)

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data" , "prices.csv")

with open(csv_file_path,something something):
    blah
    blah
    blah
    blah


print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


