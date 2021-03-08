from market_profile import MarketProfile
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, date, time, timedelta
import matplotlib.pyplot as plt 

# amzn = data.get_data_yahoo('AMZN', '2019-12-01', '2019-12-31')

symbol = 'AMZN'
sd = datetime(2021, 2, 1)
ed = datetime(2021, 2, 5)
df = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="30m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="5m", prepost=True)


fin_prod_data = df[['Open', 'High', 'Low', 'Close', 'Volume']]
mp = MarketProfile(fin_prod_data)
mp_slice2 = mp[fin_prod_data.index.min():fin_prod_data.index.max()]
mp_slice2.profile.plot(kind='bar')


# output 
mp_slice2.profile

mp_slice2.profile.plot(kind='bar', width=1.0)

mp_slice2.initial_balance()
# (1762.680054, 1805.550049)

mp_slice2.open_range()
# (1762.680054, 1805.550049)

mp_slice2.poc_price
# 1869.850000

mp_slice2.profile_range
# (1739.25, 1869.85)

mp_slice2.value_area
# (1760.95, 1869.85)

mp_slice2.balanced_target
# 2000.449999999999

mp_slice2.low_value_nodes

mp_slice2.high_value_nodes
mp_slice2.high_value_nodes.plot (kind='bar', width=1.0)




# ###############################  TPO   ################################333
# Rules: 
# if Stock price <100 use : interval = 60m/5m , tick_size=0.2 - 0.25
# if Stock price <2000-3000 use : interval = 60m/5m , tick_size=4
# if Stock price >3000 use : interval = 60m/5m , tick_size=5
# General Formula:  tick_size = 0.2 * abs(price/100)

symbol = 'AMD'
sd = datetime(2021, 2, 1)
ed = datetime(2021, 2, 28)

df2 = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")
# df2 = yf.download(tickers=symbol, start=sd, end=ed, interval="30m")
# df2 = yf.download(tickers=symbol, start=sd, end=ed, interval="15m")
# df2 = yf.download(tickers=symbol, start=sd, end=ed, interval="5m")
# df2 = yf.download(tickers=symbol, start=sd, end=ed, interval="5m", prepost=True)
# df2 = yf.download(tickers=symbol, start=sd, end=ed, interval="15m", prepost=True)

"You can change the mode to volume by replacing mode='tpo' with 'vol'. Keep tick size for Nifty as 1 and for Emini 0.25" 
# mp = MarketProfile(df2, tick_size=5, mode='tpo')
# mp = MarketProfile(df2, tick_size=.25, open_range_size=pd.to_timedelta('10 minutes'),initial_balance_delta=pd.to_timedelta('60 minutes'), mode='tpo')
# mp = MarketProfile(df2, tick_size=5, open_range_size=pd.to_timedelta('10 minutes'), initial_balance_delta=pd.to_timedelta('60 minutes'), mode='vol')
# df2['Open'][0]
tick_size = round(2.0*(df2['Open'][0]/100))/10
print ('Tick size :', tick_size)
mp = MarketProfile(df2, tick_size=tick_size, open_range_size=pd.to_timedelta('10 minutes'), initial_balance_delta=pd.to_timedelta('60 minutes'), mode='vol')

"If you have more than 1 days of intra data then use following line. Note for the US market replace 6.20 by 6.50" 
#mp_slice = mp[df2.index.max() - pd.Timedelta(6.20, 'h'):df2.index.max()]
"If you have only current days data then use following line"
mp_slice = mp[0:len(df2.index)]

"Print Value Areas"
print( "Initial balance: %f, %f" % mp_slice.initial_balance())
print( "Opening range: %f, %f" % mp_slice.open_range())
print( "POC: %f" % mp_slice.poc_price)
print( "Profile range: %f, %f" % mp_slice.profile_range)
print( "Value area: %f, %f" % mp_slice.value_area)
print( "Balanced Target: %f" % mp_slice.balanced_target)
val=mp_slice.value_area[0]
vah=mp_slice.value_area[1]
poc=mp_slice.poc_price


"Plot profile"
data = mp_slice.profile
data.plot(kind='barh')

"Plot candles with mplfinance with Volume profice
mpf.plot(df2, style='yahoo', type='candle', hlines=dict( hlines=[vah, val, poc], colors=['g','r','b'], linestyle='dashed', linewidths=0.5) )


"PLot value area as horizontal lines on price chart and save the plot as image in local disk"
plt.figure()
plt.plot(df2.Close)
plt.axhline(y=vah,linewidth=2, color='green')
plt.axhline(y=val,linewidth=2, color='red')
plt.axhline(y=poc,linewidth=2, color='yellow')

fig = plt.gcf()
fig.set_size_inches(22, 10.5)
"Change the folder name"
# fig.savefig('d:/export/mymp.png', dpi=98, bbox_inches='tight', pad_inches=0.1)
# view rawnfmp.py hosted with ❤ by GitHub