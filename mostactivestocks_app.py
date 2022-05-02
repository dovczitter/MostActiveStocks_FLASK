from flask import Flask, render_template, request
import requests
import json
import time
from mostactivestocks import MostActiveStocks

app = Flask(__name__)

@app.route('/')
def handle_home():
    return render_template('home.html')
#   return MostActiveStocks.getHomeStr(request.url).encode("utf-8")

@app.route('/beer')
def handle_beer():
    beer_url = 'https://api.punkapi.com/v2/beers/random'
    r = requests.get(beer_url)
    beer_json = r.json()

    beer = {
        'name':beer_json[0]['name'],
        'abv':beer_json[0]['abv'],
        'description':beer_json[0]['description'],
        'foodpair':beer_json[0]['food_pairing'],
    }
#   print(beer)
    return render_template('index.html',beer=beer)

@app.route('/mostactivestocks', methods = ['GET', 'POST'])
def handle_mostactivestocks():
#   https://finance.yahoo.com/most-active
#   https://finance.yahoo.com/most-active?count=300&offset=0
#   MostActiveStocks.marketListInit()
#   https://www.investing.com/equities/52-week-high
#   https://www.investing.com/equities/52-week-low
#   https://www.investing.com/equities/most-active-stocks
#   https://www.investing.com/equities/top-stock-gainers
#   https://www.investing.com/equities/top-stock-losers      

    url = request.url
    print(f'url:{request.url}, url_root;{request.url_root}, base_url:{request.base_url} host_url:{request.host_url} root_url:{request.root_url}')
    args = f'{url}'.split("=")
    market = args[1] if len(args) > 1 else ''
    homePath = f'{url}'
    marketUrl = ''
    if market == MostActiveStocks.marketYahooMostActives:
#       -wip- '&' and '?' do not work, bash limitation        
#       marketUrl = 'https://finance.yahoo.com/most-active?count=10&offset=0'
        marketUrl = 'https://finance.yahoo.com/most-active'
    elif market == MostActiveStocks.marketInvestingMostActives:
        marketUrl = 'https://www.investing.com/equities/most-active-stocks'
    if marketUrl == '':
        return MostActiveStocks.getHomeStr(homePath).encode("utf-8")
    else :
        htmlTitle, tableData = MostActiveStocks.getJson(market,marketUrl)
        return MostActiveStocks.getDataStr(htmlTitle, homePath, tableData).encode("utf-8")
