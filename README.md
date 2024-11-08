# Scrum Team 12 Project 3A

# Stock Data Visualization Web Application

## Features
- Interactive web interface for stock data visualization
- Multiple time series support:
  - Intraday (5-minute intervals)
  - Daily
  - Weekly
  - Monthly
- Chart types:
  - Line chart with improved readability
  - Bar chart with formatted labels
- Error handling and validation:
  - Date range validation
  - API error handling
  - User input validation
- Responsive web design with loading indicators

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Alpha Vantage API key (provided in code)

### Running the Application
1. Clone the repository:
```bash
git clone https://github.com/EliWuerth/Scrum-team12-project3A
cd Scrum-team12-project3A
```

2. Build and start the container:
```bash
docker-compose up --build -d
```

3. Access the application:
```
http://localhost:8080
```

4. Stop the application:
```bash
docker-compose down
```

## Usage Guide
1. Select a stock symbol from the dropdown
2. Choose chart type (Line/Bar)
3. Select time series type:
   - Intraday: 5-minute interval data
   - Daily: Day-by-day data
   - Weekly: Weekly summary
   - Monthly: Monthly summary
4. Enter date range
5. Click Generate to view the chart

## Project Structure
```
├── app.py              # Main Flask application
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Python dependencies
├── stocks.csv         # Stock symbols data
├── static/            # Generated charts
└── templates/         # HTML templates
```

## Improvements Made
- Fixed data processing for all time series types
- Added comprehensive error handling
- Improved UI with loading indicators
- Enhanced date validation
- Added debug logging
- Improved chart formatting
- Added responsive design elements
- Fixed weekly and monthly data processing

## Contributors
- Scrum team 12

## Technologies Used
- Python/Flask
- Docker/Docker Compose
- Alpha Vantage API
- HTML/CSS/JavaScript