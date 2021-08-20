"""
Script to check last updated values in database randomly.
"""
#################       Signal to HTML Display test

# import computeIndicator as cp
import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
sys.path.append('./app_web/logically')
from app_web.logically.computeIndicator import * 
import app_web.logically.datasource as data
import app_web.logically.dfutils as dutil

# auto reload modules for notebook 
# %load_ext autoreload
# %autoreload 2


# define placeholders 
ddr4H  = {}
Addr4H = {}
ddr1H  = {}
Addr1H = {}
ddr1D  = {}
Addr1D = {}

# load data 
ddr4H, symbols = data.loadDatatoMemory(interval='4H', filter=50, randomize=False)
ddr1H, _ = data.loadDatatoMemory(interval='1H', filter=50, randomize=False)
ddr1D, _ = data.loadDatatoMemory(interval='1D', filter=50, randomize=False)

# Compute all Signals 
Addr4H = compute_all(ddr=ddr4H.copy(), symbols=symbols, interval='4H')
Addr1H = compute_all(ddr=ddr1H.copy(), symbols=symbols, interval='1H')
Addr1D = compute_all(ddr=ddr1D.copy(), symbols=symbols, interval='1D')

processQ.empty()
endCompute() # quit the multiprocessing thread ## run multiple times to exit all 



# # test 

# symbols = ['SPT', 'LB', 'SPY', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'MRO', 'M', 'MAC', 'MTB', 'LYB', 'L', 'LMT', 'LKQ', 'LNC', 'LLY', 'LEG', 'LH', 'KR', 'KHC', 'KSS', 'KMI', 'MET', 'MTD', 'MGM', 'MCHP', 'NUE', 'NRG', 'NCLH', 'NOC', 'NTRS', 'NSC', 'JWN', 'NI', 'NKE', 'NLSN', 'NEE', 'NWS', 'NWSA', 'NEM', 'NWL', 'NTAP', 'NAVI', 'NOV', 'NDAQ', 'MSI', 'MOS', 'MS', 'MCO', 'MNST', 'MON', 'MDLZ', 'TAP', 'MHK', 'MAA', 'KIM', 'KMB', 'KEY', 'K', 'HPE', 'HES', 'HSY', 'HSIC', 'HP', 'HCA', 'HAS', 'HIG', 'HOG', 'HBI', 'HAL', 'GWW', 'GT', 'GS', 'GPN', 'GILD', 'GPC', 'GM', 'GIS', 'GE', 'GD', 'IT', 'GRMN', 'GPS', 'FCX', 'BEN', 'FBHS', 'FTV', 'F', 'HLT', 'ORLY', 'HOLX']

# import yfinance as yf
# import pandas as pd

# yf.download(tickers=symbols, interval='1D', period='200d', group_by="Ticker")