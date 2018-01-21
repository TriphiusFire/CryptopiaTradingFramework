from __future__ import division
import time    
import urllib
import base64  
import json    
import hmac     
import hashlib
import requests
import threading
from pandas.io.json import json_normalize
from os.path import isfile 
from operator import indexOf

class CryptopiaAPI:
    
    def __init__(self,api_key,api_secret):
        #keys
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        
    def api_query(self, method, req = None ):
        try:
            if not req:
                req = {}
            public_set = set([ "GetCurrencies", "GetTradePairs", "GetMarkets", "GetMarket", "GetMarketHistory", "GetMarketOrders", "GetMarketOrderGroups"])
            private_set = set([ "GetBalance", "GetDepositAddress", "GetOpenOrders", "GetTradeHistory", "GetTransactions", "SubmitTrade", "SubmitTransfer","CancelTrade", "SubmitTip" ])
            if method in public_set:
                url = "https://www.cryptopia.co.nz/api/" + method
                if req:
                    for param in req:
                        url += '/' + str( param )
                r = requests.get( url)
            elif method in private_set:
                url = "https://www.cryptopia.co.nz/api/" + method
                nonce = str( int( time.time() ) )
                post_data = json.dumps( req );
                m = hashlib.md5()
                m.update(post_data)
                requestContentBase64String = base64.b64encode(m.digest())
                signature = self.API_KEY + "POST" + urllib.quote_plus( url ).lower() + nonce + requestContentBase64String
                hmacsignature = base64.b64encode(hmac.new(base64.b64decode( self.API_SECRET ), signature, hashlib.sha256).digest())
                header_value = "amx " + self.API_KEY + ":" + hmacsignature + ":" + nonce
                headers = { 'Authorization': header_value, 'Content-Type':'application/json; charset=utf-8' }
                r = requests.post( url, data = post_data, headers = headers)
            response = r.text
            time.sleep(1)
            return json.loads(response)
        except: 
            print "problem in api_query"
            return None

    """
    Get the index of a key/value pair in an array of json dictionaries
    """
    def GetIndex(self,key,val,dic):
        try:
            for i in range(0,len(dic)):
                if dic[i][key]==val:return i
            return None
        except: 
            return None

    """
    Return the base symbol list discovered in __init__
    """
    def GetBaseSymbols(self):
        tradepairs = self.GetTradePairs()
        bases = []
        for p in tradepairs:
            if p["BaseSymbol"] not in bases:
                bases.append(p["BaseSymbol"])
        return bases
        
    """
    Return the minimum trade size for this base currency.
    Any number *higher* than this works, so we add 1 satoshi
    """
    def GetMinimumBaseTrade(self,base):
        try:
            tradepairs = self.GetTradePairs()
            return tradepairs[self.GetIndex("BaseSymbol",base,tradepairs)]["MinimumBaseTrade"]
        except:
            return None

    """
    Return the maximum trade size for this base currency.
    Probably won't need this...
    """
    def GetMaximumBaseTrade(self,base):
        try:
            tradepairs = self.GetTradePairs()
            return tradepairs[self.GetIndex("BaseSymbol",base,tradepairs)]["MaximumBaseTrade"]
        except: 
            return None
    """
    Get all currency data: 
        Status, Name, Algorithm, MaxWithdraw, MinWithdraw, Symbol, Id, DepositConfirmations,
        MinBaseTrade, MinTip, IsTipEnabled, ListingStatus, WithdrawFee, StatusMessage
    """
    def GetCurrencies(self):
        try:
            return self.api_query("GetCurrencies")["Data"]
        except:
            print "GetCurrencies Exception"
            return None
    
    """
    Get all tradepair data:
        Status, BaseSymbol, MinimumTrade, MaximumTrade, MaximumPrice, Symbol, MaximumBaseTrade, 
        Label, Currency, StatusMessage, TradeFee, MinimumPrice, Id, BaseCurrency, MinimumBaseTrade
    """
    def GetTradePairs(self):
        try:
            return self.api_query("GetTradePairs")["Data"]
        except: 
            print "GetTradePairs Exception"
            return None
            
    """
    Get all Market Data:
        SellVolume, Volume, LastPrice, TradePairId, SellBaseVolume, Label, High, BidPrice,
        Low, BuyBaseVolume, Close, BaseVolume, Open, AskPrice, Change, BuyVolume
    """
    def GetMarkets(self):
        try:
            return self.api_query("GetMarkets")["Data"]
        except:
            print "GetMarkets Exception"
            return None
        
    """
    Get all Buy and Sell Market Orders for a tradepair "coin_base"
    """
    def GetMarketOrders(self,pair):
        try:
            return self.api_query("GetMarketOrders",[pair])["Data"]
        except:
            print "GetMarketOrders Exception"
            return None
        
    """
    Get the average price for the amount of coin wanted to buy
    Get the actual buy price needed to fulfill the order
    tuple - (average price, actual price)
    """
    def GetAverageBuyPrice(self,pair,amount):
        try:
            #We buy from someone's sell order
            sellOrders = self.GetMarketOrders(pair)["Sell"]
            remaining = amount
            volumes = []
            prices = []
            for i in range(0,len(sellOrders)):
                if sellOrders[i]["Volume"] < remaining:
                    volumes.append(sellOrders[i]["Volume"])
                    prices.append(sellOrders[i]["Price"])
                    remaining = remaining - sellOrders[i]["Volume"]
                else:
                    actualPrice = sellOrders[i]["Price"]
                    volumes.append(remaining)
                    prices.append(sellOrders[i]["Price"])
                    products = 0
                    for j in range(0,len(volumes)):
                        products = products + (prices[j]*volumes[j])
                    averagePrice = products/sum(volumes)
                    return (averagePrice,actualPrice)   
        except:
            print "GetBuyPrice Exception"
            return None
    
    """
    Get the average price for the amount of coin wanted to sell
    Get the actual sell price needed to fulfill the order
    tuple - (average price, actual price)
    """
    def GetAverageSellPrice(self,pair,amount):
        try:
            #We sell to someone's buy order
            sellOrders = self.GetMarketOrders(pair)["Buy"]
            remaining = amount
            volumes = []
            prices = []
            for i in range(0,len(sellOrders)):
                if sellOrders[i]["Volume"] < remaining:
                    volumes.append(sellOrders[i]["Volume"])
                    prices.append(sellOrders[i]["Price"])
                    remaining = remaining - sellOrders[i]["Volume"]
                else:
                    actualPrice = sellOrders[i]["Price"]
                    volumes.append(remaining)
                    prices.append(sellOrders[i]["Price"])
                    products = 0
                    for j in range(0,len(volumes)):
                        products = products + (prices[j]*volumes[j])
                    averagePrice = products/sum(volumes)
                    return (averagePrice,actualPrice)   
        except:
            print "GetSellPrice Exception"
            return None
    
    """
    Get the coin balance for a specific coin
    """    
    def GetAvailableBalance(self,coin):
        try:
            return self.api_query("GetBalance", {"Currency":coin})["Data"][0]["Available"]
        except:
            print "GetAvailableBalance Exception"
            return None
    
    """
    Get the open orders for a specific coin
    """
    def GetOpenOrders(self,market):
        try:
            return self.api_query("GetOpenOrders",{"Market":market})["Data"]
        except:
            print "GetOpenOrders Exception"
            return None
       
    """
    Get the Trade History for a specific market, and specific number of entries
    """
    def GetTradeHistory(self,pair,count):
        try:
            return self.api_query("GetTradeHistory",{"Market":pair.replace("_","/"),"Count":count})["Data"]
        except:
            print "GetTradeHistory Exception"
            return None
        
        
    """
    Submit a buy or sell trade for an amount at a price for a specific market
    Pair must come in form coin_base
    """
    def SubmitTrade(self,t,amount,price, pair):
        try:
            return self.api_query("SubmitTrade", { "Market":pair.replace("_","/"), "Type":t, "Rate":price, "Amount":amount})
        except: 
            print "SubmitTrade Exception"
            print "Failed to",type,pair,"at price",price
            return None
