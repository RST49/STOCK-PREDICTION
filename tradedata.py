from tvDatafeed import TvDatafeed, Interval

username = 'rstfak16'
password = 'mylastpassforyou@nigga1'

tv = TvDatafeed(username, password)

# Fetch Nifty index data (with no-login method, data might be limited)
nifty_index_data = tv.get_hist(symbol='BANKNIFTY', exchange='NSE', interval=Interval.in_1_minute, n_bars=20000)

# Display the data
print(nifty_index_data)
