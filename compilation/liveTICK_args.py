import yliveticker, sys


# this function is called on each ticker update
def on_new_msg(ws, msg):
    print(msg)

# Get symbol from arguments
TICKSTRING = sys.argv

TICKERS = TICKSTRING[1:]



yliveticker.YLiveTicker(on_ticker=on_new_msg, ticker_names=TICKERS)



