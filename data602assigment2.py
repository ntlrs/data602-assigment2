#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 20:25:42 2018

@author: ntlrsmllghn
"""

import numpy as np
import pandas as pd
import requests
import json

api_request = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=0")
api = json.loads(api_request.content)

currencies = []

coins_list=[]
for coins in api:
    coins_list.append(coins["symbol"])

len(coins_list)
coins_list[:5]

#Blotter
blotter = [{"sym","volume","price", "cost", "total_price","date","cash"}]

portfolio_profit_loss = 0


for x in api:
    for coin["sym"] in blotter:
        if coin == x["symbol"]:
            #math
            
            cost = float(blotter["price"]) * float(blotter["volume"])
            current_value = float(blotter["price"]) * float(x["price_usd"])
            profit_loss = cost - current_value
            portfolio_profit_loss += profit_loss
            profit_loss_per_coin = float(x["price_usd"]) - float(blotter["volume"])
            
            
            
            print(x["name"])
            print("${0:.2f}".format(float(profit_loss_per_coin)))
            print("${0:.2f}".format(float(x["price_usd"])))
            print("cost: ${0.2f}".format(float([cost])))
            print("currnt value: ${0.2f}".format(float([current_value])))
            print("Profit/Loss: ${0.2f}".format(float([profit_loss])))
           
            
print("Portfolio Profit/Loss: ${0:.2f}".format(float(portfolio_profit_loss)))

def main_menu():       #main menu
    print 30 * "-" , "MENU" , 30 * "-"
    print("1. Trade")
    print("2. Show Blotter")
    print("3. Show P/L")
    print("4. Quit")
    print (67 * "-")
    choice = input("Please Select [1-4]: ")
  
    if choice == 1:     
        print("1. Return to Main Menu")
        print("2. Quit")
        select = input("Please Select [1 or 2]: ")
        if select == 1:
            main_menu()
        elif select == 2:
            sys.exit(0)
                
    elif choice == 2:
        print("Viewing Blotter") 
        print("Return to Main Menu or Quit?")
        print("1. Return to Main Menu")
        print("2. Quit")
        select = input("Please Select [1 or 2]: ")
        if select == 1:
            main_menu()
        elif select == 2:
            sys.exit(0)
        
              
    elif choice == 3:
        print ("Show P/L")   
        print("1. Return to Main Menu")
        print("2. Quit")
        select = input("Please Select [1 or 2]: ")
        if select == 1:
            main_menu()
        elif select == 2:
            sys.exit(0)
        
    elif choice == 4:
        print ("Quit")
        sys.exit(0)
        
    else:
        # Any integer inputs other than values 1-4 we print an error message
        input("Not An Option")
        main_menu()