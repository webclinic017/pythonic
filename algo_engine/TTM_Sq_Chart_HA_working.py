import datetime as dt
import os
import random as rnd
from datetime import date, datetime, time, timedelta

import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import yfinance as yf



symbol = 'AMD'
sd = datetime(2020, 1, 1)
ed = datetime(2021, 4, 12)
# interval = "1d"
interval = "60m"

# df = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")
# df = yf.download(tickers=symbol, start=sd, interval="60m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="1d")
# dfd = yf.download(tickers=symbol, start=sd, interval=interval,prepost=True)
dfd = yf.download(tickers=symbol, start=sd, interval=interval)
df = dfd


# Enable if 4H reampling is True 
# dfd = yf.download(tickers=symbol, start=sd, interval=interval,prepost=True)
# dfd = yf.download(tickers=symbol, start=sd, interval=interval)
# df = dfd
interval = "4h"
# Resampling Code 
## Resample to 4H timefeame 
aggregation = {'Open'  :'first',
               'High'  :'max',
               'Low'   :'min',
               'Close' :'last',
               'Volume':'sum'}
df = dfd.resample('4H').agg(aggregation).dropna()

# symbol = 'AAPL'
# sd = datetime(2020, 1, 1)
# ed = datetime(2021, 4, 7)
# dfdata = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")
# dfdata.to_pickle(symbol+'.pickle')
# dfdata.to_pickle(symbol+'.pickle')
# dfdata = pd.read_csv('h:/WorkSpace_Python/AppPy/rough/'+symbol+'.csv', index_col='Datetime', parse_dates=True)
# if os.name == 'nt': df = pd.read_pickle('h:/WorkSpace_Python/pythonic/rough/'+symbol+'.pickle')
# else: df = pd.read_pickle('/home/towshif/code/python/pythonic/rough/'+symbol+'.pickle')

# df = yf.download(tickers=symbol, start=sd, end=ed, interval="1d")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="60m", prepost=True)
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="30m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="15m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="5m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="5m", prepost=True)
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="15m", prepost=True)




############     SIMPLE CANDLE CHART w/ volume 
# style = 'yahoo','nightclouds','ibd'
# type =  'candle', 'hollow_and_filled'
# mpf.plot(mpfdf, style='yahoo', type='candle', volume=True, panel_ratios=(4,1))




################################################################################

############    ADD some INDICATORS 
# squeezes = df.ta.squeeze(lazybear=False, detailed=True, append=True)
squeezes = df.ta.squeeze(lazybear=True, detailed=True, append=True)

bollingers = df.ta.bbands(append=True) # 'BBL_5_2.0', 'BBM_5_2.0', 'BBU_5_2.0', 'BBB_5_2.0' 
macd = df.ta.macd(append=True) # 'MACD_12_26_9', 'MACDh_12_26_9','MACDs_12_26_9'],
rsi = df.ta.rsi(length=20, append=True)
rsi_SMA = df['RSI_20_SMA'] = ta.sma(rsi, length=20, append=True)

rsx = df.ta.rsx(length=20, append=True)
rsx_SMA = df['RSX_20_SMA'] = ta.sma(rsx, length=20, append=True)

ha = df.ta.ha(append=True)
df['HA_color'] = np.where(df.HA_close > df.HA_open, 1, -1)
# ema21HA = df['EMA_21HA'] = ta.ema( df.HA_close, length=21, append=True)
ema9 = df.ta.ema(length=9, append=True)
ema21 = df.ta.ema(length=21, append=True)
ema42 = df.ta.ema(length=42, append=True)
ema50 = df.ta.ema(length=50, append=True)
ema100 = df.ta.ema(length=100, append=True)
ema150 = df.ta.ema(length=150, append=True)
keltner = df.ta.kc(append=True)

# New Squeeze (black dots) : 1 = ON, 0 = OFF (for 'in_squeeze')
def in_squeeze(df):
    if df['BBL_5_2.0'] > df['KCLe_20_2'] and df['BBU_5_2.0'] < df['KCUe_20_2'] : 
        return 1 
def out_squeeze(df):
    if not (df['BBL_5_2.0'] > df['KCLe_20_2'] and df['BBU_5_2.0'] < df['KCUe_20_2']):         
        return 1    
df['squeeze_on'] = df.apply(in_squeeze, axis=1)
df['squeeze_off'] = df.apply(out_squeeze, axis=1)


mpfdf_columns = list(df.columns)

#################################  MAIN AlGO and SIGNAL GENERATION  #####################################

# define stack EMA Extreme:base=9 ::  +1: positive bullish, 0:undecided, -1:negative bearish
df['signal_StackEMA'] = np.where(
    (df.EMA_9 > df.EMA_21) & 
    (df.EMA_21 > df.EMA_50) & 
    (df.EMA_50 > df.EMA_100) &
    (df.EMA_100 > df.EMA_150)      
    ,1, np.where(
    (df.EMA_9 < df.EMA_21) & 
    (df.EMA_21 < df.EMA_50) & 
    (df.EMA_50 < df.EMA_100) &
    (df.EMA_100 < df.EMA_150), -1, 0))

# define stack EMA Softer:base=21 :: +1: positive bullish, 0:undecided, -1:negative bearish
df['signal_StackEMA21'] = np.where(
    # (df.EMA_9 > df.EMA_21) & 
    (df.EMA_21 > df.EMA_50) & 
    (df.EMA_50 > df.EMA_100) &
    (df.EMA_100 > df.EMA_150)      
    ,1, np.where(
    # (df.EMA_9 < df.EMA_21) & 
    (df.EMA_21 < df.EMA_50) & 
    (df.EMA_50 < df.EMA_100) &
    (df.EMA_100 < df.EMA_150), -1, 0))

## >>>>>>>>>>   generate long signal : 
# find 1st change Entry from day1: 0->1 and day2: reconfirmation 1->1 ; Exit 1->0

df.loc [ ((df['signal_StackEMA'] == 1) & (df['signal_StackEMA'].shift(2) == 0) & (df['signal_StackEMA'].shift(1) == 1)) , 'signal_Trade_StackEMA'] = 1 
df.loc [ ((df['signal_StackEMA'] == 0) & (df['signal_StackEMA'].shift(1) == 1) ) , 'signal_Trade_StackEMA'] = -1 
# df.loc [ ((df['signal_StackEMA'] == 0) & (df['signal_StackEMA'].shift(2) == 1) & (df['signal_StackEMA'].shift(1) == 0)) , 'signal'] = -1 
## See results: 
df[ (df.signal_Trade_StackEMA == 1) | (df.signal_Trade_StackEMA == -1)] [['signal_Trade_StackEMA', 'close']]

# df['signal'] =   ((df['signal_StackEMA'] == 1) & (df['signal_StackEMA'].shift(2) == 0) & (df['signal_StackEMA'].shift(1) == 1)) # return on DF bool 


###########################  BACK TEST  ###########################

## >>>>>>>>>>   Run a Back Test and Display results : 
def BackTester_Long (dfr, signal_col): # Entry +1 : Exit -1 ; Hold = 0 or None
    
    df = dfr.copy() # create copy or else will rename original column name
    df.rename(columns = { signal_col: 'signal' }, inplace = True)

    sessionpoints = np.where((df.signal == 1) | ( df.signal==-1))
    # sessionpoints = df.loc[(df.signal == 1) | ( df.signal==-1)]
    ## check df consistency: df.iloc[sessionpoints][['signal', 'close']]

    in_sessionLong = False; 
    start_long = None
    start_long_date = None
    exit_long = None
    exit_long_date = None

    analysisDF = pd.DataFrame(columns = ['En', 'Ex', 'EnPrice','ExPrice', 'ReturnPer' ])

    for item in sessionpoints[0] : 
        close_price = df.iloc[item].close
        signal = df.iloc[item].signal
        if (not in_sessionLong) and signal == 1: 
            in_sessionLong = True
            start_long = close_price
            start_long_date = df.index[item]

        
        elif in_sessionLong and signal == -1 : 
            exit_long = close_price
            exit_long_date = df.index[item]
            per_return = 100*(exit_long - start_long )/start_long
            delta_days = (exit_long_date - start_long_date)

            analysisDF = analysisDF.append ({
                'En' : start_long_date,
                'Ex' : exit_long_date,
                'EnPrice' : start_long,
                'ExPrice' : exit_long,
                'ReturnPer' : per_return,
                'days' : delta_days
                # , 'Signal': signal
            }, ignore_index=True)

            # reset vars 
            in_sessionLong = False; 
            start_long = None
            start_long_date = None
            exit_long = None
            exit_long_date = None
        
    print(analysisDF)
    return analysisDF 


analysisDF = BackTester_Long(df, 'signal_Trade_StackEMA')




###################################    PLOT TTM SQUEEZE & EMA21     ###################################


def long_signal_entry(signal_series, df):

    if signal_series.isnull().values.all() or (1 not in list(signal_series))  : return [] 

    signal   = []
    yrange = max(df['high']) - min(df['low'])
    offset = yrange * 0.10  # 2% of range
    for date,value in signal_series.iteritems():
        if value == 1: # buy
            signal.append(df.loc[date].low - offset ) # Put ^ marker below lows 
        else:
            signal.append(np.nan)
    return signal


def long_signal_exit(signal_series, df):

    if signal_series.isnull().values.all() or (-1 not in list(signal_series)) : return [] 

    signal   = []
    yrange = max(df['high']) - min(df['low'])
    offset = yrange * 0.10  # 2% of range    
    for date,value in signal_series.iteritems():
        if value == -1: # exit
            signal.append(df.loc[date].high + offset) # Put 'v' marker above highs 
        else:
            signal.append(np.nan)
    return signal


def get_sessions_long(analysisDF, df):
    df = df.copy()
    sessions   = []
    sessioncolors = []
    sessionReturns = [] 
    df['ReturnPlaceholder'] = np.nan
    df['ReturnMarker'] = None

    yrange = max(df['high']) - min(df['low'])
    # offset = yrange * 0.10  # 2% of range    

    print ('received range', df.index[0], df.index[-1])
    print ('df length', len(df))

    dfRange = df.index[0], df.index[-1]

    for i in analysisDF.itertuples():
        # Examaple seq of points 
        # [('2021-03-22',25),('2021-03-29',25)] # test
        en, ex, ret = i.En, i.Ex, i.ReturnPer
        # print (en,ex,ret)

        if ( en>=dfRange[0] and ex<=dfRange[1]): 
            pmax = max( df[en : ex].high )
            pmin = min( df[en : ex].low )

            # value = pmax + 0.1 * ( pmax - pmin) # 10% above high to low range 
            value = pmax + yrange*0.05 # 10% offset
            
            sessions.append([(en, value), (ex,value)])
            sessioncolors.append ('green' if ret > 0 else 'red' )
            # sessionReturns.append(ret)
            df.loc[ex, 'ReturnMarker'] = '$+' + str ( round(ret,1)) + '$' if ret > 0 else '$' + str ( round(ret,1)) + '$'

            df.loc[ex, 'ReturnPlaceholder'] = pmax + + yrange*0.10
            # print (en,ex,ret, value)
    
    # for date,value in signal_series.iteritems():
    #     if value == -1: # buy
    #         signal.append(price[date]*1.01) # Put marker below 
    #     else:
    #         signal.append(np.nan)
    sessionReturns = df[['ReturnPlaceholder', 'ReturnMarker']]
    # print (sessionReturns) # check return marker dataframe # test 
    return sessions, sessioncolors, sessionReturns



def plot (df, start=-100, end=-1, ctype='candle', analysis=None, addSignal=False, addAlgo=False, session=False, ha=False, signal='signal_Trade_StackEMA') : 

    # taplots = [] 
    # taplots += 
    # Lets start with a simple chart 

    # mpfdf = df[-500:-450]
    mpfdf = df[start:end]

    apsq = []

    #### >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>       ADD Indicators  (Panel 0)     ####################################
    
    
    markersize = 2 if len(mpfdf) > 50 else 5
    apsq = [        
            # EMA42 ref
            mpf.make_addplot(mpfdf['EMA_42'], type = "scatter", color='skyblue', markersize=markersize),  # 1D 21 EMA uses panel 0 by default

            # EMA21 ref            
            mpf.make_addplot(mpfdf['EMA_21'], type = "scatter", color='blue', markersize=markersize),  # uses panel 0 by default
            # mpf.make_addplot(mpfdf['EMA_21HA'], color='blue'),  # uses panel 0 by default
    ]
    

    
    # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>      ADD signal if addSignal = True  (Panel 0)     ###############      >>>>>>>>>>>>>>>>>>>>>>>
    
    longEntry = long_signal_entry(mpfdf[signal], mpfdf)
    longExit = long_signal_exit(mpfdf[signal], mpfdf)

    # print ('Long Entry  : ', longEntry)
    # print ('Long Exit   : ', longExit)

    if ( longEntry and longExit) : 
        apsq += [ 
            # add long entry 
            mpf.make_addplot(longEntry ,type='scatter', color='purple', markersize=40, marker='^'), 
            # add long exit 
            mpf.make_addplot( longExit ,type='scatter', color='black', markersize=40, marker='x') 
        ]


    # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      ADD TRADE SESSIONS  (Panel 0)       >>>>>>>>>>>>>>>>>>>>>>>>>>

    # add sessions if addsession = True 
    # seq_of_points=[('2021-03-22',25),('2021-03-29',25)] # test 
    seq_of_points, seq_colors, seq_Returns = get_sessions_long(analysisDF, mpfdf) # draw session lines
    # mpf.plot(df,alines=dict(alines=seq_of_points)) # test 
    # print ('Trade Area', seq_of_points)

    d = seq_Returns
    if not d.ReturnPlaceholder.isnull().values.all() : 
        mymarkers = d.ReturnMarker.tolist()
        apsq += [ 
            # add texts using markers to annotate 
            mpf.make_addplot( d.ReturnPlaceholder, type='scatter',marker=mymarkers,markersize=200,color='pink')
        ]
    # mpfchart["plot_ratios"] += common_plot_ratio # Required to add a new Panel



    #########################     Squeeze plots  (Panel 1) default #############################

    # make same as TOS colors # order is important
    data = []
    alpha = []
    for i in [-3, -4, -2, -1, 4, 5 ] : # maintain order
        d = mpfdf[squeezes.columns[i]]
        # if np.isnan(np.sum(np.asarray(d))) : 
        if d.isnull().values.all() : 
            d = d.fillna(0)
            print ("All Null/NAN : ", squeezes.columns[i])
            alpha += [0.0] # make invisible 
            print (squeezes.columns[i], 'modified')
        else : 
            alpha += [0.3]

        # alpha += [0.5]
        data += [d]
        # print (d)
        # print ("isnull", squeezes.columns[i], d.isnull().values.all())

    # set ylim 
    ylim = (min(mpfdf[squeezes.columns].min())*1.02, max(mpfdf[squeezes.columns].max()*1.02))
    
    apsq += [
            # Note order is important here    
            mpf.make_addplot(data[0], secondary_y=False, type="bar", color="blue", alpha=alpha[0], panel=1, ylim=ylim),
            mpf.make_addplot(data[1], secondary_y=False, type="bar", color="deepskyblue", alpha=alpha[1], panel=1, ylim=ylim),
            mpf.make_addplot(data[2], secondary_y=False, type="bar", color="red", alpha=alpha[2], panel=1, ylim=ylim),
            mpf.make_addplot(data[3], secondary_y=False, type="bar", color="yellow", alpha=alpha[3], panel=1, ylim=ylim),
            
            # mpf.make_addplot(mpfdf['close'], color="black", panel=1),
            mpf.make_addplot(data[4], secondary_y=False, color="green",alpha=alpha[4], panel=1, ylim=ylim, width=2),
            mpf.make_addplot(data[5], secondary_y=False, color="red", alpha=alpha[5],  panel=1, ylim=ylim, width=2)
    ]


    # squeeze metrics original flavor
    d = mpfdf['SQZ_OFF'].apply(lambda x: 0 if x==1 else np.nan)
    if not d.isnull().values.all() : 
        # print (d)
        apsq += [mpf.make_addplot(d , secondary_y=False, scatter=True, markersize=20, marker='o',color="lime",  panel=1)]
    
    d = mpfdf['SQZ_ON'].apply(lambda x: 0 if x==1 else np.nan)
    if not d.isnull().values.all() : 
        # print (d)
        apsq += [mpf.make_addplot(d, secondary_y=False, scatter=True, markersize=20, marker='o', color="red",  panel=1)]
    
    d = mpfdf['squeeze_on'].apply(lambda x: 0 if x==1 else np.nan)
    if not d.isnull().values.all() : 
        # print (d)
        apsq += [mpf.make_addplot(d, secondary_y=False, scatter=True, markersize=2, marker='o', color="black",  panel=1)]
    # mpf.make_addplot(mpfdf[squeezes.columns[3]], scatter=True,markersize=20,marker='o',color="skyblue",  panel=2),

    # mpf.make_addplot(mpfdf['squeeze_on'].apply(lambda x: -2 if x==0 else None), scatter=True,markersize=10,marker='o', color="black",  panel=1),
    # mpf.make_addplot(mpfdf['squeeze_off'].apply(lambda x: -2 if x==0 else None), scatter=True,markersize=10,marker='o', color="lime",  panel=1),   
    

    # mpf.make_addplot(long_signal_entry(mpfdf[signal], mpfdf.low) ,type='scatter', color='purple', markersize=15, marker='^'),
    # # add long exit 
    # mpf.make_addplot(long_signal_exit(mpfdf[signal], mpfdf.high) ,type='scatter', color='magenta', markersize=15, marker='v'), 




    # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    ADD Algo if addAlgo=True (Panel 2)        >>>>>>>>>>>>>>>>>>>>>>>>>>

    # All scatter plot in a single line 
    signalCols = sorted ([col for col in mpfdf if col.startswith('signal')])
    signalDF = mpfdf[signalCols]
    ylimSignal = len(signalCols)*0.5+1 # add bottom and top row for buffer to view markers 
    counter = 0.5

    # add base at 0 
    apsq += [mpf.make_addplot(mpfdf[signalCols[0]].apply(lambda x:0), scatter=True, alpha=0, panel=2, secondary_y=False, ylim=(0,ylimSignal), ylabel='Signals')]

    for col in signalCols : 
        d = mpfdf[col].copy()        
        if not d.isnull().values.all() :  # check if a null array 
            # print (d)

            # IF signal_trade indicator 
            if (col.startswith('signal_Trade')) : 
                mymarkercolor = d.apply(
                    lambda x: 'purple' if x==1 else ('red' if x==-1 else 
                    'yellow' if (x==-2 or x==2) else 'lightgray')).tolist()
                mymarker = d.apply(
                    lambda x: '^' if x==1 else ('x' if x==-1 else 
                    'o' if (x==-2 or x==2) else 'None')).tolist()
                mydata = d.apply( lambda x: counter )
                apsq += [mpf.make_addplot(mydata, scatter=True, markersize=20, marker=mymarker, color=mymarkercolor, panel=2, secondary_y=False, ylim=(0,ylimSignal))]

            # IF only signal indicator 

            else: 
                mymarkercolor = d.apply(
                    lambda x: 'limegreen' if x==1 else ('red' if x==-1 else 
                    'yellow' if (x==-2 or x==2) else 'lightgray')).tolist()
                mydata = d.apply( lambda x: counter )
                apsq += [mpf.make_addplot(mydata, scatter=True, markersize=20, marker='o', color=mymarkercolor, panel=2, secondary_y=False, ylim=(0,ylimSignal))]
            # print (mydata) # test 
            # print (mymarkercolor) # test 

        counter +=0.5

    

    # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>         Show HA is HA = True  
    final_df = mpfdf # placeholder 

    if ha : 
        # If HA HeikinAski Charts Enabled ; else remove section
        ## Generate the HA columns and rename to OHLC
        final_df = mpfdf[['HA_open', 'HA_high', 'HA_low', 'HA_close']].copy()
        final_df.columns = ['open', 'high', 'low', 'close']
        # mpf.plot(df2, type='candle', style='yahoo')


    import matplotlib.dates as mdates
    import matplotlib.ticker as mticker
    from matplotlib.ticker import AutoLocator, MultipleLocator

    # fig.tight_layout(h_pad= -1.6)

    # fig, axlist = mpf.plot(final_df, type=ctype, addplot=apsq, figscale=1, figratio=(15,8),title= symbol+'\nTTM-Squeeze: '+ interval, style='yahoo', volume=False,panel_ratios=(6,2), datetime_format=' %m/%d',xrotation=45, returnfig=True)


    # fig, axlist = mpf.plot(final_df, type=ctype, figscale=1, figratio=(15,8),title= symbol+'\nTTM-Squeeze: '+ interval, style='yahoo',datetime_format=' %b-%d',xrotation=90, returnfig=True, alines=dict(alines=seq_of_points))

    # mpf.plot(final_df, type=ctype,addplot=apsq, figscale=1, figratio=(15,8),title= symbol+'\nTTM-Squeeze: '+ interval, style='yahoo',)

    # fig, axlist = mpf.plot(final_df, type=ctype, addplot=apsq, figscale=1, figratio=(15,8),title= symbol+'\nTTM-Squeeze: '+ interval, style='yahoo', volume=False, panel_ratios=(6,2), datetime_format=' %b-%d',xrotation=90, returnfig=True, alines=dict(alines=seq_of_points, colors=seq_colors, linewidths=2,))
    
    # yrange = max(mpfdf['high']) - min(mpfdf['low'])
    # offset = yrange * 0.02  # 2% of range
    
    # fig, axlist = mpf.plot(final_df, type=ctype, addplot=apsq, figscale=1, figratio=(15,8),title= symbol+'\nTTM-Squeeze: '+ interval, style='yahoo', volume=False, panel_ratios=(6,2), datetime_format=' %b-%d',xrotation=90, returnfig=True, ) 
    ## tight_layout=Truex, ylim = ( min(mpfdf['low'] - + yrange * 0.1), max(mpfdf['high']) + yrange * 0.1)

    # Add Algo Panel # if addAlgo=True 
    fig, axlist = mpf.plot(final_df, type=ctype, addplot=apsq, figscale=1, figratio=(15,8),title= symbol+'\nTTM-Squeeze: '+ interval, style='yahoo', volume=False, panel_ratios=(6,2,2), datetime_format=' %b-%d',xrotation=90, returnfig=True, alines=dict(alines=seq_of_points, colors=seq_colors, linewidths=2,))



    # print (axlist)
    ax1 = axlist[1]  # Panel 0 
    # ax1.set_ylim( max(mpfdf['high']) + yrange * 0.1, min(mpfdf['low'] - + yrange * 0.1))
    ax2 = axlist[2]  # Panel 2

    ##>>>>>>>>>>>>>>>     Ytick Markers for Algo Names      #########################
    ax3 = axlist[-2]  # Panel 1
    counter = 0.5 
    yticks = list(np.arange (0.5, 0.5*(1+len(signalCols)), 0.5))
    # signalCols # replace prefix signal_ - clean look
    signalCols_n = [sub.replace('signal_', '') for sub in signalCols]
    print (len(yticks), len(signalCols))
    # axs = for i in axlist i.ylable="signal"
    ax3.set_yticks(yticks)
    ax3.set_yticklabels(signalCols_n, fontdict={'fontsize': 8})


    # for col in signalCols : 
    #     ax3.text(y=counter, x=ax3.get_xlim()[0]*0.9,  s=col, alpha=0.7, color='b')
    #     counter += 0.5



    # ax2.set_ylim(min(mpfdf[squeezes.columns].min()), max(mpfdf[squeezes.columns].max()))
    ax1.minorticks_on()    
    ax1.tick_params(axis='x',which='minor',direction='out',color='b',labelsize=3,labelcolor='g')
    ax1.xaxis.set_minor_locator(MultipleLocator(1))
    # ax1.xaxis.set_major_locator(MultipleLocator(2))

    # plt.rcParams['xtick.major.size'] = 8
    # plt.rcParams['xtick.minor.size'] = 4
    # plt.rcParams['xtick.label.size'] = 4
    # ax1.tick_params(axis='x', which='both',labelbottom= False, labeltop=False )
    # ax1.tick_params(axis='x', which='minor', pad = 2)
    # ax1.grid(which='major',color='k')
    # ax1.grid(which='minor',color='gray')

    # base = len(final_df)

    # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    # # ax1.xaxis.set_major_locator(mticker.IndexLocator(base=base/10, offset=0))
    # ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
    # ax1.xaxis.set_minor_locator(AutoMinorLocator())

    # mpf.plot(mpfdf, type='candle', figscale=1, style='blueskies')
    plt.show()
    # print (df[-1:][['open', 'high', 'low', 'close']])

# plot (df, start=-150, end=-50, ctype='ohlc', ha=True, signal='signal_Trade_StackEMA')
# plot (df, start=-200, ctype='ohlc', ha=True, signal='signal_Trade_StackEMA')
# plot (df, start=-50, ctype='ohlc')
# plot (df, start=-50, ctype='ohlc', ha=True, signal='signal_Trade_StackEMA')
plot (df, start=-200, end=-100, ctype='ohlc', ha=True, signal='signal_Trade_StackEMA')
# plot (df, start=-450, end=-100, ctype='ohlc', ha=False)

print (df[-1:][['open', 'high', 'low', 'close']])
