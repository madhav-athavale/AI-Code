# Alpha Vantage financial data -  https://www.alphavantage.co
import requests
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=XXXX'
#url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=XXXX'
#url = 'https://www.alphavantage.co/query?function=CPI&interval=monthly&apikey=XXXX'
#url = 'https://www.alphavantage.co/query?function=INFLATION&apikey=XXXX'
#url = 'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=2year&apikey=XXXX'
#url = 'https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=weekly&time_period=2&series_type=open&apikey=XXXX'
#url = 'https://www.alphavantage.co/query?function=VWAP&symbol=IBM&interval=15min&apikey=XXXX'
#url = 'https://www.alphavantage.co/query?function=REAL_GDP&interval=annual&apikey=XXXX'
r = requests.get(url)
data = r.json()

print(data)