from flask import Flask, render_template, request, send_from_directory
import pytz, time
from datetime import datetime
from mostactivestocks import MostActiveStocks
import os
import pandas as pd

app = Flask(__name__)

# ============================================
# Required for requestResume() call in home.html.

app.config['UPLOAD_FOLDER'] = os.getcwd()

try:
    os.makedirs(app.config['UPLOAD_FOLDER'])
except:
    pass

def get_files(target):
    for file in os.listdir(target):
        path = os.path.join(target, file)
        if os.path.isfile(path):
            yield (
                file,
                datetime.utcfromtimestamp(os.path.getmtime(path)),
                os.path.getsize(path)
            )
            
@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )
# ============================================

@app.route('/')
@app.route('/mostactivestocks')
def handle_home():
    url = request.url
    args = url.split("=")
    market = args[1] if len(args) > 1 else ''
    htmlSrc = ''
    info = {}
    tzNY = pytz.timezone('America/New_York')
    dtNY = datetime.now(tzNY).strftime("%d%b%Y:%H:%M:%S %Z")
    dtLocal = datetime.now().strftime("%d%b%Y:%H:%M:%S") + ' ' +  time.localtime().tm_zone
    yhaooHref = ''
    investingHref = ''
    bankOfChinaHref = ''

    if market == MostActiveStocks.YahooMostActivesName:
        # --- Yahoo page ---
        htmlSrc, data = MostActiveStocks.getData(market)
        headings = MostActiveStocks.getHeading(market)
        return render_template('data.html', market=market, headings=headings, data=data, htmlSrc=htmlSrc, dtNY=dtNY, MostActiveStocks=MostActiveStocks())

    elif market == MostActiveStocks.InvestingMostActivesName:
        # --- Investing page ---
        htmlSrc, data = MostActiveStocks.getData(market)
        headings = MostActiveStocks.getHeading(market)
        return render_template('data.html', market=market, headings=headings, data=data, htmlSrc=htmlSrc,  dtNY=dtNY, MostActiveStocks=MostActiveStocks())

    elif market == MostActiveStocks.BankOfChinaForexName:
        # --- fx : BankOfChina ---
        htmlSrc, data = MostActiveStocks.parseUrl(market,'Currency Name')
        headings = MostActiveStocks.getHeading(market)
        return render_template('data.html', market=market, headings=headings, data=data, htmlSrc=htmlSrc,  dtNY=dtNY, MostActiveStocks=MostActiveStocks())
        
    else:
        # --- HOME page ---
        yhaooHref = f'{url}/mostactivestocks?market={MostActiveStocks.YahooMostActivesName}'
        investingHref = f'{url}/mostactivestocks?market={MostActiveStocks.InvestingMostActivesName}'
        bankOfChinaHref =  f'{url}/mostactivestocks?market={MostActiveStocks.BankOfChinaForexName}'

        if 'pythonanywhere' in url:
            yhaooHref = yhaooHref.replace("/mostactivestocks","",1)
            investingHref = investingHref.replace("/mostactivestocks","",1)
            bankOfChinaHref = bankOfChinaHref.replace("/mostactivestocks","",1)
        info = {
            'homePath' : url,
            'YahooHref' : yhaooHref,
            'InvestingHref' : investingHref,
            'BankOfChinaHref' : bankOfChinaHref,
            'dtLocal' : dtLocal,
            'dtNY' : dtNY,
        }
        return render_template('home.html', info=info, MostActiveStocks=MostActiveStocks())
