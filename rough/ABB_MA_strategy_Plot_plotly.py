# Raw Package
import numpy as np
import pandas as pd
#Data Source
import yfinance as yf
#Data viz
import plotly.graph_objs as go

#Importing market data
data = yf.download(tickers='AMZN',period = '150d', interval = '1d')

#Adding Moving average calculated field
data['MA5'] = data['Close'].rolling(5).mean()
data['MA20'] = data['Close'].rolling(20).mean()

#declare figure
# fig = go.Figure()
fig = go.FigureWidget()

#Candlestick
fig.add_trace(go.Candlestick(x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'], 
                name = 'market data'))

#Add Moving average on the graph
fig.add_trace(go.Scatter(x=data.index, y= data['MA20'],line=dict(color='blue', width=1.5), name = 'Long Term MA'))
fig.add_trace(go.Scatter(x=data.index, y= data['MA5'],line=dict(color='orange', width=1.5), name = 'Short Term MA'))

#Updating X axis and graph
# X-Axes
fig.update_xaxes(
    rangeslider_visible=True,    
    rangeselector=dict(
        buttons=list([
            dict(count=5, label="3d", step="day", stepmode="backward"),
            dict(count=10, label="5d", step="day", stepmode="backward"),
            dict(count=7, label="WTD", step="day", stepmode="todate"),
            dict(step="all")
        ])
    ), 
    rangebreaks=[
        dict(bounds=["sat", "mon"]), #hide weekends
    ]
)

# Y-Axes 
fig.update_yaxes()



def zoom(layout, xrange):
    in_view = data.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
    yrange = (in_view.High.max() - in_view.Low.min())
    fig.layout.yaxis.range = [in_view.Low.min() - 0.05*yrange, in_view.High.max() + 0.05*yrange]

fig.layout.on_change(zoom, 'xaxis.range')

#Show
# fig.show()
fig