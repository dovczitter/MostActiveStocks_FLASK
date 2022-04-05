from flask import Flask
from flask import request
import json
import time
from mostactivestocks import MostActiveStocks

app = Flask(__name__)

@app.route('/mostactivestocks', methods = ['GET', 'POST'])
def handle_request():
    MostActiveStocks.marketListInit()
    url = request.url
    print(f'url:{request.url}, url_root;{request.url_root}, base_url:{request.base_url} host_url:{request.host_url} root_url:{request.root_url}')
    args = f'{url}'.split("=")
    market = args[1] if len(args) > 1 else ''
    homePath = f'{url}'
    marketUrl = ''
    for item in MostActiveStocks.marketList:
        if item[0].lower() == market.lower():
            marketName = item[0]
            marketUrl = item[1]
            break

    if marketUrl == '':
        return MostActiveStocks.getHomeStr(homePath).encode("utf-8")
    else :
        htmlTitle, tableData = MostActiveStocks.getJson(marketUrl, marketName)
        return MostActiveStocks.getDataStr(htmlTitle, homePath, tableData).encode("utf-8")
