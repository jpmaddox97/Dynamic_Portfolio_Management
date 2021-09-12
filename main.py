from data_retrieval import alpaca
from data_retrieval import crypto_market
from data_retrieval import getbinance
from data_retrieval import sp500_index

from functions_graphs import functions
from user_input import risk_assesment
from data_retrieval import MCForecastTools as mc

from collections import Counter

import pandas as pd
import hvplot.pandas
import numpy as np
import fbprophet as fb

# Functions for program operations

# This creates a crypto dictionary
def get_crypto_dict():
    """Returns a dictionary with ticker as index and its dataframe as a value"""

    cryptos = [
        'ADA', 
        'BNB', 
        'BTC', 
        'DOT', 
        'ETH', 
        'LINK', 
        'LTC', 
        'VET', 
        'XLM', 
        'XRP'
        ]
    crypto_dict = {}

    for ticker in cryptos:
        # Get ticker data from Binance
        df = getbinance.Binance(ticker, 3)
        df = pd.DataFrame(df)
        # Append to dictionary
        crypto_dict[ticker] = df

    return crypto_dict

# This gets the standard deviation for crypto
def get_std(crypto_dfs):
    """Returns a dictionary of all crypto stds"""

    cryptos = [
        'ADA', 
        'BNB', 
        'BTC', 
        'DOT', 
        'ETH', 
        'LINK', 
        'LTC', 
        'VET', 
        'XLM', 
        'XRP'
        ]
    crypto_std = {}

    for ticker in cryptos:
        # Create close column name
        c_name = f"{ticker}USDT_Close"
        df = crypto_dfs[ticker]
        
        # Get dail returns from functions
        funct = functions.Functions(df, c_name)
        daily_returns = funct.daily_returns()

        # Append to dictionary
        crypto_std[ticker] = funct.standard_deviation(daily_returns['daily_returns'])  

    return crypto_std

# This gets a sharpe ratio dictionary
def get_sharpe(crypto_dfs):
    """Set a list of all the cryptos"""

    cryptos = [
        'ADA', 
        'BNB', 
        'BTC', 
        'DOT', 
        'ETH', 
        'LINK', 
        'LTC', 
        'VET', 
        'XLM', 
        'XRP'
        ]
    crypto_sharpe = {}

    # Loop through list and make a dictionary of sharpe ratios
    for ticker in cryptos:
        df = crypto_dfs[ticker]
        c_name = f"{ticker}USDT_Close"
        funct = functions.Functions(df, c_name)
        daily_returns = funct.daily_returns()

        crypto_sharpe[ticker] = funct.sharpe_ratio(daily_returns['daily_returns'])
    
    return crypto_sharpe

# This sorts the standard deviation
def sort_crypto_std(crypto_std):
    """Returns a dictionary with all crypto std's sorted from low to high risk"""

    high_risk = {}
    med_risk = {}
    low_risk = {}

    # Separates tickers based on std
    print(crypto_std)
    for ticker, std in crypto_std.items():
        if float(std) <= 0.057:
            low_risk[ticker] = std
        elif float(std) > 0.057 and float(std) <= 0.073:
            med_risk[ticker] = std
        elif float(std) > 0.073:
            high_risk[ticker] = std

    return {"low":low_risk, "med":med_risk, "high":high_risk}

# Sort crypto sharpe values. Returns a dictionary
def sort_crypto_sharpe(crypto_sharpe):
    """Returns a dictionary with all crypto sharpe's sorted from low to high risk"""

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

# Returns crypto selected from risk analysis
def get_user_bins(user_info, sorted_std):
    """
    user_info: user answer dictionary,
    sorted_std: Crypto's sorted on risk

    Returns total crypto based on risk tolerance
    """
    # Init empty list
    len_crypto = []

    # Make high bin
    if user_info['Risk Tolerance'] == 'High':
        for t, v in sorted_std['high'].items():
            len_crypto.append(t)
            for t, v in sorted_std['med'].items():
                len_crypto.append(t)
                for t, v in sorted_std['low'].items():
                    len_crypto.append(t)

    # Make medium bin               
    elif user_info['Risk Tolerance'] == 'Medium':
        for t, v in sorted_std['med'].items():
            len_crypto.append(t)
            for t, v in sorted_std['low'].items():
                len_crypto.append(t)

    # Make low bin
    elif user_info['Risk Tolerance'] == 'Low':
        for t, v in sorted_std['low'].items():
            len_crypto.append(t)

    # Return user's selections
    return len_crypto

# Prints out the bins
def print_bins(sorted_std):
    """Prints out all of the sorted crypto bins"""

    [print(f"Low Risk Cryptos - {t}: {v}") for t,v in sorted_std['low'].items()]
    # for t,v in sorted_std['low'].items():
    #     print(f"Low Risk Cryptos - {t}:{v}")
    print("----------")
    [print(f"Medium Risk Cryptos - {t}: {v}") for t,v in sorted_std['med'].items()]
    # for t,v in sorted_std['med'].items():
    #     print(f"Medium Risk Cryptos - {t}:{v}")  
    print("----------")
    [print(f"High Risk Cryptos - {t}: {v}") for t,v in sorted_std['high'].items()]
    # for t,v in sorted_std['high'].items():
    #     print(f"High Risk Cryptos - {t}:{v}")

# Gets the weighting of crypto
def crypto_weighting(set_crypto, price_per_crypto, num_orders):
    """Get the weighting of risk analyzed crypto"""

    weight_calc = {}
    for ticker in set_crypto:
        print(f"Purchase ${price_per_crypto * num_orders[ticker]:.2f} of {ticker}")
        # Add to dictionary to calculate weights
        weight_calc[ticker] = float(price_per_crypto * num_orders[ticker])

# Prints the selections of crypto selected by index
def print_index_crypto(snp_crypto, price_per_crypto_i, crypto_index_allotment, user_info):
    """Print index order book"""

    for ticker in snp_crypto:
        print(f"Purchase ${price_per_crypto_i:.2f} of {ticker}")
    print("\n")
    print(f"This should equal 30%, ${crypto_index_allotment:.2f}, " 
    f"of your stated initial investment amount of {user_info['Investment Amount']}")

# Prints the information input by the user
def print_user_info(user_info):
    """Prints out the user information"""

    print("----------User Info----------")
    # Print user risk assessment dictionary
    for i, v in user_info.items():
        print(f"{i}: {v}")
    print("\n")

# Returns sorted std and crypto sharpe values
def get_sorted_std_sharpe(dictionary):
    """Returns crypto sharpe diction and sorted std dictionary"""
    
    crypto_sharpe = get_sharpe(dictionary) 

    sorted_std = sort_crypto_std(get_std(dictionary))

    return sorted_std, crypto_sharpe

# Attempt to get and print sharpe ratio values for crypto's
def print_sorted_sharpe(dictionary):
    """Try to print sharpe values"""

    try:
        print("----------Crypto Sharpe Values----------")
        sorted_sharpe = sort_crypto_sharpe(dictionary)
        for crypto, sharpe in sorted_sharpe.items():
            print(f"{crypto} Sharpe Ratio - {sharpe}")
    except:
        print("Failed to retrieve sharpe ratio values...")
        pass

    print("\n")
    print("----------Crypto Risk----------")
    print_bins(sorted_std)

# Print out the suggested orders based on risk tolerance
def order_book(user_info, sorted_std):
    """Get and print order book"""

    # Get user initial investment
    i_amount = user_info["Investment Amount"]

    # Get total crypto orders
    # Calculate weighting for risk portion of portfolio
    # using weighting get price per crypto
    len_crypto = get_user_bins(user_info, sorted_std)
    crypto_risk_allotment = i_amount * 0.7
    price_per_crypto = crypto_risk_allotment / len(len_crypto)

    print("\n")
    print("----------Order Book----------")

    # Print risk order book
    num_orders = Counter(len_crypto)
    set_crypto = set(len_crypto)


    # Print out orders of crypto
    crypto_weighting(set_crypto, price_per_crypto, num_orders)

    print("\n")
    # Prints the portion of crypto calculated
    print(f"This should equal 70%, ${crypto_risk_allotment}, "
    f"of your stated initial investment amount of {user_info['Investment Amount']}")
    print("\n")

    # Using BTC, ETH and LTC as a benchmark for the s&p we allot the last 30% to these cryptos
    # i = index
    snp_crypto = ['BTC', 'ETH', 'LTC']
    crypto_index_allotment = i_amount * 0.3
    price_per_crypto_i = crypto_index_allotment / len(snp_crypto)


    # Print index related crypto choices
    print_index_crypto(snp_crypto, price_per_crypto_i, crypto_index_allotment, user_info)

    print("\n")

# Print the value of the stock portfolio input by the user
def stock_portfolio_value(user_info):
    """Get and print stock portfolio value"""

    print("----------Stock Portfolio Value----------")
    # Pull info for user's stock portfolio
    tickers = []
    for ticker, shares in user_info['Stock Portfolio'].items():
        tickers.append(ticker)

    # Api env variables
    # For anyone running on their on computer 
    # be sure to change these env variable to reflect the names you use
    alpaca_api = "ALPACA_API_KEY_ENV"
    alpaca_secret_api = "ALPACA_SECRET_KEY_ENV"

    # Make the call to alpaca
    alpaca_call = alpaca.Alpaca(tickers, '1D', 1, alpaca_api, alpaca_secret_api)
    stocks_df = alpaca_call.run()


    # Set empty list and dictionary to 
    close_values = []
    stock_port = {}

    # Prints the last closing price of each stock in the portfolio
    for ticker in tickers:
        close = f"{ticker.upper()}_close"
        stock_port[ticker] = stocks_df[close]
        close_v = stocks_df[close][-1]
        print(f"{ticker} closed at {close_v}")
        close_values.append(close_v)

    print("\n")

    # Multiply last closing price by share amount and store in list
    portfolio_value = []
    for value in close_values:
        for ticker, share in user_info['Stock Portfolio'].items():
            ticker = float(value) * float(share)
            portfolio_value.append(ticker)

    # Sum the values in the list to get total portfolio value
    portfolio_value = sum(portfolio_value)

    print(f"The current value of your stock portfolio is ${portfolio_value:.2f}")
    print("\n")

    return stock_port, close_values

# Print graphs of cumulative returns
def print_graphs_prophet():
    """
    Get dataframes for graphs and forecasting
    Plot graphs/forecast
    """
    print("----------Print Graphs / Expected Returns----------")
    # Get CMC close
    cmc = crypto_market.cmc200(1)
    cmc.columns = ['CMC_close']
    cmc_dr = cmc['CMC_close'].pct_change().dropna()
    cmc_cum = (1 + cmc_dr).cumprod()

    # Get S&P 500 close
    sp500 = sp500_index.sp500(1)
    sp500.columns = ['SP500_close']
    sp500_dr = sp500['SP500_close'].pct_change().dropna()
    sp500_cum = (1 + sp500_dr).cumprod()

    # Concat dataframe of indexes
    index_cm = pd.concat([sp500_cum, cmc_cum], axis=1)
    index_cm.dropna(inplace=True)

    # Plot of both indexes daily close
    index_overlay_plot = index_cm.hvplot.line(title='CMC200 and S&P500 Daily Returns Overlayed')

    # Rolling mean of both indexes
    sp_cmc = index_cm.rolling(window=30).mean().dropna()

    # Plot of rolling 30 mean indexes
    index_dr_30_plot = sp_cmc.hvplot.line(title='CMC200 and S&P500 Overlayed - 30 Day')

    # Aggregate average of indexes 30 day
    sp_cmc_avg = index_cm.mean(axis=1)
    sp_cmc_avg_30 = sp_cmc_avg.rolling(window=30).mean()

    # Create a list of dataframes to concat stocks with cryptos
    list_df = []

    # Store stock dfs
    for t, df in stock_port.items():
        df = pd.DataFrame(df)
        list_df.append(df)

    # Add crypto dfs
    for t, df in dictionary.items():
        df = pd.DataFrame(df)
        df = df[f"{t}USDT_Close"]
        list_df.append(df)

    # Get new joined dataframe
    port_closes = pd.concat(list_df, axis=1, join='inner')

    # Drop NaN values
    port_daily_returns = port_closes.pct_change().dropna()

    # Get cumulative returns
    port_cum_returns = (1 + port_daily_returns).cumprod()

    # Get rolling cumulative returns
    port_cum_30 = port_cum_returns.rolling(window=30).mean()

    # Average the returns across columns to get average total returns
    combined_cum_returns = port_cum_returns.mean(axis=1)
    combined_cum_returns30 = port_cum_30.mean(axis=1)

    # Concat portfolio with index to get new dataframe
    index_returns_df = pd.concat([combined_cum_returns, index_cm, sp_cmc_avg], axis=1)
    index_returns_df = index_returns_df.dropna()
    index_returns_df.columns = [
        'Portfolio Cum. Returns', 
        'S&P 500', 
        'CMC200', 
        'Avg Index'
        ]

    # Concat average portfolio with averaged index - 30 day
    index_returns_30_df = pd.concat([combined_cum_returns30, sp_cmc_avg_30], axis=1)
    index_returns_30_df = index_returns_30_df.dropna()
    index_returns_30_df.columns = [
        'Portfolio Cum. Returns', 
        'Avg Index'
        ]

    # Format for fbProphet
    portfolio_proph = combined_cum_returns.to_frame()
    portfolio_proph = portfolio_proph.reset_index()
    portfolio_proph['index'] = pd.to_datetime(portfolio_proph['index'])
    portfolio_proph.rename(columns={'index':'ds', 0:'y'}, inplace=True)

    print(portfolio_proph.head())
    print(portfolio_proph.info())


    # Check if dataframe is formatted for Prophet
    try:
        model = fb.Prophet()
        model.fit(portfolio_proph)
        future = model.make_future_dataframe(periods=365, freq='D')
        forecast = model.predict(future)
        print(forecast[['yhat','yhat_lower','yhat_upper']].head())
    except:
        print("Dataframe Error")

    # Check if forecasts plot
    try:
        forecast.plot(forecast, xlabel='ds', ylabel='y')
    except:
        print('Failed to plot forecast')

    # Plot hvplot graphs in separate window
    hvplot.show(
        index_returns_df.hvplot(
            y=[
                'Portfolio Cum. Returns', 
                'S&P 500', 
                'CMC200', 
                'Avg Index'
            ], 
            value_label='Cumulative Returns', 
            xlabel='Date', 
            title='Portfolio Returns vs Indexes')
        +
        index_returns_30_df.hvplot(
            y=[
                'Portfolio Cum. Returns', 
                'Avg Index'
            ], 
            value_label='Cumulative Returns', 
            xlabel='Date', 
            title='Portfolio Returns vs Average Index - 30 Day')
    )

print("----------Dynamic Portfolio Management - Version 1.0----------")

# Get and print user info 
user_info = risk_assesment.get_user_risk_tolerance_port()
print_user_info(user_info) 

weights = [] # Will be used in the future to automate weight calculation

# Get crypto dictionary, sort and print returned values
dictionary = get_crypto_dict()   
sorted_std, crypto_sharpe = get_sorted_std_sharpe(dictionary)
print_sorted_sharpe(dictionary)

# Print suggested order book
order_book(user_info, sorted_std)
stock_port, close_values = stock_portfolio_value(user_info)

# Print graphs showing expected returns over previous year
print_graphs_prophet()