import pandas as pd
import requests
from bs4 import BeautifulSoup


def fetch_sp500_tickers():
    # URL of S&P 500 Wikipedia page
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the table with tickers
    table = soup.find('table', {'id': 'constituents'})
    df = pd.read_html(str(table))[0]

    # Save tickers to CSV
    tickers = df[['Symbol', 'Security']]
    tickers.to_csv('sp500_tickers.csv', index=False)
    print(f"Saved {len(tickers)} tickers to 'sp500_tickers.csv'.")


# Run the function
if __name__ == "__main__":
    fetch_sp500_tickers()
