## jsonAPI.py
## This is a ohlc, indicator, trigger API to be consumed by JS, HTML in conjunction to trading view - lightweight charts library 

####    List of Tasks 
##################################################
#   basic API ->                ohlc, volume API 
#   squeeze API ->              1 histogram (color codes), 1 marker series (color codes)
#   marker signals ->           5+ marker series (color codes) 
#   signal ohlc markers ->      over below ohlc (primary, secondary, final)
#   multitimeframe 4H,1H, 1D    plots markers 
#   visual indicator charts -> 
#                   Type #1:    2 lines, 1 hist, 1 marker       ::  WaveTrend, MACD, VPCI
#                   Type #2:    3 lines, 1 marker               ::  Volatility, 
#                   Type #3:    2 lines, 2 hist, 3 marker       ::  Koncorde4.0, 
#                   Type #4:    4 lines, 1 marker               ::  SI+Bands (+Zones)
#   Filter timeframe API ->   


"""The Algo Test API.
Impl: 
1. pandas to HTML Table 
2. mplfinance img to web render 
"""

# pylint: disable=broad-except

from flask import Flask, abort, jsonify, request, send_file, make_response 
from flask import Blueprint, render_template
import datasource as data
import pandas as pd 
import json
from json import encoder

from computeIndicator import compute_all

pd.options.display.float_format = '{:,.2f}'.format

# from rq.job import Job
# from redis_resc import redis_conn, redis_queue

# from functions import some_long_function

app = Flask(__name__)

@app.route("/test")
def apiTest():
    """Show the app is working."""
    return "JSON API is Running!"

## initialize vars for global placeholders 
symbols = None
ddr1H = None
ddr1D = None
ddr5m = None
ddr4H = None


# def initializeGlobals (): 
# initialize globals / shared 
# ddr1H, symbols = data.loadDatatoMemory(interval='1H', filter=10)
ddr1H, symbols = data.loadDatatoMemory(interval='1H')
ddr1D, symbols = data.loadDatatoMemory(interval='1D')
ddr5m, symbols = data.loadDatatoMemory(interval='5m')
ddr4H, symbols = data.loadDatatoMemory(interval='4H')
# inDict = compute_all(ddr1H,symbols) # dict of indicators updated 



@app.route("/")
def index():
    """Show the app is working."""
    # mpfdf = 
    # mpfdf[['open', 'high', 'low','close']][-50:].to_json(orient='columns', double_precision=2, date_unit='s')
    return json.dumps({'symbols' : symbols})

@app.route("/ohlc/<string:symbol>/", methods=['GET', 'POST']) # '/<string:name>/')
def ohlcLast (symbol) : 
    # data = request.get_json()
    # print ( data)
    # symbol = data['symbol']
    mpfdf = ddr1H[symbol]
    output = mpfdf[['Open', 'High', 'Low','Close']][-1000:].to_json(orient='split', double_precision=2, date_unit='s')

    return output # jsonify(output) 

# this dict selects which variable to use 
finterval = {
    "1H"    : ddr1H,
    "1D"    : ddr1D,
    "4H"    : ddr4H,
    "5m"    : ddr5m,
}

@app.route("/ohlc/<string:symbol>/<string:interval>", methods=['GET', 'POST']) # '/<string:name>/')
def ohlcIntervalSelector (symbol, interval) : 
    # data = request.get_json()
    # print ( data)
    # symbol = data['symbol']
    dfdata = finterval.get(interval, None)[symbol] # select interval and symbol from dict
    output = dfdata[['Open', 'High', 'Low','Close']][-1500:].to_json(orient='split', double_precision=2, date_unit='s')

    return output # jsonify(output) 




#   squeeze API ->              1 histogram (color codes), 1 marker series (color codes)
#   marker signals ->           5+ marker series (color codes) 
#   signal ohlc markers ->      over below ohlc (primary, secondary, final)
#   multitimeframe 4H,1H, 1D    plots markers in multitimeframe 



#   Filter date API 
#   Filter signal API  


if __name__ == "__main__":
    # app.run(debug=True)
    # initializeGlobals()

    app.run(host="0.0.0.0", port=9502, debug=False)