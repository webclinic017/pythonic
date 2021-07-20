#################       Signal to HTML Display test

# import computeIndicator as cp
from computeIndicator import * 
import datasource as data
import dfutils as dutil

# auto reload modules for notebook 
%load_ext autoreload
%autoreload 2


# define placeholders 
ddr4H  = {}
Addr4H = {}
ddr1H  = {}
Addr1H = {}
ddr1D  = {}
Addr1D = {}

# load data 
ddr4H, symbols = data.loadDatatoMemory(interval='4H', filter=10, randomize=False)
ddr1H, _ = data.loadDatatoMemory(interval='1H', filter=10, randomize=False)
ddr1D, _ = data.loadDatatoMemory(interval='1D', filter=10, randomize=False)

# Compute all Signals 
Addr4H = compute_all(ddr=ddr4H.copy(), symbols=symbols, interval='4H')
Addr1H = compute_all(ddr=ddr1H.copy(), symbols=symbols, interval='1H')
Addr1D = compute_all(ddr=ddr1D.copy(), symbols=symbols, interval='1D')

# display all computed columns 
Addr4H['AMD'].columns
ddr4H['AMD'].columns

len(Addr4H['AMD'].columns)
len(ddr4H['AMD'].columns)

# select a working DF 

dfdata = ddr4H['AMD'].copy() ; dfdata
dfAlgo = Addr4H['AMD'].copy() ; dfAlgo


# endQ()
processQ.empty()
endCompute() # quit the multiprocessing thread ## run multiple times to exit all 

# manual initialize pool of 20 process CPU threads 
# initialize_processPool(20)
# endCompute()


dfdata.columns
dfdata.shape
dfAlgo.columns
dfAlgo.shape

# now we have both algo DF = dfAlgo and ohlc df = dfdata 
dutil.findColumns(dfAlgo,startswith='SQZ')
dutil.showColumns(dfAlgo,startswith='SQZ')

# recompute indicators 
dfAlgo, _, _ = compute_indicatorsA(df=dfdata.copy(),symbol=..., interval=...)

# reduce DF memory footprint # if you dont make copy will impact original DF 
dfAlgo2 = dutil.reduce_mem_usage(dfAlgo); dfAlgo2  ## reduce memory dfAlgo
dfdata2 = dutil.reduce_mem_usage(dfdata); dfdata2  ## reduce memory dfdata

#################   NOW WE ARE READY TO PLAY WITH SIGNAL AND ALGOS ###############


# dfAlgo, _, _ = compute_indicatorsA(df=dfdata.copy(),symbol=..., interval=...)

dutil.showColumns(dfAlgo,startswith='SQZ')
dutil.showColumns(dfAlgo,startswith='squee') # squeeze: manual BB,KC calc 
dfAlgo.columns

Addr4H.keys()

dfdata = ddr4H['AMD'].copy() ; dfdata
dfAlgo = Addr4H['SPY'].copy() ; dfAlgo

dfAlgo, _, _ = compute_indicatorsA(df=dfdata.copy(),symbol=..., interval=..., verbose=True)

dutil.showColumns(dfAlgo,startswith='SQZ').tail(50)
r = dutil.showColumns(dfAlgo,startswith='SQZ').tail(50) # original SQZ (TOS)


### Work: reorganize Squeese 
r['SQZ_INC'].notnull()
np.where(r['SQZ_PINC'].notnull(), 1, np.nan)
r['SQZC'] = np.where(r['SQZ_PINC'].notnull(), 2, r['SQZC'])
r['SQZC'] = np.where(r['SQZ_PDEC'].notnull(), 1, r['SQZC'])
r['SQZC'] = np.where(r['SQZ_NDEC'].notnull(), -1, r['SQZC'])
r['SQZC'] = np.where(r['SQZ_NINC'].notnull(), -2, r['SQZC'])
dutil.showColumns(r,startswith='SQZ').tail(50) # original SQZ (TOS)

dfAlgo.columns # check cols is changes are updated 


####### ####### #######    Convert to JSON string for post 

symbol = 'AAL'
dfAlgo = Addr4H[symbol].copy() ; dfAlgo
# payload = 
dfAlgo[['open', 'high', 'low','close', 'EMA_21', 'SQZ', 'SQZ_Hist', 'SQZ_HistC']][-1000:].to_json(orient='split', double_precision=2, date_unit='s')

clip = dfAlgo[['open', 'high', 'low','close','HA_open','HA_high','HA_low','HA_close', 'EMA_21', 'EMA_42', 'SQZ', 'SQZ_Hist', 'SQZ_HistC']][-1000:].to_json(orient='split', double_precision=2, date_unit='s')
# write this to file 
with open('frontend/static/data.json', 'w', encoding='utf-8') as f :
    f.write(clip) 
    f.close()

# MTF2 SQZ data (Lower TF) 
dfAlgo2 = Addr1H[symbol].copy() ; dfAlgo2[-2000:]
clip = dfAlgo2[['HA_open','HA_high','HA_low','HA_close', 'EMA_21', 'SQZ', 'SQZ_Hist', 'SQZ_HistC']][-2000:].to_json(orient='split', double_precision=2, date_unit='s')

# write this to file 
with open('frontend/static/data1H.json', 'w', encoding='utf-8') as f :
    f.write(clip) 
    f.close()

# MTF2 SQZ data (higher TF)
dfAlgo3 = Addr1D[symbol].copy() ; dfAlgo3[-2000:]
clip = dfAlgo3[['HA_open','HA_high','HA_low','HA_close', 'EMA_21', 'SQZ', 'SQZ_Hist', 'SQZ_HistC']][-500:].to_json(orient='split', double_precision=2, date_unit='s')

# write this to file 
with open('frontend/static/data1D.json', 'w', encoding='utf-8') as f :
    f.write(clip) 
    f.close()

####### ####### #######    END


# Socket Test with Image Update 
import base64
import requests, io
from flask_socketio import emit, SocketIO

socketio = SocketIO(message_queue='redis://localhost:6379/')
# Exmaple 1 
socketio.emit('chartdata', {payload})



























######################      Execution Time Comparison  #################
#                         Sequential vs Multiprocessing  

# time a sequential execution function 
ddr4H, symbols = data.loadDatatoMemory(interval='4H', filter=50, randomize=True)
print (ddr4H.keys())
print (len(ddr4H)) # length 10 instruments 

### time the multiprocessing function 
initialize_processPool(4)
p = compute_all(ddr=ddr4H.copy(), symbols=..., interval=...) # 7s/25 stock ->run 4 times 
endQ()

### time the sequential function 
p = compute_all_seq(ddr=ddr4H.copy(), symbols=..., verbose=True) # manual time calc  # run 3 times

# %timeit compute_all_seq (ddr=ddr4H.copy(), symbols=...)  ## 17s/25 stock

# %timeit compute_all(ddr=ddr4H.copy(), symbols=..., interval=...)


########################################################################







##  Filter columns test 
dutil.findColumns(dfAlgo, endswith='e') # filters with end condition 
dutil.findColumns(dfdata, startswith='V') # filters with end condition 
dutil.findColumns(dfAlgo, startswith='H', endswith='e') # filters with 2 condition 
dutil.findColumns(dfAlgo, startswith='E', endswith='0') # filters with 2 condition EMAs



## Some console output formatting 
dutil.printInColor('COMPUTE COMPLETED. \nReady to fire')
dutil.printInHighlight('ready to fire')



# Socket Test with Image Update 
import base64
import requests, io
from flask_socketio import emit, SocketIO

socketio = SocketIO(message_queue='redis://localhost:6379/')

myurl = "https://image.shutterstock.com/image-vector/picture-icon-image-photo-260nw-1672289161.jpg"

myurl = "https://s0.2mdn.net/9684689/cs2203r0001_005_548363_us_bb_cm_cm_fy22q2_sit_precision-fixed-family_300x250_ccf.jpg"


response = requests.get(myurl)
image_bytes = io.BytesIO(response.content)

base64_img = base64.b64encode(image_bytes.getbuffer()).decode("ascii")

# Exmaple 1 
socketio.emit('chartupdate', {'chart':"data:image/png;base64,"+ base64_img, 'tick': "New Image"})




