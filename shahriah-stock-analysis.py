import pandas as pd
import requests

# Define the list of Shariah-compliant stocks
shariah_stocks = ["AAPL", "GOOGL", "MSFT", "AMZN"]

# Fetch stock data from an API (e.g., Alpha Vantage)
api_key = "YOUR_API_KEY"
base_url = "https://www.alphavantage.co/query"

# Create an empty DataFrame to store the stock data
stock_data = pd.DataFrame()

for symbol in shariah_stocks:
    # Construct the API request URL
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": api_key
    }

    # Send the API request
    response = requests.get(base_url, params=params)

    # Parse the JSON response
    json_data = response.json()

    # Extract the daily stock prices from the response
    prices = json_data["Time Series (Daily)"]

    # Convert the prices into a DataFrame
    df = pd.DataFrame(prices).T

    # Rename the columns
    df.columns = ["open", "high", "low", "close", "volume"]

    # Convert the data types of columns
    df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": int})

    # Append the data for the current stock to the main DataFrame
    stock_data = stock_data.append(df)

# Calculate the daily returns for each stock
stock_data["return"] = stock_data.groupby(level=0)["close"].pct_change()

# Calculate the cumulative returns for each stock
stock_data["cumulative_return"] = (1 + stock_data.groupby(level=0)["return"]).cumprod()

# Calculate the overall cumulative return for the portfolio
portfolio_cumulative_return = stock_data["cumulative_return"].product()

# Print the portfolio cumulative return
print("Portfolio Cumulative Return: {:.2f}%".format((portfolio_cumulative_return - 1) * 100))
