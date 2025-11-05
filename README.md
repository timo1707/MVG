# MVG Bus Departure Checker

A Python application that checks bus departures for line 180 at Olympiazentrum station in direction Berduxstraße using the MVG (Münchner Verkehrsgesellschaft) API.

## Features

- Retrieves station ID for "Olympiazentrum" station
- Fetches real-time departure information
- Filters departures for bus line 180 heading to Berduxstraße
- Displays departure times, delays, and transport type

## Requirements

- Python 3.x
- mvg package (https://github.com/mondbaron/mvg)

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

Run the application:
```bash
python mvg_app.py
```

The app will:
1. Look up the station ID for "Olympiazentrum"
2. Fetch upcoming departures
3. Filter and display departures for line 180 to Berduxstraße

## GitHub Actions Workflow

The repository includes a GitHub Actions workflow (`.github/workflows/mvg_check.yml`) that automatically runs the app:

- On every push to main/master branch
- On pull requests
- On a schedule (every hour)
- Manually via workflow dispatch

## License

This project uses the unofficial MVG API. Please note that MVG tolerates private, non-commercial moderate use of their API, but data mining is explicitly not allowed.