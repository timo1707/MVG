#!/usr/bin/env python3
"""
MVG Bus Departure Checker
This app checks bus departures from line 180 at Olympiazentrum station
in direction Berduxstraße using the MVG API.
"""

from datetime import datetime
from mvg import MvgApi
from mvg.mvgapi import MvgApiError

# Configuration constants
DEPARTURE_LIMIT = 50  # Maximum number of departures to fetch
DISPLAY_LIMIT = 10  # Maximum number of departures to display when filtering fails


def format_departure_time(timestamp):
    """
    Convert Unix timestamp to human-readable format.
    
    :param timestamp: Unix timestamp in seconds
    :return: Formatted date and time string
    """
    if timestamp == "Unknown" or timestamp is None:
        return "Unknown"
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError, OSError):
        return str(timestamp)


def main():
    """Main function to check bus departures."""
    # Station name to check
    station_name = "Olympiazentrum"
    
    print(f"Checking station ID for: {station_name}")
    
    try:
        # Get the station information
        station_info = MvgApi.station(station_name)
        if not station_info:
            print(f"Error: Could not find station '{station_name}'")
            print("Please verify the station name and try again.")
            return
        
        station_id = station_info.get("id")
        print(f"Station ID for {station_name}: {station_id}")
        print(f"Place: {station_info.get('place')}")
        
        # Initialize the MVG API with the station ID
        api = MvgApi(station_id)
        
        # Get all departures for the station
        print(f"\nFetching departures from {station_name}...")
        departures = api.departures(limit=DEPARTURE_LIMIT)
    except MvgApiError as e:
        print(f"Error: Failed to retrieve data from MVG API: {e}")
        print("Please check your internet connection and try again.")
        return
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return
    
    # Filter for line 180 in direction Berduxstraße
    line_number = "180"
    direction = "Berduxstraße"
    
    print(f"\nFiltering for line {line_number} in direction {direction}:")
    print("-" * 70)
    
    found_departures = False
    for departure in departures:
        # Check if this is the line and direction we're looking for
        if departure.get("line") == line_number and direction in departure.get("destination", ""):
            found_departures = True
            departure_time = departure.get("time", "Unknown")
            destination = departure.get("destination", "Unknown")
            delay = departure.get("delay", 0)
            transport_type = departure.get("type", "Unknown")
            
            print(f"Line: {line_number}")
            print(f"Type: {transport_type}")
            print(f"Destination: {destination}")
            print(f"Departure Time: {format_departure_time(departure_time)}")
            print(f"Delay: {delay} minutes")
            print("-" * 70)
    
    if not found_departures:
        print(f"No departures found for line {line_number} in direction {direction}")
        print("\nAll available departures:")
        for departure in departures[:DISPLAY_LIMIT]:  # Show first DISPLAY_LIMIT departures
            print(f"Line {departure.get('line')}: {departure.get('destination')} at {format_departure_time(departure.get('time'))}")


if __name__ == "__main__":
    main()
