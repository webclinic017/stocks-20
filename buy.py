import alpaca_trade_api as tradeapi
import math
import time
    
key="PKVMBWFUFDES5T26GG6I"
sec="clS0axnuKRHR9ttiqBP7xwPHDB6Vxc2FG4Ho0WAM"
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

quantity_left = quantity
half_quantity = math.floor(quantity/2)


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
print("Confirming Purchase . . .")

def findCurrentPrice():
    prev = str(api.get_position(sym))
    start = prev.find("current_price")+17
    prev = prev[start:]
    end = prev.find("'")
    prev = prev[:end]
    return float(prev)

def testBuyOrder():
    while True:
        time.sleep(0.3)
        try:
            findCurrentPrice()
            break
        except:
            None

testBuyOrder()
print("Purchase Complete")
ten = 0
seven = 0

while True:
    # if an error occurs, then that means that we longer have an open position so the limit order must have gone through
    try:
        time.sleep(2)
        current_position = findCurrentPrice() #finding new price
        current_percent = round(current_position/buy_price, 4)
        increased = False
        same = False
    
    # if current_percent is greater than 2%, cash out
    
    #stop loss
        
    
        # if there is an increase from the previous profit or from the highest profit, cancel the limit orders
        if (current_percent >= highest_percent):
            highest_percent = current_percent # updating percent increase
            increased = True
        
        if (current_percent > previous_percent):
            increased = True
        
        if(highest_percent >= 1.1):
            ten+=1
            
        if increased:
            print("Increased")
        else:
            print("Decreased")
            
        
        
        previous_percent = current_percent
    except:
        print("Trade Complete")
        break