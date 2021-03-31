import sys
from yflive import QuoteStreamer


import getopt, sys

# Get full command-line arguments
full_cmd_arguments = sys.argv

# Keep all but the first
TICKERS = full_cmd_arguments[1:]

# Get symbol from arguments 
#TICK = sys.argv[1]

#TICKERS = (str(sys.argv))

print ("TICKs :", TICKERS, len(TICKERS))



# Get QuoteStreamer singleton
qs = QuoteStreamer()

# Subscribe to AAPL, TSLA
#qs.subscribe(["INR=X", "BTC-USD"])

#qs.subscribe(["AAPL", "AMZN"])

# qs.subscribe(["AAPL"])
qs.subscribe(TICKERS)

# Override on_quote callback
qs.on_quote = lambda q: print(q)

# Start streaming
qs.start()
