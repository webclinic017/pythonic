import os, pandas
import plotly.graph_objects as go
import numpy as np
import yfinance as yf
from datetime import datetime, date, time, timedelta
import matplotlib.pyplot as plt 

# Ref: https://github.com/hackingthemarkets/ttm-squeeze


dataframes = {}

def squeeze (df) : 
    df['20sma'] = df['Close'].rolling(window=20).mean()
    df['stddev'] = df['Close'].rolling(window=20).std()
    df['lower_band'] = df['20sma'] - (2 * df['stddev'])
    df['upper_band'] = df['20sma'] + (2 * df['stddev'])

    df['TR'] = abs(df['High'] - df['Low'])
    df['ATR'] = df['TR'].rolling(window=20).mean()

    df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
    df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)

    def in_squeeze(df):
        return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

    df['squeeze_on'] = df.apply(in_squeeze, axis=1)

    if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
        print("{} is coming out the squeeze".format(symbol))

    # save all dataframes to a dictionary
    # we can chart individual names below by calling the chart() function
    # dataframes[symbol] = df
    return df

def chart(df):
    candlestick = go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])
    upper_band = go.Scatter(x=df.index, y=df['upper_band'], name='Upper Bollinger Band', line={'color': 'red'})
    lower_band = go.Scatter(x=df.index, y=df['lower_band'], name='Lower Bollinger Band', line={'color': 'red'})

    upper_keltner = go.Scatter(x=df.index, y=df['upper_keltner'], name='Upper Keltner Channel', line={'color': 'blue'})
    lower_keltner = go.Scatter(x=df.index, y=df['lower_keltner'], name='Lower Keltner Channel', line={'color': 'blue'})

    fig = go.Figure(data=[candlestick, upper_band, lower_band, upper_keltner, lower_keltner])
    fig.layout.xaxis.type = 'category'
    fig.layout.xaxis.rangeslider.visible = False
    fig.show()


symbol = 'AMD'
sd = datetime(2021, 1, 1)
ed = datetime(2021, 2, 26)

df = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="30m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="15m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="5m")
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="5m", prepost=True)
# df = yf.download(tickers=symbol, start=sd, end=ed, interval="15m", prepost=True)

cdf = squeeze(df)
chart(cdf)