#################       Signal to HTML Display test

# import computeIndicator as cp
from computeIndicator import * 
import datasource as data
import dfutils as dutil

# auto reload modules for notebook 
%load_ext autoreload
%autoreload 2

# Define some dicts
ddr = None; symbols = None;

ddr = {} # assign a dict 

# load all data to dict;
# read data from pickle first : dict {}
DATAROOT    = '/home/towshif/code/python/pythonic/database/'
flink = DATAROOT + 'dfdata4H.pickle' ; ddr['4H'] = pd.read_pickle(flink)
flink = DATAROOT + 'dfdata1H.pickle' ; ddr['1H'] = pd.read_pickle(flink)
flink = DATAROOT + 'dfdata1D.pickle' ; ddr['1D'] = pd.read_pickle(flink)
flink = DATAROOT + 'dfdata5m.pickle' ; ddr['5m'] = pd.read_pickle(flink)

#########################################################################
#####                   DATAFRAME MANIPULATION                      #####
#########################################################################

symbol      = 'AAL'
interval    = '1D'

# select a symbol from thr dict 
ddr[interval][symbol].columns
len(ddr[interval][symbol].columns)

# select a working DF 
dfdata = ddr[interval][symbol].copy() ; dfdata

### 
thisDate = '2021-08-11'

dfdata.loc[thisDate] # select / filter by index (datetime)
dfdata.loc[thisDate].index
dfdata.iloc[89]
# see : https://pandas.pydata.org/docs/reference/api/pandas.Index.get_loc.html
dfdata.index.get_loc(thisDate)
dfdata.index.get_slice_bound(thisDate, side='right') # this is right bound of the slice containing the label 'thisDate' 


locator = dfdata.index.get_slice_bound(thisDate, side='right')

dfdata.iloc[:locator] # start till locator inclusive 
dfdata.iloc[locator-7:locator] # 7 rows before locator inclusive 

# as a func 
rows = dfdata.loc[thisDate] ; rows
last = rows[-1:] ; last 


# select by index number 
dfdata.iloc[-8:] # last 8 rows 
dfdata.iloc[-8:-2] # last 8 to before last 2 rows 

from datetime import  datetime
datetime.strptime(thisDate, '%Y-%m-%d')






#########################################################################

# ##  Filter columns test 
# dutil.findColumns(dfAlgo, endswith='e') # filters with end condition 
# dutil.findColumns(dfdata, startswith='V') # filters with end condition 
# dutil.findColumns(dfAlgo, startswith='H', endswith='e') # filters with 2 condition 
# dutil.findColumns(dfAlgo, startswith='E', endswith='0') # filters with 2 condition EMAs



## Some console output formatting 
dutil.printInColor('COMPUTE COMPLETED. \nReady to fire')
dutil.printInColor('COMPUTE COMPLETED. \nReady to fire', color='magenta')
dutil.printInHighlight('ready to fire')



# Compute all Signals 
# Addr4H = compute_all(ddr=ddr4H.copy(), symbols=symbols, interval='4H')
# Addr1H = compute_all(ddr=ddr1H.copy(), symbols=symbols, interval='1H')
# Addr1D = compute_all(ddr=ddr1D.copy(), symbols=symbols, interval='1D')

