import pandas as pd
import json
import requests
import os
from bs4 import BeautifulSoup
#from io import StringIO
#import sys

# Local Ubuntu
import cloudscraper

class MostActiveStocks:

    def __init__(self):
        print('MostActiveStocks init')
        pass

    version='6.10'
    hostName=''
    serverPort=0
    YahooMostActivesName='YahooMostActives'
    InvestingMostActivesName='InvestingMostActives'
    BankOfChinaForexName='BankOfChina'
      
    #
    # ================ classmethods ================
    #

    # ------------------------------------------------------------------------
    #                       configInit
    # ------------------------------------------------------------------------
    @classmethod
    def configInit(self):
        self.hostName=''
        self.serverPort=0
        with open('webserver.json') as f:
            data = json.load(f)
        if data.get('hostName'):
            self.hostName=data['hostName']
        if data.get('serverPort'):
            self.serverPort=data['serverPort']
        return

    #
    # ================ static methods ================
    #

    # ------------------------------------------------------------------------
    #                       getYahooHref
    # ------------------------------------------------------------------------
    @staticmethod
    def getYahooHref(symbol, htmlSrc):
        href = f'https://finance.yahoo.com/quote/{symbol}?p={symbol}'
        return href

    # ------------------------------------------------------------------------
    #                       getInvestingHref
    # ------------------------------------------------------------------------
    @staticmethod
    def getInvestingHref(symbol, htmlSrc):
        href = ''
        startPos = -1
        endPos = -1
        endPos = htmlSrc.find(f"'>{symbol}</a><span class")
        if endPos > 0:
            begStr = "href='/equities/" 
            startPos = htmlSrc.rindex(begStr, 0, endPos)
        if startPos >= 0:
            startPos = startPos + len(begStr)
        if startPos >= 0 and endPos >= 0 and startPos <= endPos:
            investSymbol = htmlSrc[startPos:endPos].strip()
            href = f'https://www.investing.com/equities/{investSymbol}'
        return href

    # ------------------------------------------------------------------------
    #                       getData
    # ------------------------------------------------------------------------
    @staticmethod
    def getData(market):
        url = MostActiveStocks.getUrl(market)
        htmlSrc = ''
        data = ''
        try:
            # --- NOTE : comment out accordingly
            
            # PythonAnywhere
            #htmlSrc = requests.get(url).text
            # Local Ubuntu
            scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})
            htmlSrc = scraper.get(url).text

            df_list = pd.read_html(htmlSrc, flavor='html5lib')
            df = df_list[0]
            df.head()
        except Exception as e:
            return e, data

        jsonResult = df.to_json(orient="values")
        jsonParsed = json.loads(jsonResult)
        data = jsonParsed
#        print(f'getData data: {data}')      
        return htmlSrc, data

    # ------------------------------------------------------------------------
    #                       parseUrl
    # ------------------------------------------------------------------------
    @staticmethod
    def parseUrl(market, headerTag):
        url = MostActiveStocks.getUrl(market)
        htmlSrc = ''
        data = ''
        foundTag = False
        dfLen = len(pd.read_html(url))
        for i in range(dfLen):
            df = pd.read_html(url)[i]
            jsonResult = df.to_json(orient="values")
            jsonParsed = json.loads(jsonResult)
            if foundTag:
                data = jsonParsed
#                print(f'parse_url data: {data}')
                break
            tstr = str(df)
            if tstr.find(headerTag) != -1: 
                foundTag = True
                continue

        return htmlSrc, data
 
    # ------------------------------------------------------------------------
    #                       getHeading
    # ------------------------------------------------------------------------
    @staticmethod
    def getHeading(market):

        headings = []
        mas_dict = {}
        fx_dict = {}

        # https://www.youtube.com/watch?v=mII5mrU46rs
        # https://stackoverflow.com/questions/6740918/creating-a-dictionary-from-a-csv-file
        try:
            fn = f'{os.getcwd()}/MostActiveStocks.csv'
            mas_dict = pd.read_csv(fn).to_dict('records')

            fn = f'{os.getcwd()}/ForeignExchangeRates.csv'
            fx_dict = pd.read_csv(fn).to_dict('records')
        except Exception as e:
            return f'csv file read error: {e}'

        if (market in [MostActiveStocks.YahooMostActivesName, MostActiveStocks.InvestingMostActivesName] ):
            for row in mas_dict:
                if row['Name'] == market:
                    for index, (key, value) in enumerate(row.items()):
                        if (index > 1):
                            if not pd.isnull(value):
                                headings.append(value)
                    break
        else:
            for row in fx_dict:
                if row['Name'] == market:
                    for index, (key, value) in enumerate(row.items()):
                        if (index > 1):
                            if not pd.isnull(value):
                                headings.append(value)
                    break

        return headings
    
     # ------------------------------------------------------------------------
    #                       getUrl
    # ------------------------------------------------------------------------
    @staticmethod
    def getUrl(market):

        url = ''
        mas_dict = {}
        fx_dict = {}

        try:
            fn = f'{os.getcwd()}/MostActiveStocks.csv'
            mas_dict = pd.read_csv(fn).to_dict('records')

            fn = f'{os.getcwd()}/ForeignExchangeRates.csv'
            fx_dict = pd.read_csv(fn).to_dict('records')
        except Exception as e:
            return f'csv file read error: {e}'

        if (market in [MostActiveStocks.YahooMostActivesName, MostActiveStocks.InvestingMostActivesName] ):
            for row in mas_dict:
                if row['Name'] == market:
                    url = row['Url']
                    break
        else:
            for row in fx_dict:
                if row['Name'] == market:
                    url = row['Url']
                    break

        return url
