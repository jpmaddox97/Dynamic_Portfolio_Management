from data_retrieval import alpaca
from data_retrieval import crypto_market
from data_retrieval import getbinance
from data_retrieval import sp500_index

from functions_graphs import functions
from user_input import risk_assesment

import pandas as pd
import hvplot
import numpy as np

# print("----------IGNORE ABOVE----------")
# Creating Order Book

# Assign a weight of 70%
# Crypto list = ADA, BNB, BTC, DOT, ETH, LINK, LTC, VET, XLM, XRP
# .041-.089
# Create bins for risk tolerance level - If std is below some_low_std() goes into low risk
# 0.0 -.057 Low
# .057 - .073 Med
# .073 - 1 High

#Assign a weight of 30%
# S&P 500 - Blue chips, large cap, top 500 representative of stock market (Broad index)
# Nasdaq - Smaller cap, a lot of overlap between these two
# Russel - Smallest cap
# Pick crypto based of market cap realtion to index

def get_crypto_dict():
    # Returns a dictionary with ticker as index and its dataframe as a value
    cryptos = ['ADA', 'BNB', 'BTC', 'DOT', 'ETH', 'LINK', 'LTC', 'VET', 'XLM', 'XRP']
    crypto_dict = {}
    for ticker in cryptos:
        df = getbinance.Binance(ticker, 3)
        df = pd.DataFrame(df)
        crypto_dict[ticker] = df

    return crypto_dict

def get_std(crypto_dfs):
    # Returns a dictionary of all crypto stds
    cryptos = ['ADA', 'BNB', 'BTC', 'DOT', 'ETH', 'LINK', 'LTC', 'VET', 'XLM', 'XRP']
    crypto_std = {}
    for ticker in cryptos:
        df = crypto_dfs[ticker]
        c_name = f"{ticker}USDT_Close"
        funct = functions.Functions(df, c_name)
        daily_returns = funct.daily_returns()
        daily_returns.dropna(inplace=True)

        crypto_std[ticker] = funct.standard_deviation()
    return crypto_std

def get_sharpe(crypto_dfs):
    # Set a list of all the cryptos
    cryptos = ['ADA', 'BNB', 'BTC', 'DOT', 'ETH', 'LINK', 'LTC', 'VET', 'XLM', 'XRP']
    crypto_sharpe = {}

    # Loop through list and make a dictionary of sharpe ratios
    for ticker in cryptos:
        df = crypto_dfs[ticker]
        c_name = f"{ticker}USDT_Close"
        funct = functions.Functions(df, c_name)

        crypto_sharpe[ticker] = funct.sharpe_ratio()
    
    return crypto_sharpe

def sort_crypto_std(crypto_std):
    # Returns a dictionary with all crypto std's sorted from low to high risk
    high_risk = {}
    med_risk = {}
    low_risk = {}

    # Separates tickers based on std
    for ticker, std in crypto_std.items():
        if float(std) <= 0.057:
            low_risk[ticker] = std
        elif float(std) > 0.057 and float(std) <= 0.073:
            med_risk[ticker] = std
        elif float(std) > 0.073:
            high_risk[ticker] = std
    return {"low":low_risk, "med":med_risk, "high":high_risk}

def sort_crypto_sharpe(crypto_sharpe):
    high_risk = {}
    med_risk = {}
    low_risk = {}

    # Is supposed to separate sharpes based on their value,
    # but it's reading sharpe as a dataframe
    for ticker, sharpe in crypto_sharpe.items():
        if float(sharpe) <= 0.5:
            high_risk[ticker] = sharpe
        elif float(sharpe) > 0.5 and float(sharpe) <= 1.5:
            med_risk[ticker] = sharpe
        elif float(sharpe) > 1.5:
            low_risk[ticker] = sharpe

    return {"low":low_risk, "med":med_risk, "high":high_risk}

print("----------Dynamic Portfolio Management - Version 1.0----------")

user_info = risk_assesment.get_user_risk_tolerance_port()
print("----------User Info----------")
# Print user risk assessment dictionary
for i, v in user_info.items():
    print(f"{i}: {v}")
print("\n")

# Stores a "crypto ticker" : value, dictionary in a variable
# And calls the sort function to get
dictionary = get_crypto_dict()
sorted_std = sort_crypto_std(get_std(dictionary))

crypto_sharpe = get_sharpe(dictionary)

# Until the sharpe ratio function this keeps the code running
try:
    sorted_sharpe = sort_crypto_sharpe(dictionary)
except:
    pass
try:
    print(sorted_sharpe)
except:
    pass

print("\n")
print("----------Crypto Risk----------")

# Prints out all of the crypto bins
for t,v in sorted_std['low'].items():
    print(f"Low Risk Cryptos - {t}:{v}")
print("----------")
for t,v in sorted_std['med'].items():
    print(f"Medium Risk Cryptos - {t}:{v}")  
print("----------")
for t,v in sorted_std['high'].items():
    print(f"High Risk Cryptos - {t}:{v}")

# Get user initial investment
i_amount = user_info["Investment Amount"]

# takes input from the user and selects the appropriate bin
len_crypto = []
# Make high bin
if user_info['risk tolerance'] == 'High':
    for t, v in sorted_std['high'].items():
        len_crypto.append(t)
        for t, v in sorted_std['med'].items():
            len_crypto.append(t)
            for t, v in sorted_std['low'].items():
                len_crypto.append(t)

# Make medium bin               
elif user_info['risk tolerance'] == 'Medium':
    for t, v in sorted_std['med'].items():
        len_crypto.append(t)
        for t, v in sorted_std['low'].items():
            len_crypto.append(t)

# Make low bin
elif user_info['risk tolerance'] == 'Low':
    for t, v in sorted_std['low'].items():
        len_crypto.append(t)

# Calculate weighting for risk portion of portfolio
# using weighting get price per crypto
crypto_risk_allotment = i_amount * 0.7
price_per_crypto = crypto_risk_allotment / len(len_crypto)

print("\n")
print("----------Order Book----------")

# Print risk order book
for ticker in len_crypto:
    print(f"Purchase ${price_per_crypto} of {ticker}")

print(f"This should equal 70%, ${crypto_risk_allotment}, of your stated initial investment amount of {user_info['Investment Amount']}")
print("\n")

# Using BTC, ETH and LTC as a benchmark for the s&p we allot the last 30% to these cryptos
snp_crypto = ['BTC', 'ETH', 'LTC']

crypto_index_allotment = i_amount * 0.3
price_per_crypto_i = crypto_index_allotment / len(snp_crypto)


# Print index order book
for ticker in snp_crypto:
    print(f"Purchase ${price_per_crypto_i} of {ticker}")

print(f"This should equal 30%, ${crypto_index_allotment}, of your stated initial investment amount of {user_info['Investment Amount']}")

# Pull info for user's stock portfolio
tickers = []
for ticker, shares in user_info['Stock Portfolio'].items():
    tickers.append(ticker)

# Api env variables
alpaca_api = "ALPACA_API_KEY_ENV"
alpaca_secret_api = "ALPACA_SECRET_KEY_ENV"

# Make the call to alpaca
alpaca_call = alpaca.Alpaca(tickers, '1D', 1, alpaca_api, alpaca_secret_api)
stocks_df = alpaca_call.run()

# Prints the last closing price of each stock in the portfolio
close_values = []
stock_port = {}
for ticker in tickers:
    close = f"{ticker.upper()}_close"
    stock_port[ticker] = [close]
    close_v = stocks_df[close][-1]
    print(f"{ticker} closed at {close_v}")
    close_values.append(close_v)
print("\n")
print("----------Stock Portfolio Value----------")

# Multiply last closing price by share amount and store in list
portfolio_value = []
for value in close_values:
    for ticker, share in user_info['Stock Portfolio'].items():
        ticker = float(value) * float(share)
        portfolio_value.append(ticker)

# Sum the values in the list to get total portfolio value
portfolio_value = sum(portfolio_value)

print(f"The current value of your stock portfolio is ${portfolio_value}")

# Get CMC close
cmc = crypto_market.cmc200(1)
cmc.columns = ['CMC_close']

# Get S&P 500 close
sp500 = sp500_index.sp500(1)
sp500.columns = ['SP500_close']

# Concat dataframe of indexes
index = pd.concat([sp500, cmc], axis=1)
index.dropna(inplace=True)

# Plot of both indexes daily close
index_overlay_plot = index.hvplot.line(title='CMC200 and S&P500 Overlayed')

# Rolling mean of both indexes
sp_cmc = index.rolling(window=30).mean().dropna()

# Plot of rolling 30 mean indexes
sp_cmc.hvplot.line(title='CMC200 and S&P500 Overlayed - 30 Day')

# Aggregate average of indexes 30 day
sp_cmc_avg = index.mean(axis=1)
sp_cmc_avg_30 = sp_cmc_avg.rolling(window=30).mean()

# Aggregate plotted
sp_cmc_avg_30_plot = sp_cmc_avg_30.hvplot.line(title='CMC200 and S&P500 Aggregate - 30 Day')

for t, df in stock_port.items():
    print(df.head())