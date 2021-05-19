import plotly.graph_objs as go 

from datetime import datetime

#Data Source
import yfinance as yf

df = yf.download(tickers='AMZN',period = '20d', interval = '60m')


# Make sure dates are in ascending order
# We need this for slicing in the callback below
df.sort_index(ascending=True, inplace=True)

trace = go.Scatter(x=list(df.index),
                   y=list(df.High))

data = [trace]
layout = dict(
    title='Time series with range slider and selectors',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                    label='YTD',
                    step='year',
                    stepmode='todate'),
                dict(count=1,
                    label='1y',
                    step='year',
                    stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(
            visible = True
        ),
        type='date'
    )
)

fig = go.FigureWidget(data=data, layout=layout)

def zoom(layout, xrange):
    in_view = df.loc[fig.layout.xaxis.range[0]:fig.layout.xaxis.range[1]]
    fig.layout.yaxis.range = [in_view.High.min() - 10, in_view.High.max() + 10]

fig.layout.on_change(zoom, 'xaxis.range')

fig
