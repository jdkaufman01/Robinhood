from Robinhood import Robinhood
my_trader = Robinhood()
mfa_req = my_trader.login(username="jdkaufman01", password="")
logged_in = my_trader.login(username="jdkaufman01", password="",mfa_code="")
stock_instrument = my_trader.instruments("VSLR")[0]
quote_info = my_trader.quote_data("GBTC")

#buy_order = my_trader.place_buy_order(stock_instrument, 1)
#sell_order = my_trader.place_sell_order(stock_instrument, 1)

my_trader.logout() 

my_portfolio = my_trader.portfolios()

my_account = my_trader.get_account()

If (my_trader.instruments("VSLR")) > 1 ):
    print("yes")
import json


my_investment_profile = my_trader.investment_profile()



payload = {}

for field, value in [
        ('account', 'https://api.robinhood.com/accounts/5SK72672/'),
        ('instrument', 'https://api.robinhood.com/instruments/ec0d2e9b-258e-47ba-a91f-9abcfeebcbe9/'),
        ('symbol', 'HMY'),
        ('type', 'limit'),
        ('time_in_force', 'gtc'),
        ('trigger', 'stop'),
        ('price', 1.60),
        ('stop_price', 1.60),
        ('quantity', 1),
        ('side', 'sell')
    ]:
    if(value is not None):
        payload[field] = value

print(payload)

res = self.session.post(endpoints.orders(), data=payload, timeout=1)
res.raise_for_status()