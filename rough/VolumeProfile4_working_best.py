from market_profile import MarketProfile
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, date, time, timedelta
import matplotlib.pyplot as plt 
import mplfinance as mpf

symbol = 'AMD'
sd = datetime(2021, 2, 1)
ed = datetime(2021, 2, 28)

df2 = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")
# df2 = yf.download(tickers=symbol, start=sd, end=ed, interval="30m")

###################################      CALCULATE TPO          ##################################

"You can change the mode to volume by replacing mode='tpo' with 'vol'. Keep tick size for Nifty as 1 and for Emini 0.25" 
# mp = MarketProfile(df2, tick_size=5, mode='tpo')
# mp = MarketProfile(df2, tick_size=.25, open_range_size=pd.to_timedelta('10 minutes'),initial_balance_delta=pd.to_timedelta('60 minutes'), mode='tpo')
# mp = MarketProfile(df2, tick_size=5, open_range_size=pd.to_timedelta('10 minutes'), initial_balance_delta=pd.to_timedelta('60 minutes'), mode='vol')
tick_size = round(2.0*(df2['Open'][0]/100))/10
print ('Tick size :', tick_size)
mp = MarketProfile(df2, tick_size=tick_size, open_range_size=pd.to_timedelta('10 minutes'), initial_balance_delta=pd.to_timedelta('60 minutes'), mode='vol')

"If you have more than 1 days of intra data then use following line. Note for the US market replace 6.20 by 6.50" 
#mp_slice = mp[df2.index.max() - pd.Timedelta(6.20, 'h'):df2.index.max()]

"If you have only current days data then use following line"
mp_slice = mp[0:len(df2.index)]
val=mp_slice.value_area[0]
vah=mp_slice.value_area[1]
poc=mp_slice.poc_price
print( "POC: %f" % mp_slice.poc_price)
print( "Value area: %f, %f" % mp_slice.value_area)

###################################     PLOT CANDLES          ##################################

"Plot candles with mplfinance with Volume profice"

mpf.plot(df2, style='yahoo', type='candle', hlines=dict( hlines=[vah, val, poc], colors=['g','r','b'], linestyle='dashed', linewidths=0.5) )


###################################     PLOT THE PROFILE          ##################################

"Plot profile"
data = mp_slice.profile
data.plot(kind='barh', width=1.0, zorder=2), plt.show()

# data.plot(kind='bar', width=1.0, zorder=2)




# plt.figure(figsize=(10,4), dpi=120) # 10 is width, 4 is height
# ax1=plt.subplot(1,2,1)






###########################################################################################################
###################################    ANALYZE a VOLUME PROFILE           #################################
" Read Here: https://medium.com/swlh/how-to-analyze-volume-profiles-with-python-3166bb10ff24"


import pandas as pd
import numpy as np
from scipy import stats, signal
import plotly.express as px
import plotly.graph_objects as go

# Download data 
symbol = 'AMZN'
sd = datetime(2021, 2, 1)
ed = datetime(2021, 2, 26)

df3 = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")

############################     PLOT THE PROFILE (old method)         ##########################

tick_size = round(2.0*(df3['Open'][0]/100))/10
mp = MarketProfile(df3, tick_size=tick_size, open_range_size=pd.to_timedelta('10 minutes'), initial_balance_delta=pd.to_timedelta('60 minutes'), mode='vol')
mp_slice = mp[0:len(df3.index)]
val=mp_slice.value_area[0]
vah=mp_slice.value_area[1]
poc=mp_slice.poc_price
data = mp_slice.profile
data.plot(kind='bar'), plt.show()

"Plot profile"
data = mp_slice.profile
data.plot(kind='barh', width=1.0, zorder=2), plt.show()
data.plot(kind='bar', width=1.0, zorder=2), plt.show()

print( "POC: %f" % mp_slice.poc_price)
print( "Value area: %f, %f" % mp_slice.value_area)

###################################     START PROFILE ANALYSIS          ##################################

# df3 = d.copy()
# convert to float for stats.gaussian_kde
df3['Volume'] = df3['Volume'].astype(np.float64)
# pd.to_numeric(df3['volume'], downcast='float')

volume = df3['Volume']
close = df3['Close']

# plot pplain histogram 

px.histogram(df3, x='Volume', y='Close', nbins=150, orientation='h').show()

px.histogram(df3, x='Close', y='Volume', nbins=150, orientation='v').show()


"Kernel Density Estimator"
kde_factor = 0.05
num_samples = 500
kde = stats.gaussian_kde(close,weights=volume,bw_method=kde_factor)
xr = np.linspace(close.min(),close.max(),num_samples)
kdy = kde(xr)
ticks_per_sample = (xr.max() - xr.min()) / num_samples

def get_dist_plot(c, v, kx, ky):
    fig = go.Figure()
    fig.add_trace(go.Histogram(name='Vol Profile', x=c, y=v, nbinsx=150, 
                               histfunc='sum', histnorm='probability density',
                               marker_color='#B0C4DE'))
    fig.add_trace(go.Scatter(name='KDE', x=kx, y=ky, mode='lines', marker_color='#D2691E'))
    return fig

get_dist_plot(close, volume, xr, kdy).show()




# Finding Volume Nodes (PEAKS)

peaks,_ = signal.find_peaks(kdy)
pkx = xr[peaks]
pky = kdy[peaks]

pk_marker_args=dict(size=10)
fig = get_dist_plot(close, volume, xr, kdy)
fig.add_trace(go.Scatter(name="Peaks", x=pkx, y=pky, mode='markers', marker=pk_marker_args))

# Find prominent peaks 

min_prom = min_prom = kdy.max() * 0.3
peaks, peak_props = signal.find_peaks(kdy, prominence=min_prom)
pkx = xr[peaks]
pky = kdy[peaks]

fig = get_dist_plot(close, volume, xr, kdy)
fig.add_trace(go.Scatter(name='Peaks', x=pkx, y=pky, mode='markers', marker=pk_marker_args))

# Draw prominence lines
left_base = peak_props['left_bases']
right_base = peak_props['right_bases']
line_x = pkx
line_y0 = pky
line_y1 = pky - peak_props['prominences']

for x, y0, y1 in zip(line_x, line_y0, line_y1):
    fig.add_shape(type='line',
        xref='x', yref='y',
        x0=x, y0=y0, x1=x, y1=y1,
        line=dict(
            color='red',
            width=2,
        )
    )
fig.show()
print ("Prominent", line_x )



# PEAK WIDTH 

width_range=1
peaks, peak_props = signal.find_peaks(kdy, prominence=min_prom, width=width_range)

left_ips = peak_props['left_ips']
right_ips = peak_props['right_ips']
width_x0 = xr.min() + (left_ips * ticks_per_sample)
width_x1 = xr.min() + (right_ips * ticks_per_sample)
width_y = peak_props['width_heights']

fig = get_dist_plot(close, volume, xr, kdy)
fig.add_trace(go.Scatter(name='Peaks', x=pkx, y=pky, mode='markers', marker=pk_marker_args))

for x0, x1, y in zip(width_x0, width_x1, width_y):
    fig.add_shape(type='line',
        xref='x', yref='y',
        x0=x0, y0=y, x1=x1, y1=y,
        line=dict(
            color='red',
            width=2,
        )
    )
fig.show()
print ("Width Range", width_x0, width_x1 )

# Validate with 
data.plot(kind='bar', width=1.0, zorder=2)


############## CORE FUNCTION DONE ############



################################ OTHER OPTIONS TO PLAY  ##########################################

## 
pipsize = 0.0001
max_width_pips = 20
min_prom = kdy.max() * 0.3
width_range=(1, max_width_pips * pipsize / ticks_per_sample)
peaks, peak_props = signal.find_peaks(kdy, width=width_range, prominence=min_prom)
pkx = xr[peaks]
pky = kdy[peaks]

pk_marker_args=dict(size=10)
fig = get_dist_plot(close, volume, xr, kdy)
fig.add_trace(go.Scatter(name="Peaks", x=pkx, y=pky, mode='markers', marker=pk_marker_args))


## Density 
min_prom = kdy.max() * 0.3
peaks, peak_props = signal.find_peaks(kdy, prominence=min_prom)

left_base = peak_props['left_bases']
right_base = peak_props['right_bases']
int_from = xr.min() + (left_base * ticks_per_sample)
int_to = xr.min() + (right_base * ticks_per_sample)

[kde.integrate_box_1d(x0, x1) for x0, x1 in zip(int_from, int_to)]

pk_marker_args=dict(size=10)
fig = get_dist_plot(close, volume, xr, kdy)
fig.add_trace(go.Scatter(name="Peaks", x=pkx, y=pky, mode='markers', marker=pk_marker_args))
