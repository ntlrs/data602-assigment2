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
from datetime import datetime, timedelta
from math import sqrt
from pymongo import MongoClient
from time import strftime, gmtime
from statistics import stdev

import numpy as np

                       
def main():    
    # Initial portfolio size in cash
    cash = 100000000.0
    
    
    # Initialize data structures
    df_blotter = initialize_blotter()
    df_pl = initialize_pl()

    client = MongoClient()
    db = client.blotter
    collection = db.blotter
    new_line = {"Pair" : "Pair", 
            "Quantity" : "qty",
            "Price" : "Price", 
            "Cost" : "Total Cost",
            "Date" : "Date"
        }
    collection.insert_one(new_line)
   
    
    # Design a menu a system 
    menu = ('Buy', 'Sell', 'Show Blotter', 'Show PL', 'Quit')
    while True:
        choice = display_menu(menu,exit_option=5)
        if choice == 1:
            buy(df_blotter, collection)
                    
        elif choice == 2:       
            sell()
        
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



################################################
def buy(df_blotter, collection):
    pair = {1:"BCH-USD", 2: "BTC-USD", 3: "ETH-USD", 4: "LTC-USD", 5: "Main Menu"}
    print("Please Choose From The Following Pair")
    print('\n')
    print("1. BCH-USD" )
    print("2. BTC-USD" )
    print("3. ETH-USD" )
    print("4. LTC-USD" )
    print("5. Return to Main Menu")
    print('\n\n')
    buying = int(input("Please Choose [1-5]: "))
    while buying == 5:
        print(main())
    
    while buying != 5:
                
        if buying == 1:
            pair = 'BCH-USD' 
        elif buying == 2:
            pair = 'BTC-USD'      
        elif buying == 3:
            pair = 'ETH-USD'  
        elif buying == 4:
            pair = 'LTC-USD'
        else:
            buying = int(buying)
            if buying > 5:
                print("Not an option")
                continue
   
    
        
        
        while True:
            qty =  int(input("how much would you like to purchase?: "))
            ask, bid = get_price(pair)
            
            price = float(ask)
            print("\n\n")
            print("The price for the pair is: " + str(ask))
            total_cost = float(qty * price)
            print("your total is: " + str(total_cost))
            print("\n")
            date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            df_blotter = update_blotter(pair, qty, price, total_cost, date)
            new_line = ({"Pair": pair, "Quantity" : qty, "Price": price, "Cost": total_cost, "Date": date})
            df_blotter = df_blotter.append(new_line, ignore_index = True)
            collection.insert_one(new_line)
            
            dailymin, dailymax = get_stats(pair)
            print("\n")
            print("The daily high for " + pair + " is " + str(dailymax))
            print("The daily low for " + pair + " is " + str(dailymin))
            
            mean = dailymean(dailymin, dailymax)
            print("\n")
            print("The daily mean for " + pair + " is " + str(mean))
            
            stddev = stdev([dailymax, dailymin])
            print("\n")
            print("The daily standard deviation for " + pair + " is " + str(stddev))
            print("\n")
            
            hist = history(pair)
            print(hist)
            #df_pl = update_pl(pl, pair, qty, price, total_cost)
            print("\n")
            print(df_blotter)
           
        
            print("\n\n")
            print("Would You Like To Buy More or Return to Main Menu?: ")
            print("1. Buy Again")
            print("2. Main Menu")
            finish = int(input("Please Choose [1-2]: "))
            if finish == 1:
                buy(df_blotter, collection)
            elif finish == 2:
                print(main())
            else:
                print("Not An Option")
                print("\n\n")
                print(buy(df_blotter, collection))
            
        
    #if cost > cash:
       # print("Not Enough Cash For Transaction")
        #print(main())

         
    
        #return the value of the cash on hand
        #add values to pandas dataframe
        #return daily min, max (from pandas?)
        #return std (from pandas)
        
        
        #visualization: 
        #def 100dytrade(x_data, x_label, y1_data, y1_color, y1_label, y2_data, y2_color, y2_label, title):
                           
    
        
def sell():
    pair = {1:"BCH-USD", 2: "BTC-USD", 3: "ETH-USD", 4: "LTC-USD", 5: "Main Menu"}
    print("Please Choose From The Following Pair")
    print('\n')
    print("1. BCH-USD" )
    print("2. BTC-USD" )
    print("3. ETH-USD" )
    print("4. LTC-USD" )
    print("5. Return to Main Menu")
    print('\n\n')
    selling = int(input("Please Choose [1-5]: "))
    while selling != 5:
        
        if selling == 5:
            print(main())
        elif selling == 1:
            pair = 'BCH-USD' 
        elif selling == 2:
            pair = 'BTC-USD'      
        elif selling == 3:
            pair = 'ETH-USD'  
        elif selling == 4:
            pair = 'LTC-USD'
        else:
            selling = int(selling)
            if selling > 5:
                print("Not an option")
                continue
   
        while True:
            qty =  int(input("how many shares would you like to sell?: "))
            ask, bid = get_price(pair)
            
            price = float(bid)
            print("The price for the pair is: " + str(bid))
            total_cost = float(qty * price)
            print("your total is: " + str(total_cost))
            date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            df_blotter = update_blotter(pair, qty, price, total_cost, date, df_blotter)
            
            #df_pl = update_pl(pl, pair, qty, price, total_cost)
            print(df_blotter)
    
        
            print("\n\n")
            print("Would You Like To Buy More or Return to Main Menu?: ")
            print("1. Sell Again")
            print("2. Main Menu")
            finish = input("Please Choose [1-2]: ")
            if finish == 1:
                print(sell())
            elif finish == 2:
                print(main())
            else:
                print("Not An Option")
                print("\n\n")
                print(sell())   
        
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


    
    #get the mean to work, maybe this also needs to be a pandas dataframe


#def get_historical(pair):
    #df = client.get_product_historic_rates(pair, granularity = 86400)
    #return df
    #should this go to a pandas dataframe that I access?
    


def initialize_blotter():
    col_names = ['Pair','Quantity','Price', 'Cost', 'Date']
    return pd.DataFrame(columns=col_names)


def initialize_pl():
    pair = ['BCH-USD', 'BTC-USD', 'ETH-USD', 'LTC-USD']
    col_names = ['Pair','Position','VWAP','UPL','RPL', 'Total PL', 'Allocated By Share', 'Allocated By Dollar']
    pl = pd.DataFrame(columns=col_names)
    for p in pair:
        data = pd.DataFrame([[p,0,0,0,0,0,0,0]] ,columns=col_names)
        pl = pl.append(data, ignore_index=True)
    pl = pl.set_index('Pair')
    return pl


def update_blotter(pair, qty, price, total_cost, date, printout = False):
    df_blotter = initialize_blotter()
    col_names = ['Pair','Quantity','Price', 'Cost', 'Date']
    row = (pair, qty, price, total_cost, date)
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
    stats = requests.get('https://api.gdax.com/products/'+pair+'/stats')
    data = stats.text
    parsed = json.loads(data)
    dailymax = parsed['high']
    dailymin = parsed['low']
    return float(dailymax), float(dailymin)

def dailymean(dailymax, dailymin):
    mean = (dailymax + dailymin) / 2
    return mean

def stddev(dailymax, dailymin):
    stdev([dailymax, dailymin])
    return stddev

def hist_100():
    hist_100 = datetime.now() - timedelta(days=100)
    hist_100 = hist_100.isoformat() 
    return hist_100

def end():
    end = datetime.now()
    end = end.isoformat()
    return end


def history(pair):

    history = requests.get('https://api.gdax.com/products/' + pair + '/candles?granularity=86400')
    history = pd.read_json(history.text)
    history.columns = ['time', 'low', 'high','open','close', 'volume']
    history['time'] = pd.to_datetime(history['time'], unit = 's')
    history = history[:100]
    
    x = history['time']
    y = history['close']
    plt.title('100 Day Historical Data from ' + pair)
    graph = plt.plot(x,y)
    return plt.show(graph)
     


def load(url,printout=False,delay=0,remove_bottom_rows=0,remove_columns=[]):
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
