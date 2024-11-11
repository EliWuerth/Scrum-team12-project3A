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

## Input Validation
The application includes input validation for the following fields:
1. **Stock Symbol**: Must be capitalized and contain 1-7 alphabetic characters (e.g., "AAPL").
2. **Chart Type**: Must be either '1' (line chart) or '2' (bar chart).
3. **Time Series**: Must be one of the following: '1' (Intraday), '2' (Daily), '3' (Weekly), '4' (Monthly).
4. **Start Date**: Must be in the format YYYY-MM-DD.
5. **End Date**: Must also be in the format YYYY-MM-DD.

## Unit Testing
The project includes unit tests to ensure that the input validation functions work as expected. The tests cover various valid and invalid cases for each input type.

### Running Unit Tests
To run the unit tests, ensure you have Python installed and navigate to the directory where the test file is located. Then run the following command:

```bash
python test_input_validation.py
```

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
├── stocks.csv          # Stock symbols data
├── static/             # Generated charts
├── templates/          # HTML templates
└── mod13_emwcd7.py  # Unit tests for input validation
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