import pandas as pd 
import matplotlib.pyplot as pyplot
from polygon import RESTClient

key = ""g


with RESTClient(key) as client:
        from_ = "2019-01-01"
        to = "2021-08-01"
        resp = client.stocks_equities_aggregates("SPY", 1, "day", from_, to, unadjusted=False)
      
        ds=pd.DataFrame.from_records(resp.results,index="t")
        print(ds.head())
        
        crypto=client.crypto_aggregates("X:XRPUSD",1, "day", from_, to, unadjusted=False)
        XRP=pd.DataFrame.from_records(crypto.results,index="t")
        print(XRP.head())
        XRP["daily_returns"]=XRP["c"].pct_change().dropna()
        ds["daily_returns"]=ds["c"].pct_change().dropna()
        XRP["cumulative"]=(XRP["daily_returns"]+1).cumprod()
        ds["cumulative"]=(ds["daily_returns"]+1).cumprod()
        XRP["cumulative"].plot()