from datetime import datetime
from datetime import timedelta


import yfinance as yf
import pandas_ta as ta

#Importing market data
df = yf.download(tickers='AMZN',period = '150d', interval = '1d')

from math import pi
from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.resources import INLINE

output_notebook(resources=INLINE)
df_ = df[-50:-1].copy()

inc = df_.Close > df_.Open
dec = df_.Open > df_.Close

w = 12*60*60*1000
p = figure(x_axis_type="datetime", plot_width=800, plot_height=500, title = "Apple Inc stock price - 2020")

p.segment(df_.index, df_.High, df_.index, df_.Low, color="black")
p.vbar(df_.index[inc], w, df_.Open[inc], df_.Close[inc], fill_color="lime", line_color="black")
p.vbar(df_.index[dec], w, df_.Open[dec], df_.Close[dec], fill_color="red", line_color="black")

show(p)