from market_profile import MarketProfile
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, date, time, timedelta
import matplotlib.pyplot as plt 
import mplfinance as mpf

symbol = 'AMD'
sd = datetime(2021, 2, 22)
ed = datetime(2021, 2, 26)
dfR = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")


# symbol = 'EURUSD=X'
# dfR = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")



# df1 = yf.download(tickers=symbol, start=sd, end=ed, interval="30m")

###################################      CALCULATE TPO          ##################################

def calc_TPO (df1, tick_size = round(2.0*(df1['Open'][0]/100))/10) : 
    "You can change the mode to volume by replacing mode='tpo' with 'vol'. Keep tick size for Nifty as 1 and for Emini 0.25" 
    # mp = MarketProfile(df1, tick_size=5, mode='tpo')
    # mp = MarketProfile(df1, tick_size=.25, open_range_size=pd.to_timedelta('10 minutes'),initial_balance_delta=pd.to_timedelta('60 minutes'), mode='tpo')
    # mp = MarketProfile(df1, tick_size=5, open_range_size=pd.to_timedelta('10 minutes'), initial_balance_delta=pd.to_timedelta('60 minutes'), mode='vol')
    tick_size = round(2.0*(df1['Open'][0]/100))/10
    print ('Tick size :', tick_size)

    mp = MarketProfile(df1, tick_size=tick_size, open_range_size=pd.to_timedelta('10 minutes'), initial_balance_delta=pd.to_timedelta('60 minutes'), mode='vol')

    "If you have more than 1 days of intra data then use following line. Note for the US market replace 6.20 by 6.50" 
    #mp_slice = mp[df1.index.max() - pd.Timedelta(6.20, 'h'):df1.index.max()]

    "If you have only current days data then use following line"
    mp_slice = mp[0:len(df1.index)]
    val=mp_slice.value_area[0]
    vah=mp_slice.value_area[1]
    poc=mp_slice.poc_price
    data = mp_slice.profile
    return (data, val, vah, poc)

###################################     PLOT THE PROFILE          ##################################

"Plot profile"
data7, val, vah, poc = calc_TPO(dfR)
data7.plot(kind='barh', width=1.0, zorder=2)
# data.plot(kind='bar', width=1.0, zorder=2)


"Plot candles with mplfinance with Volume profice"

mpf.plot(dfR, style='yahoo', type='candle', hlines=dict( hlines=[vah, val, poc], colors=['g','r','b'], linestyle='dashed', linewidths=0.5) )


# plt.figure(figsize=(10,4), dpi=120) # 10 is width, 4 is height
# ax1=plt.subplot(1,2,1)


###############################     PLOT OVERLAY  (matplotlib v0)         #############################

import numpy as np
import matplotlib.pyplot as plt
from market_profile import MarketProfile
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, date, time, timedelta
import matplotlib.pyplot as plt 
import mplfinance as mpf

symbol = 'AMD'
sd = datetime(2021, 1, 1)
ed = datetime(2021, 1, 31)
df1 = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")

data1, val1, vah1, poc1 =  calc_TPO( df1 ) #, tick_size=0.2)

symbol = 'AMD'
sd = datetime(2021, 2, 1)
ed = datetime(2021, 2, 28)
df2 = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")

data2, val2, vah2, poc2 =  calc_TPO( df2 ) #,  tick_size=0.2)


fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'hspace': 0})
ax1.bar(data1.index, data1.values, width = 1.2,  zorder=2)

ax2.bar(data2.index, data2.values,width = 1.2,  zorder=2)

fig.set_tight_layout(True)
_ = plt.xticks(data2.index, data2.index, rotation=90)

###################################     PLOT OVERLAY  SNS v0        ##################################

data1
data2

import seaborn as sns
import matplotlib.pyplot as plt


############            Initialize Figure and Axes object # Simple pandas series plot 
fig, ax = plt.subplots()
ax.violinplot(data1, vert=True)
ax.violinplot(data2, vert=True)
plt.show()


############            SNS plot from data frame 
sns.set_style('whitegrid')

data = data1.to_frame()
sns.violinplot( y = data.index,  data=data)

data = data2.to_frame()
sns.violinplot( y = data.index,  data=data)
plt.show()

# # Construct iris plot
# iris = sns.load_dataset("iris")
# data = data2.to_frame().reset_index()
# sns.swarmplot(y='Volume', data=data)
# plt.show()

data.plot(kind='barh', width=1.0, zorder=2)

mpf.plot(df1)
mpf.plot(df2)





###################################     PLOT OVERLAY  SNS v0        ##################################
"Read this: https://github.com/yan365/market_profile/blob/master/Market%20Profile.ipynb"


symbol = 'AMD'
sd = datetime(2020, 1, 1)
ed = datetime(2021, 2, 28)
df1 = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")

# symbol = 'AMD'
sd = datetime(2021, 1, 1)
ed = datetime(2021, 1, 31)
df2 = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")



ymin = df1.reset_index().append(df2.reset_index()).Close.min()
ymax = df1.reset_index().append(df2.reset_index()).Close.max()
# ymin = data1.reset_index().append(data2.reset_index()).Close.min()
# ymax = data1.reset_index().append(data2.reset_index()).Close.max()

ymin = ymin - 0.001*ymin
ymax = ymax + 0.001*ymax




fig = plt.figure()

# [left, bottom, width, height] of the new axes
ax0 = fig.add_axes (    [0, 0, 0.5, 1], 
                        xticklabels=[],
                        # yticklabels=[], # ignore for 1st entry, add to subsequent
                        ylim=(ymin, ymax),                       
                        )
ax0.set(xlabel='Day 0')
ax0.set(ylabel='Price')

# d = data1.to_frame().reset_index()
d = df1.reset_index()
sns.distplot( d.Volume,  x=d.Close,  vertical=True, ax=ax0, bins=50)
ax0.axhline(poc1, ls='--')


ax0 = fig.add_axes (    [0.5, 0, 0.5, 1], 
                        xticklabels=[], 
                        yticklabels=[],
                        ylim=(ymin, ymax)
                        )
ax0.set(xlabel='Day 1')
# d = data2.to_frame().reset_index()
d = df2.reset_index()
sns.distplot( d.Volume,  x=d.Close,  vertical=True, ax=ax0, bins=50)
ax0.axhline(poc2, ls='--')
plt.title(symbol)



data2, val2, vah2, poc2 =  calc_TPO( df2 ) #,  tick_size=0.2)
print (poc2)
data2.plot(kind='barh', width=1.0, zorder=2)


# --------------------

## Plot candles overlay 
ax2 = fig.add_axes(     [0, 0, 1, 1], 
                        ylim=(ymin, ymax), 
                        xticklabels=[],
                        yticklabels=[])
ax2.patch.set_alpha(0.1)
ax2.plot(df1['Close'], alpha=.5, lw=5, color='b')
ax2.plot(df2['Close'], alpha=.5, lw=5, color='b')
plt.show()



# sns.distplot(data2.to_frame(), vertical=True, ax=ax0 )
# sns.distplot(data2.to_frame().values)


data1.plot(kind='barh', width=1.0, zorder=2)
data2.plot(kind='barh', width=1.0, zorder=2)



###################   NEGATIVE VOLUME TEST  ##########################333

df5 = df1.copy()
#########       CONDITIONAL OPERATION on COLUMNS 
# df.loc[df['column name'] condition, 'new column name'] = 'value if condition is met'

df5['PriceUp'] = df5['Close'].gt(df5['Open'])
df5['VolumeR'] =  np.where(df5['PriceUp']==True, df5['Volume'], -1*df5['Volume'])


ymin = df1.reset_index().append(df2.reset_index()).Close.min()
ymax = df1.reset_index().append(df2.reset_index()).Close.max()
# ymin = data1.reset_index().append(data2.reset_index()).Close.min()
# ymax = data1.reset_index().append(data2.reset_index()).Close.max()

ymin = ymin - 0.001*ymin
ymax = ymax + 0.001*ymax

fig = plt.figure()

# [left, bottom, width, height] of the new axes
ax0 = fig.add_axes (    [0, 0, 0.5, 1], 
                        xticklabels=[],
                        # yticklabels=[], # ignore for 1st entry, add to subsequent
                        ylim=(ymin, ymax),                       
                        )
ax0.set(xlabel='Day 0')
ax0.set(ylabel='Price')

# d = data1.to_frame().reset_index()
d = df1.reset_index()
sns.distplot( d.Volume,  x=d.Close,  vertical=True, ax=ax0, bins=50)
ax0.axhline(poc1, ls='--')


ax0 = fig.add_axes (    [0.5, 0, 0.5, 1], 
                        xticklabels=[], 
                        yticklabels=[],
                        ylim=(ymin, ymax)
                        )
ax0.set(xlabel='Day 1')
# d = data2.to_frame().reset_index()
d = df5.reset_index()
sns.distplot( d.VolumeR,  x=d.Close,  vertical=True, ax=ax0, bins=50)
ax0.axhline(poc2, ls='--')
plt.title(symbol)

