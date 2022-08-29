import threading
import time
import alpaca_trade_api as tradeapi
import math
import os

# Setting up api tools for alpaca and yahoo
key="PKXS3EU0TE5A13MPATQQ"
sec="Latm4zZCQUXnxdEzRJiW0ZW8n25HEnaAqVvTfX9L"
url="https://paper-api.alpaca.markets"
# https://app.alpaca.markets/internal/quotes?symbols=AAPL
api = tradeapi.REST(key, sec, url, api_version='v2')

sym="AAPL"
URL = "https://query1.finance.yahoo.com/v8/finance/chart/" + sym + "?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"

numTrades = 0
haveShares = False
buy_price = None
quantity = None
ref = None
amount = None
sellOrder= False

#print(URL)

#print("Amount: " + str(amount))
def findEquity():
    global amount
    amount = str(api.get_account())
    #(amount)
    amount = amount[amount.find("cash'") + len("cash'")+2:]
    amount = (amount[1:])
    num = amount.find("'")
    amount = amount[:num]
    amount = float(amount) - 3000.00
    

def findMarketPrice():
    buy_price = os.popen("curl \""+URL+"\"" ).read()
    buy_price= buy_price[buy_price.find("regularMarketPrice") + len("regularMarketPrice")+2:]
    buy_price=buy_price[:buy_price.find(",")]
    buy_price=float(buy_price)
    return buy_price

def limit_buy(a,q):
    api.submit_order(
    symbol=sym,
    qty=q,
    side='sell',
    type='limit',
    time_in_force='gtc',
    limit_price=a
)

def buy(q):
    api.submit_order(
    symbol=sym,
    qty=q,
    side='buy',
    type='market',
    time_in_force='gtc',
)

def sell(q):
    api.submit_order(
    symbol=sym,
    qty=q,
    side='sell',
    type='market',
    time_in_force='gtc',
)

def limit_sell(a,q):
    api.submit_order(
    symbol=sym,
    qty=q,
    side='sell',
    type='limit',
    time_in_force='gtc',
    limit_price=a
)

def findCurrentPosition():
    prev = str(api.get_position(sym))
    start = prev.find("current_price")+17
    prev = prev[start:]
    end = prev.find("'")
    prev = prev[:end]
    haveShares = True
    return float(prev)
    
def findBuyPrice():
    cost = str(api.get_position("AAPL"))
    cost = (cost[cost.find("avg_entry")+len("avg_entry_price': '"):])
    cost = cost[:cost.find("'")]
    cost = float(cost)
    return cost
    
current_position = None

def checkShares():
    global haveShares, buy_price, sellOrder
    while True:
        if (not haveShares):
            while True:
                time.sleep(0.3)
                try:
                    buy_price = findBuyPrice()
                    haveShares = True
                    break
                except:
                    None 
        elif (haveShares):
            None
            
            

current_market_price = findMarketPrice()
buy_price = current_market_price


def updatePrices():
    global current_market_price
    while True:
        current_market_price = findMarketPrice()

def cancelOrders():
    global current_market_price, haveShares
    while True:
        if (not haveShares):
            if (current_market_price < buy_price):
                api.cancel_all_orders()
                sentOrder = False
        else:
            break

updatePricesThread = threading.Thread(target=updatePrices) # updating the prices already
checkSharesThread = threading.Thread(target=checkShares) # constantly checking if shares have been processed in order to cancel
#cancelOrdersThread = threading.Thread(target=cancelOrders)
updatePricesThread.start()
checkSharesThread.start()
    
def randomTrade():
    global quantity, haveShares, buy_price, ref, current_market_price, sellOrder
    findEquity()
    # Setting variables that will be used and finding the equity
    
    # already checking if i have shares
    
    quantity = math.floor(amount/current_market_price) #quantity is bank over the price of each share
    # Finding amount and quantity
    
    buy(quantity)
    while (True):
        if haveShares:
            break
    
    ref = round(current_market_price,2) # we don't need alpaca api market price because we can just limit sell
    if (ref > buy_price):
        limit_sell(ref,quantity)
        sellOrder = True
    else:
        time.sleep(0.21)
        ref = round(current_market_price,2)
        if (ref > buy_price):
            limit_sell(ref,quantity)
            sellOrder = True
        else:
            time.sleep(0.1)
            ref = round(current_market_price,2)
            if (ref > buy_price):
                limit_sell(ref,quantity)
                sellOrder = True
            else:
                sell(quantity)     
    
    
    x = 0
    
    while True:
        try:
            time.sleep(0.1)
            findCurrentPosition()
            x+=1
            if (x==5):
                api.cancel_all_orders()
                time.sleep(0.15)
                try:
                    findCurrentPosition()
                except:
                    sell(quantity)
        except:
            haveShares = False
            break
        
def run():
    global haveShares
    while True:
        if (not haveShares):
            randomTrade()
        # Updating Number of trades
    
run()        