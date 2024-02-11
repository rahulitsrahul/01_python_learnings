import requests
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

print('running')

def calculate_at_the_money(strike_prices, current_price):
    # Find the strike price closest to the current price
    atm_strike = min(strike_prices, key=lambda x: abs(x - current_price))
    
    return atm_strike

url_nifty = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

print(f'url: {url_nifty}')

session = requests.Session()  # Correct instantiation of the Session object
request = session.get(url=url_nifty, headers=headers).json()

raw_data = pd.DataFrame(request)


# Informations
expiry_dates = raw_data['records']['expiryDates']
spot_price = raw_data['records']['underlyingValue']
timestamp = raw_data['records']['timestamp']
strikePrices = raw_data['records']['strikePrices']
data = raw_data['records']['data']
ATM = calculate_at_the_money(strikePrices, spot_price)

expiry_search = '11-Jan-2024'
filtered_data_expiry = []

for el in data:
    if el['expiryDate'] == expiry_search:
        filtered_data_expiry.append(el)
        

print("example_data")
print(filtered_data_expiry[40])

print("---------------------")

ltps = {}
for el in filtered_data_expiry:
    strikePrice = el['strikePrice']
    PE_ltp = el['PE']['lastPrice']
    PE_oi = el['PE']['openInterest']
    
    CE_ltp = el['CE']['lastPrice']
    PE_oi = el['CE']['openInterest']
    
    if (strikePrice == (ATM+50)): print(f"--------------ATM, spot:{spot_price}-----------------")
    print(f"{str(CE_ltp).rjust(11)}  {strikePrice} PE {str(PE_ltp).rjust(8)}") if (strikePrice <= ATM) else print(f"CE {str(CE_ltp).rjust(8)}  {strikePrice} {str(PE_ltp).rjust(8)}")
    
    ltps[strikePrice] = {}
    ltps[strikePrice]['CE'] = CE_ltp
    ltps[strikePrice]['PE'] = PE_ltp
    
    

selected_strike = 21500 
flag = 'PE'
entry_price = ltps[selected_strike][flag]
ltps_keys = list(ltps.keys())
ATM_strike_price_index = ltps_keys.index(ATM)

diff = 15
start = ATM_strike_price_index - diff
end = ATM_strike_price_index + diff

strike_prices = ltps_keys[start:end]

X = np.arange(strike_prices[0], strike_prices[-1])
PnL_expiry = []
for spot in X:
    res = 0
    if flag == 'CE':
        if (spot <= selected_strike):
            res = entry_price * 50
        else:
            res = (entry_price - (spot - selected_strike)) * 50
    
    if flag == 'PE':
        if (spot >= selected_strike):
            res = entry_price * 50
        else:
            res = (entry_price - (selected_strike- spot)) * 50 
    
    PnL_expiry.append(res)


##---------------------------------------------------------

fig, ax = plt.subplots(figsize=(16, 8), dpi=80)
plt.grid(True, color='k', linestyle='--', linewidth='0.1')
line, = plt.plot(X, PnL_expiry, 'g-', label='PnL')
plt.axhline(0)
plt.axvline(spot_price)

# Filling above zero with green and below zero with red
plt.fill_between(X, PnL_expiry, where=(np.array(PnL_expiry) > 0), color='green', alpha=0.3)
plt.fill_between(X, PnL_expiry, where=(np.array(PnL_expiry) < 0), color='red', alpha=0.3)

# Filling above zero with green and below zero with red
plt.fill_between(X, PnL_expiry, where=(np.array(PnL_expiry) > 0), color='green', alpha=0.3)
plt.fill_between(X, PnL_expiry, where=(np.array(PnL_expiry) < 0), color='red', alpha=0.3)

# Find maximum profit and corresponding spot price
max_profit = max(PnL_expiry)
spot_price_at_max_profit = X[np.argmax(PnL_expiry)]

# Annotate maximum profit
plt.annotate(f"Max Profit: {max_profit:.2f} at Spot Price: {spot_price_at_max_profit}",
             xy=(spot_price_at_max_profit, max_profit),
             xytext=(spot_price_at_max_profit + 20, max_profit + 500),  # Position of the annotation text
             arrowprops=dict(facecolor='black', arrowstyle='->'))

# Find where PnL hits 0 if it exists
zero_pnl_indices = np.where(np.array(PnL_expiry) < 0)[0]
if zero_pnl_indices.size > 0:
    spot_price_at_zero_pnl = X[zero_pnl_indices[0]]

    # Annotate where PnL hits 0
    plt.annotate(f"PnL = 0 at Spot Price: {spot_price_at_zero_pnl}",
                 xy=(spot_price_at_zero_pnl, 0),
                 xytext=(spot_price_at_zero_pnl + 20, 500),
                 arrowprops=dict(facecolor='black', arrowstyle='->'))
else:
    print("PnL does not hit 0 within the specified range.")

#-------------------------MOuse HOver-------------------------------#
spot_price_text = ax.text(0.1, 0.9, '', transform=ax.transAxes, fontsize=12)
profit_text = ax.text(0.1, 0.8, '', transform=ax.transAxes, fontsize=12)
vline = ax.axvline(x=spot_price, color='black', linestyle='--')

def on_move(event):
    if event.xdata:
        x_pos = event.xdata
        y_pos = np.interp(x_pos, X, PnL_expiry)
        spot_price_text.set_text(f'Spot Price: {x_pos:.2f}')
        spot_price_text.set_position((0.7, 0.9))
        vline.set_xdata(x_pos)
        vline.set_visible(True)
        
        profit = np.interp(x_pos, X, PnL_expiry)
        profit_text.set_text(f'Profit: {profit:.2f}')
        profit_text.set_position((0.8, 0.8))
        
        plt.draw()
    else:
        spot_price_text.set_text('')
        profit_text.set_text('')
        vline.set_visible(False)
        plt.draw()

fig.canvas.mpl_connect('motion_notify_event', on_move)

plt.show()




    
