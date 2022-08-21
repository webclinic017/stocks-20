import alpaca_trade_api as tradeapi
import math

def findInt(a):
    a.replace(" ", "")
    x = a[:a.find("/")]
    y = a[a.find("/")+1:]
    z = math.floor(float(x)/float(y))
    return int(z)
    
key="PKL48NDPB2FMOAPMXK9R"
sec="ILehBwGAB7lzHgZTLFydWCs6o9ZdZ5lSIGzabUjI"
url="https://paper-api.alpaca.markets"
# https://app.alpaca.markets/internal/quotes?symbols=AAPL
api = tradeapi.REST(key, sec, url, api_version='v2')

sym = input("Symbol: ")
num = (input("Quanity: "))



api.submit_order(
    symbol=sym,
    qty=num,
    side='sell',
    type='market',
    time_in_force='gtc'
)