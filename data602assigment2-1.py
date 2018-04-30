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
from datetime import datetime
from math import sqrt
from pymongo import MongoClient
import time





#client = gdax.PublicClient()

#api_request = requests.get("https://api.gdax.com/products")
#api = json.loads(api_request.content)

                       
def main():    
    # Initial portfolio size in cash
    cash = 100000000.0
    pair = ['BCH-USD', 'BTC-USD', 'ETH-USD', 'LTC-USD'] # assume usd base
        
    #bid, ask = get_price('btc-usd')
    
    
    # Initialize data structures
    df_blotter = initialize_blotter()
    df_pl = initialize_pl(pair)
    df_products = get_products(pair)

    # Design a menu a system 
    menu = ('Buy', 'Sell', 'Show Blotter', 'Show PL', 'Quit')
    while True:
        choice = display_menu(menu,exit_option=5)
        if choice == 1:
            buy(df_products, df_pl, df_blotter, pair, cash)
                    
        elif choice == 2:       
            sell(df_products, df_pl, df_blotter, pair, cash)
        
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
        print(menu.index(m)+1,"-------------------------- ",m)
    choice = int(input("Please Choose From The Following Options [1-5]: "))
    if choice==exit_option:
        print("Bye")
        quit()
    return choice


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

def initialize_blotter():
    col_names = ['Pair','Quantity','Price', 'Cost', 'Date']
    return pd.DataFrame(columns=col_names)


def initialize_pl(pair):
    col_names = ['Pair','Position','VWAP','UPL','RPL', 'Total PL', 'Allocated By Share', 'Allocated By Dollar']
    pl = pd.DataFrame(columns=col_names)
    for p in pair:
        data = pd.DataFrame([[p,0,0,0,0,0,0,0]] ,columns=col_names)
        pl = pl.append(data, ignore_index=True)
    pl = pl.set_index('Pair')
    return pl


def update_blotter(pair, qty, price, cost, date, df_blotter,printout=False):
    col_names = ['Pair','Quantity','Price', 'Cost', 'Date']
    row = (pair, qty, price, cost, date)
    data = pd.DataFrame([row], columns=col_names)
    df_blotter.append(data)
    if printout:
        print(df_blotter)
    return df_blotter 

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

        # TODO update 'Allocated By Share', 'Allocated By Dollar'
        #results = pl.append(results)
        #add a return
        
#def current_cash():
   # pass

def get_price(pair):
    #print("pairs are ...  " + str(pair))
    df = load('https://api.gdax.com/products/'+ str(pair) +'/book',printout=False)
    pricedf = pd.DataFrame(df, index = [0]) 
    #print("dataframe looks like ..")
    #print(df)
    ask = pricedf.iloc[0]['asks'][0]
    bid = pricedf.iloc[0]['bids'][0]
    return float(ask), float(bid)

def get_stats(pair):
    df = requests.get('https://api.gdax.com/products/'+pair+'/stats')
    df = pd.read_json('['+df.text+']')
    dailymax = df.json()['high']
    dailymin = df.json()['low']
    return float(dailymax), float(dailymin)

def high_low(pair):
    r = requests.get('https://api.gdax.com/products/'+pair+'/stats')
    df = pd.read_json('['+r.text+']')
    high = r.json()['high']
    low = r.json()['low']
    return float(high), float(low)

def get_products(pair):
    df = load('https://api.gdax.com/products',printout=False)
    return df



################################################
def buy(pair, get_price, df_blotter, df_pl, update_blotter):
    print("Please Choose From The Following Pair")
    print('\n')
    print("1. BCH-USD" )
    print("2. BTC-USD" )
    print("3. ETH-USD" )
    print("4. LTC-USD" )
    print("5. Return to Main Menu")
    print('\n\n')
    
    buying = int(input("Please Select [1-5]:  "))
     
    qty = int(input('How Many Shares?: '))
        
    if buying == 1:
        pairs = 'BCH-USD'
            
    elif buying == 2:
        pairs = 'BTC-USD'
        
    
    elif buying == 3:
        pairs = 'ETH-USD'
        
    
    elif buying == 4:
        pairs = 'LTC-USD'
        
    
    #else: 
        #print(main())

    
    ask, bid = get_price(pairs)
    cost = float(ask * qty)
    date = datetime.datetime.now()
    df_blotter = update_blotter(pairs, qty, ask, cost, date)
    df_pl = update_pl(df_pl,pairs,qty,ask)
    print(df_blotter)
    print("Viewing Blotter")
    
        
    #if cost > cash:
       # print("Not Enough Cash For Transaction")
        #print(main())

         
    
        #return the value of the cash on hand
        #add values to pandas dataframe
        #return daily min, max (from pandas?)
        #return std (from pandas)
        
        
        #visualization: 
        #def 100dytrade(x_data, x_label, y1_data, y1_color, y1_label, y2_data, y2_color, y2_label, title):
                           
    
        
def sell(df_blotter,df_pl,pair, get_price):
    print("Please Choose The Pair You Woud Like To Sell")
    print("Please Choose From The Following Pair")
    print('\n')
    print("1. BCH-USD" )
    print("2. BTC-USD" )
    print("3. ETH-USD" )
    print("4. LTC-USD" )
    print("5. Return to Main Menu")
    print('\n\n')
    selling = input("Please Select [1:5]: ")
    
    qty = int(input('How Many Shares Are You Selling?: '))
    
    if selling == 1:
        pair = ('BCH-USD')
               
    elif selling == 2:
        pair = 'BTC-USD'
       
    elif selling == 3:
        pair = "ETH-USD"
        
    elif selling == 4:
        pair = "LTC-USD"
      
   
    ask, bid = get_price()    
            
    cost = float(qty * bid)
    date = datetime.datetime.now()
    df_blotter = update_blotter(pair, qty, bid, cost, date, df_blotter)
    df_pl = update_pl(df_pl, pair, qty, bid)
        
        #return the value of the cash on hand
        #add values to pandas dataframe

        
    
    #while pair > (pandas entry that has how many stocks you have on hand:
        #print("Not Enought Stocks To Make Transaction")
        #share_volume2= int(input('How Many Shares Are You Selling?: ')) 
    #else:
        #price2 = round(price * share_volume2,2)
        #price2 = str(price2)
        #print("Your total amount is : $"+price2)
        
    

def view_blotter(df_blotter):
    print("---- Trade Blotter")
    print(df_blotter)
    print("\n\n")


def view_pl(df_pl):
    # TODO Update UPL here
    print("---- PL")
    print(df_pl)
    print("\n\n")



#def dailymean(pair):
    #mean = (high() + low()) /2
    #return mean
    
    #get the mean to work, maybe this also needs to be a pandas dataframe


#def get_historical(pair):
    #df = client.get_product_historic_rates(pair, granularity = 86400)
    #return df
    #should this go to a pandas dataframe that I access?


if __name__ == "__main__":
    main()
