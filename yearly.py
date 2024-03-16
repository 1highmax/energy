import requests
from datetime import datetime, timedelta

# Define the base URL and endpoint for the API
api_base_url = "https://api.energy-charts.info"
endpoint_path = "/price"
bidding_zone = "DE-LU"  # Assuming Germany-Luxembourg as the bidding zone
efficiency = 0.8
years = 5

# Number of hours in a day
hours_per_day = 24

# Initialize a dictionary to store earnings per year
earnings_per_year = {}

# Process data for each year
for year in range(1, years + 1):
    # Calculate the start and end dates for the current year
    end_date = datetime.utcnow() - timedelta(days=365 * (year - 1))
    start_date = end_date - timedelta(days=365)
    
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
    
    # Initialize total earnings for the current year
    total_earnings = 0
    
    # Process each day's data
    for i in range(len(prices) // hours_per_day):  # Adjusted for hourly data
        # Calculate indices for buying at night
        buy_index_night = i * hours_per_day + 2  # Assuming the list starts at 00:00 and ends at 23:00
        sell_index_night = i * hours_per_day + 6

        # Calculate indices for buying in the afternoon
        buy_index_afternoon = i * hours_per_day + 12
        sell_index_afternoon = i * hours_per_day + 18

        # Calculate potential earnings at night
        if buy_index_night < len(prices) and sell_index_night < len(prices):
            nightly_earnings = (prices[sell_index_night] - prices[buy_index_night]) * efficiency
            total_earnings += nightly_earnings

        # Calculate potential earnings in the afternoon
        if buy_index_afternoon < len(prices) and sell_index_afternoon < len(prices):
            afternoon_earnings = (prices[sell_index_afternoon] - prices[buy_index_afternoon]) * efficiency
            total_earnings += afternoon_earnings
    
    # Store the earnings for the current year
    earnings_year = end_date.year
    earnings_per_year[earnings_year] = total_earnings

# Print the earnings for each year
for year, earnings in earnings_per_year.items():
    print(f"Earnings for {year}: EUR {earnings:.2f}")

# Calculate and print the average earnings per year
average_earnings = sum(earnings_per_year.values()) / years
print(f"Yearly average potential earnings over the last {years} years: EUR {average_earnings:.2f}")
