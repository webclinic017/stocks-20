import alpaca_trade_api as tradeapi

key="PKZH3SZZ15ZSMNNMDKZO"
sec="3U3G7oy0GVFN7CNczj0NQqwBq1OCgT7H2opJBRcQ"
url="https://paper-api.alpaca.markets"
# https://app.alpaca.markets/internal/quotes?symbols=AAPL
api = tradeapi.REST(key, sec, url, api_version='v2')


amount = str(api.get_account())
amount = amount[amount.find("regt_buying_power'") + len("regt_buying_power'")+3:]
amount = amount[:amount.find("'")]
amount = float(amount)
print(amount)