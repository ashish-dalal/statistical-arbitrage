import yfinance as yf
import pandas as pd

def fetch_data(stocks):
    yf.set_tz_cache_location('disable')
    data_dict = {}
    for ticker in stocks:
        print(f"Download data for: {ticker}")
        yfticker = yf.Ticker(ticker)
        df = yfticker.history(
            period='5y',
            interval='1d',
            auto_adjust=True
        )
        data_dict[ticker] = df
    return data_dict