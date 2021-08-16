import pandas_datareader.data as pdr
import pandas as pd
from datetime import date, datetime

def cmc200(years):
    """
    Retrieves historical data from the coinmarketcap top 200 cryptocurrencies index.
    Does not return days the stockmarket is closed (May alter analysis but fine for initial purposes)
    Inputs:
        Years (an integer representing the number of years of historical data the user needs for analysis)
    Output:
        A dataframe with the adj_close price of the cmc200 index
    """
    # Set and format date strings for the datareader call.
    end_date = date.today() - pd.Timedelta(days=1)
    start_date = (end_date - pd.Timedelta(weeks=52*(int(years))))

    # Using pandas datareader we get data for the cmc200 index
    df = pdr.DataReader('^CMC200', 'yahoo', start=str(start_date), end=str(end_date))
    df = df.drop(columns=['High', 'Low', 'Open', 'Volume', 'Close'])
    df = df.rename(columns={'Adj Close':'Close'})

    return df

print(cmc200(3))