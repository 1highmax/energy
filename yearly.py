import requests
from datetime import datetime, timedelta

# Define the base URL and endpoint for the API
api_base_url = "https://api.energy-charts.info"
endpoint_path = "/price"
bidding_zone = "DE-LU"  # Assuming Germany-Luxembourg as the bidding zone
efficiency = 0.8

# Calculate the start and end dates for the last year
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=365)  # Change this to 365 days

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

# Number of hours in a day
hours_per_day = 24

# Process each day's data
for i in range(len(prices) // hours_per_day):  # Adjusted for hourly data
    # Calculate indices for buying at night
    buy_index_night = i * hours_per_day + 2  # Assuming the list starts at 00:00 and ends at 23:00
    sell_index_night = i * hours_per_day + 7

    # Calculate indices for buying in the afternoon
    buy_index_afternoon = i * hours_per_day + 12
    sell_index_afternoon = i * hours_per_day + 19

    # Calculate potential earnings at night
    if buy_index_night < len(prices) and sell_index_night < len(prices):
        nightly_earnings = (prices[sell_index_night] - prices[buy_index_night]) * efficiency
        total_earnings += nightly_earnings

    # Calculate potential earnings in the afternoon
    if buy_index_afternoon < len(prices) and sell_index_afternoon < len(prices):
        afternoon_earnings = (prices[sell_index_afternoon] - prices[buy_index_afternoon]) * efficiency
        total_earnings += afternoon_earnings

# Print the total potential earnings
print(f"Total potential earnings over the last year: EUR {total_earnings:.2f}")
