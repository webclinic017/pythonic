from datetime import datetime
from datetime import timedelta


import yfinance as yf
import pandas_ta as ta

#Importing market data
df = yf.download(tickers='AMZN',period = '150d', interval = '1d')
ema21 = df.ta.ema(length=21, append=True)
ema08 = df.ta.ema(length=8, append=True)
df['date']= df.index
df['bar'] = df.index

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Slider
from bokeh.io import output_notebook, show
from bokeh.resources import INLINE
from bokeh.models.widgets import Select
from bokeh.layouts import column
# from data_wrangling import get_df_from_table, add_bar_counter
# from db_connection import DBConnection

output_notebook(resources=INLINE)


# https://github.com/zvapa/candlestick-chart-with-slider

def get_display_range():
    """Set the range of bars to display, based on slider value and desired zoom level. Return (start, end)
    tuple of indices."""

    end = slider.value
    start = max(0, (end - bars_to_display))
    return start, end


# def fetch_data(name):
#     """Retrieve data from the db based on table name. Return a pandas dataframe."""

#     dataframe = get_df_from_table(name, conn)[['date', 'open', 'high', 'low', 'close']][:]
#     add_bar_counter(dataframe)
#     return dataframe


def update_source(df):
    """Update the data source to be displayed.
    This is called once when the plot initiates, and then every time the slider moves, or a different instrument is
    selected from the dropdown.
    """
    start, end = get_display_range()

    # create new view from dataframe
    df_view = df.iloc[start:end]

    # create new source
    new_source = df_view.to_dict(orient='list')

    # add colors to be used for plotting bull and bear candles
    # use 'white' and 'black' as needed 
    colors = ['lime' if cl >= op else 'red' for (cl, op)
              in zip(df_view.close, df_view.open)]
    new_source['colors'] = colors

    # source.data.update(new_source)
    source.data = new_source


def make_plot(src):
    """Draw the plot using the ColumnDataSource"""
    
    w = 12*60*60*1000 # width of candle # just use this 
    
    p = figure(x_axis_type="datetime", title=f"daily", plot_width=900, plot_height=400)
    p.segment('bar', 'high', 'bar', 'low', source=src, line_width=1, color='black')  # plot the wicks
    p.vbar('bar', w, 'close', 'open', source=src, line_color='black', fill_color='colors', )  # plot the body

    hover = HoverTool(tooltips=[
        ('bar', '@bar'),
        ('date', '@date{%F %T}'),
        ('open', '@open{0.0000f}'),
        ('high', '@high{0.0000f}'),
        ('low', '@low{0.0000f}'),
        ('close', '@close{0.0000f}')
    ],
        formatters={'date': 'datetime'})
    p.add_tools(hover)
    return p


def slider_handler(attr, old, new):
    """Handler function for the slider. Updates the ColumnDataSource to a new range given by the slider's position."""
    update_source(df)


# def dropdown_handler(attr, old, new):
#     global df
#     df = fetch_data(selector.value)
#     last_entry = df.shape[0]

#     # reset the slider (also calls the slider handler implicitly)
#     slider.value = slider.end = last_entry


# # connect to db
# dbc = DBConnection()
# conn = dbc.connection
# menu = [(n, n) for n in dbc.tables]

# # configure dropdown selector
# selector = Select(name="Select instrument..", options=menu, value='AAPL')
# selector.on_change('value', dropdown_handler)

# get data based on selection
# df = fetch_data(selector.value)

last_entry = df.shape[0]

# set the zoom level - how many bars to display (more bars = smaller candles)
bars_to_display = 50

# configure slider
slider = Slider(start=max(0, (last_entry - bars_to_display)), end=last_entry,
                value=last_entry, step=1, title="Bar", width=900)
slider.on_change('value', slider_handler)

# initialize the data source
source = ColumnDataSource()
update_source(df)

# draw the plot
plot = make_plot(source)

curdoc().add_root(
    column(
        # selector,
        plot,
        slider
    ))

# show(plot)

######################### RUM APP 
#       bokeh serve --show CandlePlotter_Brokeh_03.py


# Simulate websocket
