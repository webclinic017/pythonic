import sys
from yflive import QuoteStreamer

print("Enter TICKERS are arguments list AAPL AMZN FB.")

# Get symbol from arguments
TICKSTRING = sys.argv

TICKERS = TICKSTRING[1:]

#print (TICKSTRING[0], TICKSTRING[1], TICKSTRING[2])
#print (TICKSTRING[1], TICKSTRING[2])

#print (TICKSTRING[1:])

print (TICKSTRING, " => TICKs :", TICKERS, len(TICKERS))


# Get QuoteStreamer singleton
qs = QuoteStreamer()

# Subscribe to AAPL, TSLA
#qs.subscribe(["INR=X", "BTC-USD"])

#qs.subscribe(["AAPL", "AMZN"])

# qs.subscribe(["AAPL"])
qs.subscribe(TICKERS)

# Override on_quote callback
qs.on_quote = lambda qs, q: print(q)

# Start streaming
# qs.start()
qs.start(should_thread=False)
