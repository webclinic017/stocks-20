import alpaca_trade_api as tradeapi
import json
import math
    
key="PKL48NDPB2FMOAPMXK9R"
sec="ILehBwGAB7lzHgZTLFydWCs6o9ZdZ5lSIGzabUjI"
url="https://paper-api.alpaca.markets"
# https://app.alpaca.markets/internal/quotes?symbols=AAPL
api = tradeapi.REST(key, sec, url, api_version='v2')


sym = input("Symbol: ")
num = (input("Quanity: "))


        
        





# api.submit_order(
#     symbol=sym,
#     qty=num,
#     side='sell',
#     type='trailing_stop',
#     trail_percent=1.5,  # stop price will be hwm*0.99  price is hwm * (1 - percentage)
#     time_in_force='gtc',
# )
