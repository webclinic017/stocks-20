import threading
import time
import alpaca_trade_api as tradeapi
import math
import os

# Setting up api tools for alpaca and yahoo
key="PKNIR8SDM20I7JU29Z1C"
sec="lZEV20YQ7fPjT8yEhqHpJYqU400Sbi1LwFGxMOh0"
url="https://paper-api.alpaca.markets"
# https://app.alpaca.markets/internal/quotes?symbols=AAPL
api = tradeapi.REST(key, sec, url, api_version='v2')

# api.submit_order(
#     symbol="AAPL",
#     qty=1,
#     side='buy',
#     type='market',
#     time_in_force='gtc',
# )

cost = str(api.get_position("AAPL"))
cost = (cost[cost.find("avg_entry")+len("avg_entry_price': '"):])
cost = cost[:cost.find("'")]
cost = float(cost)
print(cost)
