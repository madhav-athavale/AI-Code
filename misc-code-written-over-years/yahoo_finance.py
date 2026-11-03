# Sample code to get stock price using Alpha Vantage.

import yfinance as yf
import requests
import os
from dotenv import load_dotenv

load_dotenv()

AV_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

msft = yf.Ticker('MSFT')


msft_historical = msft.history(start="2023-01-03", end="2023-01-04", interval="1d")
print(msft_historical)

symbol = "WFC"

url = "https://www.alphavantage.co/query"
params = {
    "function": "GLOBAL_QUOTE",
    "symbol": symbol,
    "apikey": AV_API_KEY
}

response = requests.get(url, params=params)
data = response.json()

print(data["Global Quote"]["05. price"])

