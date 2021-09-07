#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
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

st.title('Uber pickups in NYC')


