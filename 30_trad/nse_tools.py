from nsetools import Nse

# Create an instance of the Nse class
nse = Nse()

# Get the list of Nifty 50 stock symbols
nifty_50_symbols = nse.get_index_constituents('nifty 50')

# Print the list of Nifty 50 stock names
for symbol, name in nifty_50_symbols.items():
    print(name)
