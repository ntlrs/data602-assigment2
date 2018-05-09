#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  7 19:46:42 2018

@author: ntlrsmllghn
"""

import requests as r
import pandas as pd
import datetime
import json
from time import strftime, gmtime
import matplotlib as plt

##import bittrex API

bittrex = r.get('https://bittrex.com/api/v1.1/public/getmarkets').json()

print(bittrex)


cryptopia = r.get('https://www.cryptopia.co.nz/api/GetMarketHistory/100').json()
print(cryptopia)

cryptopiapairs = r.get('https://www.cryptopia.co.nz/api/GetTradePairs').json()
print(cryptopiapairs)

#url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_BTC_USD/latest?period_id=1MIN'
#headers = {'X-CoinAPI-Key' : '68FDBBAF-CA59-4D11-A41E-51C9D2B67DA4'}
#response = requests.get(url, headers=headers)


url = 'https://rest.coinapi.io/v1/symbols'
headers = {'X-CoinAPI-Key' : '68FDBBAF-CA59-4D11-A41E-51C9D2B67DA4'}
response = r.get(url, headers=headers)
print(response.text)

#def get_hist():
    #rl = 'https://rest.coinapi.io/v1/symbols'
    #headers = {'X-CoinAPI-Key' : '68FDBBAF-CA59-4D11-A41E-51C9D2B67DA4'}
    #response = r.get(url, headers=headers)
    #hist_df = pd.DataFrame.from_dict(response, orient='columns') 
    #base_id = hist_df.iloc[0]['asset_id_base'][0]
    #print (base_id)


def get_coin():
    url = 'https://rest.coinapi.io/v1/symbols'
    headers = {'X-CoinAPI-Key' : '68FDBBAF-CA59-4D11-A41E-51C9D2B67DA4'}
    coin = r.get(url, headers=headers)
    data = coin.text
    parsed = json.loads(data)
    coin_df = pd.DataFrame.from_dict(parsed, orient='columns')
    base_id = coin_df['symbol_id']
    #print(coin_df)
    #return base_id
    print(base_id)
    

def get_hist():
    url = 'https://rest.coinapi.io/v1/ohlcv/BINANCE_SPOT_ETH_BTC/latest?period_id=2YRS'
    headers = {'X-CoinAPI-Key' : '68FDBBAF-CA59-4D11-A41E-51C9D2B67DA4'}
    hist = r.get(url, headers=headers)
    data = hist.text
    parsed = json.loads(data)
    hist_df = pd.DataFrame.from_dict(parsed, orient='columns')
    print(hist_df)
