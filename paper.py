import alpaca_trade_api as tradeapi


key="PKL3OZOAZ1N02WL2J7YV"
sec="QfMJ00VZnoEXOPJEIuMajprSHM12BBU01eoU2HEV"
url="https://paper-api.alpaca.markets"
# https://app.alpaca.markets/internal/quotes?symbols=AAPL
api = tradeapi.REST(key, sec, url, api_version='v2')

#sym = 'QRTEB'
num = 3500

# api.submit_order(
#     symbol=sym,
#     qty=num,
#     side='buy',
#     type='market',
#     time_in_force='gtc'
# )

# # Alternatively, you could use trail_percent:
# api.submit_order(
#     symbol=sym,
#     qty=num,
#     side='sell',
#     type='trailing_stop',
#     trail_percent=1,  # stop price will be hwm*0.99  price is hwm * (1 - percentage)
#     time_in_force='gtc',
# )


# Submit a trailing stop order to sell 1 share of Apple at a
# # trailing stop of
# api.submit_order(
#     symbol=sym,
#     qty=4500,
#     side='sell',
#     type='trailing_stop',
#     trail_price=1.00,  # stop price will be hwm - 1.00$
#     time_in_force='gtc',
# )