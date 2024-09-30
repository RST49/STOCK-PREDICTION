import yfinance as yf

# Ticker for Nifty 50 Index (use "^NSEI" for Nifty 50 or replace with other asset tickers)
ticker = "^NSEI"

# Download historical data for the last 6 months (or specify other periods)
nifty_data = yf.download(ticker, period="6mo", interval="1d")

# Display the first few rows of the data
print(nifty_data.head())

# Load the ticker for which you want to retrieve options data
stock = yf.Ticker(ticker)

# Get available expiration dates for options
expirations = stock.options
print("Available expiration dates:", expirations)

# Choose a specific expiration date
expiration = expirations[28]  # Use the first expiration date as an example

# Get the option chain for the selected expiration date
option_chain = stock.option_chain(expiration)

# Separate call and put options data
calls = option_chain.calls
puts = option_chain.puts

# Display the first few rows of the calls and puts
print("Calls:")
print(calls.head())

print("Puts:")
print(puts.head())
# Get available expiration dates for the options
expirations = stock.options
print("Available expiration dates:", expirations)
