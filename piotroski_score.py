import pandas as pd
import os


def calculate_piotroski_score(ticker):
    try:
        print(f"Processing {ticker}...")  # Debugging
        financials = pd.read_csv(
            f"financial_data/{ticker}_financials.csv", index_col=0)
        balance_sheet = pd.read_csv(
            f"financial_data/{ticker}_balance_sheet.csv", index_col=0)
        cashflow = pd.read_csv(
            f"financial_data/{ticker}_cashflow.csv", index_col=0)

        print(f"Loaded data for {ticker}. Financials: {financials.shape}, Balance Sheet: {
              balance_sheet.shape}, Cashflow: {cashflow.shape}")

        # Check if data exists for required fields
        required_fields = ['Net Income', 'Total Assets',
                           'Total Cash From Operating Activities']
        for field in required_fields:
            if field not in financials.index or financials.loc[field].isna().all():
                print(f"Missing or empty field {field} for {ticker}")
                return None

        # Initialize score
        score = 0

        # Profitability Criteria
        net_income = financials.loc['Net Income', :].iloc[0]
        total_assets = balance_sheet.loc['Total Assets', :].iloc[0]
        roa = net_income / total_assets
        if roa > 0:
            score += 1

        operating_cf = cashflow.loc['Total Cash From Operating Activities', :].iloc[0]
        if operating_cf > 0:
            score += 1

        roa_previous = financials.loc['Net Income', :].iloc[1] / \
            balance_sheet.loc['Total Assets', :].iloc[1]
        if roa > roa_previous:
            score += 1

        if operating_cf > net_income:
            score += 1

        try:
            debt = balance_sheet.loc['Long Term Debt', :].iloc[0]
            debt_previous = balance_sheet.loc['Long Term Debt', :].iloc[1]
            if debt < debt_previous:
                score += 1
        except KeyError:
            print(f"Missing 'Long Term Debt' for {ticker}")

        current_assets = balance_sheet.loc['Total Current Assets', :].iloc[0]
        current_liabilities = balance_sheet.loc['Total Current Liabilities', :].iloc[0]
        current_ratio = current_assets / current_liabilities
        current_ratio_previous = balance_sheet.loc['Total Current Assets',
                                                   :].iloc[1] / balance_sheet.loc['Total Current Liabilities', :].iloc[1]
        if current_ratio > current_ratio_previous:
            score += 1

        gross_profit = financials.loc['Gross Profit', :].iloc[0]
        revenue = financials.loc['Total Revenue', :].iloc[0]
        gross_margin = gross_profit / revenue
        gross_margin_previous = financials.loc['Gross Profit',
                                               :].iloc[1] / financials.loc['Total Revenue', :].iloc[1]
        if gross_margin > gross_margin_previous:
            score += 1

        revenue_previous = financials.loc['Total Revenue', :].iloc[1]
        asset_turnover = revenue / total_assets
        asset_turnover_previous = revenue_previous / \
            balance_sheet.loc['Total Assets', :].iloc[1]
        if asset_turnover > asset_turnover_previous:
            score += 1

        return score
    except Exception as e:
        print(f"Error calculating score for {ticker}: {e}")
        return None


def main():
    results = []
    tickers = ['AAPL', 'MSFT']  # Test with a few tickers
    for ticker in tickers:
        print(f"Calculating Piotroski Score for {ticker}...")
        score = calculate_piotroski_score(ticker)
        if score is not None:
            results.append({'Ticker': ticker, 'Piotroski Score': score})

    results_df = pd.DataFrame(results)
    results_df.to_csv('piotroski_scores.csv', index=False)
    print("Saved Piotroski scores to 'piotroski_scores.csv'.")


if __name__ == "__main__":
    main()
