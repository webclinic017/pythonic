import os
from datetime import date, datetime, time, timedelta

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf
from market_profile import MarketProfile
from matplotlib.widgets import Button

TICKDATA    = '/home/towshif/code/python/pythonic/database/data/'
ALGODATA    = '/home/towshif/code/python/pythonic/database/dataAlgo/'
RESULTS     = '/home/towshif/code/python/pythonic/database/dataResults/'
DATAROOT    = '/home/towshif/code/python/pythonic/database/' 
OLDDATA    = '/home/towshif/code/python/pythonic/database/olddata/' 



def create_Data_1H_twoyrs (symbols) : 
    for symbol in symbols : 

        flink = TICKDATA + symbol+'.1H.pickle'
        if not os.path.exists(flink) : 
            dfdata = yf.download(tickers=symbol, interval="60m", period="730d")
            if len(dfdata)>0  : # if successful download     
                pd.to_pickle(dfdata, flink)
                print ("Successful : ", symbol)
                # print (dfdata.head(10))
            else : 
                print (symbol, 'ERROR!')
                # exit loop 
        else : 
            print (symbol, 'already exists')

    ## direct download = p1d = yf.download(tickers=symbols, interval="5m", period="60d", group_by="Ticker")
    ## https://stackoverflow.com/questions/63107594/how-to-deal-with-multi-level-column-names-downloaded-with-yfinance
    
# create_Data_1H_twoyrs (symbols=['SPX', 'SPY', 'MU']) # test 


def create_Data_1D_twoyrs (symbols) : 
    for symbol in symbols : 

        flink = TICKDATA + symbol+'.1D.pickle'
        if not os.path.exists(flink) : 
            dfdata = yf.download(tickers=symbol, interval="60m", period="730d")
            if len(dfdata)>0  : # if successful download                
                pd.to_pickle(dfdata, flink)
                print ("Successful : ", symbol)
                # print (dfdata.head(10))
            else : 
                print (symbol, 'ERROR!')
                # exit loop 
        else : 
            print (symbol, 'already exists')

# create_Data_1D_twoyrs (symbols=['SPX', 'SPY', 'MU']) # test 


def initDBWatchList () : 
    symbols = ['SPY', 'VIX', 'SPXU', 'SPXS', 'JNUG', 'AAL', 'WGO', 'DAL', 'AAPL', 'AMAT', 'AMD', 'AMZN', 'BA', 'BAC', 'CLX', 'COST', 'DIS', 'FB', 'GOOG', 'INTC', 'IVV', 'KLAC', 'LRCX', 'MRNA', 'MSFT', 'MU', 'NFLX', 'NVDA', 'ONEQ', 'PTON', 'QQQ', 'SAIA', 'SBUX', 'SKX', 'SPCE', 'TSLA', 'UAL', 'URI', 'VDE', 'ZM', 'SPX', 'VIX', 'LPX', 'SNBR', 'UCTT', 'WSM', 'APPS', 'HZO', 'WAL', 'COWN', 'DHI', 'ARCB', 'UFPI', 'LGIH', 'AMAT', 'THI', 'ABG', 'CTB', 'KIRK', 'LAD', 'TFII', 'LOB', 'TPX', 'USAK', 'CENTA', 'LEN', 'LOW', 'SYNA', 'TBBK', 'WGO', 'CALX', 'GSL', 'KLIC', 'AVNW', 'HZNP', 'AMRK', 'BGFV', 'CCS', 'GROW', 'HIBB', 'IDT', 'KBH', 'MDC', 'MHO', 'SCVL', 'SLM', 'UNFI', 'ACLS', 'AOUT', 'GPI', 'HIMX', 'HTH', 'RCII', 'TRQ', 'CUBI', 'DAC', 'HVT', 'ICHR', 'MIK', 'ODFL', 'OMI', 'AGCO']

    df = pd.DataFrame(columns=['TICK', 'info' ])

    for symbol in symbols: 
        df=df.append({
            'TICK' : symbol        
        }, ignore_index=True)
    print (df)
    df.to_pickle(DATAROOT+'WatchListDB.pickle')

initDBWatchList() # just to initialize the watchlist 


def create_Data_from_Watchlist (watchlist):
    dfdata = pd.read_pickle(DATAROOT + watchlist +'.pickle') 
    symbols = dfdata['TICK'].tolist() 
    print (symbols)
    create_Data_1D_twoyrs (symbols)
    create_Data_1H_twoyrs (symbols)

create_Data_from_Watchlist('WatchListDB') # test


# dfdata = pd.read_pickle('h:/WorkSpace_Python/AppPy/rough/'+symbol+'.pickle')

# dfdata = dfdata.iloc[500:]
# print("Read pickle", symbol)

# dfdata['Date'] = dfdata.index
# dfdata['Date'] = dfdata['Date'].dt.tz_localize(None)
# dfdata.set_index('Date', inplace=True)


# def updater()  : 

# ############      DOWNLOAD YAHOO DATA     ############

# symbol = 'AMZN'
# sd = datetime(2020, 1, 1)  # sd = datetime(2019, 4, 1)
# ed = datetime(2021, 2, 28)
# dfdata = yf.download(tickers=symbol, start=sd, end=ed, interval="60m")
# # dfdata.to_pickle(symbol+'.pickle')
# # dfdata = pd.read_csv('h:/WorkSpace_Python/AppPy/rough/'+symbol+'.csv', index_col='Datetime', parse_dates=True)

# if os.name == 'nt': dfdata = pd.read_pickle('h:/WorkSpace_Python/pythonic/rough/'+symbol+'.pickle')
# else: dfdata = pd.read_pickle('/home/towshif/code/python/pythonic/rough/'+symbol+'.pickle')



def read_from_old () :  ## DO NOT WASTE TIME 

    # path to the old data 

    ### Transform 1h data 
    PATHDIR = '/home/towshif/code/python/thepythontrader/data/NASDAQ/60m/' ## add format:  AAP_60m.csv
    OLDDATA    = '/home/towshif/code/python/pythonic/database/olddata/' 
    content=os.listdir(PATHDIR)
    dataFiles=[]
    for i in content:
        if '.csv' in i:
            dataFiles.append(PATHDIR + i)
    len(dataFiles)
    priceData=[]
    notfound = []

    for filelink in dataFiles : 
        data= pd.read_csv(filelink, parse_dates=True, index_col='Date')
        symbol = data.iloc[1]['Name']
        data = data.drop([ 'Name'] ,axis=1)
        data['Adj Close'] = data.Close

        flink = OLDDATA + symbol+'.1H.pickle'
        if len(data)>0  : # if successful download                
            pd.to_pickle(data, flink)
            print ("Successful : ", symbol)
            # print (dfdata.head(10))
        else : 
            print (symbol, 'ERROR!')
            # exit loop 

    ### Transform 1d data 
    PATHDIR = '/home/towshif/code/python/thepythontrader/data/NASDAQ/1d/' ## add format:  AAP_60m.csv
    OLDDATA    = '/home/towshif/code/python/pythonic/database/olddata/' 
    content=os.listdir(PATHDIR)
    dataFiles=[]
    for i in content:
        if '.csv' in i:
            dataFiles.append(PATHDIR + i)
    len(dataFiles)
    priceData=[]
    notfound = []

    for filelink in dataFiles : 
        data= pd.read_csv(filelink, parse_dates=True, index_col='Date')
        symbol = data.iloc[1]['Name']
        data = data.drop([ 'Name'] ,axis=1)
        data['Adj Close'] = data.Close


        flink = OLDDATA + symbol+'.1D.pickle'
        if len(data)>0  : # if successful download                
            pd.to_pickle(data, flink)
            print ("Successful : ", symbol)
            # print (dfdata.head(10))
        else : 
            print (symbol, 'ERROR!')
            # exit loop 


    # for symbol in symbols: 
    #     flink = '/home/towshif/code/python/thepythontrader/data/NASDAQ/60m/' + symbol+'_60m.csv'
    #     # print (flink)

    #     if not os.path.exists(flink) :
    #         print (symbol, "Not Found")
    #         notfound.append(symbol)

    # print (len(notfound), notfound)
    # data= pd.read_csv(dataFiles[0], parse_dates=True, index_col='Date')
    # # data.rename(columns = {'Datetime':'Date'}, inplace = True)
    # # data = data.drop([ 'Dividends', 'Stock Splits', 'Name'] ,axis=1)
    # # data['Date']=data.index
    # # data['Date']= data['Date'].dt.tz_localize(None)
    # data.index




def initDBCoreWatchList () : 
    symbols = ['SPY', 'VIX', 'SPXU', 'SPXS', 'JNUG', 'AAL', 'WGO', 'DAL', 'AAPL', 'AMAT', 'AMD', 'AMZN', 'BA', 'BAC', 'CLX', 'COST', 'DIS', 'FB', 'GOOG', 'INTC', 'IVV', 'KLAC', 'LRCX', 'MRNA', 'MSFT', 'MU', 'NFLX', 'NVDA', 'ONEQ', 'PTON', 'QQQ', 'SAIA', 'SBUX', 'SKX', 'SPCE', 'TSLA', 'UAL', 'URI', 'VDE', 'ZM', 'SPX', 'VIX', 'LPX', 'SNBR', 'UCTT', 'WSM', 'APPS', 'HZO', 'WAL', 'COWN', 'DHI', 'ARCB', 'UFPI', 'LGIH', 'AMAT', 'THI', 'ABG', 'CTB', 'KIRK', 'LAD', 'TFII', 'LOB', 'TPX', 'USAK', 'CENTA', 'LEN', 'LOW', 'SYNA', 'TBBK', 'WGO', 'CALX', 'GSL', 'KLIC', 'AVNW', 'HZNP', 'AMRK', 'BGFV', 'CCS', 'GROW', 'HIBB', 'IDT', 'KBH', 'MDC', 'MHO', 'SCVL', 'SLM', 'UNFI', 'ACLS', 'AOUT', 'GPI', 'HIMX', 'HTH', 'RCII', 'TRQ', 'CUBI', 'DAC', 'HVT', 'ICHR', 'MIK', 'ODFL', 'OMI', 'AGCO', 
    '^DJI', '^NDX', '^GDAXI', '^FTSE', '^HSI', '^N225', '^NYA', '^SSEC', 
    'WGO', 'SAIA', 'MMM','ABT','ABBV','ACN','ATVI','AYI','ADBE','AMD','AAP','AES','AET',
    'AMG','AFL','A','APD','AKAM','ALK','ALB','ARE','ALXN','ALGN','ALLE',
    'AGN','ADS','LNT','ALL','GOOGL','GOOG','MO','AMZN','AEE','AAL','AEP',
    'AXP','AIG','AMT','AWK','AMP','ABC','AME','AMGN','APH','APC','ADI','ANDV',
    'ANSS','ANTM','AON','AOS','APA','AIV','AAPL','AMAT','APTV','ADM','ARNC',
    'AJG','AIZ','T','ADSK','ADP','AZO','AVB','AVY','BHGE','BLL','BAC','BK',
    'BAX','BBT','BDX','BRK.B','BBY','BIIB','BLK','HRB','BA','BWA','BXP','BSX',
    'BHF','BMY','AVGO','BF.B','CHRW','CA','COG','CDNS','CPB','COF','CAH','CBOE',
    'KMX','CCL','CAT','CBG','CBS','CELG','CNC','CNP','CTL','CERN','CF','SCHW',
    'CHTR','CHK','CVX','CMG','CB','CHD','CI','XEC','CINF','CTAS','CSCO','C','CFG',
    'CTXS','CLX','CME','CMS','KO','CTSH','CL','CMCSA','CMA','CAG','CXO','COP',
    'ED','STZ','COO','GLW','COST','COTY','CCI','CSRA','CSX','CMI','CVS','DHI',
    'DHR','DRI','DVA','DE','DAL','XRAY','DVN','DLR','DFS','DISCA','DISCK','DISH',
    'DG','DLTR','D','DOV','DWDP','DPS','DTE','DRE','DUK','DXC','ETFC','EMN','ETN',
    'EBAY','ECL','EIX','EW','EA','EMR','ETR','EVHC','EOG','EQT','EFX','EQIX','EQR',
    'ESS','EL','ES','RE','EXC','EXPE','EXPD','ESRX','EXR','XOM','FFIV','FB','FAST',
    'FRT','FDX','FIS','FITB','FE','FISV','FLIR','FLS','FLR','FMC','FL','F','FTV',
    'FBHS','BEN','FCX','GPS','GRMN','IT','GD','GE','GGP','GIS','GM','GPC','GILD',
    'GPN','GS','GT','GWW','HAL','HBI','HOG','HRS','HIG','HAS','HCA','HCP','HP','HSIC',
    'HSY','HES','HPE','HLT','HOLX','HD','HON','HRL','HST','HPQ','HUM','HBAN','HII',
    'IDXX','INFO','ITW','ILMN','IR','INTC','ICE','IBM','INCY','IP','IPG','IFF','INTU',
    'ISRG','IVZ','IQV','IRM','JEC','JBHT','SJM','JNJ','JCI','JPM','JNPR','KSU','K','KEY',
    'KMB','KIM','KMI','KLAC','KSS','KHC','KR','LB','LLL','LH','LRCX','LEG','LEN','LUK',
    'LLY','LNC','LKQ','LMT','L','LOW','LYB','MTB','MAC','M','MRO','MPC','MAR','MMC','MLM',
    'MAS','MA','MAT','MKC','MCD','MCK','MDT','MRK','MET','MTD','MGM','KORS','MCHP','MU',
    'MSFT','MAA','MHK','TAP','MDLZ','MON','MNST','MCO','MS','MOS','MSI','MYL','NDAQ',
    'NOV','NAVI','NTAP','NFLX','NWL','NFX','NEM','NWSA','NWS','NEE','NLSN','NKE','NI',
    'NBL','JWN','NSC','NTRS','NOC','NCLH','NRG','NUE','NVDA','ORLY','OXY','OMC','OKE',
    'ORCL','PCAR','PKG','PH','PDCO','PAYX','PYPL','PNR','PBCT','PEP','PKI','PRGO','PFE',
    'PCG','PM','PSX','PNW','PXD','PNC','RL','PPG','PPL','PX','PCLN','PFG','PG','PGR',
    'PLD','PRU','PEG','PSA','PHM','PVH','QRVO','PWR','QCOM','DGX','RRC','RJF','RTN','O',
    'RHT','REG','REGN','RF','RSG','RMD','RHI','ROK','COL','ROP','ROST','RCL','CRM','SBAC',
    'SCG','SLB','SNI','STX','SEE','SRE','SHW','SIG','SPG','SWKS','SLG','SNA','SO','LUV',
    'SPGI','SWK','SBUX','STT','SRCL','SYK','STI','SYMC','SYF','SNPS','SYY','TROW','TPR',
    'TGT','TEL','FTI','TXN','TXT','TMO','TIF','TWX','TJX','TMK','TSS','TSCO','TDG','TRV',
    'TRIP','FOXA','FOX','TSN','UDR','ULTA','USB','UAA','UA','UNP','UAL','UNH','UPS','URI',
    'UTX','UHS','UNM','VFC','VLO','VAR','VTR','VRSN','VRSK','VZ','VRTX','VIAB','V','VNO',
    'VMC','WMT','WBA','DIS','WM','WAT','WEC','WFC','HCN','WDC','WU','WRK','WY','WHR','WMB',
    'WLTW','WYN','WYNN','XEL','XRX','XLNX','XL','XYL','YUM','ZBH','ZION','ZTS',]

    df = pd.DataFrame(columns=['TICK', 'info' ])

    for symbol in symbols: 
        df=df.append({
            'TICK' : symbol        
        }, ignore_index=True)
    print (df)
    df.to_pickle(DATAROOT+'WatchListDBFull.pickle')
    create_Data_from_Watchlist('WatchListDBFull') # test
    
initDBCoreWatchList()
