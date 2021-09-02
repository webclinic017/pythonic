from datetime import datetime
from os import error
# import module
import traceback
from PyInquirer import prompt
# from examples import custom_style_1, custom_style_2
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.styles import Style


## STYLES NOT WORKING with PyInquirer style_from_dict AS DESIGNED IN PYTHON 3 
# from PyInquirer import style_from_dict
custom_style_1 = Style.from_dict({
    "separator": '#cc5454',
    "questionmark": '#673ab7 bold',
    "selected": '#cc5454',  # default
    "pointer": '#673ab7 bold',
    "instruction": '',  # default
   "answer": '#f44336 bold',
    "question": '',
})

custom_style_2 = Style.from_dict({
    "separator": '#6C6C6C',
    "questionmark": '#FF9D00 bold',
    "selected": '#5F819D', # '#cc5454',
    "pointer": '#FF9D00 bold',
    "instruction": '',  # default
    "answer": '#5F819D bold',
    "question": '',
})

custom_style_3 = Style.from_dict({
    "questionmark": '#E91E63 bold',
    "selected": '#673AB7 bold',
    "instruction": '',  # default
    "answer": '#2196f3 bold',
    "question": '',
})

########### END STYLES



# Some placeholders
# Define some dicts
ddr = None; symbols = None;

class NumberValidator(Validator):

    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a number",
                                  cursor_position=len(document.text))

class StringValidator(Validator):

    def validate(self, document):
        try:
            sym = str(document.text)
            if (not sym) or (not sym.isalpha()): ## if string is empty
                raise ValidationError(message="Please enter a Symbol",
                                cursor_position=len(document.text))
        except ValueError:
            raise ValidationError(message="Please enter a Symbol",
                                  cursor_position=len(document.text))
class DateValidator(Validator):

    def validate(self, document):
        try:
            sym = datetime.strptime(str(document.text), '%Y-%m-%d')
        except ValueError:
            raise ValidationError(message="Incorrect data format, should be YYYY-MM-DD",
                                  cursor_position=len(document.text))

mainMenuChoice = [
    {
        'type': 'list',
        'name': 'user_option',
        'message': '---------------  Welcome to Pythonic Data Viewer  ---------------',
        'choices': [
            "Tail Data",
            "Head Data",
            "Symbols",
            "Browse Data",
            "Clear",
            "Stats Validate",
            "Validate All Data",
            "Consolidate/Update",
            "Data Update",
            "quit"
        ]
    },
]

inputs = {
        'type': "input",
        "name": "integer",
        "message": "Enter step size (number)",
        "validate": NumberValidator,
        "filter": lambda val: int(val)
}

confirmations = {
        'type': 'confirm',
        'message': 'Do you want to exit?[default Enter]',
        'name': 'exit',
        'default': True,
}

inputSymbol= {
        'type': "input",
        "name": "symbol",
        "message": "Enter symbol name : ",
        "validate": StringValidator,
        "filter": lambda val: str(val).upper()
    }
inputSymbolDefault= {
        'type': "input",
        "name": "symbol",
        "message": "Enter symbol name : ",
        "default": "SPY",
        "validate": StringValidator,
        "filter": lambda val: str(val).upper()
}

inputDate =  {
        'type': "input",
        "name": "date",
        "message": "Enter Date format:'2021-05-02' : ",
        "validate": DateValidator,
        "filter": lambda val: str(val).upper()
    }


def scrollArray (orderlist = None) : 
    # https://github.com/CITGuru/PyInquirer/issues/69
    if orderlist is None: 
        return ["Prev", "Next", "Last","Market Profile", "Date", "Symbol", "Interval", "Step", "Clear", "Back"]
    else: 
        return orderlist; 


selectNext = {
        'type': 'list',
        'name': 'user_option',
        'message': '',
        'choices': scrollArray() # dynamic list update 
}

selectInterval = {
        'type': 'list',
        'name': 'user_option',
        'message': '#####      SELECT INTERVAL    ####',
        'choices': ["1H", "4H", "1D", "5m"]
    },


def getTwoInputs():
    answers = prompt.prompt(inputs, style=custom_style_1)
    a = answers.get("a")
    b = answers.get("b")
    return a, b

def getSymbolInputs():
    answers = prompt.prompt(inputSymbol, style=custom_style_1)
    return answers.get("symbol")

def validateData() :
    import pandas as pd
    from datetime import date
    import app_web.logically.datasource as data
    # import datasource as data
    import os.path, time

    ## following define # entries per day
    cinterval = {
        "1D"    : 1,
        "1d"    : 1,
        "1h"    : 7,
        "1H"    : 7,
        "4H"    : 2,
        "4h"    : 2,
        "5m"    : 78,
    }

    # Define some dicts
    global ddr, symbols

    ### check for data consistency
    # watchlist = data.getWatchlist('WatchListLive.pickle') # defaults to default watchlist
    # symbolslist = symbols # watchlist.TICK.to_list()
    # len(symbolslist)

    print ("\n*************     DATA HEALTH ANALYSIS        ****************")

    for interval in  ['1D', '1H', '5m', '4H'] :
        outlierlist = []
        for symbol in symbols : #[:-2]:
            dfdata = ddr[interval][symbol].dropna() # read from global dict 
            # dfdata = data.getDataFromPickle(symbol=symbol, interval=interval) # read from pickle 

            outlierData = data.dataConsistencyCheck(dfdata, interval, verbose=False).loc[str(date.today().year):]
            if len(outlierData) >0 : outlierlist.append((symbol,outlierData.iloc[-1].Open, outlierData.iloc[-1:].index[0].strftime("%m/%d/%y")))
            # print (outlierData)

        print ("\n#############")
        print (f"{interval} Analysis ::::  Found {len(outlierlist)} outliers")
        print ("Expected count/day = ", cinterval.get(interval, None)) # expected count

        print (outlierlist)

def statsValidate(symbol = None) :

    import pandas as pd
    from datetime import date
    import app_web.logically.datasource as data
    # import datasource as data
    import sys, os.path, time

    if symbol is None:
        print ("Please reenter valid Symbol name.")
        return

    ## following define # entries per day
    cinterval = {
        "1D"    : 1,
        "1d"    : 1,
        "1h"    : 7,
        "1H"    : 7,
        "4H"    : 2,
        "4h"    : 2,
        "5m"    : 78,
    }


    ### check for data consistency
    #watchlist = data.getWatchlist('WatchListLive.pickle') # defaults to default watchlist
    #symbolslist = watchlist.TICK.to_list()
    # len(symbolslist)

    print ("\n*************     DATA HEALTH ANALYSIS        ****************")

    for interval in  ['1D', '1H', '5m'] :
        print ("\n#############")
        print (f"{interval} Analysis ::	{symbol}")
        # print ("Expected count/day = ", cinterval.get(interval, None)) # expected count

        dfdata = ddr[interval][symbol] # read from global dict 
        # data.getDataFromPickle(symbol=symbol, interval=interval) # read
        if dfdata is None : exit(0)

        outlierData = data.dataConsistencyCheck(dfdata, interval, verbose=True).loc[str(date.today().year):]

        if len(outlierData) >0 :
            print ("Current Year: ", len(outlierData))

def getHeadTail(symbol=None, tail=True) :
    import pandas as pd
    import app_web.logically.datasource as data
    import os.path, time
    import sys

    if symbol is None:
        print ("Please reenter valid Symbol name.")
        return

    if tail: print (f"************** TAIL {symbol} **************")
    else: print (f"************** HEAD {symbol} **************")

    print ("Timeframe : 1D")
    if tail: d = ddr['1D'][symbol].tail(3)
    else : d = ddr['1D'][symbol].head(3)
    c1D = d.iloc[-1].Close
    print (d)

    print ("Timeframe : 4H")
    if tail: d = ddr['4H'][symbol].tail(6)
    else : d = ddr['4H'][symbol].head(6)
    c4H = d.iloc[-1].Close
    print (d)

    print ("Timeframe : 1H")
    if tail: d = ddr['1H'][symbol].tail(9)
    else : d = ddr['1H'][symbol].head(9)
    c1H = d.iloc[-1].Close
    print (d)

    print ("Timeframe : 5m")
    if tail: d = ddr['5m'][symbol].tail(5)
    else : d = ddr['5m'][symbol].head(5)
    c5m = d.iloc[-1].Close
    print (d)

    print ("**** Comparing Close Data ****")
    print (f'Close [\n1D : {c1D}\n4H : {c4H}\n1H : {c1H}\n5m : {c5m}]')

    # print ("**** Last Modified date ****")
    fname = "/home/towshif/code/python/pythonic/database/data/SPY.1H.pickle"
    print("Last modified: %s" % time.ctime(os.path.getmtime(fname)))
    # print("Created: %s" % time.ctime(os.path.getctime(fname)))
    print ()


## terminal graohing function using `termgraph` lib
def terminalBarChart (labels, values, **kwargs):
    """ Requires pip install termgraph 
        labels, values for barchart 
    """
    from termgraph.termgraph import chart

    args = {
        "stacked": False,
        "width": 50,
        "no_labels": False,
        "format": "{:<5.2f}",
        "suffix": "",
        "vertical": False,
        "histogram": False,
        "no_values": False,
    }
    args.update(kwargs)
    data = [[x] for x in values]
    chart(colors=[], data=data, args=args, labels=labels)


def plot_terminal(profile_labels, profile_prices) :
    """pip install termplotlib
    """
    import termplotlib as tpl
    
    ## barchart
    fig = tpl.figure()
    
    # fig.barh([3, 10, 5, 2], ["Cats", "Dogs", "Cows", "Geese"], force_ascii=False)
    fig.barh(profile_prices, profile_labels, force_ascii=False)    
    fig.show()

    # ## v histogram 
    # fig = tpl.figure()
    # # fig.hist(counts, bin_edges, orientation="horizontal", force_ascii=False)
    # fig.hist(profile_prices, profile_labels, orientation="horizontal", force_ascii=False)
    # fig.show()


def generateMarketProfile (dfdata=None, last=100 , nbins=20, rowPointer=None) : 
    """ dfdata = datafram containing yfinance DFs 
        last : -last rows from rowPointer
        nbins: number of price buckets / bins of histogram 
        rowPounter: points to last row number from which `-last` will be counter; 
    """
    from market_profile import MarketProfile
    import pandas as pd
    from datetime import datetime, timedelta
    
    # nbins = 20          # only 20 bins 

    ## filter data based on criteria - days, ticks etc 
    df3 = None 
    if not rowPointer: 
        df3 = dfdata[-last:] # last 700 tick 
    else: 
        df3 = dfdata.iloc[rowPointer-last :rowPointer]

    # iloc[locator-pacer:locator]     
    # df3 = dfdata[-100:] 

    #############   CODE FOR MARKET PROFILE GENERATION      #########

    # find max and min for price range for chart/histogram 
    mx = df3[["Open", "Close"]].max().max()
    mi = df3[["Open", "Close"]].min().max()

    # What should be tickSize for a default nbin = 20 
    tick_size = (mx-mi)/nbins

    print (f"mx:{mx} mi:{mi}, tick_ize:{tick_size}") # debug 
    
    # tick_size = 10 #  round(2.0*(df3['Open'][0]/100))/10

    #### Generate market profile object 
    mp = MarketProfile(df3, tick_size=tick_size, open_range_size=pd.to_timedelta('10 minutes'), initial_balance_delta=pd.to_timedelta('60 minutes'), mode='vol')
    mp_slice = mp[0:len(df3.index)]

    # valArea = mp_slice.value_area
    val=mp_slice.value_area[0]
    vah=mp_slice.value_area[1]
    poc=mp_slice.poc_price
    data = mp_slice.profile
    volNodes = mp_slice.high_value_nodes

    ###############     Done market profile gen #############################

    print (f"Length {last}, Range[] , date [{df3.index[0]}, {df3.index[-1]}]")
    print (f"POC: {poc}")
    # \n Value Nodes {volNodes}")
    # print (f'Profile: {data}')

    ###############     CHARTING HISTOGRAM / BAR chart ##############

    # generate bin-labels and counts
    plabels = list(data.index)[::-1]
    profile_prices = [str(round(x,2)) for x in plabels]
    profile_nodes = list(data.values)[::-1]
    # print (profile_prices)
    # print (profile_nodes)

    ### Chart `tprint` func
    terminalBarChart(labels=profile_prices, values=profile_nodes, format="{:<5.0f}")
    print (f"Last: {df3.index[-1]}")
    
    ##############  END CHARTING  ####################


    # from termgraph import Data, BarChart, Args, Colors
    # data = Data(data=[[765, 787], [781, 769]], labels=["6th G", "7th G"], categories=["Boys", "Girls"])
    # chart = BarChart(data, Args(title="Total Marks Per Class", colors=[Colors.Red, Colors.Magenta], space_between=True))
    # chart.draw()

    # # plot_terminal (np.array(plabels), np.array(profile_nodes))
    # import numpy as np 
    # plot_terminal (profile_prices, np.array(profile_nodes))
    
    
    # print (data)
    # data.plot(kind='barh', width=1.0, zorder=2)

    # mp = MarketProfile(dfdata[-700:])
    # mp_slice = mp[0:-1]
    # mp_slice.profile.plot(kind='barh', width=1.0, zorder=2)

    return 


def updateData () : 
    import sys
    sys.path.append('./app_web/logically') # use to append lib path

    import app_web.logically.EODUpdater as eod
    
    print ("Updating data")
    return 
    

def consolidateData():
    import pandas as pd
    from datetime import date
    import app_web.logically.datasource as data

    DATAROOT    = '/home/towshif/code/python/pythonic/database/'

    # Define some dicts
    global ddr, symbols
    ddr = {} # assign a dict 

    # load all data to dict;
    ddr['4H'], symbols = data.loadDatatoMemoryOptimize(interval='4H') # 3-5MB
    ddr['1H'], _ = data.loadDatatoMemoryOptimize(interval='1H') # 12-20MB
    ddr['1D'], _ = data.loadDatatoMemoryOptimize(interval='1D') # 12-20MB
    ddr['5m'], _ = data.loadDatatoMemoryOptimize(interval='5m') # 3-10MB

    flink = DATAROOT + 'dfdata4H.pickle'
    pd.to_pickle(ddr['4H'], flink)

    flink = DATAROOT + 'dfdata1H.pickle'
    pd.to_pickle(ddr['1H'], flink)

    flink = DATAROOT + 'dfdata1D.pickle'
    pd.to_pickle(ddr['1D'], flink)

    flink = DATAROOT + 'dfdata5m.pickle'
    pd.to_pickle(ddr['5m'], flink)

def readData() :
    import pandas as pd
    from datetime import date, datetime
    import app_web.logically.datasource as data
    import os

    # Define some dicts
    global ddr, symbols
    ddr = {} # assign a dict 

    # read data from pickle first : dict {}
    DATAROOT    = '/home/towshif/code/python/pythonic/database/'
    flink = DATAROOT + 'dfdata4H.pickle'

    if not os.path.exists(flink) : consolidateData() # update the pickles

    ddr['4H'] = pd.read_pickle(flink)

    flink = DATAROOT + 'dfdata1H.pickle'
    ddr['1H'] = pd.read_pickle(flink)

    flink = DATAROOT + 'dfdata1D.pickle'
    ddr['1D'] = pd.read_pickle(flink)

    flink = DATAROOT + 'dfdata5m.pickle'
    ddr['5m'] = pd.read_pickle(flink)

    symbols = list(ddr['1D'].keys()) # all the symbols
    print ("Reading data from pickles")


def browseSymbols () :
    print (symbols)
    print ("# Symbols 1D:", len(list(ddr['1D'].keys())))
    print ("# Symbols 1H:", len(list(ddr['1H'].keys())))
    print ("# Symbols 5m:", len(list(ddr['5m'].keys())))
    print ("# Symbols 4H:", len(list(ddr['4H'].keys())))


def browseData () :

    # get symbol
    symbol = prompt.prompt(inputSymbolDefault, style=custom_style_1).get("symbol") #default SPY
    interval = prompt.prompt(selectInterval, style=custom_style_1).get("user_option")
    confirm = confirmations.copy()
    confirm['message'] = "Disable profile charts (default YES)]"
    answer = prompt.prompt(confirm, style=custom_style_1)
    mkpf = not answer.get("exit")
    print ("MKPF = ", mkpf )
    
    # get date starting
    dfdata = ddr[interval][symbol] # selected dataframe 

    # searchdate = prompt.prompt(inputDate, style=custom_style_1).get("date")

    # print (dfdata.loc[searchdate])


    # while loop to Next(-->) (Default), Prev (<--), Back [X]
    # add selectable prev date next date or 

    locator = len(dfdata)-1
    
    searchdate = "2021-08-11"
    # try : 
    #     # this will return right bound of the slice
    #     locator = dfdata.index.get_slice_bound(searchdate, side='right')
    # except: 
    #     # this will return array (get_loc); use last element
    #     locator = dfdata.index.get_loc(searchdate, method='nearest')[-1]
    #     pass

    sinterval = {"1D": 45,"1H": 210,"4H": 90,"5m":  2340} # short interval 30 days 
    linterval = {"1D": 130,"1H": 780,"4H": 260,"5m":  10140} # long interval 6 months
    pinterval = {"1D": 130,"1H": 780,"4H": 260,"5m":  10140} # pacer length

    pacer = 7  # default 
    
    # print df default first 
    print(chr(27) + "[2J") # clear screen in python3 

    # default print 
    try: 
        print (dfdata.iloc[locator-pacer:locator])
        last = sinterval[interval]
        if mkpf: generateMarketProfile(dfdata, last=last, rowPointer=locator)
        print(symbol, interval, 'range:', last)
    except: pass
    
    while True:

        try: 
            searchdate = dfdata.index[locator].strftime('%Y-%m-%d') # update date at locator 
        except:
            traceback.print_exc()
            pass

        # sub-menu selection 
        myscroll = prompt.prompt(selectNext, style=custom_style_2)

        if myscroll.get("user_option") == "Next":
            try: 
                locator = locator+pacer # need locator update 

                if mkpf: print(chr(27) + "[2J") # clear screen in python3 

                print(symbol, interval, 'step:', pacer)
                print (dfdata.iloc[locator-pacer:locator])
                # last = 100 
                last = sinterval[interval]
                if mkpf: generateMarketProfile(dfdata, last=last, rowPointer=locator)
                print(symbol, interval, 'range:', last)


            except:
                traceback.print_exc()
                pass
   
            selectNext["choices"] = ["Next", "Prev", "Last","Market Profile", "Date", "Symbol", "Interval", "Step", "Clear", "Back"]
            # scrollArray(["Next", "Prev", "Date", "Back"])

        elif  myscroll.get("user_option") == "Prev":
            try: 
                locator = locator-pacer # need locator after 

                if mkpf: print(chr(27) + "[2J") # clear screen in python3 

                print(symbol, interval, 'step:', pacer, '(reverse sorted)')
                print (dfdata.iloc[locator-pacer:locator][::-1])
                # last = 100 
                last = sinterval[interval]
                if mkpf: generateMarketProfile(dfdata, last=last, rowPointer=locator)
                print(symbol, interval, 'range:', last)

            except:
                traceback.print_exc()
                pass
            
            selectNext["choices"] = ["Prev", "Next", "Last","Market Profile", "Date", "Symbol", "Interval", "Step", "Clear", "Back"]
        
        elif  myscroll.get("user_option") == "Last":
            try: 
                print(symbol, interval, 'step:', pacer)                
                locator = len(dfdata)-1
                print (dfdata.iloc[locator-pacer:locator])
                # last = 100 
                last = sinterval[interval]
                if mkpf: generateMarketProfile(dfdata, last=last, rowPointer=locator)
                print(symbol, interval, 'range:', last)
            except : pass

        elif  myscroll.get("user_option") == "Date":
            try: 
                print(symbol, interval, 'step:', pacer)
                searchdate = prompt.prompt(inputDate, style=custom_style_1).get("date")
                locator = dfdata.index.get_slice_bound(searchdate, side='right')
                print (dfdata.iloc[locator-pacer:locator])
                last = sinterval[interval]
                if mkpf: generateMarketProfile(dfdata, last=last, rowPointer=locator)
                print(symbol, interval, 'range:', last)

            except : pass

        elif  myscroll.get("user_option") == "Symbol":
            try: 
                symbol = prompt.prompt(inputSymbol, style=custom_style_1).get("symbol")
                dfdata = ddr[interval][symbol] # selected dataframe 
                print (f"Searching date {searchdate} ")
                locator = dfdata.index.get_slice_bound(searchdate, side='right')
                print (dfdata.iloc[locator-pacer:locator])
                last = sinterval[interval]
                if mkpf: generateMarketProfile(dfdata, last=last, rowPointer=locator)
                print(symbol, interval, 'range:', last)

            except : pass

        elif  myscroll.get("user_option") == "Interval":
            try: 
                interval = prompt.prompt(selectInterval, style=custom_style_1).get("user_option")
                dfdata = ddr[interval][symbol] # selected dataframe 
                locator = dfdata.index.get_slice_bound(searchdate, side='right')
                print (dfdata.iloc[locator-pacer:locator])
                last = sinterval[interval]
                if mkpf: generateMarketProfile(dfdata, last=last, rowPointer=locator)
                print(symbol, interval, 'range:', last)

            except : pass

        elif  myscroll.get("user_option") == "Step":
            try: 
                pacer = prompt.prompt(inputs, style=custom_style_1).get("integer")
                print (dfdata.iloc[locator-pacer:locator])
                
            except : pass

        elif  myscroll.get("user_option") == "Market Profile":
            try: 
                last = linterval[interval]
                generateMarketProfile(dfdata, last=last, rowPointer=locator)
                print(symbol, interval, 'range:', last)
                # generateMarketProfile(dfdata, last=100)
                # print (dfdata.iloc[locator-pacer:locator])

            except: 
                traceback.print_exc()
                pass
        elif  myscroll.get("user_option") == "Clear":
            print(chr(27) + "[2J") # clear screen in python3 
             

        elif  myscroll.get("user_option") == "Back":
            break
    
    # dfdata = ddr['5m']['AMD']
    # dfdata.index[-1].strftime('%Y-%m-%d')

    return


def main():
    # Consolidate and update pickle
    readData() ## read all the dict to memory

    while True:
        answers = prompt.prompt(mainMenuChoice, style=custom_style_2)

        if answers.get("user_option") == "quit":
            answers = prompt.prompt(confirmations, style=custom_style_1)
            if answers.get("exit") :
                break

        elif answers.get("user_option") == "Validate All Data":
            try : validateData()
            except: pass

        elif answers.get("user_option") == "Consolidate/Update":
            try : consolidateData()
            except: pass
        elif answers.get("user_option") == "Data Update":
            try : updateData()
            except: 
                traceback.print_exc()
                pass

        elif answers.get("user_option") == "Symbols":
            try :
                browseSymbols()
                # consolidateData()
            except: pass

        elif answers.get("user_option") == "Clear":
            try :
                print(chr(27) + "[2J") # in python3 
                # https://stackoverflow.com/questions/2084508/clear-terminal-in-python                
            except: pass

        elif answers.get("user_option") == "Browse Data":
            # symbol = getSymbolInputs()
            try: browseData()
            except: pass

        elif answers.get("user_option") == "Tail Data":
            symbol = prompt.prompt(inputSymbolDefault, style=custom_style_1).get("symbol")
            try: getHeadTail(symbol=symbol, tail=True)
            except: pass

        elif answers.get("user_option") == "Head Data":
            symbol = prompt.prompt(inputSymbolDefault, style=custom_style_1).get("symbol")
            try: getHeadTail(symbol=symbol, tail=False)
            except: pass

        elif answers.get("user_option") == "Stats Validate":
            symbol = prompt.prompt(inputSymbolDefault, style=custom_style_1).get("symbol")
            try: statsValidate(symbol=symbol)
            except: pass

        elif answers.get("user_option") == "quit":
            break

    print("Quitting Now. Bye.")


if __name__ == "__main__":
    main()

