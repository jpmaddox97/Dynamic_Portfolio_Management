import os
from dotenv import load_dotenv
from binance.client import Client
import pandas as pd
import datetime
import time


def Binance(symbol, years):
    """
    Gets historical crypto data from the binance API
    Inputs:
        Symbol as shown on exchanges, years(int) of historical data to get the
    Outputs:
        A dataframe with date as index, close and volume data
    """

        
    years = int(years)

    # Format symbol for api call
    symbol = symbol.upper()
    binance_symbol = f"{symbol}USDT"

    # Load environment vairables
    # Set variables to binance api key env files
    load_dotenv()
    binance_api = os.getenv("BINANCE_API")
    binance_secret = os.getenv("BINANCE_SECRET")

    # Create api client variable
    client = Client(binance_api, binance_secret)

    # Create and format date
    start_date = datetime.date.today() - pd.Timedelta(weeks=52*years)
    start_date = start_date.strftime("%d %b, %Y")

    # make api call and get returned data
    candles = client.get_historical_klines(binance_symbol, Client.KLINE_INTERVAL_1DAY, limit=1000, start_str=start_date) 

    # Create and format dataframe 
    # Returns close and volume with date as index
    columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'close time', 'quote asset volume', 
    'number of trades', 'taker buy base asset volume', 'taker buy quote asset volume', 'ignore']
    df = pd.DataFrame(candles, columns=columns)

    mills = df['date']
    date = pd.Series([datetime.datetime.fromtimestamp(mill/1000) for mill in mills])

    # Combine dataframes and drop columns
    df = pd.concat([date, df], axis=1, join='inner')
    df = df.drop(columns=['date', 'open', 'high', 'low', 'close time', 'quote asset volume', 'number of trades', 
    'taker buy base asset volume', 'taker buy quote asset volume', 'ignore'], axis=1)

    # Set data type to float
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    # Rename columns with ticker values
    df = df.rename(columns={0:'date', 'close':f'{binance_symbol}_Close', 'volume':f'{binance_symbol}_Volume'})

    # Set date index
    df = df.set_index(['date'])
    df.index = df.index.date

    return df