import pprint, os
from dotenv import load_dotenv
from binance.client import Client
import pandas as pd
import datetime
import time


class Binance():

    def __init__(self, symbol, years):
        self.symbol = symbol
        self.years = int(years)

    def run(self): 

        # Format symbol for api call
        self.symbol = self.symbol.upper()
        binance_symbol = f"{self.symbol}USDT"

        # Load environment vairables
        load_dotenv()
        binance_api = os.getenv("BINANCE_API")
        binance_secret = os.getenv("BINANCE_SECRET")

        # Create api client variable
        client = Client(binance_api, binance_secret)

        # Create and format date
        start_date = datetime.date.today() - pd.Timedelta(weeks=52*self.years)
        start_date = start_date.strftime("%d %b, %Y")

        # make api call and get returned data
        candles = client.get_historical_klines(binance_symbol, Client.KLINE_INTERVAL_1DAY, limit=1000, start_str=start_date) 

        # Create and format dataframe 
        # Returns close and volume with date as index
        columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'close time', 'quote asset volume', 'number of trades', 'taker buy base asset volume', 'taker buy quote asset volume', 'ignore']
        df = pd.DataFrame(candles, columns=columns)
        mills = df['date']
        date = pd.Series([datetime.datetime.fromtimestamp(mill/1000) for mill in mills])
        df = pd.concat([date, df], axis=1, join='inner')
        df = df.drop(columns=['date', 'open', 'high', 'low', 'close time', 'quote asset volume', 'number of trades', 'taker buy base asset volume', 'taker buy quote asset volume', 'ignore'], axis=1)
        df = df.rename(columns={0:'date'})
        df = df.set_index(['date'])
        df.index = df.index.date

        return df