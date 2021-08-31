from os import error
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
            sym = str(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a Symbol",
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
            "quit"
        ]
    },
]

inputs = [
    {
        'type': "input",
        "name": "symbol",
        "message": "Enter the symbol name:",
        "validate": StringValidator,
        "filter": lambda val: str(val).upper()
    },

    {
        'type': "input",
        "name": "b",
        "message": "Enter the second number",
        "validate": NumberValidator,
        "filter": lambda val: str(val).upper()
    }
]

confirmations = [
    {
        'type': 'confirm',
        'message': 'Do you want to exit?[default Enter]',
        'name': 'exit',
        'default': True,
    },
]

inputText= {
        'type': "input",
        "name": "symbol",
        "message": "Enter symbol name : ",
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

selectNext = {
        'type': 'list',
        'name': 'user_option',
        'message': '#####      Welcome to Pythonic Data Viewer     ####',
        'choices': ["Next", "Prev", "Date", "Back"]
}


selectInterval = {
        'type': 'list',
        'name': 'user_option',
        'message': '#####      Welcome to Pythonic Data Viewer     ####',
        'choices': ["1D", "1H", "4H", "5m"]
    },


def getTwoInputs():
    answers = prompt.prompt(inputs, style=custom_style_1)
    a = answers.get("a")
    b = answers.get("b")
    return a, b

def getSymbolInputs():
    answers = prompt.prompt(inputText, style=custom_style_1)
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
    from datetime import date
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
    symbol = prompt.prompt(inputText, style=custom_style_1).get("symbol")
    interval = prompt.prompt(selectInterval, style=custom_style_1).get("user_option")
    # get date starting
    dfdata = ddr[interval][symbol] # selected dataframe 

    searchdate = prompt.prompt(inputDate, style=custom_style_1).get("date")

    print (dfdata.loc[searchdate])

    # while loop to Next(-->) (Default), Prev (<--), Back [X]
    # add selectable prev date next date or 

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
            symbol = getSymbolInputs()
            try: getHeadTail(symbol=symbol, tail=True)
            except: pass

        elif answers.get("user_option") == "Head Data":
            symbol = getSymbolInputs()
            try: getHeadTail(symbol=symbol, tail=False)
            except: pass

        elif answers.get("user_option") == "Stats Validate":
            symbol = getSymbolInputs()
            try: statsValidate(symbol=symbol)
            except: pass

        elif answers.get("user_option") == "quit":
            break

    print("Quitting Now. Bye.")


if __name__ == "__main__":
    main()

