#Cryptopia Framework
#Copyright Jeremy Scott 2017

#imports
from __future__ import division
import time     # used in api query
import urllib   # used in api query
import base64   # used in api query
import json     # used in api query
import hmac     # used in api query
import hashlib  # used in api query
import requests # used in api query
import threading
from os.path import isfile # for saving settings

def api_query( method, req = None ):
    try:
        if not req:
            req = {}
        public_set = set([ "GetCurrencies", "GetTradePairs", "GetMarkets", "GetMarket", "GetMarketHistory", "GetMarketOrders" ])
        private_set = set([ "GetBalance", "GetDepositAddress", "GetOpenOrders", "GetTradeHistory", "GetTransactions", "SubmitTrade", "SubmitTransfer","CancelTrade", "SubmitTip" ])
        if method in public_set:
            url = "https://www.cryptopia.co.nz/api/" + method
            if req:
                for param in req:
                    url += '/' + str( param )
            r = requests.get( url )
                    #print url
        elif method in private_set:
            url = "https://www.cryptopia.co.nz/api/" + method
            nonce = str( int( time.time() ) )
            post_data = json.dumps( req );
            m = hashlib.md5()
            m.update(post_data)
            requestContentBase64String = base64.b64encode(m.digest())
            signature = API_KEY + "POST" + urllib.quote_plus( url ).lower() + nonce + requestContentBase64String
            hmacsignature = base64.b64encode(hmac.new(base64.b64decode( API_SECRET ), signature, hashlib.sha256).digest())
            header_value = "amx " + API_KEY + ":" + hmacsignature + ":" + nonce
            headers = { 'Authorization': header_value, 'Content-Type':'application/json; charset=utf-8' }
            r = requests.post( url, data = post_data, headers = headers )
        response = r.text
        time.sleep(1)
        return response
    except:
        print "problem in api_query"
        return None

def getCurrencies():
    try:
        currencies_query = api_query("GetCurrencies")
        currencies = json.loads(currencies_query)
        return currencies
    except:
        print "problem in getCurrencies"
        return None

def getCurrencyDataByCoinSymbol(symbol):
    try:
        currencies = getCurrencies()
        index = -1
        for i in range (0,len(currencies["Data"])):
            if currencies["Data"][i]["Symbol"] == symbol:
                index = i
        data = {}
        data['Id'] = currencies['Data'][index]['Id']
        data['Name'] = currencies['Data'][index]['Name']
        data['Symbol'] = currencies['Data'][index]['Symbol']
        data['Algorithm'] = currencies['Data'][index]['Algorithm']
        data['WithdrawFee'] = '{:.8f}'.format(currencies['Data'][index]['WithdrawFee'])
        data['MinWithdraw'] = '{:.8f}'.format(currencies['Data'][index]['MinWithdraw'])
        data['MinBaseTrade'] = '{:.8f}'.format(currencies['Data'][index]['MinBaseTrade'])
        data['IsTipEnabled'] = currencies['Data'][index]['IsTipEnabled']
        data['MinTip'] = currencies['Data'][index]['MinTip']
        data['DepositConfirmations'] = currencies['Data'][index]['DepositConfirmations']
        data['Status'] = currencies['Data'][index]['Status']
        data['StatusMessage'] = currencies['Data'][index]['StatusMessage']
        data['ListingStatus'] = currencies['Data'][index]['ListingStatus']
        return data
    except:
        print "problem in getCurrencyDataByCoinSymbol"
        return None

def getTradePairs():
    try:
        tradePairs_query = api_query("GetTradePairs")
        tradePairs = json.loads(tradePairs_query)
        return tradePairs
    except:
        print "problem in getTradePairs"
        return None

def getTradePairDataByLabel(label):
    try:
        tradePairs = getTradePairs()
        index = -1
        for i in range (0,len(tradePairs["Data"])):
            if tradePairs["Data"][i]["Label"] == label:
                index = i
        data = {}
        data['Id'] = tradePairs['Data'][index]['Id']
        data['Label'] = tradePairs['Data'][index]['Label']
        data['Currency'] = tradePairs['Data'][index]['Currency']
        data['Symbol'] = tradePairs['Data'][index]['Symbol']
        data['BaseCurrency'] = tradePairs['Data'][index]['BaseCurrency']
        data['BaseSymbol'] = tradePairs['Data'][index]['BaseSymbol']
        data['Status'] = tradePairs['Data'][index]['Status']
        data['StatusMessage'] = tradePairs['Data'][index]['StatusMessage']
        data['TradeFee'] = '{:.8f}'.format(tradePairs['Data'][index]['TradeFee'])
        data['MinimumTrade'] = '{:.8f}'.format(tradePairs['Data'][index]['MinimumTrade'])
        data['MaximumTrade'] = '{:.8f}'.format(tradePairs['Data'][index]['MaximumTrade'])
        data['MinimumBaseTrade'] = '{:.8f}'.format(tradePairs['Data'][index]['MinimumBaseTrade'])
        data['MaximumBaseTrade'] = '{:.8f}'.format(tradePairs['Data'][index]['MaximumBaseTrade'])
        data['MinimumPrice'] = '{:.8f}'.format(tradePairs['Data'][index]['MinimumPrice'])
        data['MaximumPrice'] = '{:.8f}'.format(tradePairs['Data'][index]['MaximumPrice'])

        return data
    except:
        print "problem in getTradePairDataByLabel"
        return None

def getMarkets(base,hours):
    try:
        markets_query = api_query("GetMarkets",[base,hours])
        markets = json.loads(markets_query)
        return markets
    except:
        print 'problem in getMarkets'
        return None

def getMarket(pair):
    try:
        market_query = api_query("GetMarket",[pair])
        market = json.loads(market_query)
        data = {}
        data['TradePairId'] = market['Data']['TradePairId']
        data['Label'] = market['Data']['Label']
        data['AskPrice'] = '{:.8f}'.format(market['Data']['AskPrice'])
        data['BidPrice'] = '{:.8f}'.format(market['Data']['BidPrice'])
        data['Low'] = '{:.8f}'.format(market['Data']['Low'])
        data['High'] = '{:.8f}'.format(market['Data']['High'])
        data['Volume'] = '{:.8f}'.format(market['Data']['Volume'])
        data['LastPrice'] = '{:.8f}'.format(market['Data']['LastPrice'])
        data['BuyVolume'] = '{:.8f}'.format(market['Data']['BuyVolume'])
        data['SellVolume'] = '{:.8f}'.format(market['Data']['SellVolume'])
        data['Change'] = '{:.8f}'.format(market['Data']['Change'])
        data['Open'] = '{:.8f}'.format(market['Data']['Open'])
        data['Close'] = '{:.8f}'.format(market['Data']['Close'])
        data['BaseVolume'] = '{:.8f}'.format(market['Data']['BaseVolume'])
        data['BuyBaseVolume'] = '{:.8f}'.format(market['Data']['BuyBaseVolume'])
        data['SellBaseVolume'] = '{:.8f}'.format(market['Data']['SellBaseVolume'])
        return data
    except:
        print "couldn't get market for",pair
        return None

def getMarketHistory(pair):
    try:
        marketHistory_query = api_query("GetMarketHistory",[pair])
        marketHistory = json.loads(marketHistory_query)
        return marketHistory
    except:
        print "couldn't get market history for",pair
        return None

def getMarketOrders(pair):
    try:
        marketOrders_query = api_query("GetMarketOrders",[pair])
        marketOrders = json.loads(marketOrders_query)
        return marketOrders
    except:
        print "couldn't get market orders for", pair
        return None

def getCoinBalance(coin):
    try:
# print coin,"balance: ", api_query("GetBalance", {'Currency':coin})
        coinBalance_query = api_query("GetBalance", {'Currency':coin})
        coinBalance = json.loads(coinBalance_query)
        return coinBalance["Data"][0]["Available"]
    except:
        print "problem in getCoinBalance"
        return None

def getBaseBalance():
    try:
    # print coin,"balance: ", api_query("GetBalance", {'Currency':coin})
        baseBalance_query = api_query("GetBalance", {'Currency':base})
        baseBalance = json.loads(baseBalance_query)
        return baseBalance["Data"][0]["Available"]
    except:
        print "problem in getBaseBalance"
        return None

def getAllOrders():
    try:
        orders_query = api_query("GetOpenOrders")
        orders = json.loads(orders_query)
        return orders
    except:
        print "couldn't get the open sell orders..."
        return None

def getOpenOrders(coin,orders):
    try:
        orderlist = []
        buys = 0
        sells = 0
        for i in range(0,len(orders['Data'])):
            if orders['Data'][i]['Market']==coin+'/'+base:
                orderlist.append(orders['Data'][i])
                if orders['Data'][i]['Type'] == "Buy": buys += 1
                if orders['Data'][i]['Type'] == "Sell": sells += 1
        return orderlist, buys, sells
    except:
        print "couldn't get open orders for",coin+'/'+base
        return None

#place a buy order at sellPrice for coin of pair
def buyCoin(amount,sellPrice, pair):
    try:
        m = getMarket(pair)
        q = api_query("SubmitTrade", { 'TradePairId':m['TradePairId'], 'Type':"Buy", 'Rate':sellPrice, 'Amount':amount})
        print q
        return json.loads(q)
    except:
        print "may have failed to buy",pair,"at price",sellPrice
        return None


#place a sell order at sellPrice for coin of pair
def sellCoin(amount, sellPrice, pair):
    try:
        m = getMarket(pair)
        q = api_query("SubmitTrade", { 'TradePairId':m['TradePairId'], 'Type':"Sell", 'Rate':sellPrice, 'Amount':amount})
        print q
        return json.loads(q)
    except:
        print "may have failed to place sell order for",pair,"at price ",sellPrice
        return None


def checkBuyCancel(coin,oo):
    try:
        print "OO:",oo[0]
        for i in range(0,len(oo)):
            print oo[i]
            if oo[i]["Type"] == "Buy":
                oid = oo[i]["OrderId"]
                return api_query("CancelTrade",{"Trade":oid,"OrderId":oid})
    except:
        print "Problem in checkBuyCancel"
        return None

def listBasePairs():
    try:
        tradePairs = getTradePairs()
        #empty list for pairs that have user's base currency
        pairList = []
        for i in range(0,len(tradePairs['Data'])):
            if tradePairs['Data'][i]['BaseSymbol'] == base:
                pairList.append(tradePairs['Data'][i]['Symbol'])
        return pairList
    except:
        print "problem in listBasePairs"
        return None

def topFiftyMarkets(markets,plus):
    mv = []
    numMarkets = len(markets['Data'])
    for i in range(0,numMarkets):
        mv.append((markets['Data'][i]['Label'],float(markets['Data'][i]['BaseVolume'])))
    x = sorted(mv,key=lambda x: float(x[1]), reverse=True)[0:50+plus]
    topvolumepairs = []
    for e in x: topvolumepairs.append(e[0])
    for i in range(0,len(topvolumepairs)):
        topvolumepairs[i]=str.split(str(topvolumepairs[i]),'/')[0]

    return topvolumepairs

def transfer(transferAmount):
    #returns an error BUT IT STILL WORKS! tested 3 times, 100 satoshi each time
    api_query('SubmitTransfer',{'Currency':base,'Username':'TriphiusFire','Amount':transferAmount})

Rise = 0.0
base = 'BTC'
settings_file = "./Settings.json"
restore = None

if isfile(settings_file):

    restore = str(raw_input("\nrestore settings? Y/N : "))

    if restore == 'Y' or restore == 'y':
        with open(settings_file) as json_data:
            config_data = json.load(json_data)

            API_KEY = config_data['API_KEY']
            API_SECRET = config_data['API_SECRET']

            altcoininputlist = config_data['altcoinlist']
            altcoinlist = str.split(str(altcoininputlist),';')
            for i in range(0,len(altcoinlist)):
                altcoinlist[i] = altcoinlist[i]+'/BTC'
            print 'altcoinlist',altcoinlist
            exclusioninputlist = config_data['exclusionlist']

            exclusionlist = str.split(str(exclusioninputlist),';')
            print 'exclusionlist',exclusionlist
            risk = config_data['risk']
            Rise = config_data['rise']

            keep = config_data['keep']

if restore == None or (restore != 'Y' and restore != 'y'):
    #Customer Manually Enters api keys, base market, risk, min volume, rise for sell, drop for buy, alt coin keep, max trades per coin
    API_KEY = str(raw_input("\nAPI KEY? : "))
    API_SECRET = str(raw_input("API SECRET? : "))

    # API_KEY = ''       # for hardcoding personal use
    # API_SECRET = ''
    altcoininputlist = str(raw_input("\nEnter the coin abbreviations you want to trade separated by semicolons.  no spaces. \nOr don't write any just press <enter> \nthen the top 50 highest volume markets will be chosen during each cycle :\n"))
    altcoinlist = []
    if altcoininputlist != '':
        altcoinlist = str.split(altcoininputlist,';')
        for i in range(0,len(altcoinlist)): altcoinlist[i] = altcoinlist[i]+'/BTC'
    exclusioninputlist = str(raw_input("Enter the coin abbreviations you NEVER want to trade separated by semicolons. no spaces. \nOr don't write any just press <enter> \nthen you will trade all coins considered :\n"))
    exclusionlist = str.split(exclusioninputlist,';')
    risk = input("Slingshot's total BTC Risk? (ie: 0.5) : ")
    Rise = input("\nRise percentage? (Minimum profit, ie: 13) : ")
    keep = input("\nWhat percent of altcoin would you like to keep from each buy? (ie: 5) : ")
    keep = (100.0-keep)/100.0
    markets = getMarkets(base,24)           #get all possible markets

    if len(altcoinlist) == 0:
        altcoinlist = topFiftyMarkets(markets,len(exclusionlist))
        #print 'altcoinliststart',altcoinlist
        altcoininputlist = ''
        for i in range(0,len(altcoinlist)):
            altcoininputlist = altcoininputlist + ';' + altcoinlist[i]+'/BTC'
        altcoininputlist = altcoininputlist[1:len(altcoininputlist)]
        altcoinlist = str.split(altcoininputlist,';')

    save = str(raw_input("\nSave settings to auto-load next time? Y/N : "))
    if save == "Y" or save == "y":
        with open('Slingshot5v0Settings.json','w') as outfile:
            jsondata={}
            jsondata['API_KEY'] = API_KEY
            jsondata['API_SECRET'] = API_SECRET
            jsondata['altcoinlist'] = altcoininputlist
            jsondata['exclusionlist'] = exclusioninputlist
            jsondata['risk'] = risk
            jsondata['rise'] = Rise
            jsondata['keep'] = keep
            json.dump(jsondata,outfile)


clocktime = 30
class config:
    clock = 0
    allOrders = None
###############################################################################
# Main Algorithm
#

config.clock = 0

def mainLoop(p,rise):
    try:
        #THIS IS WHERE THE TRADING ALGORITHM GOES
        #THIS FILE WAS ORIGINALLY MY TRADING ROBOT "SLINGSHOT"
        #FEEL FREE TO MODIFY IT TO MAKE YOUR OWN TRADING LIST
        #THE FRAMEWORK I GIVE FOR FREE, IF YOU CAN USE THIS FRAMEWORK
        #TO RECREATE MY BOT, OR CREATE YOUR OWN, THEN BY ALL MEANS
        #GO FOR IT
    except:
        time.sleep(3)
        print "ERR TRUE", p
        #p WAS THE COIN INDEX WHERE THE ERROR HAPPENED
        mainLoop(p,Rise)
        return


while True:
    if config.clock <=0:
        config.clock = clocktime
        threading.Thread(target=mainLoop,args=(0,Rise)).start()
    time.sleep(1)
    config.clock = config.clock - 1
    #print "clock: ",config.clock
