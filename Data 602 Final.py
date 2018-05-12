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
import numpy

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
    base_id = pd.DataFrame(base_id)
    

    
    #print(coin_df)
    return base_id
    print(base_id)
    
def bittrex():
    url = 'https://rest.coinapi.io/v1/symbols'
    headers = {'X-CoinAPI-Key' : '68FDBBAF-CA59-4D11-A41E-51C9D2B67DA4'}
    coin = r.get(url, headers=headers)
    data = coin.text
    parsed = json.loads(data)
    coin_df = pd.DataFrame.from_dict(parsed, orient='columns')
    base_id = coin_df['symbol_id']
    base_id = pd.DataFrame(base_id)
    bittrex_df = base_id['symbol_id'].str.split('_',expand=True)
    bittrex_df = bittrex_df.loc[bittrex_df[0] == 'BITTREX']
    bittrex_df = bittrex_df.loc[bittrex_df[3] == 'USDT']
    return bittrex_df
    

def poloniex():
    url = 'https://rest.coinapi.io/v1/symbols'
    headers = {'X-CoinAPI-Key' : '68FDBBAF-CA59-4D11-A41E-51C9D2B67DA4'}
    coin = r.get(url, headers=headers)
    data = coin.text
    parsed = json.loads(data)
    coin_df = pd.DataFrame.from_dict(parsed, orient='columns')
    base_id = coin_df['symbol_id']
    base_id = pd.DataFrame(base_id)
    poloniex_df = base_id['symbol_id'].str.split('_',expand=True)
    poloniex_df = poloniex_df.loc[poloniex_df[0] == 'POLONIEX']
    poloniex_df = poloniex_df.loc[poloniex_df[3] == 'USDT']
    return poloniex_df

url = 'https://rest.coinapi.io/v1/symbols'
headers = {'X-CoinAPI-Key' : '68FDBBAF-CA59-4D11-A41E-51C9D2B67DA4'}
coin = r.get(url, headers=headers)
data = coin.text
parsed = json.loads(data)
coin_df = pd.DataFrame.from_dict(parsed, orient='columns')
base_id = coin_df['symbol_id']
base_id = pd.DataFrame(base_id)
poloniex_df = base_id['symbol_id'].str.split('_',expand=True)
poloniex_df = poloniex_df.loc[poloniex_df[0] == 'POLONIEX']
poloniex_df = poloniex_df.loc[poloniex_df[3] == 'USDT']
poloniex_df.columns = ['exchange', 'type', 'coin 1', 'coin 2', '4','5','6']
poloniex_df = poloniex_df[['exchange', 'type', 'coin 1', 'coin 2']]
poloniex_df["pair"] = poloniex_df["exchange"].map(str) + '_' + poloniex_df["type"]+'_'+poloniex_df["coin 1"]+'_'+poloniex_df["coin 2"]
poloniex_pair = poloniex_df[['pair']] 





def get_hist():
    url = 'https://rest.coinapi.io/v1/ohlcv/'+ poloniex_pair + '/latest?period_id=1DAY&time_start=2017-05-07T00:00:00&limit=365'
    headers = {'X-CoinAPI-Key' : '68FDBBAF-CA59-4D11-A41E-51C9D2B67DA4'}
    hist = r.get(url, headers=headers)
    data = hist.text
    parsed = json.loads(data)
    hist_df = pd.DataFrame.from_dict(parsed, orient='columns')
    #x = hist_df['time_open']
    #y = hist_df['price_open']
   
    #graph = plt.plot(x,y)
    #return plt.show(graph)
    
    print(hist_df)
    
    



def value():
    url = 'https://rest.coinapi.io/v1/quotes/current?filter_symbol_id=ETH'
    headers = {'X-CoinAPI-Key' : '68FDBBAF-CA59-4D11-A41E-51C9D2B67DA4'}
    response = r.get(url, headers=headers)
    data = response.text
    parsed = json.loads(data)
    whatevs = pd.DataFrame.from_dict(parsed, orient='columns')

    print(whatevs)
    
