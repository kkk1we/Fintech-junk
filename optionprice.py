import numpy as np
import yfinance as yf
from DTops import DTdiff,option_exp
import requests

#treasury 1 month rate for closest to maturity date
api_key = "VX3LDRKN25J5R2RX"
url = f"https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=1month&apikey={api_key}"
response = requests.get(url)
data = response.json()
# Extract the most recent rate
latest_rate = float(data['data'][-1]['value']) / 100
print(f"1-Month T-Bill Rate: {latest_rate:.4%}")

# Example for AVGO
stock_name = "AVGO"
stock = yf.Ticker(stock_name)
options_data = stock.option_chain(option_exp)  # Example expiration date
calls = options_data.calls
puts = options_data.puts

#RF interest rate
symbol = "^IRX"  # T-Bill index for 3-month yield
data = yf.Ticker(symbol)





def binomial_tree_american(S, K, T, r, sigma, N, option_type='call'):
    """
    Calculate the price of an American option using the Binomial Tree Model.
    
    Parameters:
        S (float): Current stock price.
        K (float): Strike price.
        T (float): Time to expiration in years.
        r (float): Risk-free interest rate.
        sigma (float): Volatility of the underlying stock.
        N (int): Number of steps in the binomial tree.
        option_type (str): 'call' or 'put'.
    
    Returns:
        float: Value of the American option.
    """
    # Time step
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))  # Up factor
    d = 1 / u                        # Down factor
    p = (np.exp(r * dt) - d) / (u - d)  # Risk-neutral probability
    discount = np.exp(-r * dt)
    
    # Initialize stock price tree
    stock_prices = np.zeros((N + 1, N + 1))
    for i in range(N + 1):
        for j in range(i + 1):
            stock_prices[j, i] = S * (u ** (i - j)) * (d ** j)
    
    # Initialize option value tree
    option_values = np.zeros((N + 1, N + 1))
    if option_type == 'call':
        option_values[:, -1] = np.maximum(stock_prices[:, -1] - K, 0)
    elif option_type == 'put':
        option_values[:, -1] = np.maximum(K - stock_prices[:, -1], 0)
    else:
        raise ValueError("Option type must be 'call' or 'put'")
    
    # Backward induction
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            intrinsic_value = (stock_prices[j, i] - K if option_type == 'call' else K - stock_prices[j, i])
            intrinsic_value = max(intrinsic_value, 0)
            continuation_value = discount * (p * option_values[j, i + 1] + (1 - p) * option_values[j + 1, i + 1])
            option_values[j, i] = max(intrinsic_value, continuation_value)
            # print(f"Intrinsic Value: {intrinsic_value}, Continuation Value: {continuation_value}")

    return option_values[0, 0]

# Usage
S = stock.history(period="1d")['Close'].iloc[-1]
K = 185     # Strike price
specific_call = calls[calls['strike'] == K]
specific_put = puts[puts['strike'] == K]
T = DTdiff / 365  # Time to expiration (in years)
r = latest_rate   # Risk-free interest rate
Csigma = specific_call['impliedVolatility'].iloc[0] 
Psigma = specific_put['impliedVolatility'].iloc[0]

N = 2500     # Number of steps in the binomial tree

call_price = binomial_tree_american(S, K, T, r, Csigma, N, option_type='call')
put_price = binomial_tree_american(S, K, T, r, Psigma, N, option_type='put')
print(S)
print(f"American Call Option Price: ${call_price:.2f}, for strike price: ${K}, Exp date: {option_exp}")
print(f"American Put Option Price: ${put_price:.2f}, for strike price: ${K}, Exp date: {option_exp}")
