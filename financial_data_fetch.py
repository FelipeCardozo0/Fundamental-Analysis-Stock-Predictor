import pandas as pd
import yfinance as yf
import os

# Load tickers from the CSV file


def load_tickers(file_path):
    tickers_df = pd.read_csv(file_path)
    return tickers_df['Symbol'].tolist()

# Fetch financial data for a single ticker


def fetch_financial_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        financials = {
            "balance_sheet": stock.balance_sheet,
            "cashflow": stock.cashflow,
            "financials": stock.financials
        }
        return financials
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Save financial data to files


def save_financial_data(ticker, data):
    os.makedirs('financial_data', exist_ok=True)
    for key, value in data.items():
        if value is not None:
            file_path = os.path.join('financial_data', f"{ticker}_{key}.csv")
            value.to_csv(file_path)
            print(f"Saved {key} data for {ticker} to {file_path}")

# Main function


def main():
    tickers = load_tickers('sp500_tickers.csv')
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        financial_data = fetch_financial_data(ticker)
        if financial_data:
            save_financial_data(ticker, financial_data)


# Run the script
if __name__ == "__main__":
    main()
