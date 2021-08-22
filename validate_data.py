"""
Script to Validate entire database.
All pickles will be rewritten. Backup data before use.
Use this with caution. This action cannot be reversed.
"""

import pandas as pd
import app_web.logically.datasource as data
import random
import os.path, time

data.force_sort_index_all()


# # test 

# symbols = ['SPT', 'LB', 'SPY', 'MPC', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MAT', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'MRO', 'M', 'MAC', 'MTB', 'LYB', 'L', 'LMT', 'LKQ', 'LNC', 'LLY', 'LEG', 'LH', 'KR', 'KHC', 'KSS', 'KMI', 'MET', 'MTD', 'MGM', 'MCHP', 'NUE', 'NRG', 'NCLH', 'NOC', 'NTRS', 'NSC', 'JWN', 'NI', 'NKE', 'NLSN', 'NEE', 'NWS', 'NWSA', 'NEM', 'NWL', 'NTAP', 'NAVI', 'NOV', 'NDAQ', 'MSI', 'MOS', 'MS', 'MCO', 'MNST', 'MON', 'MDLZ', 'TAP', 'MHK', 'MAA', 'KIM', 'KMB', 'KEY', 'K', 'HPE', 'HES', 'HSY', 'HSIC', 'HP', 'HCA', 'HAS', 'HIG', 'HOG', 'HBI', 'HAL', 'GWW', 'GT', 'GS', 'GPN', 'GILD', 'GPC', 'GM', 'GIS', 'GE', 'GD', 'IT', 'GRMN', 'GPS', 'FCX', 'BEN', 'FBHS', 'FTV', 'F', 'HLT', 'ORLY', 'HOLX']

# import yfinance as yf
# import pandas as pd

# yf.download(tickers=symbols, interval='1D', period='200d', group_by="Ticker")