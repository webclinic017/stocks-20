import alpaca_trade_api as tradeapi
import math
import time
    
key="PK8XHJFVLZ7ZP07Z4FVM"
sec="hyrhi1tYOAQBZEGyJivUPvCm8bCD5SPX6j8L94JL"
url="https://paper-api.alpaca.markets"
# https://app.alpaca.markets/internal/quotes?symbols=AAPL
api = tradeapi.REST(key, sec, url, api_version='v2')


# Gets Inputs
sym = (input("Symbol: "))

# amount
amount = str(api.get_account())
amount = amount[amount.find("regt_buying_power'") + len("regt_buying_power'")+3:]
amount = amount[:amount.find("'")]
amount = float(amount) - 2000.00
print("Amount: " + str(amount))

# Determining current market price from yahoo finance
import os
URL = "https://query1.finance.yahoo.com/v8/finance/chart/" + sym.capitalize()+ "?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"
buy_price = os.popen("curl \""+URL+"\"" ).read()
buy_price= buy_price[buy_price.find("regularMarketPrice") + len("regularMarketPrice")+2:]
buy_price=buy_price[:buy_price.find(",")]
buy_price=float(buy_price)
print("Market Buy Price: " + str(buy_price))

quantity = math.floor(amount/buy_price)
print("Quanity: " + str(quantity))


def buy():
    api.submit_order(
    symbol=sym,
    qty=quantity,
    side='buy',
    type='market',
    time_in_force='gtc',
    stop_loss={'stop_price': buy_price * 0.985,
               'limit_price':  buy_price * 0.985},
    )

# Buys the stock
buy()
print("Bought Stocks ...")

def sell():
    api.submit_order(
    symbol=sym,
    qty=quantity,
    side='sell',
    type='market',
    time_in_force='gtc'
    )
    
def limit_sell(a):
    api.submit_order(
    symbol=sym,
    qty=quantity,
    side='sell',
    type='limit',
    time_in_force='gtc',
    limit_price=a
)



#finds the current price
def findCurrentPrice():
    prev = str(api.get_position(sym))
    start = prev.find("current_price")+17
    prev = prev[start:]
    end = prev.find("'")
    prev = prev[:end]
    return float(prev)

highest_percent = 1.0000

#wait(100)

# Using 
#Checking if stock is found so that there is no error in the next while loop
while True:
    time.sleep(0.4)
    try:
        price = findCurrentPrice()
        break
    except:
        None
        
print("Tracking Prices ...")

previous_percent = 1.0000

while True:
    # if an error occurs, then that means that we longer have an open position so the limit order must have gone through
    try:
        time.sleep(0.4)
        current_position = findCurrentPrice() #finding new price
        current_percent = round(current_position/buy_price, 4)
    
    #stop loss
        if (current_percent<=.982 and current_percent < previous_percent):
            limit_sell(current_position)
    
        # if there is an increase from the previous profit or from the highest profit, cancel the limit orders
        if (current_percent >= highest_percent):
            api.cancel_all_orders()
            highest_percent = current_percent # updating percent increase
        
        if (current_percent > previous_percent):
            api.cancel_all_orders()
        
        if (highest_percent != current_percent):
            # Handles Near 0.9 to 1.5 percent cases 
             if (highest_percent >= 1.009 and highest_percent < 1.018 and current_percent < previous_percent and current_percent <= 1.002):
                limit_sell(current_position)   
            
            
             elif (highest_percent < 1.07 and highest_percent>1.018 and current_percent < previous_percent and highest_percent - current_percent >= 0.016):
                limit_sell(current_position)
            #print(percent)
            #print(current_percent)
            
             if (highest_percent >= 1.07 and highest_percent - current_percent >= 0.01 and current_percent < previous_percent):
                limit_sell(current_position)
            #print(current_percent)
        
        previous_percent = current_percent
    except:
        print("Trade Complete")
        break