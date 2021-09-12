import os
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as trade_api
from datetime import date

class Alpaca:
    """
    ///Only for standard stocks and bonds///
    A class that accepts inputs for tickers, the api key, 
    it's secret key, a time frame as well as the amount of 
    years of historical data requested. The object then 
    returns a cleaned dataframe of just close prices and volume.

    Inputs:
        ticker_list = list of tickers that we want data for 
        alpaca_api, alpaca_secret_key = name of alpaca api saved to env variable
        timeframe = expressed as ("1(D,W,M,H,S)")
        endpoint_years = accepts an int amount of years

    Output:
        Cleaned dataframe that stores the close and volume values for each stock
    """
    def __init__(self, ticker_list, timeframe, endpoint_years, alpaca_api=None, alpaca_secret_key=None):
        # Init class variables and set them equal to inputs

        self.ticker_list = ticker_list
        self.alpaca_api = str(alpaca_api)
        self.alpaca_secret_key = str(alpaca_secret_key)
        self.timeframe = timeframe
        self.endpoint_years = endpoint_years

    def load_variables(self):
        # Load environment variables to make api calls

        load_dotenv()

        try:
            self.alpaca_api = os.getenv(self.alpaca_api)
            self.alpaca_secret_key = os.getenv(self.alpaca_secret_key)
        except:
            self.alpaca_api = os.getenv("ALPACA_API_KEY_ENV")
            self.alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY_ENV")


    def create_api_call(self):
        # Set up alpaca api call

        self.alpaca = trade_api.REST(
        self.alpaca_api,
        self.alpaca_secret_key,
        api_version="v2")

        return self.alpaca

    def clean_tickers(self):
        # Take the list of tickers ipnut by the user and properly format for api call

        self.tickers = []
        for ticker in self.ticker_list:
            ticker = ticker.upper()
            self.tickers.append(ticker)

        return self.tickers

    def get_dataframe(self):
        # Make the api call

        # Using the date module and pandas Timedelta we get the current day as the start
        # And using the input from the user we go back x amount of years
        end_date = date.today() - pd.Timedelta(days=1)
        start_date = (end_date - pd.Timedelta(weeks=52*(self.endpoint_years)))

        # Make alpaca api call
        self.df_portfolio = self.alpaca.get_barset(
        self.tickers,
        self.timeframe,
        start = pd.Timestamp(start_date, tz="America/New_York").isoformat(),
        end = pd.Timestamp(end_date, tz="America/New_York").isoformat(),
        limit=1000
        ).df

        return self.df_portfolio

    def clean_dataframe(self):
        # Drop NaN values and set index to a pure date (yyyy-mm-dd)
        self.df_portfolio = self.df_portfolio.dropna()
        self.df_portfolio.index = self.df_portfolio.index.date
        clean_ticker_df = []
        columns = []

        # Set column names and parse dataframe down to just close and volume
        for ticker in self.tickers:

            close = f"{ticker}_close"
            volume = f"{ticker}_volume"

            columns.append(close)
            columns.append(volume)

            ticker = self.df_portfolio[ticker][['close', 'volume']]
            
            clean_ticker_df.append(ticker)

        # Concat resulting dataframes into one main dataframe
        self.clean_df = pd.concat(clean_ticker_df, axis='columns', join='inner')
        self.clean_df.columns = columns

        return self.clean_df

    def run(self):

        self.load_variables()

        self.create_api_call()

        self.clean_tickers()

        self.get_dataframe()

        self.clean_dataframe()

        # print(self.clean_df)
        
        return self.clean_df

tickers = ['aapl']
alpaca_api = "ALPACA_API_KEY_ENV"
alpaca_secret_api = "ALPACA_SECRET_KEY_ENV"
timeframe = "1D"
years = 3


if __name__ == '__main__':
    object = Alpaca(tickers, timeframe, years, alpaca_api, alpaca_secret_api)
    # object = Alpaca(tickers, timeframe, years)
    object.run()