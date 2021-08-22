#%%
from datetime import date
import pandas as pd
import MCForecastTools
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame


PUBLIC_ALPACA= "PKJ0AKA1AOARSOXTX7DK"
SECRET_ALPACA= "HB8vLd8SL6corG8lFqWiqUGVQ5E3hbyYLqktPclf"
api=tradeapi.REST(PUBLIC_ALPACA, SECRET_ALPACA)
timeframe="1D"

# Format current date as ISO format
# Set both the start and end date at the date of your prior weekday 
# This will give you the closing price of the previous trading day
# Alternatively you can use a start and end date of 2020-01-07 

start_date=pd.Timestamp("2020-01-07", tz="America/New_York").isoformat()
end_date=pd.Timestamp("2021-08-07", tz="America/New_York").isoformat()
aapl=api.get_barset(["AAPL","CSCO","MSFT","GMC200"],timeframe,start=start_date,end=end_date,limit=1000).df
sim=MCForecastTools.MCSimulation(aapl,[.25,.25,.25,.25],500,252)
sim.calc_cumulative_return()
sim.plot_simulation()



"""
aapl=pd.read_csv("HistoricalData_aapl.csv")
csco=pd.read_csv("HistoricalData_csco.csv")
msft=pd.read_csv("HistoricalData_msft.csv")
print(aapl.head())
print(csco.head())
print(msft.head())


#forcast_aapl=MCForecastTools.MCSimulation(aapl,num_simulation=10,num_trading_days=252)

aapl=aapl.rename(columns={"Close/Last":"close"})
csco=csco.rename(columns={"Close/Last":"close"})
msft=msft.rename(columns={"Close/Last":"close"})

#forcast_aapl=MCForecastTools.MCSimulation(aapl,num_simulation=10,num_trading_days=252)
col_list=[]
for item in aapl.columns:
    col_list.append( ("aapl",item)) 
idx=pd.MultiIndex.from_tuples(col_list)

print(idx)
#aapl.(idx,axis="columns")
print(aapl.head())
#forcast_aapl=MCForecastTools.MCSimulation(aapl,num_simulation=10,num_trading_days=252)
test = idx.to_frame()
print(test.head())
"""