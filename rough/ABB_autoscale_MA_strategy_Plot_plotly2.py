# Raw Package
import numpy as np
import pandas as pd
#df Source
import yfinance as yf
#df viz
import plotly.graph_objs as go

#Importing market df
# df = yf.download(tickers='SPY',period = '150d', interval = '1d')
df = yf.download(tickers='SPY',period = '21d', interval = '60m')

#Adding Moving average calculated field
df['MA5'] = df['Close'].rolling(9).mean()
df['MA20'] = df['Close'].rolling(21).mean()

#declare figure
# fig = go.Figure()
fig = go.FigureWidget()

#Candlestick
fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'], 
                name = 'market data'),)

#Add Moving average on the graph
fig.add_trace(go.Scatter(x=df.index, y= df['MA20'],line=dict(color='blue', width=1.5), name = 'Long Term MA'))
fig.add_trace(go.Scatter(x=df.index, y= df['MA5'],line=dict(color='orange', width=1.5), name = 'Short Term MA'))

#Updating X axis and graph
# X-Axes
fig.update_xaxes(   
    # showticklabels=True,
    showspikes=True, spikemode='across', spikesnap='cursor', spikethickness=1,  
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
        dict(pattern='hour', bounds=[16, 9]) # hide after hours use 60m candles for best output 
    ]
)

# Y-Axes 
fig.update_yaxes(
    showspikes=True, spikemode='across', spikesnap='cursor', showline=True, spikethickness=1, 
    # showticklabels=True,
)

# layout update 
# fig.update_layout(hoverdistance=1000, hovermode='closest') # hovermode='x unified')
# fig.update_layout(hoverdistance=0, hovermode='x unified')

fig.update_layout(
    # xaxis_zeroline=False, 
    # yaxis_zeroline=False,
    yaxis=dict(
        # tickfont=dict(size=14, color='#e6e6e6'),
        tickfont=dict(size=14, color='black'),
        #         title='Quote',
        #         titlefont_size=16,
        # gridcolor='#283442',
        # linecolor='#283442',
        # spikecolor="white", 
        spikethickness=1, spikemode='across',
        spikesnap='cursor'
    ),
    spikedistance=-1,
#     hoverdistance=0,
    hovermode='y',
    font=dict(
        color='black',
        size=15
    ),
    
    # paper_bgcolor='rgb(17,17,17)',
    # plot_bgcolor='rgb(17,17,17)',
)

fig.update_traces(hoverinfo="y",)

### Add Auto Scale functionality to candle stick charts 
def zoom(layout, xrange):
    in_view = df.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
    yrange = (in_view.High.max() - in_view.Low.min())
    fig.layout.yaxis.range = [in_view.Low.min() - 0.05*yrange, in_view.High.max() + 0.05*yrange]

fig.layout.on_change(zoom, 'xaxis.range')

#Show
# fig.show()
fig


## import everything 
#
# df = yf.download(tickers='AMZN',period = '150d', interval = '1d')
# 
# from plotly.subplots import make_subplots
# fig = make_subplots(rows=2, cols=1, row_heights=[0.8, 0.2], vertical_spacing=0)

# fig.add_trace(go.Candlestick(open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
#                              increasing_line_color='#0384fc', decreasing_line_color='#e8482c', name='UN'), row=1, col=1)

# fig.add_trace(go.Scatter(y=np.random.randint(20, 40, len(df)), marker_color='#fae823', name='VO', hovertemplate=[]), row=2, col=1)

# fig.update_layout({'plot_bgcolor': "#21201f", 'paper_bgcolor': "#21201f", 'legend_orientation': "h"},
#                   legend=dict(y=1, x=0),
#                   font=dict(color='#dedddc'), dragmode='pan', hovermode='x unified',
#                   margin=dict(b=20, t=0, l=0, r=40))

# fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False,
#                  showspikes=True, spikemode='across', spikesnap='cursor', showline=False, spikedash='solid')

# fig.update_xaxes(showgrid=False, zeroline=False, rangeslider_visible=False, showticklabels=False,
#                  showspikes=True, spikemode='across', spikesnap='cursor', showline=False, spikedash='solid')

# fig.update_layout(hoverdistance=0)

# fig.update_traces(xaxis='x', hoverinfo='none')
# fig.show()