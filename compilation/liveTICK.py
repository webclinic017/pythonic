import yliveticker

# this function is called on each ticker update
def on_new_msg(msg):
	print ("Hello") 
	print(msg)


#yliveticker.YLiveTicker(on_ticker=on_new_msg, ticker_names=[
#	"BTC=X", "^GSPC", "^DJI", "^IXIC", "^RUT", "CL=F", "GC=F", "SI=F", "EURUSD=X", "^TNX", "^VIX", "GBPUSD=X", "JPY=X", "BTC-USD", "^CMC200", "^FTSE", "^N225"])


yliveticker.YLiveTicker(on_ticker=on_new_msg, ticker_names=["AAPL", "AMZN"])
print ("execucted")
#yliveticker.YLiveTicker(on_ticker=on_new_msg, ticker_names=["AAPL", "AMZN"])
#yliveticker.YLiveTicker(on_ticker=on_new_msg, ticker_names=["AAPL"])
