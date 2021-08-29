![Portfolio Management Image](readme_images/Financial-Management.png)
# Dynamic Portfolio Management

>"Manage Risk, Cryptocurrency Recommendation, Portfolio Historical Returns"

## Directory
[Main Code](main.py)

[Data and Data Retrieval](data_retrieval)

[Additional Data](Resources)

[Functions](functions_graphs)

### Dependancies:

# Install Anaconda: [Anaconda](https://www.anaconda.com/)

# Save an ENV file of your Alpaca and Binance public and secret keys in the same folder as the repository.
# You will need store the variables later in the program.

# Install Alpaca: [Alpaca SDK](https://alpaca.markets/docs/)
**Change "ALPACA_API_KEY_ENV" and "ALPACA_SECRET_KEY_ENV" to your own personal alpaca_api env variables.
Lines 227-228 of main.py**
[Alpaca API](main.py)
```Python:
alpaca_api = "ALPACA_API_KEY_ENV"
alpaca_secret_api = "ALPACA_SECRET_KEY_ENV"
```

# Install Fire: [Fire](https://google.github.io/python-fire/guide/#installation)
```bash:
pip install fire
```

# Install Questionary: [Questionary](https://pypi.org/project/questionary/#installation)
```bash:
pip install questionary
```

# Install Binance Python Client: [Binance](https://python-binance.readthedocs.io/en/latest/overview.html)
**Change "BINANCE_API" and "BINANCE_SECRET" to your own personal binance_api env variables.
Lines 28-29 of getbinance.py**
[Binance API](data_retrieval/getbinance.py)
```Python:
binance_api = os.getenv("BINANCE_API")
binance_secret = os.getenv("BINANCE_SECRET")
```

# Install Tweepy: [Tweepy](https://pypi.org/project/tweepy/)
# You will need a Twitter API Key which you can apply for here: [Twitter API](https://developer.twitter.com/en/products/twitter-api)
**Change "twitter_credentials.consumer_key" and "twitter_credentials.consumer_secret" to your own personal binance_api env variables.
Second Cell of tweet_sentiment_analysis_crypto_final_draft.ipynb.py**
[Tweepy File](data_retrieval/tweet_sentiment_analysis_crypto_final_draft.ipynb.py)
```Python:
# create OAuthHandler object
self.auth = OAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
# set access token and secret
self.auth.set_access_token(twitter_credentials.access_token, twitter_credentials.access_token_secret)
```

# Install Binance Python TextBlob: [TextBlob](https://textblob.readthedocs.io/en/dev/install.html#:~:text=Installation%20%C2%B6%201%20Installing%2FUpgrading%20From%20the%20PyPI%20%C2%B6.,5%20Migrating%20from%20older%20versions%20%28%3C%3D0.7.1%29%20%C2%B6.%20)
```bash:
pip install -U textblob
```
**Using Conda Install (Anaconda)
```bash:
conda install -c conda-forge textblob
```

# Install hvPlot: [hvPlot](https://pypi.org/project/hvplot/#:~:text=Installation.%20hvPlot%20supports%20Python%202.7%2C%203.5%2C%203.6%20and,are%20the%20last%20item%20in%20a%20notebook%20cell.)
```bash:
pip install hvplot
```
**Using Conda Install (Anaconda)
```bash:
conda install -c pyviz hvplot
```
