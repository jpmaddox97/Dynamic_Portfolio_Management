from data_retrieval import alpaca
from data_retrieval import crypto_market
from data_retrieval import getbinance
from functions_graphs import functions
from user_input import risk_assesment
import pandas as pd
print("----------IGNORE ABOVE----------")
# permutations = ra.get_user_risk_tolerance()

# print(permutations)

# Creating Order Book

# Assign a weight of 70%
# Crypto list = ADA, BNB, BTC, DOT, ETH, LINK, LTC, VET, XLM, XRP
# Low = BTC, ETH, LTC
# Med = ADA, BNB, XLM
# High = LINK, DOT, VET, XRP
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

# cryptos = ['ADA', 'BNB', 'BTC', 'DOT', 'ETH', 'LINK', 'LTC', 'VET', 'XLM', 'XRP']
# crypto_df = []

# for ticker in cryptos:

#     call = gb.Binance(ticker, 3)
#     df = call.run()
#     crypto_df.append(df)

# print(crypto_df)

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
        df = funct.daily_returns()
        df.dropna(inplace=True)

        crypto_std[ticker] = funct.standard_deviation()
#         display(df.head())
    return crypto_std

def sort_crypto_std(crypto_std):
    # Returns a dictionary with all crypto std's sorted from low to high risk
    high_risk = {}
    med_risk = {}
    low_risk = {}
    for ticker, std in crypto_std.items():
        if float(std) <= 0.057:
            low_risk[ticker] = std
        if float(std) > 0.057 and float(std) <= 0.073:
            med_risk[ticker] = std
        if float(std) > 0.073:
            high_risk[ticker] = std


    return {"low":low_risk, "med":med_risk, "high":high_risk}

user_info = risk_assesment.get_user_risk_tolerance_port()
print("----------User Info----------")
for i, v in user_info.items():
    print(f"{i}: {v}")

dictionary = get_crypto_dict()
crypto_std = get_std(dictionary)
sorted_std = sort_crypto_std(crypto_std)

for t,v in sorted_std['low'].items():
    print(f"Low Risk Cryptos - {t}:{v}")
print("----------")
for t,v in sorted_std['med'].items():
    print(f"Medium Risk Cryptos - {t}:{v}")  
print("----------")
for t,v in sorted_std['high'].items():
    print(f"High Risk Cryptos - {t}:{v}")

i_amount = user_info["Investment Amount"]

len_crypto = []
if user_info['risk tolerance'] == 'High':
    for t, v in sorted_std['high'].items():
        len_crypto.append(t)
elif user_info['risk tolerance'] == 'Medium':
    for t, v in sorted_std['med'].items():
        len_crypto.append(t)
elif user_info['risk tolerance'] == 'Low':
    for t, v in sorted_std['low'].items():
        len_crypto.append(t)

crypto_risk_allotment = i_amount * 0.7
price_per_crypto = crypto_risk_allotment / len(len_crypto)

for ticker in len_crypto:
    print(f"Purchase ${price_per_crypto} of {ticker}")
    
print(f"This should equal 70%, ${crypto_risk_allotment}, of your stated initial investment amount of {user_info['Investment Amount']}")