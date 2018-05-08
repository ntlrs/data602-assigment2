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

from datetime import datetime, timedelta

from pymongo import MongoClient
from time import strftime, gmtime
from statistics import stdev

   
#reference: https://www.youtube.com/watch?v=8GRUwftKAps


                       
def main():    
    funds = 100000000.0 
       
    mongo = 'mongodb://test:test@ds235239.mlab.com:35239/data6022'
    client = MongoClient(mongo, connectTimeoutMS=30000)
    db = client.get_database("data602")
    db_blotter = db.db_blotter
    
    # Initialize data structures
    df_pl = initialize_pl()
    

    # Design a menu a system 
    menu = ('Buy', 'Sell', 'Show Blotter', 'Show PL', 'Quit')
    while True:
        choice = display_menu(menu,exit_option=5)
        if choice == 1:
            buy()
                    
        elif choice == 2:       
            sell(db_blotter)
        
        elif choice == 3:
            view_blotter(blotter)
        
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
def buy():

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
            
            new_line = {"Pair": pair, "Quantity" : qty, "Price": price, "Cost": total_cost, "Date": date}
            
            dailymin, dailymax = get_stats(pair)
            print("The daily high for " + pair + " is " + str(dailymin))
            print("The daily low for " + pair + " is " + str(dailymax))
            
            mean = dailymean(dailymin, dailymax)
            print("The daily mean for " + pair + " is " + str(mean))
            
            stddev = stdev([dailymax, dailymin])
            print("The daily standard deviation for " + pair + " is " + str(stddev))
            print("\n")
            
            hist = history(pair)
            print(hist)
            #df_pl = update_pl(pl, pair, qty, price, total_cost)
            
            
            
            data = pd.DataFrame([["Buy", pair, qty, ask, date, total_cost]], columns= ['Side','Pair','Volume','Executed Price', 'Time' , 'Cash Balance'])
            blotter_update = df_blotter.append(data, ignore_index = True)
            print(blotter_update)
            
            print("\n\n")
            print("Would You Like To Buy More or Return to Main Menu?: ")
            print("1. Buy Again")
            print("2. Main Menu")
            finish = int(input("Please Choose [1-2]: "))
            if finish == 1:
                buy(db_blotter, df_blotter, blotter)
            elif finish == 2:
                print(main())
            else:
                print("Not An Option")
                print("\n\n")
                print(buy(db_blotter, df_blotter, blotter))
            
            
            #if cost > cash:
            # print("Not Enough Cash For Transaction")
            #print(main())

         
    
        #return the value of the cash on hand
        #add values to pandas dataframe
        
        
        
def sell(df_blotter, collection):
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
            qty =  int(input("how much would you like to sell?: "))
            qty = (qty * -1)
            ask, bid = get_price(pair)
            
            price = float(bid)
            print("\n\n")
            print("The bid price for the pair is: " + str(bid))
            total_cost = float(qty * price)
            print("your total sale is: " + str(total_cost))
            print("\n")
            date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            df_blotter = update_blotter(pair, qty, price, total_cost, date)
            new_line = ({"Pair": pair, "Quantity" : qty, "Price": price, "Cost": total_cost, "Date": date})
            #df_blotter = df_blotter.append(new_line, ignore_index = True)
            update_db(new_line)
            
            dailymin, dailymax = get_stats(pair)
            print("\n")
            print("The daily high for " + pair + " is " + str(dailymin))
            print("The daily low for " + pair + " is " + str(dailymax))
            
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
            print("Would You Like To Sell More or Return to Main Menu?: ")
            print("1. Sell Again")
            print("2. Main Menu")
            finish = int(input("Please Choose [1-2]: "))
            if finish == 1:
                sell(df_blotter, collection)
            elif finish == 2:
                print(main())
            else:
                print("Not An Option")
                print("\n\n")
                print(sell(df_blotter, collection))
        
        #return the value of the cash on hand
        #add values to pandas dataframe

        
    
    #while pair > (pandas entry that has how many stocks you have on hand:
        #print("Not Enought Stocks To Make Transaction")
        #share_volume2= int(input('How Many Shares Are You Selling?: ')) 
    #else:
        #price2 = round(price * share_volume2,2)
        #price2 = str(price2)
        #print("Your total amount is : $"+price2)

def update_db(new_line):
    db_blotter.insert_one(new_line)    

def view_blotter(blotter):
    print("---- Trade Blotter")
    print(df_blotter)
    print("\n\n")


def view_pl(df_pl):
    # TODO Update UPL here
    print("---- PL")
    print(df_pl)
    print("\n\n")


def initialize_pl():
    pair = ['BCH-USD', 'BTC-USD', 'ETH-USD', 'LTC-USD']
    col_names = ['Pair','Position','VWAP','UPL','RPL', 'Total PL', 'Allocated By Share', 'Allocated By Dollar']
    pl = pd.DataFrame(columns=col_names)
    for p in pair:
        data = pd.DataFrame([[p,0,0,0,0,0,0,0]] ,columns=col_names)
        pl = pl.append(data, ignore_index=True)
    pl = pl.set_index('Pair')
    return pl

def update_cash(funds):
    cash = blotter['Cash Balance'].iloc[-1]
    return cash



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

def blotter():
    cols = ['Side','Pair','Volume','Executed Price', 'Time' , 'Cash Balance']
    df_blotter = pd.DataFrame(index = [0], columns=cols)
    return df_blotter



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


def history(pair):

    history = requests.get('https://api.gdax.com/products/' + pair + '/candles?granularity=86400')
    history = pd.read_json(history.text)
    history.columns = ['time', 'low', 'high','open','close', 'volume']
    history['time'] = pd.to_datetime(history['time'], unit = 's')
    history = history[:100]
    
    x = history['time']
    y = history['close']
    plt.title('100 Day Historical Data for ' + pair)
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
