#!/usr/bin/env python3
"""
Flask Web Application for MVG Bus Departure Checker
Displays bus departures from line 180 at Olympiazentrum station in direction Berduxstraße.
"""

from flask import Flask, render_template, jsonify
from datetime import datetime
from mvg import MvgApi
from mvg.mvgapi import MvgApiError

app = Flask(__name__)

# Configuration constants
DEPARTURE_LIMIT = 50
STATION_NAME = "Olympiazentrum"
LINE_NUMBER = "180"
DIRECTION = "Berduxstraße"


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


def get_departures_data():
    """
    Fetch departure data from MVG API.
    
    :return: Dictionary with station info and departures
    """
    try:
        # Get station information
        station_info = MvgApi.station(STATION_NAME)
        if not station_info:
            return {
                "error": f"Could not find station '{STATION_NAME}'",
                "station_name": STATION_NAME
            }
        
        station_id = station_info.get("id")
        
        # Initialize MVG API and get departures
        api = MvgApi(station_id)
        departures = api.departures(limit=DEPARTURE_LIMIT)
        
        # Filter for line 180 in direction Berduxstraße
        filtered_departures = []
        for departure in departures:
            if departure.get("line") == LINE_NUMBER and DIRECTION in departure.get("destination", ""):
                filtered_departures.append({
                    "line": departure.get("line"),
                    "type": departure.get("type", "Unknown"),
                    "destination": departure.get("destination", "Unknown"),
                    "time": format_departure_time(departure.get("time")),
                    "time_raw": departure.get("time"),
                    "delay": departure.get("delay", 0),
                    "platform": departure.get("platform"),
                    "cancelled": departure.get("cancelled", False)
                })
        
        return {
            "station_name": STATION_NAME,
            "station_id": station_id,
            "place": station_info.get("place"),
            "line_number": LINE_NUMBER,
            "direction": DIRECTION,
            "departures": filtered_departures,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    except MvgApiError as e:
        return {
            "error": "Failed to retrieve data from MVG API. Please try again later.",
            "station_name": STATION_NAME
        }
    except Exception as e:
        return {
            "error": "An unexpected error occurred. Please try again later.",
            "station_name": STATION_NAME
        }


def get_raw_departures():
    """
    Fetch raw departure data from MVG API without formatting.
    
    :return: Dictionary with raw API response
    """
    try:
        # Get station information
        station_info = MvgApi.station(STATION_NAME)
        if not station_info:
            return {
                "error": f"Could not find station '{STATION_NAME}'",
                "station_name": STATION_NAME
            }
        
        station_id = station_info.get("id")
        
        # Initialize MVG API and get departures
        api = MvgApi(station_id)
        all_departures = api.departures(limit=DEPARTURE_LIMIT)
        
        # Filter for line 180 in direction Berduxstraße
        filtered_departures = []
        for departure in all_departures:
            if departure.get("line") == LINE_NUMBER and DIRECTION in departure.get("destination", ""):
                filtered_departures.append(departure)
        
        return {
            "station_name": STATION_NAME,
            "station_id": station_id,
            "place": station_info.get("place"),
            "line_number": LINE_NUMBER,
            "direction": DIRECTION,
            "departures": filtered_departures,
            "last_update_timestamp": int(datetime.now().timestamp())
        }
    
    except MvgApiError as e:
        return {
            "error": "Failed to retrieve data from MVG API. Please try again later.",
            "station_name": STATION_NAME
        }
    except Exception as e:
        return {
            "error": "An unexpected error occurred. Please try again later.",
            "station_name": STATION_NAME
        }


@app.route('/')
def index():
    """Render the main page with departure information."""
    data = get_departures_data()
    return render_template('index.html', data=data)


@app.route('/api/departures')
def api_departures():
    """API endpoint returning departure data as JSON."""
    data = get_departures_data()
    return jsonify(data)


@app.route('/raw')
def raw_departures():
    """Raw API endpoint returning unformatted departure data for iOS Shortcuts and automation."""
    data = get_raw_departures()
    return jsonify(data)


if __name__ == '__main__':
    import os
    # Only enable debug mode if explicitly set in environment variable
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
