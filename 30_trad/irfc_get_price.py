import yfinance as yf
import pandas as pd

# Define the stock ticker
ticker = "ITC.NS"  # ".NS" for NSE (National Stock Exchange of India)

# Get the stock data
stock_data = yf.Ticker(ticker)

# Get the stock closing prices for the past month
"""
period options available: 1d, 5d, 1mo, 3mo, 6mo, 1y, 

"""
stock_history = stock_data.history(period="1mo") 

# Print the closing prices
print(stock_history['Close'])
