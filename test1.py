# temp varss

username = "jdkafuman01"
password = "WbEgQc2zkP11EgP7vHsQibrTMDgHKVGU"
mfa_code = "861209"

stock_ticker = 'HMY'
shares_to_purchase = 1
stop_loss_order_percent = .0025
percent_to_replace_stop = .036


# Log IN

from Robinhood import Robinhood
my_trader = Robinhood()

mfa_req = my_trader.login(username="jdkaufman01", password="WbEgQc2zkP11EgP7vHsQibrTMDgHKVGU")
logged_in = my_trader.login(username="jdkaufman01", password="WbEgQc2zkP11EgP7vHsQibrTMDgHKVGU", mfa_code=982172)


stock_instrument = my_trader.instrument(stock_ticker)

# need to expand Robinhood.py to retrieve market data and market hours

market = my_trader.session.get(stock_instrument[0]['market'].json())
market_hours = my_trader.session.get(market['todays_hours']).json()

if market_hours['is_open'] == True:
    print("market is open")

current_quote_info = my_trader.get_quote(stock_ticker)


# check to see if you have funds to cover
my_account = my_trader.get_account()
cost = float(current_quote_info['bid_price']) * float(shares_to_purchase)
# what is buying power?? 
if cost <= my_account['cash']:
  print("enough to cover")
else:
  print("not enough cash!")

# buy stock!
buy_order = my_trader.place_buy_order(stock_instrument[0], shares_to_purchase)


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

# Create intial stock loss option

stop_loss_price = cost * (1 - stop_loss_order_percent)

# USe shares_held_for_buys or quantity?? 

if sec_to_sell['quantity'] < sec_to_sell['shares_held_for_buys']:
    print(sec_to_sell['shares_held_for_buys'])
    quantity = int(float(sec_to_sell['shares_held_for_buys']))
else:
    quantity = int(float(sec_to_sell['quantity']))

stop_loss_order = my_trader.place_stop_loss_sell_order('https://api.robinhood.com/instruments/ec0d2e9b-258e-47ba-a91f-9abcfeebcbe9/',symbol='HMY',time_in_force="gtc",stop_price=1.60,quantity=1)

# email crap
order = my_trader.submit_order(instrument_URL='https://api.robinhood.com/instruments/ec0d2e9b-258e-47ba-a91f-9abcfeebcbe9/',symbol='HMY',order_type="limit",time_in_force="gtc",trigger='stop',price=1.60,stop_price=1.60,quantity=1,side="sell")


import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"

password = "BlindTiger2013"
sender_email = "blindtigerlawrenceks@gmail.com"  # Enter your address
receiver_email = "jesse.kaufman@gmail.com"  # Enter receiver address
message = """
Subject: Hi there 

This message is sent from Python."""


# Create a secure SSL context
sslcontext = ssl.create_default_context()

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(sender_email, password)
server.debuglevel(1)
server.sendmail(sender_email, receiver_email, message)
server.quit()

import smtplib

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("blindtigerlawrenceks@gmail.com", "BlindTiger2013")
server.sendmail(
  "blindtigerlawrenceks@gmail.com", 
  "jesse.kaufman@gmail.com", 
  "this message is from python")
server.quit()

