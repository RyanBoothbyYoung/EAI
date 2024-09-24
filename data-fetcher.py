import yfinance as yf
import pandas as pd

# Scrape the S&P 500 data from Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
table = pd.read_html(url)  # Extract all tables from the URL

# The first table contains the S&P 500 data
sp500_table = table[0]

# Extract the 'Symbol' column as a list of ticker symbols
sp500_tickers = sp500_table['Symbol'].tolist()

# Create an empty DataFrame to store the combined data
combined_df = pd.DataFrame()

# Loop through each ticker and download its data
for ticker in sp500_tickers:
    try:
        # Download historical data from Yahoo Finance
        df = yf.download(ticker, start='2023-01-01', end='2024-01-01')

        # Check if the DataFrame is empty or missing data
        if df.empty:
            print(f"Skipping {ticker}: No data available")
            continue
        
        # Fetch the ticker's financial info (e.g., Price-to-Book, Beta, etc.)
        ticker_info = yf.Ticker(ticker).info

        # Extract key financial metrics
        price_to_book = ticker_info.get('priceToBook', None)
        beta = ticker_info.get('beta', None)
        market_cap = ticker_info.get('marketCap', None)
        forward_pe = ticker_info.get('forwardPE', None)
        dividend_yield = ticker_info.get('dividendYield', None)

        # Add a column to identify the ticker symbol and financial metrics
        df['Ticker'] = ticker
        df['Price_to_Book'] = price_to_book
        df['Beta'] = beta
        df['Market_Cap'] = market_cap
        df['Forward_PE'] = forward_pe
        df['Dividend_Yield'] = dividend_yield

        # Append the data to the combined DataFrame
        combined_df = pd.concat([combined_df, df])
        print(f"Downloaded and added data for {ticker}")

    except Exception as e:
        print(f"ERROR for {ticker}: {e}")

# Save the combined DataFrame to a single CSV file
combined_df.to_csv("csp500_data_with_financials.csv")
print("Saved combined data with financial metrics to sp500_data_with_financials.csv")
