#!/usr/bin/env python3
"""
MVG Bus Departure Checker
This app checks bus departures from line 180 at Olympiazentrum station
in direction Berduxstraße using the MVG API.
"""

from mvg import MvgApi


def main():
    """Main function to check bus departures."""
    # Station name to check
    station_name = "Olympiazentrum"
    
    print(f"Checking station ID for: {station_name}")
    
    # Get the station information
    station_info = MvgApi.station(station_name)
    if not station_info:
        print(f"Could not find station: {station_name}")
        return
    
    station_id = station_info.get("id")
    print(f"Station ID for {station_name}: {station_id}")
    print(f"Place: {station_info.get('place')}")
    
    # Initialize the MVG API with the station ID
    api = MvgApi(station_id)
    
    # Get all departures for the station
    print(f"\nFetching departures from {station_name}...")
    departures = api.departures(limit=50)
    
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
            print(f"Departure Time: {departure_time}")
            print(f"Delay: {delay} minutes")
            print("-" * 70)
    
    if not found_departures:
        print(f"No departures found for line {line_number} in direction {direction}")
        print("\nAll available departures:")
        for departure in departures[:10]:  # Show first 10 departures
            print(f"Line {departure.get('line')}: {departure.get('destination')} at {departure.get('time')}")


if __name__ == "__main__":
    main()
