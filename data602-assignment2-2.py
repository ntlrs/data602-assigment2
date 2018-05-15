#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 11 15:35:45 2018

@author: ntlrsmllghn
"""

import requests
import matplotlib.pyplot as plt
import pandas as pd
import json
import io
import time
from datetime import datetime, timedelta
from pymongo import MongoClient
from time import strftime, gmtime
from statistics import stdev

def main():    
   # Initial portfolio size in cash
    funds = 100000000.0
    pair = ["BCH-USD","BTC-USD","ETH-USD","LTC-USD"] # assume usd base

   # Initialize data structures
    df_blotter = initialize_blotter()
    df_pl = initialize_pl(pair)

   # Design a menu a system
    menu = ('Buy', 'Sell', 'Show Blotter', 'Show PL', 'Quit')
    while True:
        choice = display_menu(menu,exit_option=5)
        if choice == 1:
            pair, qty = select_crypto()
            if pair != "Back":
                ask, bid = get_price(pair)               
                price = float(ask)
                total_cost = float(qty * price)
                show_stats(pair)
                print("Buying "+ str(qty) + " share of " + pair + " for " + str(total_cost))
                blotter = trade(pair, qty, price, total_cost)
                df_blotter.append(blotter)
                return df_blotter   
            else:
                pass
           
        elif choice == 2:
            pair, qty = select_crypto()
            qty = -1 * qty
            if pair != "Back":
                ask, bid = get_price(pair)
                price = float(bid)
                total_cost = float(qty * price)
                show_stats(pair)
                print("Selling " + str(qty) + " share of " + pair + " for " + str(total_cost))
                blotter = trade(pair, qty, price, total_cost)
                df_blotter.append(blotter)
                return df_blotter
            else:
                pass
            
        elif choice == 3:
            view_blotter(df_blotter)
        elif choice == 4:
            view_pl(df_pl)
        elif choice == 5:
            quit()
        else:
          print("Not An Option ")
          return
            

def display_menu(menu,exit_option=-1):
    for m in menu:
        print(menu.index(m)+1,".  ",m)
    choice = int(input("Enter choice [1-5]: "))
    if choice==exit_option:
        print("Bye")
        quit()
    return choice

def trade(pair, qty, price, total_cost):
    blotter = []
    date = strftime("%Y-%m-%d %H:%M:%S", gmtime()) 
    confirm = input("Confirm Transaction [Y/N]: ")
    conf = confirm.upper()
    if conf=="Y" or "y":
        transaction = [pair, qty, price, date, total_cost]
        blotter.append(transaction)
        print("Tranaction Complete")
    return blotter
         

def show_stats(pair):
    print("\n")
    dailymin, dailymax = get_stats(pair)
    print("The daily high for " + pair + " is " + str(dailymin))
    print("The daily low for " + pair + " is " + str(dailymax))
    mean = dailymean(dailymin, dailymax)
    print("The daily mean for " + pair + " is " + str(mean))
    stddev = round(stdev([dailymax, dailymin]), 2)
    print("Today's standard deviation for " + pair + " is " + str(stddev))
    print("\n")
    hist = history(pair)
    print(hist)

   
def select_crypto():
    pair = ["BCH-USD", "BTC-USD",  "ETH-USD",  "LTC-USD", "Back"]
    for p in pair:
        print(pair.index(p)+1,".  ", p)
    crypto = int(input("Please Choose From The Following Pair or Return to Main Menu: "))
    item = crypto-1
    pair = pair[item]
    qty =  int(input("How Many Shares Would You Like To Trade?: "))   
    return pair, qty

def calc_vwap(current_qty,current_vwap,qty,price):
    dollar = current_qty * current_vwap
    new_dollar = dollar + (qty * price)
    new_qty = current_qty + qty
    new_vwap = new_dollar / new_qty
    return new_vwap

def update_pl(pl,pair,qty,price):
    if qty > 0: # buy
        current_qty = pl.at[pair,'Position']
        current_vwap = pl.at[pair,'VWAP']
        new_vwap = calc_vwap(current_qty,current_vwap,qty,price) #bid
        pl.at[pair,'Position'] = current_qty + qty
        pl.at[pair,'VWAP'] = new_vwap
        mkt_value = qty * current_vwap
        upl = price - mkt_value
        pl.at[pair, 'UPL'] = upl
        rpl = pl.at[pair, 'RPL']
        total_pl = upl + rpl
        pl.at[pair, 'Total PL'] = total_pl
        
        
        
        # TODO update 'Allocated By Share', 'Allocated By Dollar'
        #results = pl.append(results)
        #add a return
    
    elif qty < 0: #sell
        current_qty = pl.at[pair,'Position']
        current_vwap = pl.at[pair,'VWAP']
        new_vwap = calc_vwap(current_qty,current_vwap,qty,price) #ask
        pl.at[pair, 'Position'] = current_qty - qty
        pl.at[pair,'VWAP'] = new_vwap
        rpl = (price - current_vwap) * qty
        pl.at[pair, 'RPL'] = rpl
        new_upl = (current_qty * current_vwap) - rpl
        pl.at[pair, 'UPL'] = new_upl
        total_pl = upl + rpl
        pl.at[pair, 'Total PL'] = total_pl
    
        print("Insert code handling a sale - recalc UPL,RPL & position")


def view_blotter(df_blotter):
    print("Trade Blotter")
    print(df_blotter)
    print()


def view_pl(df_pl):
    # TODO Update UPL here
    print("Profit & Loss")
    print(df_pl)
    print()


def get_price(pair):
    df = load('https://api.gdax.com/products/'+ str(pair) +'/book',printout=False)
    pricedf = pd.DataFrame(df, index = [0]) 
    ask = pricedf.iloc[0]['asks'][0]
    bid = pricedf.iloc[0]['bids'][0]
    return float(ask), float(bid)


def initialize_blotter():
    cols = ['Side','Ticker','Qty','Price','Date','Cost','Cash']
    df_blotter = pd.DataFrame(columns= cols)
    df_blotter.drop(['Cash'], axis = 1, inplace = True) 
    return df_blotter



def initialize_pl(pair):
    col_names = ['Pair','Position','VWAP','UPL','RPL', 'Total PL', 'Allocated By Share', 'Allocated By Dollar']
    pl = pd.DataFrame(columns=col_names)
    for p in pair:
        data = pd.DataFrame([[p,0,0,0,0,0,0,0]] ,columns=col_names)
        pl = pl.append(data, ignore_index=True)
    pl = pl.set_index('Pair')
    return pl

def dailymean(dailymax, dailymin):
    mean = (dailymax + dailymin) / 2
    return mean

def stddev(dailymax, dailymin):
    stdev([dailymax, dailymin])
    return stddev

def get_stats(pair):
    stats = requests.get('https://api.gdax.com/products/'+pair+'/stats')
    data = stats.text
    parsed = json.loads(data)
    dailymax = parsed['high']
    dailymin = parsed['low']
    return float(dailymax), float(dailymin)

def history(pair):
    history = requests.get('https://api.gdax.com/products/' + pair + '/candles?granularity=86400')
    history = pd.read_json(history.text)
    history.columns = ['time', 'low', 'high','open','close', 'volume']
    history['time'] = pd.to_datetime(history['time'], unit = 's')
    history = history[:100]    
    x = history['time']
    y = history['close']
    plt.xticks(rotation=45)
    plt.title('100 Day Historical Data for ' + pair)
    graph = plt.plot(x,y)
    return plt.show(graph)


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

if __name__ == "__main__":
    main()