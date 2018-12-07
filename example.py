from Robinhood import Robinhood
my_trader = Robinhood()
mfa_req = my_trader.login(username="jdkaufman01", password="WbEgQc2zkP11EgP7vHsQibrTMDgHKVGU")
logged_in = my_trader.login(username="jdkaufman01", password="WbEgQc2zkP11EgP7vHsQibrTMDgHKVGU",mfa_code="349947")
stock_instrument = my_trader.instruments("VSLR")[0]
quote_info = my_trader.quote_data("GBTC")

#buy_order = my_trader.place_buy_order(stock_instrument, 1)
#sell_order = my_trader.place_sell_order(stock_instrument, 1)

my_trader.logout() 

my_trader.portfolios()

If (my_trader.instruments("VSLR")) > 1 ):
    print("yes")
import json

