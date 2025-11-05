#!/usr/bin/env python3
"""
Static Site Generator for MVG Bus Departure Checker
Generates a static HTML page for GitHub Pages deployment.
"""

from datetime import datetime
from mvg import MvgApi
from mvg.mvgapi import MvgApiError
import os

# Configuration constants
DEPARTURE_LIMIT = 50
STATION_NAME = "Olympiazentrum"
LINE_NUMBER = "180"
DIRECTION = "Berduxstraße"


def format_departure_time(timestamp):
    """Convert Unix timestamp to human-readable format."""
    if timestamp == "Unknown" or timestamp is None:
        return "Unknown"
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError, OSError):
        return str(timestamp)


def generate_static_html():
    """Generate static HTML page with current departure data."""
    
    # Fetch data
    try:
        station_info = MvgApi.station(STATION_NAME)
        if not station_info:
            error_msg = f"Could not find station '{STATION_NAME}'"
            return generate_error_page(error_msg)
        
        station_id = station_info.get("id")
        api = MvgApi(station_id)
        departures = api.departures(limit=DEPARTURE_LIMIT)
        
        # Filter departures
        filtered_departures = []
        for departure in departures:
            if departure.get("line") == LINE_NUMBER and DIRECTION in departure.get("destination", ""):
                filtered_departures.append({
                    "line": departure.get("line"),
                    "type": departure.get("type", "Unknown"),
                    "destination": departure.get("destination", "Unknown"),
                    "time": format_departure_time(departure.get("time")),
                    "delay": departure.get("delay", 0),
                    "platform": departure.get("platform"),
                    "cancelled": departure.get("cancelled", False)
                })
        
        # Generate HTML
        html = generate_html_page(
            station_name=STATION_NAME,
            station_id=station_id,
            place=station_info.get("place"),
            line_number=LINE_NUMBER,
            direction=DIRECTION,
            departures=filtered_departures,
            last_update=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        return html
        
    except MvgApiError as e:
        return generate_error_page(f"Failed to retrieve data from MVG API: {e}")
    except Exception as e:
        return generate_error_page(f"An unexpected error occurred: {e}")


def generate_html_page(station_name, station_id, place, line_number, direction, departures, last_update):
    """Generate the HTML page with departure data."""
    
    departures_html = ""
    if departures:
        for dep in departures:
            cancelled_class = " cancelled" if dep.get("cancelled") else ""
            cancelled_msg = '<div style="margin-top: 10px; color: #dc3545; font-weight: bold;">❌ This departure has been cancelled</div>' if dep.get("cancelled") else ""
            
            delay = dep.get("delay", 0)
            if delay == 0:
                delay_badge = '<span class="delay-badge delay-none">On Time</span>'
            elif delay <= 3:
                delay_badge = f'<span class="delay-badge delay-warning">+{delay} min</span>'
            else:
                delay_badge = f'<span class="delay-badge delay-danger">+{delay} min</span>'
            
            platform_html = ""
            if dep.get("platform"):
                platform_html = f'''
                <div class="detail-item">
                    <span class="detail-label">Platform</span>
                    <span class="detail-value">{dep.get("platform")}</span>
                </div>
                '''
            
            departures_html += f'''
            <div class="departure-card{cancelled_class}">
                <div class="departure-header">
                    <span class="line-badge">Line {dep["line"]}</span>
                    <span class="time-display">{dep["time"]}</span>
                </div>
                <div class="departure-details">
                    <div class="detail-item">
                        <span class="detail-label">Destination</span>
                        <span class="detail-value">{dep["destination"]}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Type</span>
                        <span class="detail-value">{dep["type"]}</span>
                    </div>
                    {platform_html}
                    <div class="detail-item">
                        <span class="detail-label">Delay</span>
                        <span class="detail-value">{delay_badge}</span>
                    </div>
                </div>
                {cancelled_msg}
            </div>
            '''
    else:
        departures_html = f'''
        <div class="no-departures">
            <p>No departures found for Line {line_number} to {direction}</p>
        </div>
        '''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="300">
    <title>MVG Bus Departures - Olympiazentrum</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        h1 {{
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .station-info {{
            color: #666;
            font-size: 1.1em;
            margin-top: 10px;
        }}
        
        .info-badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            margin-right: 10px;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        
        .departures-container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .departure-card {{
            background: #f8f9fa;
            border-left: 5px solid #667eea;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .departure-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .departure-card.cancelled {{
            opacity: 0.6;
            border-left-color: #dc3545;
        }}
        
        .departure-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .line-badge {{
            background: #667eea;
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 1.2em;
        }}
        
        .time-display {{
            font-size: 1.4em;
            font-weight: bold;
            color: #333;
        }}
        
        .departure-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        
        .detail-item {{
            display: flex;
            flex-direction: column;
        }}
        
        .detail-label {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}
        
        .detail-value {{
            color: #333;
            font-weight: 500;
            font-size: 1.1em;
        }}
        
        .delay-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        
        .delay-none {{
            background: #28a745;
            color: white;
        }}
        
        .delay-warning {{
            background: #ffc107;
            color: #333;
        }}
        
        .delay-danger {{
            background: #dc3545;
            color: white;
        }}
        
        .no-departures {{
            text-align: center;
            padding: 40px;
            color: #666;
            font-size: 1.2em;
        }}
        
        .last-update {{
            text-align: center;
            color: #666;
            margin-top: 20px;
            font-size: 0.9em;
        }}
        
        .refresh-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-size: 1em;
            cursor: pointer;
            transition: background 0.3s;
            margin-top: 20px;
        }}
        
        .refresh-btn:hover {{
            background: #5568d3;
        }}
        
        @media (max-width: 768px) {{
            h1 {{
                font-size: 1.8em;
            }}
            
            .departure-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚌 MVG Bus Departures</h1>
            <div class="station-info">
                <strong>Station:</strong> {station_name}, {place}
            </div>
            <div class="station-info">
                <strong>Station ID:</strong> {station_id}
            </div>
            <div>
                <span class="info-badge">Line {line_number}</span>
                <span class="info-badge">→ {direction}</span>
            </div>
        </div>
        
        <div class="departures-container">
            <h2 class="section-title">Upcoming Departures</h2>
            {departures_html}
            
            <div class="last-update">
                Last updated: {last_update}
                <br>
                <button class="refresh-btn" onclick="location.reload()">🔄 Refresh</button>
                <div style="margin-top: 10px; font-size: 0.85em;">
                    Page auto-refreshes every 5 minutes
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    return html


def generate_error_page(error_msg):
    """Generate error page."""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MVG Bus Departures - Error</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .error-container {{
            background: white;
            border-radius: 15px;
            padding: 40px;
            max-width: 600px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-align: center;
        }}
        h1 {{
            color: #dc3545;
            margin-bottom: 20px;
        }}
        p {{
            color: #666;
            font-size: 1.1em;
        }}
    </style>
</head>
<body>
    <div class="error-container">
        <h1>⚠️ Error</h1>
        <p>{error_msg}</p>
    </div>
</body>
</html>'''
    return html


if __name__ == "__main__":
    html_content = generate_static_html()
    
    # Create docs directory for GitHub Pages
    os.makedirs("docs", exist_ok=True)
    
    # Write to index.html
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("Static site generated successfully in docs/index.html")
