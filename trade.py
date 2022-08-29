import threading
import time
import alpaca_trade_api as tradeapi
import math
import os

key="PK1NQTJ8ROXOKL6DUTPA"
sec="Gd72uLQOEmB8o0MEV4z7WoQ0m8JXj4wcsJaEs7HD"
url="https://paper-api.alpaca.markets"
# https://app.alpaca.markets/internal/quotes?symbols=AAPL
api = tradeapi.REST(key, sec, url, api_version='v2')
sym="ETH"
URL = "https://query1.finance.yahoo.com/v8/finance/chart/" + sym + "?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"
# amount
haveShares = False
sentOrder = False
sellOrder = False
ref = None
print(URL)
amount = None

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
    
current_position = None

def checkShares():
    global haveShares
    while True:
        #time.sleep(0.3)
        try:
            findCurrentPosition()
            haveShares = True
            print()
            print()
            print("              Bought SHARES                        ")
            print()
            print()
            break
        except:
            None

None

previous_market_price = findMarketPrice()
time.sleep(1)
current_market_price = findMarketPrice()
buy_price = current_market_price


def updatePrices():
    global haveShares,previous_market_price, current_market_price
    while True:
        time.sleep(0.2)
        previous_market_price = current_market_price
        current_market_price = findMarketPrice()
        print("Previous Price: " + str(previous_market_price))
        print("Current: " + str(current_market_price))

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
cancelOrdersThread = threading.Thread(target=cancelOrders)
updatePricesThread.start()
buy_price = None
quantity = None

def trade():
    global sentOrder, haveShares, buy_price, quantity, sellOrder
    checkSharesThread.start()
    findEquity()
    current_position = None
    quantity = None
    
    while True:
        if (not haveShares and not sentOrder):
            buy_price = round(current_market_price, 2)
            if (buy_price > previous_market_price):
                quantity = math.floor(amount/buy_price)
                # print(amount)
                # print(buy_price)
                buy(buy_price, quantity) # you buy if the prices are going up
                sentOrder = True
                #cancelOrdersThread.start()
        # elif (sentOrder and not haveShares):
        #     if (current_market_price < buy_price and not sellOrder):
        #         api.cancel_all_orders()
        #     sentOrder = False
        elif (haveShares):
            time.sleep(0.3) #api only allows 200 requests per minute
            current_position = findCurrentPosition()
            if (current_position > buy_price):
                sell(current_position, quantity)
                sellOrder = True
                break
            else:
                time.sleep(0.25)
                if (current_position > buy_price):
                    sell(current_position, quantity)
                    sellOrder = True
                    print()
                    print()
                    print("              SOLD SHARES                        ")
                    print()
                    print()
                    break
                elif (current_position < buy_price):
                    sell(current_position, quantity)
                    sellOrder = True
                    print()
                    print()
                    print("              SOLD SHARES                  ")
                    print()
                    print()
                    break
                           
            
    sellOrder = False
    sentOrder = False
    haveShares = False
    
def randomTrade():
    global quantity, haveShares, buy_price, ref
    findEquity()
    checkSharesThread.start()
    quantity = math.floor(amount/current_market_price)
    # Finding amount and quantity
    
    buy()
    while (True):
        if haveShares:
            break
    
    ref = current_market_price
    if (ref > buy_price):
        limit_sell(ref,quantity)
    else:
        time.sleep(0.22)
        ref = current_market_price
        if (ref > buy_price):
            limit_sell(ref,quantity)
        else:
            sell(quantity)
            
    while True:
        try:
            findCurrentPosition()
        except:
            break
        
    
def run():
    while True:
        randomTrade()
    
run()
        
                
        
    
