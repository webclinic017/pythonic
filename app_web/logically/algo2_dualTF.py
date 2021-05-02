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
import finta as ft

import datasource as data  # disable this whn API is runing 

# # key reference ind and plots
# https://github.com/peerchemist/finta
# https://github.com/twopirllc/pandas-ta
# https://github.com/matplotlib/mplfinance/

symbol = None

def initData (symbol = 'SPY', interval="4H", bars=700, live=False) : 
    symbol = symbol
    df = None
    # symbol = 'AAL'
    # sd = datetime(2020, 1, 1)
    # ed = datetime(2021, 4, 12)
    # # interval = "1d"
    # interval = "60m"
    # , live=True if live : 
    # # df = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")
    # # df = yf.download(tickers=symbol, start=sd, interval="60m")
    # # df = yf.download(tickers=symbol, start=sd, end=ed, interval="1d")
    # # dfd = yf.download(tickers=symbol, start=sd, interval=interval,prepost=True)
    # dfd = yf.download(tickers=symbol, start=sd, interval=interval)
    
    if interval=="4H": 
        if live : df = data.getLiveData(symbol=symbol, interval="1H", period='300d')        
        else:  df = data.getData(symbol=symbol, interval="1H", bars=(-4900, None))
        # df = data.getData(symbol=symbol, interval="1H", bars=(-1000, None))


        # df = df[-4000:]
        # df = data.getData(symbol, bars=(-900, -325))

        # # Enable if 4H reampling is True 
        # dfd = yf.download(tickers=symbol, start=sd, interval=interval,prepost=True)
        # dfd = yf.download(tickers=symbol, start=sd, interval=interval)
        # df = dfd
        interval = "4H"
        # Resampling Code 
        ## Resample to 4H timefeame 
        aggregation = {'Open'  :'first',
                    'High'  :'max',
                    'Low'   :'min',
                    'Close' :'last',
                    'Volume':'sum'}
        df = df.resample('4H').agg(aggregation).dropna()
    
    
    else: # for Other timeframes 1H, 1D - no resampling
        if not live: df = data.getData(symbol, interval=interval)
        else : 
            if interval =="1D" : period = '500d' 
            elif interval =="1H" : period = '100d' 
            df = data.getLiveData(symbol=symbol, interval=interval, period=period)

    return df


def addIndicators(df): 
    ################################################################################

    ############    ADD some INDICATORS 

    print ('Initial DF length ', len(df))
    # squeezes = df.ta.squeeze(lazybear=False, detailed=True, append=True)
    squeezes = df.ta.squeeze(lazybear=True, detailed=True, append=True)
    bollingers = df.ta.bbands(append=True) # 'BBL_5_2.0', 'BBM_5_2.0', 'BBU_5_2.0', 'BBB_5_2.0' 
    # macd = df.ta.macd(append=True) # 'MACD_12_26_9', 'MACDh_12_26_9','MACDs_12_26_9'],
    # rsi = df.ta.rsi(length=20, append=True)
    # rsi_SMA = df['RSI_20_SMA'] = ta.sma(rsi, length=20, append=True)

    # rsx = df.ta.rsx(length=20, append=True)
    # rsx_SMA = df['RSX_20_SMA'] = ta.sma(rsx, length=20, append=True)

    ha = df.ta.ha(append=True) # heikinashi bars 
    df['HA_color'] = np.where(df.HA_close > df.HA_open, 1, -1)
    # ema21HA = df['EMA_21HA'] = ta.ema( df.HA_close, length=21, append=True)
    ema9 = df.ta.ema(length=9, append=True)
    ema21 = df.ta.ema(length=21, append=True)
    ema42 = df.ta.ema(length=42, append=True)
    ema50 = df.ta.ema(length=50, append=True)
    ema100 = df.ta.ema(length=100, append=True)
    ema150 = df.ta.ema(length=150, append=True)
    keltner = df.ta.kc(append=True)

    df['signal_SQ2gauss']= ft.TA.SQZMI(df).apply(lambda x: -1 if x else 0)
    df['signal_trTTM'] = df.ta.ttm_trend(append=True)

    # df['signal_decreasing'] = df.ta.decreasing(length=8).apply(lambda x: -1 if x==1 else x)
    # df['signal_increasing'] =df.ta.increasing(length=8)
    # length = 3 
    # df['signal_IDClose'] = df.ta.decreasing(close=df.HA_close, length=length, strict=True).apply(lambda x: -1 if x==1 else x) + df.ta.increasing(close=df.HA_close,length=length, strict=True)
    # df['signal_IDhigh'] = df.ta.decreasing(close=df.HA_high, length=length, strict=True).apply(lambda x: -1 if x==1 else x) + df.ta.increasing(close=df.HA_high,length=length, strict=True)

    # Exit Chandelier (based on FINTA)
    chandelier = ft.TA.CHANDELIER(df, long_period=15, short_period=15)
    df['chxLong'], df['chxShort'] = chandelier['Long.'], chandelier['Short.']
    df['chxLong'] = np.where(df['chxLong'] >= df['close'], np.NaN, df['chxLong'])
    df['chxShort']= np.where(df['chxShort'] < df['close'], np.NaN, df['chxShort'])
    df['signal_sChandelier'] = np.where(df['chxShort'] > 0, -1, 1) # first hint of red
    # df['signal_chandelierL'] = np.where(df['chxLong'] > 0, 1, -1)


    # New Squeeze (black dots) : 1 = ON, 0 = OFF (for 'in_squeeze')
    def in_squeeze(df):
        if df['BBL_5_2.0'] > df['KCLe_20_2'] and df['BBU_5_2.0'] < df['KCUe_20_2'] : 
            return 1 
    def out_squeeze(df):
        if not (df['BBL_5_2.0'] > df['KCLe_20_2'] and df['BBU_5_2.0'] < df['KCUe_20_2']):         
            return 1    
    df['squeeze_on'] = df.apply(in_squeeze, axis=1)
    df['squeeze_off'] = df.apply(out_squeeze, axis=1)

    # PSAR Stop Reverse (based on pandas_TA)
    psar = df.ta.psar( append=True)
    # add psar signal -1 0 +1 
    df['signal_slPSAR'] = df['PSARl_0.02_0.2'].apply(lambda x: 1 if x>0 else -1)
    df['rPSAR'] = df['PSARr_0.02_0.2'].apply(lambda x: -8 if x==True else 0)

    def rPSAR (df): 
        if df['PSARl_0.02_0.2'] > 0 and df['PSARr_0.02_0.2'] : return 9 
        elif df['PSARs_0.02_0.2'] > 0  and df['PSARr_0.02_0.2'] :  return -9 
        else : return 0

    df['signal_rPSAR'] = df[['PSARl_0.02_0.2', 'PSARs_0.02_0.2', 'PSARr_0.02_0.2' ]].apply(rPSAR, axis=1)
    # df[['signal_rPSAR', 'signal_rPSAR']].tail(50)

    ## SAR based on Finta SAR 
    sar = df['SAR'] = ft.TA.SAR(df)    
    df['signal_sSAR'] = np.where (df['SAR']<df['low'], 1, -1)


    # add HA_Color to signal -1 0 +1 
    df['signal_trHAcolor'] = df['HA_color']

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


    return df  # loaded with indicators 




###################################    PLOT TTM SQUEEZE & EMA21     ###################################


def long_signal_entry(signal_series, df, secondary=False):

    factor = 1.0 if not secondary else 1.5
    if signal_series.isnull().values.all() or (1 not in list(signal_series))  : return [] 

    signal   = []
    yrange = max(df['high']) - min(df['low'])
    offset = yrange * 0.10  # 2% of range
    for date,value in signal_series.iteritems():
        if value == 1: # buy
            signal.append(df.loc[date].low - factor* offset ) # Put ^ marker below lows 
        else:
            signal.append(np.nan)
    return signal


def long_signal_exit(signal_series, df, secondary=False):

    factor = 1.5 if not secondary else 2.0
    if signal_series.isnull().values.all() or (-1 not in list(signal_series)) : return [] 

    signal   = []
    yrange = max(df['high']) - min(df['low'])
    offset = yrange * 0.10  # 2% of range    
    for date,value in signal_series.iteritems():
        if value == -1: # exit
            signal.append(df.loc[date].high + factor * offset) # Put 'v' marker above highs 
        else:
            signal.append(np.nan)
    return signal


def get_reversals(signal_series, df):

    if signal_series.isnull().values.all() : return [], [] 

    signal   = []
    markercolor = []
    yrange = max(df['high']) - min(df['low'])
    offset = yrange * 0.10  # 2% of range
    for date,value in signal_series.iteritems():
        if value == -9: # reversal bear
            signal.append(df.loc[date].high + 1.5 *offset ) # Put o marker above highs 2x 
            markercolor.append('red')
        
        elif value == 9: # reversal bull
            signal.append(df.loc[date].high + 1.5* offset ) # Put o marker above highs 1x
            markercolor.append('green')
        else:
            signal.append(np.nan)
            markercolor.append('None')

    return signal, markercolor


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




############     SIMPLE CANDLE CHART w/ volume 
# style = 'yahoo','nightclouds','ibd'
# type =  'candle', 'hollow_and_filled'
# mpf.plot(mpfdf, style='yahoo', type='candle', volume=True, panel_ratios=(4,1))



def plotAll (df, symbol="SPY", interval="4H", start=-100, end=None, ctype='candle', addSignal=False, addAlgo=False, session=False, ha=False, signal='signalxTrade_StackEMA', analysisDF=None,figratio=(15,8), figscale=1,panel_ratios=(6,2,4), scale_padding=dict(left=.05,right=0.95, top=0.3, bottom=0.6), header="") : 

    # taplots = [] 
    # taplots += 
    # Lets start with a simple chart 

    # mpfdf = df[-500:-450]
    mpfdf_columns = list(df.columns)
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
    
    # # if PSAR enabled : draw lines 
    # apsq += [
    #      # psar 
    #         mpf.make_addplot(mpfdf['PSARl_0.02_0.2'], color='pink', markersize=markersize, width=1),  # uses panel 0 by default
    #         mpf.make_addplot(mpfdf['PSARs_0.02_0.2'], color='orange', markersize=markersize, width=1),  # uses panel 0 by default
    # ]

    # # if PSAR enabled : draw lines 
    # apsq += [
    #     # psar 
    #     mpf.make_addplot(mpfdf['SAR'], type = "scatter", color='pink', markersize=markersize, width=1),  # uses panel 0 by default
    # ]

    # # if Chandelier Ex enabled : draw lines 
    # apsq += [
    #      # chandelier Exit  
    #         mpf.make_addplot(mpfdf['chxLong'], color='green', markersize=markersize, width=1),  # uses panel 0 by default
    #         mpf.make_addplot(mpfdf['chxShort'], color='red', markersize=markersize, width=1),  # uses panel 0 by default
    # ]


    
    # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>      ADD signal if addSignal = True  (Panel 0)     ###############      >>>>>>>>>>>>>>>>>>>>>>>
    
    longEntry = long_signal_entry(mpfdf[signal], mpfdf)
    longExit = long_signal_exit(mpfdf[signal], mpfdf)

    # print ('Long Entry  : ', longEntry)
    # print ('Long Exit   : ', longExit)

    if ( longEntry) : 
        apsq += [ 
            # add long entry 
            mpf.make_addplot(longEntry, type='scatter', color='purple', markersize=40, marker='^')
        ]

    if (longExit) : 
        apsq += [ 
            # add long exit 
            mpf.make_addplot( longExit, type='scatter', color='black', markersize=40, marker='x') 
        ]


    ## Add anything that starts with SignalxTrade Add the above logic to draw on chart Panel 0 

    signalCols = sorted ([col for col in mpfdf if col.startswith('signalx_')])
    for col in signalCols : 
        longEntry = long_signal_entry(mpfdf[col], mpfdf, secondary=True)
        longExit = long_signal_exit(mpfdf[col], mpfdf, secondary=True)

        # print ('Long Entry  : ', longEntry)
        # print ('Long Exit   : ', longExit)

        if ( longEntry ) : 
            if col.startswith('signalx_L1') : 
                colorme = 'turquoise'    # 'greenyellow' # 'aquamarine'
                markersz = 10;  
            else : 
                colorme = 'violet', 
                markersz = 25; 
            apsq += [ 
                # add long entry 
                mpf.make_addplot(longEntry, type='scatter', color=colorme, markersize=markersz, marker='$\\bigtriangleup$')
            ]
        if (longExit) : 
             apsq += [ 
                # add long exit 
                mpf.make_addplot( longExit, type='scatter', color='gray', markersize=25, marker='x') 
            ]


    # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      ADD STOPS  (Panel 0)       >>>>>>>>>>>>>>>>>>>>>>>>>>
    # todo


    # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      ADD SR levels  (Panel 0)       >>>>>>>>>>>>>>>>>>>>>>>>>>
    #  todo 


    # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      ADD TRADE SESSIONS  (Panel 0)       >>>>>>>>>>>>>>>>>>>>>>>>>>

    # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>      ADD Reversal indicator  (Panel 0)       >>>>>>>>>>>>>>>>>>>>>>>>>>
    d, markercolor = get_reversals(mpfdf['signal_rPSAR'], mpfdf)
    # print (len(d), len(mpfdf['signal_rPSAR']), len(mpfdf['signal_rPSAR']))
    # print (d) 
    # print (markercolor)   
    # print (mpfdf['signal_rPSAR'].tolist())
    if d : # check has values
        # mymarkers = d.ReturnMarker.tolist()
        apsq += [ 
            # add texts using markers to annotate 
            # mpf.make_addplot( d, type='scatter',marker='o',markersize=5,color='black')
            mpf.make_addplot( d, type='scatter',marker='o',markersize=5,color=markercolor)
        ]
    


    # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>  ADD TRADE SESSION if addsession = True   (Panel 0)  >>>>>>>>>>>>>>>>>>>>>>>>>>
    # seq_of_points=[('2021-03-22',25),('2021-03-29',25)] # test 
    seq_of_points, seq_colors, seq_Returns = get_sessions_long(analysisDF, mpfdf) if analysisDF is not None else (None, None, None) # draw session lines
    # mpf.plot(df,alines=dict(alines=seq_of_points)) # test 
    # print ('Trade Area', seq_of_points)

    if seq_Returns is not None : 
        if not seq_Returns.ReturnPlaceholder.isnull().values.all() : 
            mymarkers = seq_Returns.ReturnMarker.tolist()
            apsq += [ 
                # add texts using markers to annotate 
                mpf.make_addplot( seq_Returns.ReturnPlaceholder, type='scatter',marker=mymarkers,markersize=200,color='pink')
            ]
    # mpfchart["plot_ratios"] += common_plot_ratio # Required to add a new Panel



    #########################     Squeeze plots  (Panel 1) default #############################

    # make same as TOS colors # order is important
    data = []
    alpha = []
    squeezes = [col for col in mpfdf if col.startswith('SQZ')]
    for i in [-3, -4, -2, -1, 4, 5 ] : # maintain order
        d = mpfdf[squeezes[i]]
        # if np.isnan(np.sum(np.asarray(d))) : 
        if d.isnull().values.all() : 
            d = d.fillna(0)
            print ("All Null/NAN : ", squeezes[i])
            alpha += [0.0] # make invisible 
            print (squeezes[i], 'modified')
        else : 
            alpha += [0.3]

        # alpha += [0.5]
        data += [d]
        # print (d)
        # print ("isnull", squeezes[i], d.isnull().values.all())

    # set ylim 
    ylim = (min(mpfdf[squeezes].min())*1.02, max(mpfdf[squeezes].max()*1.02))
    
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
        apsq += [mpf.make_addplot(d, secondary_y=False, scatter=True, markersize=2, marker='o', color="black", panel=1)]
    # mpf.make_addplot(mpfdf[squeezes[3]], scatter=True,markersize=20,marker='o',color="skyblue",  panel=2),

    # mpf.make_addplot(mpfdf['squeeze_on'].apply(lambda x: -2 if x==0 else None), scatter=True,markersize=10,marker='o', color="black",  panel=1),
    # mpf.make_addplot(mpfdf['squeeze_off'].apply(lambda x: -2 if x==0 else None), scatter=True,markersize=10,marker='o', color="lime",  panel=1),   
    

    # mpf.make_addplot(long_signal_entry(mpfdf[signal], mpfdf.low), type='scatter', color='purple', markersize=15, marker='^'),
    # # add long exit 
    # mpf.make_addplot(long_signal_exit(mpfdf[signal], mpfdf.high), type='scatter', color='magenta', markersize=15, marker='v'), 




    # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>    ADD Algo if addAlgo=True (Panel 2)        >>>>>>>>>>>>>>>>>>>>>>>>>>

    # All scatter plot in a single line 
    signalCols = sorted ([col for col in mpfdf if col.startswith('signal')])
    signalDF = mpfdf[signalCols]
    ylimSignal = len(signalCols)*0.5+1 # add bottom and top row for buffer to view markers 
    counter = 0.5

    # add base at 0 
    apsq += [mpf.make_addplot(mpfdf[signalCols[0]].apply(lambda x:0), scatter=True, alpha=0, panel=2, secondary_y=False, ylim=(0,ylimSignal), ylabel='Signals')]

    # define markersize 
    l = len(mpfdf)
    markersize = 5 if l > 150 else 20 
    for col in signalCols : 
        d = mpfdf[col].copy()        
        if not d.isnull().values.all() :  # check if a null array 
            # print (d)

            # IF signalxtrade indicator 
            if (col.startswith('signalxTrade')) : 
                mymarkercolor = d.apply(
                    lambda x: 'purple' if x==1 else ('red' if x==-1 else 
                    'yellow' if (x==-2 or x==2) else 'lightgray')).tolist()
                mymarker = d.apply(
                    lambda x: '^' if x==1 else ('x' if x==-1 else 
                    'o' if (x==-2 or x==2) else 'None')).tolist()
                mydata = d.apply( lambda x: counter )
                apsq += [mpf.make_addplot(mydata, scatter=True, markersize=markersize, marker=mymarker, color=mymarkercolor, panel=2, secondary_y=False, ylim=(0,ylimSignal))]


            # IF only signal indicator which starts with 'signal'
            else: 
                mymarkercolor = d.apply(
                    lambda x: 'limegreen' if x==1 else ('red' if x==-1 
                    else 'yellow' if (x==-2 or x==2) 
                    else ( 'black' if x ==-8 
                    else ( 'green' if x== 9 
                    else ('red' if x == -9 
                    else 'lightgray'))))).tolist()
                mydata = d.apply( lambda x: counter )
                apsq += [mpf.make_addplot(mydata, scatter=True, markersize=markersize, marker='o', color=mymarkercolor, panel=2, secondary_y=False, ylim=(0,ylimSignal))]
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

    # Add Algo Panel # if addAlgo=True and AnalysisDF is not None 
    # kwargs=dict(title)
    

    # For Tight layout True 
    #fig, axlist = mpf.plot(final_df, type=ctype, addplot=apsq, figscale=1, figratio=(15,8),title= symbol+' '+ interval + header, style='yahoo', volume=False, panel_ratios=(6,2,4), datetime_format=' %b-%d',xrotation=90, returnfig=True, tight_layout=False, alines=dict(alines=seq_of_points, colors=seq_colors, linewidths=2,)) if seq_of_points is not None else mpf.plot(final_df, type=ctype, addplot=apsq, figscale=1, figratio=(15,8),title= symbol+' '+ interval + header, style='yahoo', volume=False, panel_ratios=(6,2,4), datetime_format=' %b-%d',xrotation=90, returnfig=True, tight_layout=True, scale_padding=dict(left=.15,right=5))

    # For Tight layout False 
    fig, axlist = mpf.plot(final_df, type=ctype, addplot=apsq, figscale=figscale, figratio=figratio,title= symbol+' '+ interval + header, style='yahoo', volume=False, panel_ratios=panel_ratios, datetime_format=' %b-%d',xrotation=90, returnfig=True, tight_layout=False, alines=dict(alines=seq_of_points, colors=seq_colors, linewidths=2,)) if seq_of_points is not None else mpf.plot(final_df, type=ctype, addplot=apsq, figscale=figscale, figratio=figratio, title= symbol+' '+ interval + header, style='yahoo', volume=False, panel_ratios=panel_ratios, datetime_format=' %b-%d',xrotation=90, returnfig=True, tight_layout=False, scale_padding=scale_padding)


    
    # print (axlist)
    ax1 = axlist[1]  # Panel 0 
    # ax1.set_ylim( max(mpfdf['high']) + yrange * 0.1, min(mpfdf['low'] - + yrange * 0.1))
    ax2 = axlist[2]  # Panel 2

    ##>>>>>>>>>>>>>>>     Ytick Markers for Algo Names      #########################
    ax3 = axlist[-2]  # Panel 1
    counter = 0.5 
    yticks = list(np.arange (0.5, 0.5*(1+len(signalCols)), 0.5))
    # signalCols # replace prefix signal_ - clean look
    signalCols_n = [sub.replace('signalx', '') for sub in signalCols]
    signalCols_n = [sub.replace('signal_', '') for sub in signalCols_n]
    print ("YTICKS, signalcols", len(yticks), len(signalCols))
    # axs = for i in axlist i.ylable="signal"
    ax3.set_yticks(yticks)
    ax3.set_yticklabels(signalCols_n, fontdict={'fontsize': 8})


    # for col in signalCols : 
    #     ax3.text(y=counter, x=ax3.get_xlim()[0]*0.9,  s=col, alpha=0.7, color='b')
    #     counter += 0.5



    # ax2.set_ylim(min(mpfdf[squeezes].min()), max(mpfdf[squeezes].max()))
    ax1.minorticks_on()    
    ax1.tick_params(axis='x',which='minor',direction='out',color='b',labelsize=3,labelcolor='g')
    ax1.xaxis.set_minor_locator(MultipleLocator(1))

    # # calculate tick intervals # 25 majors for 100 bars : bars / 4
    # fdict = {
    #     '1H': 7, 
    #     '4H':2, 
    #     '1D': 3
    # }
    totalbars = len(mpfdf)
    numMajors = 25
    # locator = -(start-end)/fdict.get(interval)
    # if locator > 1: 
    #     ax1.xaxis.set_major_locator(MultipleLocator(round(locator)))

    # if (len(mpfdf) <=50) : 
    ax1.xaxis.set_major_locator(MultipleLocator(round(totalbars/numMajors)))
    # elif (len(mpfdf) <=100): 
    #     ax1.xaxis.set_major_locator(MultipleLocator(3))


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
    # plt.show()
    # print (df[-1:][['open', 'high', 'low', 'close']])
    print ( "Done")

    return fig, axlist

def runTest(symbol="SPY", interval="4H", bars=(-700, None)): 

    df = initData(symbol=symbol, interval=interval) # load/download data to df

    addIndicators(df)
    algo(df)

    analysisDF = BackTester_Long(df, 'signalxTrade_StackEMA')

    # all Plot calls 
    s, e = bars 

    # plotAll (df, start=-150, end=-50, ctype='ohlc', ha=True, signal='signalxTrade_StackEMA', symbol=symbol, interval=interval)
    # plotAll (df, start=-200, ctype='ohlc', ha=True, signal='signalxTrade_StackEMA', symbol=symbol, interval=interval)
    # plotAll (df, start=-50, ctype='ohlc', symbol=symbol, interval=interval)
    # plotAll (df, start=-10, ctype='candle', ha=True, signal='signalxTrade_StackEMA', symbol=symbol, interval=interval)
    # plotAll (df, start=-220, end=-150, ctype='candle', ha=True, signal='signalxTrade_StackEMA', symbol=symbol, interval=interval)
    # plotAll (df, start=-450, end=-325, ctype='ohlc', ha=True, signal='signalxTrade_StackEMA', symbol=symbol, interval=interval)
    # plotAll (df, start=-200, ctype='ohlc', ha=False, signal='signalxTrade_StackEMA', symbol=symbol, interval=interval)
    plotAll (df, start= s, end= e, ctype='ohlc', ha=True, signal='signalxTrade_StackEMA', symbol=symbol, interval=interval, header='Live')
    # plotAll (df, start=-450, end=-300, ctype='ohlc', ha=False)

    print (df[-1:][['open', 'high', 'low', 'close']])
        # yf.Ticker(symbol).get

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


# analysisDF = BackTester_Long(df, 'signalxTrade_StackEMA')


# figwidth=45
df = None 

def AlgoImage(symbol="SPY", interval="4H", bars=(-700, None), full=False, mini=False, live=True): 

    df = initData(symbol=symbol, interval=interval, live=True) # load/download data to df

    addIndicators(df)

    # algo0(df)
    algo(df)

    # analysisDF = BackTester_Long(df, 'signalxTrade_StackEMA')

    # all Plot calls 
    s, e = bars 

    trade_Identifier = 'signalxTrade_SQTest'
    # trade_Identifier = 'signalxTrade_StackEMA'

    if full :  # full page image # ~200KB 
        fig = plotAll (df, start= s, end= e, ctype='ohlc', ha=True, signal=trade_Identifier, symbol=symbol, interval=interval, figratio=(16,8),panel_ratios=(8,2,4), figscale=1.6, scale_padding=dict(left=.05,right=0.7, top=0.3, bottom=0.6), header="\n"+ str(df[-1:].iloc[0].close))
        #fig = plotAll (df, start= s, end= e, ctype='ohlc', ha=True, signal=trade_Identifier, symbol=symbol, interval=interval, figratio=(28,8),panel_ratios=(6,2,4), figscale=1)

    elif mini : # recommend 50 bars max 
        fig = plotAll (df, start= s, end= e, ctype='ohlc', ha=True, signal=trade_Identifier, symbol=symbol, interval=interval, figratio=(2,2),panel_ratios=(8,2,6), figscale=0.8, scale_padding=dict(left=.05,right=2.3, top=0.3, bottom=0.8))


    else: # miniimage ~ 100kb # Medium image : recommend 150 bars max 
        fig = plotAll (df, start= s, end= e, ctype='ohlc', ha=True, signal=trade_Identifier, symbol=symbol, interval=interval, header="\n"+ str(df[-1:].iloc[0].close))
    # plotAll (df, start=-450, end=-300, ctype='ohlc', ha=False)



    # print (df[-1:][['open', 'high', 'low', 'close']])
        # yf.Ticker(symbol).get
    return fig


def algo0 (df): 
        
    #################################  MAIN AlGO and SIGNAL GENERATION  #####################################

    
    ## >>>>>>>>>>   generate long signal : 
    # find 1st change Entry from day1: 0->1 and day2: reconfirmation 1->1 ; Exit 1->0

    df.loc [ ((df['signal_StackEMA'] == 1) & (df['signal_StackEMA'].shift(2) == 0) & (df['signal_StackEMA'].shift(1) == 1)) , 'signalxTrade_StackEMA'] = 1 
    df.loc [ ((df['signal_StackEMA'] == 0) & (df['signal_StackEMA'].shift(1) == 1) ) , 'signalxTrade_StackEMA'] = -1 
    # df.loc [ ((df['signal_StackEMA'] == 0) & (df['signal_StackEMA'].shift(2) == 1) & (df['signal_StackEMA'].shift(1) == 0)) , 'signal'] = -1 
    ## See results: 
    df[ (df['signalxTrade_StackEMA'] == 1) | (df['signalxTrade_StackEMA'] == -1)] [['signalxTrade_StackEMA', 'close']]
    
    
    # df['signal'] =   ((df['signal_StackEMA'] == 1) & (df['signal_StackEMA'].shift(2) == 0) & (df['signal_StackEMA'].shift(1) == 1)) # return on DF bool 


def algo(df) : 

    # Stack EMA Change 0-> 1, 1-> 0 
    # df.loc [ (df['signal_StackEMA'] == 1) & (df['signal_StackEMA'].shift(1) == 0) , 'signalx_StackEMA'] = 1 
    # df.loc [ (df['signal_StackEMA'] == 0) & (df['signal_StackEMA'].shift(1) == 1) , 'signalx_StackEMA'] = -1    


    # detect squeeze fired 
    df['redSQFire'] = ta.cross_value(df.SQZ_ON, 0.5, above=False, offset=0) # ZQZ  1-> 0 


    # detect mini squeeze 
    df['miniSQFire'] = ta.cross_value(df.squeeze_on.fillna(0), 0.5, above=False, offset=0) # ZQZ  1-> 0 


    # condition: SQ fired, StackEMA true and SQZ Mom increasing > 0 
    df['signalxTrade_SQTest'] = df['redSQFire'] * df['signal_StackEMA'].apply(lambda x: 1 if x ==1 else 0 )  * (df['SQZ_INC']>0).apply(lambda x:1 if x else 0) 


    # black sq opportunity red SQZ off and miniSQ fire ON
    df['signalx_yMiniSQ'] = df.SQZ_OFF * df['miniSQFire'] * df['signal_StackEMA'].apply(lambda x: 1 if x ==1 else 0 )  * (df['SQZ_INC']>0).apply(lambda x:1 if x else 0) 


    # simple All SQZ OFF and SQ momentum + StackEMA 
    df['signalx_SQMomo'] = df.SQZ_OFF * df.squeeze_off.fillna(0) * ta.cross_value(df.SQZ_INC, 0.0, above=True, offset=0) * df['signal_StackEMA'].apply(lambda x: 1 if x ==1 else 0 ) * df['signal_sSAR']  # also test * df['signal_sChandelier'] or df['signal_sSAR'] 
    # Note: chandelier is good for Exit; SAR good for entry 

    # Try SQ release + green Chandelier with Gray Stack EMA with exit on 8~10 bar SQMomo |  Pull back scenario 






##########################      TEST AND BUILD ALGO     ##########################
# # Use 'signalx for primary signals - hollow marker in panel 0 
# # Use 'signalxTrade for final  
#

symbol="WGO"  # TRY GE, 
interval='4H'
miniinterval ='1H'
microinterval = '5m'
df = None 
bars = None 
# bars=(-600, -300)
# bars=(-500, -350)
# bars=(-350, None)
bars=(-202, None )
# >>>>>>>>>>>>>>>
df = initData(symbol=symbol, interval=interval, live=False) # load/download data to df

addIndicators(df)

# >>>>>>>>>>>>>>>
# pandas_ta Utility (5)

#     Above: above
#     Above Value: above_value
#     Below: below
#     Below Value: below_value
#     Cross: cross

# algo(df)

# # Stack EMA Change 0-> 1, 1-> 0 
# df.loc [ (df['signal_StackEMA'] == 1) & (df['signal_StackEMA'].shift(1) == 0) , 'signalx_StackEMA'] = 1 
# df.loc [ (df['signal_StackEMA'] == 0) & (df['signal_StackEMA'].shift(1) == 1) , 'signalx_StackEMA'] = -1    


##########>>>>>>>>>>>       1 LOWER TIME FRAME CALCULATIONS and Resampling          <<<<<<<<<<<##########
df2 = initData(symbol=symbol, interval=miniinterval, live=False) # load/download data to df
addIndicators(df2)
# Stack EMA Change 0-> 1, 1-> 0 
df2.loc [ (df2['signal_StackEMA'] == 1) & (df2['signal_StackEMA'].shift(1) == 0) , 'signalx_StackEMA'] = 1 
df2.loc [ (df2['signal_StackEMA'] == 0) & (df2['signal_StackEMA'].shift(1) == 1) , 'signalx_StackEMA'] = -1    
# df['signalx_1HStackEMA'] = df2['signalx_StackEMA'] # this will not work - different index. use pd.concat axis=1
df2['miniSQFire'] = ta.cross_value(df2.squeeze_on.fillna(0), 0.5, above=False, offset=0) # ZQZ  1-> 0 
df2['confirm_SQZ_INC'] = (df2['SQZ_INC']).apply(lambda x: 0 if np.isnan(x) else 1)
# df2['confirm_SQZ_INC'] = df2['confirm_SQZ_INC'] * df2['confirm_SQZ_INC'].shift(1)  # confim if atleast 2 consecutive SQZ_INC values (green rising) 
df2['confirm_SQZ_INC'] = df2['confirm_SQZ_INC'] * df2['confirm_SQZ_INC'].shift(1) * df2['confirm_SQZ_INC'].shift(2) # confim if atleast 3 consecutive SQZ_INC values (green rising) 
df2['confirm_StackEMA'] = df2['signal_StackEMA'] * df2['signal_StackEMA'].shift(1) * df2['signal_StackEMA'].shift(2) # confim if atleast 3 consecutive SQZ_INC values (green rising) 
df2['signalx_yMiniSQ'] = df2['miniSQFire'] * df2['SQZ_OFF'] * df2['confirm_StackEMA'] * df2['confirm_SQZ_INC'] * (df2['SQZ_INC']>0).apply(lambda x:1 if x else 0) 
df2['redSQFire'] = ta.cross_value(df2.SQZ_ON, 0.5, above=False, offset=0) # ZQZ  1-> 0 
df2['signalxTrade_SQTest'] = df2['redSQFire'] * df2['squeeze_off'] * df2['signal_StackEMA'] * df2['confirm_SQZ_INC'] * (df2['SQZ_INC']>0).apply(lambda x:1 if x else 0)
aggregation = {
            'signalx_StackEMA'  :'max',
            'signalx_yMiniSQ'  :'max',
            'signalxTrade_SQTest' : 'max',
            # 'Low'   :'min',
            # 'Close' :'last',
            # 'Volume':'sum'
            }
dfr = df2.resample(interval).agg(aggregation)  # keep without  .dropna() # dropna caused problems (keep issue open for now)
# df['signalx_L1StackEMA'] = dfr['signalx_StackEMA']  # or do manually # stackEMA only signal (not confirmation)
df['signalx_L1yMiniSQ'] = dfr['signalx_yMiniSQ'] # or do manually 
df['signalx_L1xTradeSQTest'] = dfr['signalxTrade_SQTest'] # or do manually 

# dfr.columns = ['signalx_LStackEMA', 'signalx_yLMiniSQ'] # rename columns and then concat to main DF (higher timeframe)
# df = pd.concat([df,dfr], axis=1)
# df2[df2['signalx_yMiniSQ'] == 1]
# dfr[dfr['signalx_yLMiniSQ'] == 1 ]


# >>>>>>>>>>             Key learning b/w 4H and 1H  timeframe mix      (VERY IMPORTANT !!! )               <<<<<<<<
# after each blue arrow in 1H if SQ momentum in 4H (higher TF) > 0  = THERE WILL BE A CONFIRMED BREAKOUT
# if blue occurred in a SQ Squeeze in Higher TF. End of the SQ is entry and it will spike IFF Momntum did not go negaive in the Squeeze period
# Trend breaks when momentum becomes -ve 
# remember : blue should only be used in pairs with another blue or end of a squeeze with positive momo.
## TODO: need blue to blue tracking for entry : 1st signal is yellow if in SQZ - track momo till get SQZ over and +ve momo; break on -ve momo
## 

########## END


# detect squeeze fired 
df['signal_yRedSQFire'] = ta.cross_value(df.SQZ_ON, 0.5, above=False, offset=0) # ZQZ  1-> 0 
# detect mini squeeze fired 
df['miniSQFire'] = ta.cross_value(df.squeeze_on.fillna(0), 0.5, above=False, offset=0) # ZQZ  1-> 0 
# condition: SQ fired, StackEMA true and SQZ Mom increasing > 0 
df['confirm_SQZ_INC'] = (df['SQZ_INC']).apply(lambda x: 0 if np.isnan(x) else 1) # confirm atleast 2 positive mom tick 
df['confirm_SQZ_INC'] = df['confirm_SQZ_INC'] * df['confirm_SQZ_INC'].shift(1) * df['confirm_SQZ_INC'].shift(2) # confim if atleast 3 consecutive SQZ_INC values (green rising) 
df['signalxTrade_SQTest'] = df['signal_yRedSQFire'] * df['signal_StackEMA'] * (df['SQZ_INC']>0).apply(lambda x:1 if x else 0)
# black sq opportunity 
df['signalx_yMiniSQ'] = df['miniSQFire'] * df['signal_StackEMA'] * df['confirm_SQZ_INC'] # * (df['SQZ_INC']>0).apply(lambda x:1 if x else 0)
# simple SQ momentum + StackEMA 
df['signalxSQMomo'] = ta.cross_value(df.SQZ_INC, 0.0, above=True, offset=0) * df['signal_StackEMA']


## TODO : delayed squeeze fire and positive momentum 



if bars == None : bars=(-600, None)
# Plot it 
s,e = bars 

fig, axlist = plotAll (df, start= s, end= e, ctype='ohlc', ha=True, signal='signalxTrade_SQTest', symbol=symbol, interval=interval, header="\n"+ str(df[-1:].iloc[0].close))
# fig.show()
# df[['open', 'close']].tail(20)
# fig = plotAll (df, start= s, end= e, ctype='ohlc', ha=True, signal='signalxTrade_StackEMA', symbol=symbol, interval=interval)
# fig.show()


# ##->>>>>>>>>>>>>>>>>      Text annotate example 
# ax1 = axlist[0]
# style = dict(size=5, color='black')
# xpos = df[s:e].index.get_loc('2021-03-19 10:30', method='nearest') # find row # with the nearest index to x
# # df[s:e].index.get_loc('2021-03-19 10:30') # find nearest value of a slice 
# axlist[0].text(xpos, 40, "| 03/19", **style)
# fig.show()
