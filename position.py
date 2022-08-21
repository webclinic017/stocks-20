# import alpaca_trade_api as tradeapi
# from multiprocessing.connection import wait

# key="PKYIUJ4DN9AY6X2E4CDP"
# sec="7e6LuRgaK0zGFhWvOrir2wCYxJsa13pncqmfk4EX"
# url="https://paper-api.alpaca.markets"
# # https://app.alpaca.markets/internal/quotes?symbols=AAPL
# api = tradeapi.REST(key, sec, url, api_version='v2')

# sym = input("Symbol: ")

# def findCurrentPrice():
#     prev = str(api.get_position(sym))
#     start = prev.find("current_price")+17
#     prev = prev[start:]
#     end = prev.find("'")
#     prev = prev[:end]
#     return float(prev)
    
# print(findCurrentPrice())
