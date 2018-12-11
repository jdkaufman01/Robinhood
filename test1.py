# temp vars

import pause,smtplib,time 

username = "jdkafuman01"

password = ""

mfa_code = ""

stock_ticker = 'HMY'

shares_to_purchase = 1

stop_loss_order_percent = .0025

percent_to_replace_stop = .036

def calc_stop_loss_price(cost, stop_loss_order_percent):
    # Create intial stock loss option
    
    stop_loss_price = round((cost * (1 - stop_loss_order_percent)), 2)

    return stop_loss_price 

def calc_replace_price(cost,percent_to_replace_stop):

    replace_price = round((cost + (cost * percent_to_replace_stop)), 2)

    return replace_price

def get_current_quote_bid_price(stock_instrument,my_trader):

    current_quote_bid_price = float(my_trader.get_quote(stock_instrument['symbol'])['bid_price'])
    
    return current_quote_bid_price

def send_email(mail_recipient, subject, body):
	FROM = mail_user
	TO = mail_recipient if type(mail_recipient) is list else [mail_recipient]
	SUBJECT = subject
	TEXT = body

	# Prepare actual message
	message = """From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	
	server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
	server.ehlo()
	server.login("blindtigerlawrenceks@gmail.com", "")
	server.sendmail(FROM, TO, message)
	server.close()

def RH_buy(stock_instrument,shares_to_purchase,my_trader):

    current_quote_info = my_trader.get_quote(stock_ticker)

    # check to see if you have funds to cover
    my_account = my_trader.get_account() 
    
    cost = float(current_quote_info['bid_price']) * float(shares_to_purchase)
    
    # what is buying power??  using cash per my account 
    if cost <= my_account['cash']:
        # buy stock!
        buy_order = my_trader.place_buy_order(stock_instrument, shares_to_purchase)
    else:
        print("not enough cash!")

    return buy_order.json() 

def RH_stop_loss_order(stock_instrument,cost,my_trader):
    # Ensure stock exits in account 
    # not currently accounting for existing shares owned...
    my_securities = my_trader.securities_owned() 
    
    for sec_owned in my_securities['results']:
        if(sec_owned['instrument'] == stock_instrument['url']):
            sec_to_sell = sec_owned
            stock_in_portfolio = True
    
    # currently setting sell order on all of identified security 

    if stock_in_portfolio == True:
        # stock found in portfolio, setting stop limit order 
        # shares held for buys + quantity 
        # use quantity or shares_held_for_buys... 
          if sec_to_sell['quantity'] < sec_to_sell['shares_held_for_buys']:
              quantity = int(float(sec_to_sell['shares_held_for_buys']))
          else:
              quantity = int(float(sec_to_sell['quantity']))    
    else: 
        print("stock wasn't found!")
               
    # why the fuck doesn't this work!
    # stop_loss_order = my_trader.place_stop_loss_sell_order('https://api.robinhood.com/instruments/ec0d2e9b-258e-47ba-a91f-9abcfeebcbe9/',symbol='HMY',time_in_force="gtc",stop_price=1.60,quantity=1)
    
    # stop_loss order from the basic order function - not as elegant.. 
    stop_loss_order = my_trader.submit_order(instrument_URL=stock_instrument['url'],symbol=stock_instrument['symbol'],order_type="limit",time_in_force="gtc",trigger='stop',price=stop_loss_price,stop_price=stop_loss_price,quantity=quantity,side="sell").json()
    
    return stop_loss_order

def RH_cancel_order(stop_loss_order,my_trader):

    canceled_order = my_trader.cancel_order(stop_loss_order['id'])
    
    if canceled_order == None:
        send_email("jesse.kaufman@gmail.com","py_RH_stoplimit Failed!",("Cancelindg order {} for {} failed, something fucky happened!").format(stop_loss_order['id'],stock_ticker))

# function that filters vowels
def filter_order(order_history,order_id):
    
    if order_history['id'] == order_id:
        return True
    else:
        return False

# Log IN

from Robinhood import Robinhood
my_trader = Robinhood()
logged_in = None

# why doesn't this piece of shit take str variable?
logged_in = my_trader.login(username=username, password=password)
if logged_in == None: 
    mfa_code = input('Enter the mfa_code: ')
    logged_in = my_trader.login(username="jdkaufman01", password="", mfa_code=652052)
    # need to determine how long the auth is for... 

# hackityhack because a wild list appears
if type(my_trader.instrument(stock_ticker)) == list:
    stock_instrument = my_trader.instrument(stock_ticker)[0]
else:
    stock_instrument = my_trader.instrument(stock_ticker)

# need to expand Robinhood.py to retrieve market data and market hours

market = my_trader.session.get(stock_instrument['market']).json()
market_hours = my_trader.session.get(market['todays_hours']).json()

# only monitor when the market in question is opn 

if market_hours['is_open'] == True:
    buy_order = RH_buy(stock_instrument,shares_to_purchase,my_trader)
    stop_loss_price = calc_stop_loss_price(buy_order['price'],stop_loss_order_percent)
    stop_loss_order = RH_stop_loss_order(stock_instrument,stop_loss_price,my_trader)
    replace_price = calc_replace_price(buy_order['price'],percent_to_replace_stop)
else:
    next_open = my_trader.session.get(market_hours['next_open_hours']).json()
    market_tz = market['timezone']



# do while stop loss order has not been fufilled.
while [order for order in (my_trader.order_history()['results']) if order['id'] == stop_loss_order['id'] ][0]['state'] != 'filled':
# get a quote every 5 seconds, compare to replace_price, cancel current stop loss order, create new stop loss order, 
    while True:    
        if get_current_quote_bid_price(stock_instrument,my_trader) <= replace_price:
            time.sleep(5)
            print('sleeping...watching...waiting...')
            if get_current_quote_bid_price(stock_instrument,my_trader) > replace_price:
                break
                RH_cancel_order(stop_loss_order,my_trader)
                stop_loss_price = calc_stop_loss_price(get_current_quote_bid_price(stock_instrument,my_trader), stop_loss_order_percent)
                stop_loss_order = RH_stop_loss_order(stock_instrument,stop_loss_price_my_trader)
            # how to cycle back up to the top....


my_trader.logout()