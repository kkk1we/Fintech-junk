from datetime import datetime

option_exp = '2025-01-03'
# Define the future date (YYYY-MM-DD format)
future_date = datetime.strptime(option_exp, "%Y-%m-%d")

# Get today's date
today = datetime.today()

# Calculate the difference in days
DTdiff = (future_date - today).days

#VX3LDRKN25J5R2RX ALPHA VANTAGE API