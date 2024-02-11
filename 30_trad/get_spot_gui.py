import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import requests
import pandas as pd
import numpy as np
import mplcursors

def calculate_at_the_money(strike_prices, current_price):
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

expiry_search = '25-Jan-2024'
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
    
    

selected_strike = 22000 
flag = 'CE'
entry_price = ltps[selected_strike][flag]
ltps_keys = list(ltps.keys())
ATM_strike_price_index = ltps_keys.index(ATM)

diff = 30
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

def update_PnL(expiry_search, selected_strike, flag):
    
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
        
        

    # selected_strike = 22000 
    # flag = 'CE'
    entry_price = ltps[selected_strike][flag]
    ltps_keys = list(ltps.keys())
    ATM_strike_price_index = ltps_keys.index(ATM)

    diff = 30
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
    
    return PnL_expiry




#-------------------------------------------------------
def plot_graph():
    selected_expiry = expiry_var.get()
    selected_strike = int(strike_var.get())
    selected_flag = flag_var.get()

    PnL_expiry = update_PnL(expiry_search=selected_expiry, selected_strike=selected_strike, flag=selected_flag)    

    fig = Figure(figsize=(16, 8), dpi=80)
    ax = fig.add_subplot(111)
    ax.grid(True, color='k', linestyle='--', linewidth='0.1')
    line, = ax.plot(X, PnL_expiry, 'g-', label='PnL')
    ax.axhline(0)
    ax.axvline(spot_price)

    # Filling above zero with green and below zero with red
    ax.fill_between(X, PnL_expiry, where=(np.array(PnL_expiry) > 0), color='green', alpha=0.3)
    ax.fill_between(X, PnL_expiry, where=(np.array(PnL_expiry) < 0), color='red', alpha=0.3)

    # Find maximum profit and corresponding spot price
    max_profit = max(PnL_expiry)
    spot_price_at_max_profit = X[np.argmax(PnL_expiry)]

    # Annotate maximum profit
    ax.annotate(f"Max Profit: {max_profit:.2f} at Spot Price: {spot_price_at_max_profit}",
                xy=(spot_price_at_max_profit, max_profit),
                xytext=(spot_price_at_max_profit + 20, max_profit + 500),  # Position of the annotation text
                arrowprops=dict(facecolor='black', arrowstyle='->'))

    # Find where PnL hits 0 if it exists
    zero_pnl_indices = np.where(np.array(PnL_expiry) < 0)[0]
    if zero_pnl_indices.size > 0:
        spot_price_at_zero_pnl = X[zero_pnl_indices[0]]

        # Annotate where PnL hits 0
        ax.annotate(f"PnL = 0 at Spot Price: {spot_price_at_zero_pnl}",
                    xy=(spot_price_at_zero_pnl, 0),
                    xytext=(spot_price_at_zero_pnl + 20, 500),
                    arrowprops=dict(facecolor='black', arrowstyle='->'))
    else:
        print("PnL does not hit 0 within the specified range.")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=20)
    
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
            
            canvas.draw_idle()  # Update the canvas
        else:
            spot_price_text.set_text('')
            profit_text.set_text('')
            vline.set_visible(False)
            canvas.draw_idle()  # Update the canvas

    fig.canvas.mpl_connect('motion_notify_event', on_move)


root = tk.Tk()
root.title("Options Plotter")

frame = ttk.Frame(root)
frame.pack(padx=20, pady=20)


row_val = 0
# Dropdown for Expiry Dates
expiry_label = ttk.Label(frame, text="Select Expiry:")
expiry_label.grid(row=row_val, column=0, padx=5, pady=5)
expiry_var = tk.StringVar()
expiry_dropdown = ttk.Combobox(frame, textvariable=expiry_var, values=expiry_dates)
expiry_dropdown.grid(row=row_val, column=1, padx=5, pady=5)
expiry_dropdown.current(0)

# Dropdown for Strike Prices
row_val = 1
strike_label = ttk.Label(frame, text="Select Strike Price:")
strike_label.grid(row=row_val, column=0, padx=5, pady=5)
strike_var = tk.StringVar()
strike_dropdown = ttk.Combobox(frame, textvariable=strike_var, values=strike_prices)
strike_dropdown.grid(row=row_val, column=1, padx=5, pady=5)
strike_dropdown.current(0)

# Radio buttons for PE/CE selection
row_val = 2
flag_label = ttk.Label(frame, text="Select Flag:")
flag_label.grid(row=2, column=0, padx=5, pady=5)
flag_var = tk.StringVar(value="CE")
pe_radio = ttk.Radiobutton(frame, text="PE", variable=flag_var, value="PE")
pe_radio.grid(row=row_val, column=1, padx=5, pady=5)
ce_radio = ttk.Radiobutton(frame, text="CE", variable=flag_var, value="CE")
ce_radio.grid(row=row_val, column=2, padx=5, pady=5)

# Button to generate plot
row_val = 3
plot_button = ttk.Button(frame, text="Plot", command=plot_graph)
plot_button.grid(row=row_val, column=0, columnspan=3, padx=5, pady=10)

# Display spot price
row_val = 4
spot_price_label = ttk.Label(frame, text=f"Spot Price: {spot_price:.2f}")
spot_price_label.grid(row=row_val, column=0, columnspan=3, padx=5, pady=5)


# Display the strike prices
expiry_val = expiry_var.get()
filtered_data_expiry = []

for el in data:
    if el['expiryDate'] == expiry_val:
        filtered_data_expiry.append(el)
        

print("example_data")
print(filtered_data_expiry[40])

print("---------------------")

row_val = 4
ltps = {}
for el in filtered_data_expiry:
    strikePrice = el['strikePrice']
    PE_ltp = el['PE']['lastPrice']
    PE_oi = el['PE']['openInterest']
    
    CE_ltp = el['CE']['lastPrice']
    PE_oi = el['CE']['openInterest']
    
    if (strikePrice == (ATM+50)): print(f"--------------ATM, spot:{spot_price}-----------------")
    text = (f"{str(CE_ltp).rjust(11)}  {strikePrice} PE {str(PE_ltp).rjust(8)}") if (strikePrice <= ATM) else print(f"CE {str(CE_ltp).rjust(8)}  {strikePrice} {str(PE_ltp).rjust(8)}")
    
    row_val += 1
    spot_price_label = ttk.Label(frame, text=f"Spot Price: {spot_price:.2f}")
    spot_price_label.grid(row=row_val, column=0, columnspan=3, padx=5, pady=5)

    
    ltps[strikePrice] = {}
    ltps[strikePrice]['CE'] = CE_ltp
    ltps[strikePrice]['PE'] = PE_ltp

root.mainloop()


