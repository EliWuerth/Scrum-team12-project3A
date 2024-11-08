from flask import Flask, render_template, request
import requests
import pygal
import csv
from lxml import etree
from datetime import datetime
import os

app = Flask(__name__)
app.config["DEBUG"] = True

# Function to validate date inputs
def validate_dates(start_date, end_date):
    """Validate date inputs"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        if end < start:
            return False, "End date must be after start date"
        if end > datetime.now():
            return False, "End date cannot be in the future"
        return True, ""
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD"

# Function to get stock data from Alpha Vantage
def get_stock_data(symbol, function):
    api_key = "3B5JUABSNGNCK67I"
    # Add interval parameter for intraday data
    if function == "TIME_SERIES_INTRADAY":
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval=5min&apikey={api_key}'
    else:
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}'
    
    print(f"Requesting URL: {url}")  # Debug print
    response = requests.get(url)
    data = response.json()
    
    # Print response for debugging
    if 'Error Message' in data:
        print(f"API Error: {data['Error Message']}")
    elif 'Note' in data:
        print(f"API Note: {data['Note']}")
    else:
        print(f"Available keys in response: {data.keys()}")
        
    return data

# Load stock symbols from a CSV file using the csv module
def load_stock_symbols():
    stock_symbols = []
    try:
        with open('stocks.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                stock_symbols.append(row['Symbol'])  # Assuming the header is 'Symbol'
        return stock_symbols
    except FileNotFoundError:
        print("Warning: stocks.csv file not found")
        return []

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    stock_data = None
    chart_file = None
    error_message = None
    stock_symbols = load_stock_symbols()
    
    if request.method == 'POST':
        print("Form data:", request.form)
        try:
            symbol = request.form.get('stock_symbols')
            chart_type = request.form.get('chartType')
            function = request.form.get('timeSeries')
            start_date = request.form.get('startDate')
            end_date = request.form.get('endDate')

            # Input validation
            if not all([symbol, function, start_date, end_date, chart_type]):
                raise ValueError("All fields are required")

            # Date validation
            is_valid, date_error = validate_dates(start_date, end_date)
            if not is_valid:
                raise ValueError(date_error)

            # Get stock data
            stock_data = get_stock_data(symbol, function)
            
            # API error checking
            if 'Error Message' in stock_data:
                raise ValueError(f"API Error: {stock_data.get('Error Message')}")
            if 'Note' in stock_data:
                raise ValueError(f"API Limit: {stock_data.get('Note')}")

            # Process and plot data
            dates, open_prices, high_prices, low_prices, closing_prices = process_data(stock_data, start_date, end_date, function)
            
            if not dates:
                raise ValueError("No data available for the selected date range")

            chart_file = plot_data(dates, open_prices, high_prices, low_prices, closing_prices, chart_type, symbol)

        except ValueError as e:
            error_message = str(e)
            print(f"Validation error: {str(e)}")
        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            print(f"Error details: {e}")
            stock_data = {"error": str(e)}

    return render_template('index.html', 
                         stock_symbols=stock_symbols,
                         stock_data=stock_data,
                         chart_file=chart_file,
                         error_message=error_message)

def process_data(data, start_date, end_date, function):
    # Different time series have different keys in the JSON response
    time_series_keys = {
        "TIME_SERIES_DAILY": "Time Series (Daily)",
        "TIME_SERIES_WEEKLY": "Weekly Time Series",
        "TIME_SERIES_MONTHLY": "Monthly Time Series",
        "TIME_SERIES_INTRADAY": "Time Series (5min)"  # For intraday data
    }
    
    # Get the correct key for the time series
    time_series_key = time_series_keys.get(function)
    if not time_series_key:
        print(f"Unsupported function: {function}")
        print("Available data in response:", data.keys())  # Debug print
        return [], [], [], [], []
        
    # Get the time series data
    time_series = data.get(time_series_key, {})
    if not time_series:
        print("No time series data found. Available keys:", data.keys())
        print("Full response data:", data)  # Debug print
        return [], [], [], [], []

    print(f"Processing {function} data")
    print("Available dates in API response:", time_series.keys())
    dates = []
    open_prices = []
    high_prices = []
    low_prices = []
    closing_prices = []
    
    for date, values in time_series.items():
        # For intraday, only use the date part for comparison
        compare_date = date.split()[0] if function == "TIME_SERIES_INTRADAY" else date
        
        if start_date <= compare_date <= end_date:
            dates.append(date)
            try:
                open_prices.append(float(values['1. open']))
                high_prices.append(float(values['2. high']))
                low_prices.append(float(values['3. low']))
                closing_prices.append(float(values['4. close']))
            except (KeyError, ValueError) as e:
                print(f"Error processing values for date {date}: {e}")
                print("Values received:", values)
                continue

    # Sort data by date
    if dates:
        sorted_data = sorted(zip(dates, open_prices, high_prices, low_prices, closing_prices))
        dates = [item[0] for item in sorted_data]
        open_prices = [item[1] for item in sorted_data]
        high_prices = [item[2] for item in sorted_data]
        low_prices = [item[3] for item in sorted_data]
        closing_prices = [item[4] for item in sorted_data]
    else:
        print("No data found for the specified date range")

    print(f"Processed {len(dates)} data points")
    return dates, open_prices, high_prices, low_prices, closing_prices

def plot_data(dates, open_prices, high_prices, low_prices, closing_prices, chart_type, symbol):
    if chart_type.lower() == 'line':
        chart = pygal.Line(title=f'Stock Price for {symbol}', 
                          x_title='Date',
                          y_title='Price',
                          x_label_rotation=45)  # Rotate labels for better readability
    elif chart_type.lower() == 'bar':
        chart = pygal.Bar(title=f'Stock Price for {symbol}',
                         x_title='Date',
                         y_title='Price',
                         x_label_rotation=45)
    else:
        print("Unsupported chart type.")
        return None
    
    # Ensure static directory exists
    os.makedirs('static', exist_ok=True)
    
    # Format dates for better display
    formatted_dates = []
    for date in dates:
        if ' ' in date:  # Intraday data
            dt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            formatted_dates.append(dt.strftime('%Y-%m-%d %H:%M'))
        else:  # Daily/Weekly data
            formatted_dates.append(date)
    
    chart.x_labels = formatted_dates
    chart.add('Open', open_prices)
    chart.add('High', high_prices)
    chart.add('Low', low_prices)
    chart.add('Close', closing_prices)

    # Save to static folder
    chart_file = 'static/stock_price_chart.svg'
    chart.render_to_file(chart_file)
    return chart_file

if __name__ == '__main__':
    # Ensure static directory exists
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=8080)