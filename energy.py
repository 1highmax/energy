import requests
from datetime import datetime, timedelta

# Define the base URL and endpoint for the API
api_base_url = "https://api.energy-charts.info"
endpoint_path = "/price"
bidding_zone = "DE-LU"  # Assuming Germany-Luxembourg as the bidding zone
efficiency = 0.8


# Calculate the start and end dates for the last month
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=30)

# Format dates in ISO 8601 format
start_date_iso = start_date.strftime('%Y-%m-%dT00:00Z')
end_date_iso = end_date.strftime('%Y-%m-%dT23:59Z')

# Define API parameters
params = {
    "bzn": bidding_zone,
    "start": start_date_iso,
    "end": end_date_iso
}

# Make the API request
response = requests.get(f"{api_base_url}{endpoint_path}", params=params)
data = response.json()

# Extract the prices and timestamps
prices = data.get("price", [])
timestamps = data.get("unix_seconds", [])

# Initialize total earnings
total_earnings = 0

# Process each day's data
for i in range(len(prices)//24):  # Assuming hourly data
    # price over night
    buy_index = i * 24 + 2  # Assuming the list starts at 00:00 and ends at 23:00
    sell_index = i * 24 + 7

    if buy_index < len(prices) and sell_index < len(prices):
        # Calculate earnings for the day
        daily_earnings = prices[sell_index] - prices[buy_index]
        # Add to total earnings
        total_earnings += daily_earnings


    # price over afternoon
    buy_index = i * 24 + 12  # Assuming the list starts at 00:00 and ends at 23:00
    sell_index = i * 24 + 19

    if buy_index < len(prices) and sell_index < len(prices):
        # Calculate earnings for the day
        daily_earnings = prices[sell_index] - prices[buy_index]
        # Add to total earnings
        total_earnings += daily_earnings

total_earnings *= efficiency
# Print the total potential earnings
print(f"Total potential earnings over the last month: EUR {total_earnings:.2f}")
