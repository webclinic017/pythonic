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


    ## direct download = p1d = yf.download(tickers=symbols, interval="5m", period="60d", group_by="Ticker")
    ## https://stackoverflow.com/questions/63107594/how-to-deal-with-multi-level-column-names-downloaded-with-yfinance


def create_Data_1H_twoyrs (symbols) : 
    for symbol in symbols : 

        flink = TICKDATA + symbol+'.1H.pickle'
        if not os.path.exists(flink) : 
            dfdata = yf.download(tickers=symbol, interval="60m", period="730d")
            if len(dfdata)>0  : # if successful download     

                # Timezone/ daylight saving fix 
                dfdata['Datetime'] = dfdata.index
                dfdata['Datetime'] = dfdata['Datetime'].dt.tz_localize(None)
                dfdata.set_index('Datetime', inplace=True)  
                
                pd.to_pickle(dfdata, flink)
                print ("Successful : ", symbol)
                # print (dfdata.head(10))
            else : 
                print (symbol, 'ERROR!')
                # exit loop 
        else : 
            print (symbol, 'already exists')
    print (notfound)
    
# create_Data_1H_twoyrs (symbols=['SPX', 'SPY', 'MU']) # test 
# create_Data_1H_twoyrs (['MRNA']) # manual download 

def create_Data_1D_twoyrs (symbols) : 

    notfound = []
    for symbol in symbols : 

        flink = TICKDATA + symbol+'.1D.pickle'
        if not os.path.exists(flink) : 
            dfdata = yf.download(tickers=symbol, interval="1D", period="5000d")

            if len(dfdata)>0  : # if successful download   
                # Timezone/ daylight saving fix 
                dfdata['Datetime'] = dfdata.index
                dfdata['Datetime'] = dfdata['Datetime'].dt.tz_localize(None)
                dfdata.set_index('Datetime', inplace=True)  

                pd.to_pickle(dfdata, flink)
                print ("Successful : ", symbol)
                # print (dfdata.head(10))
            else : 
                print (symbol, 'ERROR!')
                notfound.append(symbol)

                # exit loop 
        else : 
            print (symbol, 'already exists')
    print (notfound)

# create_Data_1D_twoyrs (symbols=['SPX', 'SPY', 'MU']) # test 


def create_Data_5m_60days (symbols) : 

    notfound = []
    for symbol in symbols : 

        flink = TICKDATA + symbol+'.5m.pickle'
        if not os.path.exists(flink) : 
            dfdata = yf.download(tickers=symbol, interval="5m", period="60d")
            if len(dfdata)>0  : # if successful download    
                 # Timezone/ daylight saving fix 
                dfdata['Datetime'] = dfdata.index
                dfdata['Datetime'] = dfdata['Datetime'].dt.tz_localize(None)
                dfdata.set_index('Datetime', inplace=True)   
                pd.to_pickle(dfdata, flink)
                print ("Successful : ", symbol)
                # print (dfdata.head(10))
            else : 
                print (symbol, 'ERROR!')
                notfound.append(symbol)
                # exit loop 
        else : 
            print (symbol, 'already exists')
    print (notfound)



def initDBWatchList () : 
    symbols = ['SPY', 'SPXU', 'SPXS', 'JNUG', 'AAL', 'WGO', 'DAL', 'AAPL', 'AMAT', 'AMD', 'AMZN', 'BA', 'BAC', 'CLX', 'COST', 'DIS', 'FB', 'GOOG', 'INTC', 'IVV', 'KLAC', 'LRCX', 'MRNA', 'MSFT', 'MU', 'NFLX', 'NVDA', 'ONEQ', 'PTON', 'QQQ', 'SAIA', 'SBUX', 'SKX', 'SPCE', 'TSLA', 'UAL', 'URI', 'VDE', 'ZM', 'LPX', 'SNBR', 'UCTT', 'WSM', 'APPS', 'HZO', 'WAL', 'COWN', 'DHI', 'ARCB', 'UFPI', 'LGIH', 'AMAT', 'THI', 'ABG', 'CTB', 'KIRK', 'LAD', 'TFII', 'LOB', 'TPX', 'USAK', 'CENTA', 'LEN', 'LOW', 'SYNA', 'TBBK', 'WGO', 'CALX', 'GSL', 'KLIC', 'AVNW', 'HZNP', 'AMRK', 'BGFV', 'CCS', 'GROW', 'HIBB', 'IDT', 'KBH', 'MDC', 'MHO', 'SCVL', 'SLM', 'UNFI', 'ACLS', 'AOUT', 'GPI', 'HIMX', 'HTH', 'RCII', 'TRQ', 'CUBI', 'DAC', 'HVT', 'ICHR', 'MIK', 'ODFL', 'OMI', 'AGCO', '^GSPC', '^NDX', '^DJI', '^VIX', ]

    df = pd.DataFrame(columns=['TICK', 'info' ])

    for symbol in symbols: 
        df=df.append({
            'TICK' : symbol        
        }, ignore_index=True)
    print (df)
    df.to_pickle(DATAROOT+'WatchListDB.pickle')

# initDBWatchList() # just to initialize the watchlist 


def create_Data_from_Watchlist (watchlist):
    dfdata = pd.read_pickle(DATAROOT + watchlist +'.pickle') 
    symbols = dfdata['TICK'].tolist() 
    print (symbols)
    create_Data_1D_twoyrs (symbols)
    # create_Data_1H_twoyrs (symbols)
    # create_Data_5m_60days (symbols)



def fix_timezone (watchlist) : 
    # Timezone/ daylight saving fix 
    dfdata = pd.read_pickle(DATAROOT + watchlist +'.pickle') 
    symbols = dfdata['TICK'].tolist() 
    notfound = []

    for tf in ['.5m', '.1H', '.1D'] : 
        for symbol in symbols : 
            flink = TICKDATA + symbol+ tf + '.pickle'
            if os.path.exists(flink) : 
                dfdata = pd.read_pickle(flink)
                dfdata['Datetime'] = dfdata.index
                dfdata['Datetime'] = dfdata['Datetime'].dt.tz_localize(None)
                dfdata.set_index('Datetime', inplace=True)

                if len(dfdata)>0  : # if successful download     
                    pd.to_pickle(dfdata, flink)
                    print ("Successful : ", symbol)
                    # print (dfdata.head(10))
                # else :                     
                    # exit loop 
            else :                 
                print (symbol, 'ERROR!')
                notfound.append(symbol)
    print (notfound)

# fix_timezone('WatchListDB')
# fix_timezone('WatchListDBFull')



# create_Data_from_Watchlist('WatchListDB') # test


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
    symbols = ['SPY', 'SPXU', 'SPXS', 'JNUG', 'AAL', 'WGO', 'DAL', 'AAPL', 'AMAT', 'AMD', 'AMZN', 'BA', 'BAC', 'CLX', 'COST', 'DIS', 'FB', 'GOOG', 'INTC', 'IVV', 'KLAC', 'LRCX', 'MRNA', 'MSFT', 'MU', 'NFLX', 'NVDA', 'ONEQ', 'PTON', 'QQQ', 'SAIA', 'SBUX', 'SKX', 'SPCE', 'TSLA', 'UAL', 'URI', 'VDE', 'ZM', 'LPX', 'SNBR', 'UCTT', 'WSM', 'APPS', 'HZO', 'WAL', 'COWN', 'DHI', 'ARCB', 'UFPI', 'LGIH', 'THI', 'ABG', 'CTB', 'KIRK', 'LAD', 'TFII', 'LOB', 'TPX', 'USAK', 'CENTA', 'LEN', 'LOW', 'SYNA', 'TBBK', 'CALX', 'GSL', 'KLIC', 'AVNW', 'HZNP', 'AMRK', 'BGFV', 'CCS', 'GROW', 'HIBB', 'IDT', 'KBH', 'MDC', 'MHO', 'SCVL', 'SLM', 'UNFI', 'ACLS', 'AOUT', 'GPI', 'HIMX', 'HTH', 'RCII', 'TRQ', 'CUBI', 'DAC', 'HVT', 'ICHR', 'MIK', 'ODFL', 'OMI', 'AGCO', '^GSPC', '^NDX', '^GDAXI', '^FTSE', '^HSI', '^N225', '^NYA', 'MMM', 'ABT', 'ABBV', 'ACN', 'ATVI', 'AYI', 'ADBE', 'AAP', 'AES', 'AMG', 'AFL', 'A', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALXN', 'ALGN', 'ALLE', 'ADS', 'LNT', 'ALL', 'GOOGL', 'MO', 'AEE', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'ANTM', 'AON', 'AOS', 'APA', 'AIV', 'APTV', 'ADM', 'ARNC', 'AJG', 'AIZ', 'T', 'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'BLL', 'BK', 'BAX', 'BDX', 'BBY', 'BIIB', 'BLK', 'HRB', 'BWA', 'BXP', 'BSX', 'BHF', 'BMY', 'AVGO', 'CHRW', 'COG', 'CDNS', 'CPB', 'COF', 'CAH', 'CBOE', 'KMX', 'CCL', 'CAT', 'CNC', 'CNP', 'CERN', 'CF', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CTXS', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'COP', 'ED', 'STZ', 'COO', 'GLW', 'COTY', 'CCI', 'CSX', 'CMI', 'CVS', 'DHR', 'DRI', 'DVA', 'DE', 'XRAY', 'DVN', 'DLR', 'DFS', 'DISCA', 'DISCK', 'DISH', 'DG', 'DLTR', 'D', 'DOV', 'DTE', 'DRE', 'DUK', 'DXC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMR', 'ETR', 'EOG', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS', 'EL', 'ES', 'RE', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FE', 'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FL', 'F', 'FTV', 'FBHS', 'BEN', 'FCX', 'GPS', 'GRMN', 'IT', 'GD', 'GE', 'GIS', 'GM', 'GPC', 'GILD', 'GPN', 'GS', 'GT', 'GWW', 'HAL', 'HBI', 'HOG', 'HIG', 'HAS', 'HCA', 'HP', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HPQ', 'HUM', 'HBAN', 'HII', 'IDXX', 'INFO', 'ITW', 'ILMN', 'IR', 'ICE', 'IBM', 'INCY', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IQV', 'IRM', 'JBHT', 'SJM', 'JNJ', 'JCI', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'KMB', 'KIM', 'KMI', 'KSS', 'KHC', 'KR', 'LB', 'LH', 'LEG', 'LLY', 'LNC', 'LKQ', 'LMT', 'L', 'LYB', 'MTB', 'MAC', 'M', 'MRO', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'MET', 'MTD', 'MGM', 'MCHP', 'MAA', 'MHK', 'TAP', 'MDLZ', 'MON', 'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'NDAQ', 'NOV', 'NAVI', 'NTAP', 'NWL', 'NEM', 'NWSA', 'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'JWN', 'NSC', 'NTRS', 'NOC', 'NCLH', 'NRG', 'NUE', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'PCAR', 'PKG', 'PH', 'PDCO', 'PAYX', 'PYPL', 'PNR', 'PBCT', 'PEP', 'PKI', 'PRGO', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PNC', 'RL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RRC', 'RJF', 'O', 'REG', 'REGN', 'RF', 'RSG', 'RMD', 'RHI', 'ROK', 'ROP', 'ROST', 'RCL', 'CRM', 'SBAC', 'SLB', 'STX', 'SEE', 'SRE', 'SHW', 'SIG', 'SPG', 'SWKS', 'SLG', 'SNA', 'SO', 'LUV', 'SPGI', 'SWK', 'STT', 'SRCL', 'SYK', 'SYF', 'SNPS', 'SYY', 'TROW', 'TPR', 'TGT', 'TEL', 'FTI', 'TXN', 'TXT', 'TMO', 'TJX', 'TSCO', 'TDG', 'TRV', 'TRIP', 'FOXA', 'FOX', 'TSN', 'UDR', 'ULTA', 'USB', 'UAA', 'UA', 'UNP', 'UNH', 'UPS', 'UHS', 'UNM', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'V', 'VNO', 'VMC', 'WMT', 'WBA', 'WM', 'WAT', 'WEC', 'WFC', 'WDC', 'WU', 'WRK', 'WY', 'WHR', 'WMB', 'WLTW', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', 'XYL', 'YUM', 'ZBH', 'ZION', 'ZTS']

    df = pd.DataFrame(columns=['TICK', 'info' ])

    for symbol in symbols: 
        df=df.append({
            'TICK' : symbol        
        }, ignore_index=True)
    print (df)
    df.to_pickle(DATAROOT+'WatchListDBFull.pickle')
 
# initDBCoreWatchList()

# create_Data_from_Watchlist('WatchListDBFull') # test

