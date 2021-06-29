"""The Algo Test API.
Impl: 
1. pandas to HTML Table 
2. mplfinance img to web render 
"""

# pylint: disable=broad-except

from flask import Flask, abort, jsonify, request, send_file, make_response 
import logically.datasource2 as data
import logically.algo1 as algo1
import pandas as pd 

pd.options.display.float_format = '{:,.2f}'.format

# from rq.job import Job
# from redis_resc import redis_conn, redis_queue

# from functions import some_long_function

app = Flask(__name__)

@app.route("/")
def home():
    """Show the app is working."""
    return "Running!"

@app.route("/data")
def getTICK():
    symbol = request.args.get('symbol')
    # print ("got Sym", symbol)
    p = data.getData(symbol, bars=(-300,None))
    # print (p)
    
    """Show the app is working."""
    return symbol + "</br>" +  p.sort_index(axis=0, ascending=False).to_html(); 

@app.route("/live")
def getLiveTICK():
    symbol = request.args.get('symbol')
    print ("Got Sym", symbol)
    p = None
    if symbol == "" : symbol = None
    if 'symbol' in request.args and symbol is not None:       
        p = data.getLiveData(symbol, bars=(-50,None), period="10d")
    else : 
        p = data.getLiveData(bars=(-50,None))
        symbol = 'SPY'
    print (p) # test print df 
    
    """Show the app is working."""
    if p is None:
        return "NOT FOUND" 
    else : 
        return symbol + "</br>" +  p.sort_index(axis=0, ascending=False).to_html()

#########################  PLOTTING API TESTS ########################

@app.route("/showplot")
def plotfig():
    p = None
    nbar = None
    symbol = request.args.get('symbol')
    interval = request.args.get('interval')
    nbar= request.args.get('bars')
    print ("Got Sym", symbol)
    
    if symbol == "" : symbol = None
    if 'symbol' not in request.args and symbol == None: 
        symbol = 'SPY'
    if 'interval' not in request.args and interval == None: 
        interval = '4H'
    if 'bars' not in request.args and nbar== None: 
        nbar= 50
    nbar = -1*int(nbar)
    # Generate the figure from Algo return 
    fig = algo1.AlgoImage(symbol=symbol, interval=interval, bars=(nbar, None), full= True if -nbar>200 else False)

    # Save it to a temporary buffer.
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, pad_inches= 0, transparent=True)
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
    
    # # Canvas approach 
    # canvas = FigureCanvas(fig)
    # output = io.BytesIO()
    # canvas.print_png(output)
    # response = make_response(output.getvalue())
    # response.mimetype = 'image/png'
    # return response



@app.route("/showplot2")
def plotfig2():
    p = None
    nbars = None
    nbare = None
    symbol = request.args.get('symbol')
    interval = request.args.get('interval')
    nbars= request.args.get('bars')
    nbare= request.args.get('bare')
    print ("Got Sym", symbol)
    
    if symbol == "" : symbol = None
    if 'symbol' not in request.args and symbol == None: 
        symbol = 'SPY'
    if 'interval' not in request.args and interval == None: 
        interval = '4H'
    if 'bars' not in request.args and nbars== None: 
        nbars= 50
    if 'bare' not in request.args and nbare== None: 
        nbare= 50
    nbar = int(nbare)- int(nbars)
    if nbar < 0 : return "ERROR; Period Close is before Beginning"
    nbars = int(nbars)
    nbare = int(nbare)
    
    # Generate the figure from Algo return 
    fig = algo1.AlgoImage(symbol=symbol, interval=interval, bars=(nbars, nbare), full= True if nbar>200 else False, live=False)

    # Save it to a temporary buffer.
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, pad_inches= 0, transparent=True)
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
    
    # # Canvas approach 
    # canvas = FigureCanvas(fig)
    # output = io.BytesIO()
    # canvas.print_png(output)
    # response = make_response(output.getvalue())
    # response.mimetype = 'image/png'
    # return response





#########################  PLOTTING API TESTS #########################

import random
import io
import matplotlib.pyplot as plt

@app.route('/plottest')
def plotTest1():
    # fig = Figure()
    f, axis = plt.subplots(figsize=(11, 9))

    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]

    axis.plot(xs, ys)
    
    # here is the trick save your figure into a bytes object and you can afterwards expose it via flas
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return send_file(bytes_image, 
            attachment_filename='plot.png',
            mimetype='image/png')

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

@app.route('/canvastest')
def plotTest2():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


import base64

@app.route("/matplot")
def hello():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"




# Ref to this library for Python Web API Plotting 
# >>>>>>>>>>>>>>>>>          http://www.pygal.org/en/stable/
# >>>>>>>>>>>>>>>>>          https://github.com/zvapa/candlestick-chart-with-slider
# https://towardsdatascience.com/visualizing-stock-trading-agents-using-matplotlib-and-gym-584c992bc6d4




# if __name__ == "__main__":
#     # app.run(debug=True)
app.run(host="0.0.0.0", port=9500, debug=True)