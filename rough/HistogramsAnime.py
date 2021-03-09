from datetime import date, datetime, time, timedelta

import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf
from market_profile import MarketProfile

###################################     PLOT OVERLAY  SNS v0        ##################################
"Read this: https://github.com/yan365/market_profile/blob/master/Market%20Profile.ipynb"


symbol = 'AAPL'
sd = datetime(2020, 1, 1)
ed = datetime(2021, 2, 28)
df1 = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")

# symbol = 'AMD'
sd = datetime(2021, 1, 1)
ed = datetime(2021, 1, 31)
df2 = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")


def calc_TPO (df1, tick_size = round(2.0*(df1['Open'][0]/100))/10) : 
    "You can change the mode to volume by replacing mode='tpo' with 'vol'. Keep tick size for Nifty as 1 and for Emini 0.25" 
    tick_size = round(2.0*(df1['Open'][0]/100))/10
    print ('Tick size :', tick_size)

    mp = MarketProfile(df1, tick_size=tick_size, open_range_size=pd.to_timedelta('10 minutes'), initial_balance_delta=pd.to_timedelta('60 minutes'), mode='vol')

    "If you have only current days data then use following line"
    mp_slice = mp[0:len(df1.index)]
    val=mp_slice.value_area[0]
    vah=mp_slice.value_area[1]
    poc=mp_slice.poc_price
    data = mp_slice.profile
    return (data, val, vah, poc)

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

data1, val1, vah1, poc1 =  calc_TPO( df1 ) #, tick_size=0.2)
data2, val2, vah2, poc2 =  calc_TPO( df2 ) #,  tick_size=0.2)


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





###############################    SNS PLOTTING FIGURES TEST FUNCTIONS      ###################################

# d = df5.reset_index()
 d=df5.copy()

# WRONG - SINGLE VARIATE distribution of PRICE Close : 
ax = sns.displot( d.Volume,  x=d.Close, bins=50) # Wrong - need 2nd variable - BIVARIATE Distribution

# CORRECT method for hist (x = Close, y=sum of Volume)
ax = sns.displot( d.Volume,  x=d.Close, weights=d.Volume, bins=50) # CORRECT- need 2nd variable 
ax = sns.displot( d.Volume,  x=d.Close, weights=d.VolumeR, bins=50, hue=d.PriceUp) # CORRECT- need 2nd variable 

ax = sns.kdeplot(data=d, x="Close") # CORRECT- need 2nd variable 
# PLOTTING the MAX Value 
x = ax.lines[0].get_xdata() # Get the x data of the distribution
y = ax.lines[0].get_ydata() # Get the y data of the distribution
maxid = np.argmax(y) # The id of the peak (maximum of y data)
plt.plot(x[maxid],y[maxid], 'bo', ms=10)


ax = sns.displot(d, x="Close", y="Volume")

# ax = sns.displot(d, x="Close", y="Volume", binwidth=(2, 5000), cbar=True) # time consuming 

# x = d.Close.max() # Get the x data of the distribution
# y = d.Volume.max # Get the y data of the distribution
# maxid = np.argmax(y) # The id of the peak (maximum of y data)
# plt.plot(x[maxid],y[maxid], 'bo', ms=10)


# All GOOD [CORRECT]
ax = sns.displot(d, x="Close", y="Volume", kind="kde", fill=True,  levels=[.01, .05, .1, .8], cbar=True)
ax = sns.displot(d, x="Close", y="Volume", kind="kde", fill=True,  levels=10, cbar=True)
ax = sns.displot(d, x="Close", y="Volume", kind="kde", fill=True, hue="PriceUp")


## All GOOD [CORRECT] - but not relevant 
ax = sns.jointplot(data=d, x="Close", y="Volume") # Color by Scale 

ax = sns.jointplot(
    data=d, 
    # y="Volume", 
    x="Close", 
    # hue="PriceUp",x
    weights=d.Volume.astype(np.float64),  
    kind="kde", 
    # kde_kws={'bw_method': 0.05}, # disable if y disabled 
    fill=True
)


#######  Histogram with PLOTLY [CORRECT] 
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats, signal
import plotly.express as px
import plotly.graph_objects as go


# px.histogram(df3, x='Volume', y='Close', nbins=150, orientation='h').show()
# px.histogram(df3, x='Close', y='VolumeR', nbins=150, orientation='v').show()
px.histogram(d, x='Close', y='Volume', nbins=150, orientation='v').show()


########## Plot displot with weights 

# Density Estimator on Volume vs Close [CORRECT] - 2D PLOTS
ax = sns.displot(d, x="Close", y="Volume" ) # 2D 
ax = sns.displot(d.Volume, x=d.Close, y=d.Volume) # 2D 
ax = sns.displot(d.Volume, x=d.Close, weights=d.Volume)  # 1D y=weighted volume

ax = sns.displot(d.Volume, x=d.Close, weights=d.Volume, bins = 50) 
ax = sns.displot(d.Volume, x=d.Close, weights=d.Volume, bins = 50, kind="hist") # same 


# Plot volume sum histogram overlapping 
ax = sns.displot(d.Volume, x=d.Close, weights=d.Volume, bins = 50) 

# with KDE and bins : Note the np.float64 to convert from int32/64 to float 
ax = sns.displot(d.Volume, x=d.Close, weights=d.Volume.astype(np.float64), bins=50, kde=True) 
ax = sns.displot(d.Volume, x=d.Close, weights=d.VolumeR, bins = 150)


########## Plot dist with weights ###################################
ax = sns.distplot(d.Volume, x=d.Close,hist_kws={'weights':d.Volume}, bins = 100) # can make kde=False 
ax = sns.distplot(d.VolumeR, x=d.Close,hist_kws={'weights':d.VolumeR}, bins = 100) # can make kde=False 
ax = sns.distplot(d.VolumeR, x=d.Close,hist_kws={'weights':d.VolumeR}, bins = 100) # can make kde=False 

########## Plot hist with weight #################################
ax = sns.histplot(data=d, x='Close', hue="PriceUp", weights=d.Volume, bins = 100)

ax = sns.histplot(data=d, x='Close', y='Volume', hue="PriceUp", weights=d.Volume, bins = 100) # 2D Scatter hist 
sns.histplot(data=d, x='Close',  weights=d.VolumeR, bins = 100) # hist 

# PLOTTING the MAX Value 
fig = plt.figure(figsize=(12,6))
ax = fig.add_axes ([0, 0.1, 0.65, 0.9])

sns.histplot(data=d, x='Close',  weights=d.VolumeR, bins = 100, ax=ax) # hist

# get hist data 
bars = [patch.get_height() for patch in ax.patches] # change to get_width and get
ticks = [patch.get_x() for patch in ax.patches]
for item in zip (ticks, bars) : print (item)
# [(x,y) if x>120 else 0 for x,y in zip (ticks,bars)] # test filter operations
sum([y if x>120 and x<130 else 0 for x,y in zip (ticks,bars)]) # sum of all hist bars bw[120,130]

# x = ax.lines[0].get_xdata() # Get the x data of the distribution
# y = ax.lines[0].get_ydata() # Get the y data of the distribution
# maxid = np.argmax(y) # The id of the peak (maximum of y data)
# plt.plot(x[maxid],y[maxid], 'bo', ms=10)


# Create an array with the colors you want to use
colors = ["#ff3061", "#00b061"]# Set your custom color palette
customPalette = sns.set_palette(sns.color_palette(colors))


ax = sns.histplot(data=d, x='Close', hue="PriceUp", weights=d.Volume, bins = 100, palette=customPalette,  alpha=1)
ax = sns.histplot(data=d, x='Close', hue="PriceUp", weights=d.Volume.astype(np.float64), bins = 100, stat="density", palette=customPalette,  alpha=1)
ax = sns.histplot(data=d, x='Close', hue="PriceUp", weights=d.Volume.astype(np.float64), bins = 100, stat="density", palette=customPalette,  alpha=1, kde=True)  # with kde distributions 

kde_factor = 0.05
# on x axis 
ax = sns.histplot(data=d, x='Close', weights=d.Volume.astype(np.float64), bins=100, stat="density", palette=customPalette,  alpha=0.2, kde=True, kde_kws={'bw_method': kde_factor}) # normalize Y # add :  hue="PriceUp" for split +/- 

# flip to y axis 
ax = sns.histplot(data=d, y='Close', weights=d.Volume.astype(np.float64), bins=100, stat="density", palette=customPalette,  alpha=0.2, kde=True, kde_kws={'bw_method': kde_factor}) # normalize Y # add :  hue="PriceUp" for split +/- 


# flip to right y axis 
fig,ax = plt.subplots()
ax21 = ax.twiny()
# ax21 = fig.add_subplot(111, sharey=ax, frameon=False)
ax21.yaxis.tick_right()
sns.histplot(data=d, y='Close', weights=d.Volume.astype(np.float64), bins=100, stat="density", palette=customPalette,  alpha=0.2, kde=True, kde_kws={'bw_method': kde_factor}, ax=ax21) # normalize Y # add :  hue="PriceUp" for split +/- 



######## Plot KDE with weight s
ax = sns.kdeplot(data=d, y='Close', hue="PriceUp", weights=d.Volume.astype(np.float64), palette=customPalette,  alpha=0.2, bw_method=kde_factor, fill=True) # normalize Y 


######### Draw price line and Annotate 
ax.axhline(poc2, ls='--')
ax.text(x=poc2, y=ax.get_ylim()[1]*0.95, s=poc2, alpha=0.7, color='b')


# ax.get_ylim()
# ax.lines[0].get_ydata().max()
# ax.lines[0].get_xdata().max()


"Kernel Density Estimator"
kde_factor = 0.20
num_samples = 500
kde = stats.gaussian_kde(d.Close,weights=d.Volume.astype(np.float64),bw_method=kde_factor)
xr = np.linspace(d.Close.min(),d.Close.max(),num_samples)
kdy = kde(xr)
ticks_per_sample = (xr.max() - xr.min()) / num_samples




# difference in Volume Up/Down 
ax = sns.displot(d.Volume, x=d.Close, weights=d.Volume.astype(np.float64), bins = 50, hue=d.PriceUp) # weight Volume 
ax = sns.displot(d.Volume, x=d.Close, weights=d.VolumeR.astype(np.float64), bins = 50, hue=d.PriceUp) # weight Volume and +/- values



sns.scatterplot(data=d, x='Close', y='Volume')
sns.histplot(data=d, x='Close', y='Volume', hue="PriceUp")
sns.kdeplot(data=d, x='Close', y='Volume')

# sns.catplot(data=d, x='Close', y='Volume', hue="PriceUp", kind="violin",)

sns.relplot(data=d, x='Close', y='Volume', hue="PriceUp")
sns.kdeplot(x=d.Close, y=d.Volume)

# sns histogram with distribution and y=sum of Volume 
ax = sns.displot(d, x="Close", weights="Volume", bins=100) # weight Volume = sum of Volume 
ax = sns.displot(d, x="Close", y="Volume", weights="Volume", bins=150) # 2D Scatter plots 
ax = sns.displot(d, x="Close", weights="Volume", bins=150, hue="PriceUp")




#############       WRONG       ###   WHATs WRONG WITH THESE 

sns.distplot( d.Volume,  x=d.Close, vertical=False, bins=150) # Volume no role 
sns.distplot( x=d.Close,  vertical=False, bins=150) # Volume no role 

sns.displot( d,  x=d.Close, bins=150) # Volume no role 
# sns.histplot(data=d, x='Close', y='Volume', bins=150)


# sns.distplot( d.Volume[1000:],  vertical=False, bins=150)
sns.displot(x=d.Close, bins=150)
sns.displot(d, x="Close", bins=150)
ax = sns.displot(d, x="Close", bins=150)



######  Density Estimator on Close [CORRECT] - BUT USELESS 
ax = sns.displot(d, x="Close", hue="PriceUp", kind="kde")
ax = sns.displot(d, x="Close", hue="PriceUp", kind="kde", stat="density") 
ax = sns.displot(d, x="Close", hue="PriceUp", kind="kde", multiple="stack")



################     UNI-variate ANALYSIS: Density by Closing Price only no Volume
d = df5.reset_index()
# d = d.Close.to_frame()
ax = sns.displot(d, x="Close")
ax = sns.displot(d, x="Close", hue="PriceUp")
ax = sns.displot(d, x="Close", hue="PriceUp", element="step")
# ax = sns.displot(d, x="Close", hue="PriceUp", multiple="stack")  # useless 
ax = sns.displot(d, x="Close", hue="PriceUp", stat="density")
ax = sns.displot(d, x="Close", hue="PriceUp", stat="density", common_norm=False)












########################    ANIMATION TEST      #############################
