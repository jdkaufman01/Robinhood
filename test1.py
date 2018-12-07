# temp varss

username = "jdkafuman01"
password = "WbEgQc2zkP11EgP7vHsQibrTMDgHKVGU"
mfa_code = "349947"

stock_ticker = 'HMY'
shares_to_purchase = 1
stop_loss_order_percent = .0025
percent_to_replace_stop = .036


# Log IN

from Robinhood import Robinhood
my_trader = Robinhood()

mfa_req = my_trader.login(username=username, password=password)
logged_in = my_trader.login(username=username, password=password, mfa_code=mfa_code)


stock_instrument = my_trader.instrument(stock_ticker)
current_quote_info = my_trader.get_quote(stock_ticker)


# check to see if you have funds to cover
my_account = my_trader.get_account()
cost = float(current_quote_info['bid_price']) * int(shares_to_purchase)


# buy stock!
buy_order = my_trader.place_buy_order(stock_instrument, shares_to_purchase)


# Ensure stock exits in account 
# not currently accounting for existing shares owned...
my_securities = my_trader.securities_owned() 

for sec_owned in my_securities['results']:
  if(sec_owned['instrument'] == stock_instrument[0]['url']):
    sec_to_sell = sec_owned
    stock_in_portfolio = True

if stock_in_portfolio == True:
    print("stock found in portfolio, setting stop limit order")

else: 
    print("stock wasn't found!")

stop_loss_price = cost * (1 - stop_loss_order_percent)