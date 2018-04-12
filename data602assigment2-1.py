#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 00:56:31 2018

@author: ntlrsmllghn
"""

import requests
import matplotlib.pyplot as plt
import pandas as pd
import json
import io
import time
import datetime as dt
import gdax

client = gdax.PublicClient()
api_request = requests.get("https://api.gdax.com/products")
api = json.loads(api_request.content)

                       
def main():    
    # Initial portfolio size in cash
    funds = 100000000.0
    pairs = ['BCH-USD', 'BTC-USD', 'ETH-USD', 'LTC-USD'] # assume usd base
        
    
    # Initialize data structures
    df_blotter = initialize_blotter()
    df_pl = initialize_pl(pairs)
    df_products = get_products()

    # Design a menu a system 
    menu = ('Buy', 'Sell', 'Show Blotter', 'Show PL', 'Quit')
    while True:
        choice = display_menu(menu,exit_option=5)
        if choice == 1:
            # Buy
            print("Choice 1 chosen")
        elif choice == 2:
            print("Choice 2 chosen")
            # Sell
        elif choice == 3:
            view_blotter(df_blotter)
        elif choice == 4:
            view_pl(df_pl)
        elif choice == 5:
            print("goodbye")
            break
        else:
            print("Not an option")
            print("\n\n\n\n")
            main()

def display_menu(menu,exit_option=-1):
    for m in menu:
        print(menu.index(m)+1,". ",m)
    choice = int(input("Enter choice >> #"))
    if choice==exit_option:
        print("Bye")
        quit()
    return choice

def calc_vwap(current_qty,current_vwap,qty,price):
    dollar = current_qty * current_vwap
    new_dollar = dollar + (qty * price)
    new_qty = current_qty + qty
    new_vwap = new_dollar / new_qty
    return new_vwap

def update_pl(pl,pairs,qty,price):
    if qty > 0: # buy
        current_qty = pl.at[pairs,'Position']
        current_vwap = pl.at[pairs,'VWAP']
        new_vwap = calc_vwap(current_qty,current_vwap,qty,price) #bid
        pl.at[pairs,'Position'] = current_qty + qty
        pl.at[pairs,'VWAP'] = new_vwap
        mkt_value = qty * current_vwap
        upl = price - mkt_value
        pl.at[pairs, 'UPL'] = upl
        rpl = pl.at[pairs, 'RPL']
        total_pl = upl + rpl
        pl.at[pairs, 'Total PL'] = total_pl
        # TODO Recalc UPL
    elif qty < 0: #sell
        current_qty = pl.at[pairs,'Position']
        current_vwap = pl.at[pairs,'VWAP']
        new_vwap = calc_vwap(current_qty,current_vwap,qty,price) #ask
        pl.at[pairs, 'Position'] = current_qty - qty
        pl.at[pairs,'VWAP'] = new_vwap
        rpl = (price - current_vwap) * qty
        pl.at[pairs, 'RPL'] = rpl
        new_upl = (current_qty * current_vwap) - rpl
        pl.at[pairs, 'UPL'] = new_upl
        total_pl = upl + rpl
        pl.at[pairs, 'Total PL'] = total_pl
        
        print("Insert code handling a sale - recalc UPL,RPL & position")




def view_blotter(df_blotter):
    print("---- Trade Blotter")
    print(df_blotter)
    print("\n\n")


def view_pl(df_pl):
    # TODO Update UPL here
    print("---- PL")
    print(df_pl)
    print("\n\n")


def get_price(pairs):
    df = load('https://api.gdax.com/products/'+pairs+'/book',printout=False)
    ask = df.iloc[0]['ask'][0]
    bid = df.iloc[0]['bid'][0]
    return float(ask), float(bid)

def get_stats(pairs):
    r = requests.get('https://api.gdax.com/products/'+pairs+'/stats')
    df = pd.read_json('['+r.text+']')
    high = r.json()['high']
    low = r.json()['low']
    return float(high), float(low)

def get_historical(pairs):
    df = client.get_product_hisotric_rates(pairs, granularity = 86400 * 100)
    return df


def initialize_blotter():
    col_names = ['Pair','Quantity','Price', 'Cost', 'Date', 'Cash Balance']
    return pd.DataFrame(columns=col_names)


def initialize_pl(pairs):
    col_names = ['Pairs','Position','VWAP','UPL','RPL', 'Total PL', 'Allocated By Share', 'Allocated By Dollar']
    pl = pd.DataFrame(columns=col_names)
    for p in pairs:
        data = pd.DataFrame([[p,0,0,0,0,0,0,0]] ,columns=col_names)
        pl = pl.append(data, ignore_index=True)
    pl = pl.set_index('Pairs')
    return pl

def get_products():
    df = load('https://api.gdax.com/products',printout=False)
    return df

def load(url,printout=False,delay=0,remove_bottom_rows=0,remove_columns=[]):
    time.sleep(delay)
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    r = requests.get(url, headers=header)
    df = pd.read_json(r.text)
    if remove_bottom_rows > 0:
        df.drop(df.tail(remove_bottom_rows).index,inplace=True)
    df.drop(columns=remove_columns,axis=1)
    df = df.dropna(axis=1)
    if printout:
        print(df)
    return df

main()
