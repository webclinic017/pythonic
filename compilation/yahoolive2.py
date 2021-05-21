from yflive import QuoteStreamer

# Get QuoteStreamer singleton
qs = QuoteStreamer()

# Subscribe to AAPL, TSLA
#qs.subscribe(["INR=X", "BTC-USD"])
qs.subscribe(["AAPL", "TSLA", "KLAC", "AMZN", "GOOG"]) 

# Override on_quote callback
qs.on_quote = lambda qs, q: print(q)

# Non-blocking if blocking=False (default is True)
qs.start(blocking=True)