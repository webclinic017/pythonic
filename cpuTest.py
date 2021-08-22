"""
Script to check last updated values in database randomly.
"""
#################       Signal to HTML Display test

# import computeIndicator as cp
import sys
sys.path.append('./app_web/logically')
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py

from app_web.logically.computeIndicator import * 
import app_web.logically.datasource as data
import app_web.logically.dfutils as dutil

# # auto reload modules for notebook 
# %load_ext autoreload
# %autoreload 2


# define placeholders 
ddr4H  = {}
Addr4H = {}
ddr1H  = {}
Addr1H = {}
ddr1D  = {}
Addr1D = {}

# define control symbols
symbols = ['NKE','IVV', 'COST', 'AMAT', 'JNUG', 'AAPL', 'DIS', 'BA', 'MRNA', 'AMZN', 'INTC', 'SPXU', 'CLX', 'GOOG', 'AAL', 'DAL', 'AMD', 'MSFT', 'SPXS', 'FB', 'WGO', 'MU', 'LRCX', 'SPY', 'BAC', 'KLAC', 'PTON', 'NVDA', 'NFLX', 'SAIA', 'SPCE', 'QQQ', 'ONEQ', 'SKX', 'ZM', 'SBUX', 'TSLA', 'LPX', 'UAL', 'UCTT', 'UFPI', 'SNBR', 'WSM', 'URI', 'HZO', 'APPS', 'VDE', 'WAL', 'DHI', 'ARCB', 'COWN', 'TFII', 'ABG', 'LGIH', 'LAD', 'KIRK', 'LOB', 'LOW', 'CALX', 'AVNW', 'TPX', 'LEN', 'USAK', 'CENTA', 'HZNP', 'TBBK', 'GROW', 'HIBB', 'AMRK', 'SYNA', 'CCS', 'MHO', 'IDT', 'KLIC', 'GSL', 'AOUT', 'KBH', 'SCVL', 'BGFV', 'MDC', 'UNFI', 'SLM', 'CUBI', 'HTH', 'HIMX', 'ACLS', 'RCII', 'GPI', 'AGCO', 'TRQ', 'HVT', '^DJI', 'ODFL', 'DAC', 'ICHR', '^VIX', '^NDX', 'OMI', '^GSPC', 'SPXU', 'MRNA', 'SPY', 'AAL', 'SPXS', 'JNUG', 'WGO', 'AAPL', 'AMZN', 'DIS', 'DAL', 'COST', 'AMD', 'BA', 'BAC', 'CLX', 'AMAT', 'KLAC', 'INTC', 'LRCX', 'MSFT', 'MU', 'IVV', 'FB', 'GOOG', 'PTON', 'SPCE', 'ZM', 'NFLX', 'NVDA', 'ONEQ', 'SAIA', 'SKX', 'QQQ', 'SBUX', 'UAL', 'LPX', 'UFPI', 'SNBR', 'VDE', 'DHI', 'UCTT', 'ARCB', 'URI', 'TSLA', 'WAL', 'COWN', 'APPS', 'WSM', 'HZO','SPY', 'SPXU', 'SPXS', 'JNUG', 'AAL', 'WGO', 'DAL', 'AAPL', 'AMAT', 'AMD', 'AMZN', 'BA', 'BAC', 'CLX', 'COST', 'DIS', 'FB', 'GOOG', 'INTC', 'IVV', 'KLAC', 'LRCX', 'MRNA', 'MSFT', 'MU', 'NFLX', 'NVDA', 'ONEQ', 'PTON', 'QQQ', 'SAIA', 'SBUX', 'SKX', 'SPCE', 'TSLA', 'UAL', 'URI', 'VDE', 'ZM', 'LPX', 'SNBR', 'UCTT', 'WSM', 'APPS', 'HZO', 'KLAC', 'GE','WAL', 'COWN', 'DHI', 'ARCB', 'UFPI','INTC', 'TSLA', 'NVDA', 'BAC', 'COWN', 'LPX']

# load data for 100 symbols
ddr4H, symbols = data.loadDatatoMemory(interval='4H', filter=None, randomize=False, symbols=symbols)
ddr1D, _ = data.loadDatatoMemory(interval='1D', filter=None, randomize=False, symbols=symbols)
ddr1H, _ = data.loadDatatoMemory(interval='1H', filter=None, randomize=False, symbols=symbols)
ddr5m, _ = data.loadDatatoMemory(interval='5m', filter=None, randomize=False, symbols=symbols)

# ## reduce memory footprint of DF ; Does not speed up compute. # from initial test 
# for symbol in ddr4H.keys(): 
#     ddr4H[symbol] = reduce_mem_usage(ddr4H[symbol], verbose=False)


# Print Row Counts 
print ( f'Interval: 4H, rows : {ddr4H["SPY"].shape }')
print ( f'Interval: 1D, rows : {ddr1D["SPY"].shape }')
print ( f'Interval: 1H, rows : {ddr1H["SPY"].shape }')
print ( f'Interval: 5m, rows : {ddr5m["SPY"].shape }')

# Compute all Signals 
Addr4H = compute_all(ddr=ddr4H.copy(), symbols=symbols, interval='4H')
Addr1D = compute_all(ddr=ddr1D.copy(), symbols=symbols, interval='1D')
Addr1H = compute_all(ddr=ddr1H.copy(), symbols=symbols, interval='1H')
Addr5m = compute_all(ddr=ddr1D.copy(), symbols=symbols, interval='5m')


processQ.empty()
endCompute() # quit the multiprocessing thread ## run multiple times to exit all 



# # test 

# symbols = ['SPT', 'LB', 'SPY', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'MRO', 'M', 'MAC', 'MTB', 'LYB', 'L', 'LMT', 'LKQ', 'LNC', 'LLY', 'LEG', 'LH', 'KR', 'KHC', 'KSS', 'KMI', 'MET', 'MTD', 'MGM', 'MCHP', 'NUE', 'NRG', 'NCLH', 'NOC', 'NTRS', 'NSC', 'JWN', 'NI', 'NKE', 'NLSN', 'NEE', 'NWS', 'NWSA', 'NEM', 'NWL', 'NTAP', 'NAVI', 'NOV', 'NDAQ', 'MSI', 'MOS', 'MS', 'MCO', 'MNST', 'MON', 'MDLZ', 'TAP', 'MHK', 'MAA', 'KIM', 'KMB', 'KEY', 'K', 'HPE', 'HES', 'HSY', 'HSIC', 'HP', 'HCA', 'HAS', 'HIG', 'HOG', 'HBI', 'HAL', 'GWW', 'GT', 'GS', 'GPN', 'GILD', 'GPC', 'GM', 'GIS', 'GE', 'GD', 'IT', 'GRMN', 'GPS', 'FCX', 'BEN', 'FBHS', 'FTV', 'F', 'HLT', 'ORLY', 'HOLX']

# import yfinance as yf
# import pandas as pd

# yf.download(tickers=symbols, interval='1D', period='200d', group_by="Ticker")