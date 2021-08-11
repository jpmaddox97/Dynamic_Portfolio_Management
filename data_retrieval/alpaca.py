import os
import pandas as pd
import json
import requests
from dotenv import load_dotenv
import alpaca_trade_api as trade_api

class Alpaca:

    def __init__(self, ticker, alpaca_api, alpaca_secret_key):
        self.ticker = ticker
    
    def load_dotenv(self):
        load_dotenv()

    def 
