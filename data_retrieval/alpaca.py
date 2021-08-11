import os
import pandas as pd
import json
import requests
from dotenv import load_dotenv
import alpaca_trade_api as trade_api
from datetime import date

class Alpaca:

    def __init__(self, ticker_list, alpaca_api, alpaca_secret_key, timeframe, endpoint_years):
        self.ticker_list = ticker_list
        self.alpaca_api = alpaca_api
        self.alpaca_secret_key = alpaca_secret_key
        self.timeframe = timeframe
        self.endpoint_years = endpoint_years

    def load_variables(self):
        load_dotenv()
        self.alpaca_api = os.getenv(self.alpaca_api)
        self.alpaca_secret_key = os.getenv(self.alpaca_secret_key)


    def create_api_call(self):
        self.alpaca = trade_api.REST(
        self.alpaca_api,
        self.alpaca_secret_key,
        api_version="v2")
        return self.alpaca

    def clean_tickers(self):
        self.tickers = []
        for ticker in self.ticker_list:
            ticker = ticker.upper()
            self.tickers.append(ticker)

        # print(self.tickers)

        return self.tickers

    def get_dataframe(self):
        end_date = date.today() - pd.Timedelta(days=1)
        start_date = (end_date - pd.Timedelta(weeks=52*(self.endpoint_years)))
        self.df_portfolio = self.alpaca.get_barset(
        self.tickers,
        self.timeframe,
        start = pd.Timestamp(start_date, tz="America/New_York").isoformat(),
        end = pd.Timestamp(end_date, tz="America/New_York").isoformat(),
        limit=1000
        ).df
        
        # print(type(self.df_portfolio))
        # print(self.df_portfolio)

        return self.df_portfolio

    def clean_dataframe(self):
        self.df_portfolio = self.df_portfolio.dropna()
        self.df_portfolio.index = self.df_portfolio.index.date
        clean_ticker_df = []
        columns = []

        for ticker in self.tickers:

            close = f"{ticker}_close"
            volume = f"{ticker}_volume"

            columns.append(close)
            columns.append(volume)

            ticker = self.df_portfolio[ticker][['close', 'volume']]
            
            clean_ticker_df.append(ticker)
            

        # for df in clean_ticker_df:
        #     print(df)

        self.clean_df = pd.concat(clean_ticker_df, axis='columns', join='inner')
        self.clean_df.columns = columns

        # print(columns)
        # print(self.clean_df)

        return self.clean_df

#    def sample_df(self):
#        self.clean_df.head()
#        self.clean_df.tail()

    def run(self):

        self.load_variables()

        self.create_api_call()

        self.clean_tickers()

        self.get_dataframe()

        self.clean_dataframe()

    #    self.sample_df()
        print(self.clean_df)
        
        return self.clean_df

tickers = ['aapl', 'msft', 'csco']
alpaca_api = "ALPACA_API_KEY_ENV"
alpaca_secret_api = "ALPACA_SECRET_KEY_ENV"
timeframe = "1D"
years = 3


if __name__ == '__main__':
    object = Alpaca(tickers, alpaca_api, alpaca_secret_api, timeframe, years)
    object.run()