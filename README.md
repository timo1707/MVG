# MVG Bus Departure Checker

A Python application that checks bus departures for line 180 at Olympiazentrum station in direction Berduxstraße using the MVG (Münchner Verkehrsgesellschaft) API.

## Features

- Retrieves station ID for "Olympiazentrum" station
- Fetches real-time departure information
- Filters departures for bus line 180 heading to Berduxstraße
- Displays departure times in human-readable format (YYYY-MM-DD HH:MM:SS)
- **Web interface** with Flask application
- **Static website** deployed to GitHub Pages with automatic updates

## Requirements

- Python 3.x
- mvg package (https://github.com/mondbaron/mvg)
- Flask (for web application)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/timo1707/MVG.git
cd MVG
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Run the console application:
```bash
python mvg_app.py
```

The app will:
1. Look up the station ID for "Olympiazentrum"
2. Fetch upcoming departures
3. Filter and display departures for line 180 to Berduxstraße

### Web Application

Run the Flask web application:
```bash
python app.py
```

For development with debug mode enabled:
```bash
FLASK_DEBUG=true python app.py
```

Then open your browser and navigate to `http://localhost:5000` to see the web interface with:
- Real-time departure information
- Beautiful, responsive design
- Color-coded delays (green for on-time, yellow for minor delays, red for major delays)
- Auto-refresh functionality

#### API Endpoints

The Flask app provides multiple JSON API endpoints:

1. **Formatted Departures** - Returns formatted data with human-readable times:
   ```
   GET http://localhost:5000/api/departures
   ```

2. **Raw Departures** - Returns unformatted raw API response (perfect for iOS Shortcuts):
   ```
   GET http://localhost:5000/raw
   ```
   
   Returns departure data with Unix timestamps and all original fields from the MVG API.

## GitHub Pages Deployment

The repository automatically deploys a static version of the departure board to GitHub Pages:

- **Live Site**: https://timo1707.github.io/MVG/
- **Raw JSON Data**: https://timo1707.github.io/MVG/raw.json (for iOS Shortcuts)
- Updates every 5 minutes via GitHub Actions
- No server required - pure static HTML

### GitHub Actions Workflows

The repository includes two GitHub Actions workflows:

1. **MVG Check** (`.github/workflows/mvg_check.yml`):
   - Runs the console app to check departures
   - Triggers: push, pull requests, hourly schedule, manual

2. **Deploy to GitHub Pages** (`.github/workflows/deploy_pages.yml`):
   - Generates static HTML with current departure data
   - Deploys to GitHub Pages
   - Triggers: push, manual, every 5 minutes

## Project Structure

```
MVG/
├── mvg_app.py              # Console application
├── app.py                  # Flask web application
├── generate_static.py      # Static site generator for GitHub Pages
├── templates/
│   └── index.html         # Flask HTML template
├── requirements.txt        # Python dependencies
├── .github/
│   └── workflows/
│       ├── mvg_check.yml          # Console app workflow
│       └── deploy_pages.yml       # GitHub Pages deployment
└── README.md
```

## License

This project uses the unofficial MVG API. Please note that MVG tolerates private, non-commercial moderate use of their API, but data mining is explicitly not allowed.