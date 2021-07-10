#   dfutil.py 
#   LIST of Useful functions for Dataframe operations   

import numpy as np
import pandas as pd
import pandas_ta as ta
from time import sleep

def findColumns (df, startswith=None, endswith=None) :
    """ Returns a list of columns with name starting or ending with args text
        Either, OR, Both conditions are valid 
    """
    if startswith is None and endswith is None: 
        print ( "Argument Error")
        return  None 
    if endswith is None:
        return [col for col in df if col.startswith(startswith)]
    if startswith is None:
        return [col for col in df if col.endswith(endswith)]
    if startswith is not None and endswith is not None:
        return [col for col in df if col.startswith(startswith) and col.endswith(endswith)] # filter by both 

def showColumns (df, startswith=None, endswith=None) :
    """ Returns a list of columns with name starting or ending with args text
        Either, OR, Both conditions are valid 
    """
    if startswith is None and endswith is None: 
        print ( "Argument Error")
        return  None 
    if endswith is None:
        cols = [col for col in df if col.startswith(startswith)]
        return df[cols]
    if startswith is None:
        cols = [col for col in df if col.endswith(endswith)]
        return df[cols]
    if startswith is not None and endswith is not None:
        cols = [col for col in df if col.startswith(startswith) and col.endswith(endswith)] # filter by both 
        return df[cols]



def printInColor(mytext="Hello Test!") : 
    # https://pypi.org/project/termcolor/
    # text: grey,red,green,yellow,blue,magenta,cyan,white
    # Attributes: bold,dark,underline,blink,reverse,concealed
    # highlight: on_grey,on_red,on_green,on_yellow,on_blue,on_magenta,on_cyan,on_white,    

    import sys
    from termcolor import colored, cprint

    # text = colored(mytext, 'green', attrs=['reverse', 'blink'])
    text = colored(mytext, 'green', attrs=['bold'])
    print(text)
    # cprint(mytext, 'blue', 'on_yellow')



def printWarning(mytext="Hello Test!") : 
    # https://pypi.org/project/termcolor/
    # text: grey,red,green,yellow,blue,magenta,cyan,white
    # Attributes: bold,dark,underline,blink,reverse,concealed
    # highlight: on_grey,on_red,on_green,on_yellow,on_blue,on_magenta,on_cyan,on_white,    

    import sys
    from termcolor import colored, cprint

    # text = colored(mytext, 'green', attrs=['reverse', 'blink'])
    text = colored(mytext, 'red', attrs=['bold'])
    print(text)
    # cprint(mytext, 'blue', 'on_yellow')


def printInHighlight(mytext="Hello Test!") : 
    # https://pypi.org/project/termcolor/
    # text: grey,red,green,yellow,blue,magenta,cyan,white
    # Attributes: bold,dark,underline,blink,reverse,concealed
    # highlight: on_grey,on_red,on_green,on_yellow,on_blue,on_magenta,on_cyan,on_white,    

    import sys
    from termcolor import colored, cprint

    # text = colored(mytext, 'red', attrs=['reverse', 'blink'])
    # print(text)
    cprint(mytext, 'green', 'on_yellow')


# https://www.mikulskibartosz.name/how-to-reduce-memory-usage-in-pandas/
# 70% compression with smaller datatypes

def reduce_mem_usage(df, verbose=True):
    start_mem = df.memory_usage().sum() / 1024**2
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024**2

    if verbose: # print compression results 
        print('Memory usage after optimization is: {:.2f} MB'.format(end_mem))
        print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
        
    return df