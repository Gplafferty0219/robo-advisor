# app/robo_advisor.py

#IMPORT STUFFS
import csv
import json
import os
from dotenv import load_dotenv
import requests
import datetime

load_dotenv()

def get_response(symbol):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(request_url)
    parsed_response = json.loads(response.text)
    return parsed_response

def transform_response(parsed_response):
    # parsed_response should be a dictionary representing the original JSON response
    # it should have keys: "Meta Data" and "Time Series Daily"
    tsd = parsed_response["Time Series (Daily)"]

    rows = []
    for date, daily_prices in tsd.items(): # see: https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/datatypes/dictionaries.md
        row = {
            "timestamp": date,
            "open": float(daily_prices["1. open"]),
            "high": float(daily_prices["2. high"]),
            "low": float(daily_prices["3. low"]),
            "close": float(daily_prices["4. close"]),
            "volume": int(daily_prices["5. volume"])
        }
        rows.append(row)

    return rows

#CONVERT TO $USD
def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

#READS THE API KEY OFF THE .ENV FILE
api_key = os.getenv("ALPHAVANTAGE_API_KEY", default= "oops")

if __name__ == "__main__":
    #WELCOME MESSAGE
    print("---------------------------------------------")
    print("           WELCOME TO STOCK GENIE!           ")
    print("---------------------------------------------")

    #LOOPS THE FUNCTION SO YOU CAN ENTER MANY STOCKS
    while True:
        #USER INPUT
        symbol = input("Please enter a ticker or type 'DONE' when you are finished: ")
        if symbol == "DONE":
            print("THANKS FOR USING STOCK GENIE! GOOD LUCK!")
            exit()

        #FIRST VALIDATION TO MAKE SURE USER ISN'T TOTALLY LOST
        while True:
            if str.isnumeric(symbol) or len(symbol) > 5:
                print("---------------------------------------------")
                print("Sorry, you might be a bit confused. Try entering a stock ticker that looks something like this: 'AAPL'")
                print("---------------------------------------------")
                symbol = input("Please enter a ticker or type 'DONE' when you are finished: ")
            else:
                break

        #SECOND VALIDATION IF TICKER IS WRONG
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
        response = requests.get(request_url)   
        if "Error Message" in response.text:
            print(f"We're sorry! The ticker '{symbol}' could not be found. Please try again.")
            exit()
        else:
            parsed_response = json.loads(response.text)

        #LATEST DAY
        last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

        tsd = parsed_response["Time Series (Daily)"]
        dates = list(tsd.keys())

        #LATEST CLOSE
        latest_day = dates[0]
        latest_close = tsd[latest_day]["4. close"]

        #PRICING MODEL
        high_prices = []
        low_prices = []
        for date in dates:
            high_price = tsd[date]["2. high"]
            high_prices.append(float(high_price))
            low_price = tsd[date]["3. low"]
            low_prices.append(float(low_price))
        #RECENT HIGH
        recent_high = max(high_prices)
        #RECENT LOW
        recent_low = min(low_prices)

        #IMPORT DATA TO PRICES FILE
        csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data" , "prices.csv")
        csv_headers = ("timestamp", "open", "high", "low", "close", "volume")
        with open(csv_file_path, "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            writer.writeheader()
            for date in dates:
                daily_prices = tsd[date]
                writer.writerow({
                    "timestamp": date,
                    "open": daily_prices["1. open"],
                    "high": daily_prices["2. high"],
                    "low": daily_prices["3. low"],
                    "close": daily_prices["4. close"],
                    "volume": daily_prices["5. volume"]
                })

        #REQUEST TIME
        today = datetime.datetime.today()

        #-----------------------------------------#
        #RECEIPT
        print("-------------------------")
        print(f"SELECTED SYMBOL: {symbol}")
        print("-------------------------")
        print("REQUESTING STOCK MARKET DATA...")
        print("REQUEST MADE AT: ", today.strftime("%m/%d/%Y %I:%M %p"))
        print("-------------------------")
        print(f"LATEST DAY: {last_refreshed}")
        print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
        print(f"RECENT HIGH: {to_usd(float(recent_high))}")
        print(f"RECENT LOW: {to_usd(float(recent_low))}")
        print("-------------------------")
    #RECOMMENDS YOU BUY WHEN STOCK IS LOW AND SELL WHEN HIGH
    #RECOMMENDS YOU TO HOLD IF THERE IS OVERLAP OR IF STOCK IS IN THE MIDDLE OF THIS RANGE
        if float(latest_close) >= (0.80*(float(recent_high))) and float(latest_close) <= (1.20*(float(recent_low))):
            print("RECOMMENDATION: HOLD")
            print("RECOMMENDATION: Your stock is not very volatile. Hold for nowand hope for some steady returns.")
        elif float(latest_close) <= (1.20*(float(recent_low))):
            print("RECOMMENDATION: BUY!") 
            print("RECOMMENDATION REASON: The stock is at a relatively low price. Buy now before it rises!")
        elif float(latest_close) >= (0.80*(float(recent_high))):
            print("RECOMMENDATION: SELL!") 
            print("RECOMMENDATION REASON: The stock is at a relatively high price. Consider cashing out on it now!")
        else:
            print("RECOMMENDATION: HOLD")
            print("RECOMMENDATION: Your stock is not moving too much. Hold for now and hope for a good performance soon.")
        print("-------------------------")
        print(f"WRITING DATA TO CSV {csv_file_path}...")
        print("-------------------------")
        print("HAPPY INVESTING!")
        print("-------------------------")
