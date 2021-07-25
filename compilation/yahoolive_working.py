from yflive import QuoteStreamer

# Get QuoteStreamer singleton
qs = QuoteStreamer()

# Subscribe to AAPL, TSLA
qs.subscribe(["INR=X", "BTC-USD", "ETH-USD"])

#qs.subscribe(["AAPL", "AMZN", "AMAT"])

#qs.subscribe(["AAPL"])

# Override on_quote callback
qs.on_quote = lambda qs, q: print(q)

# Start streaming
qs.start()
