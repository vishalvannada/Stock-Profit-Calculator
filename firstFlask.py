import requests
import sys
from flask import Flask, jsonify, request, render_template
import urllib3
import datetime
from pytz import timezone

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def hello():

    if(request.method == 'POST'):

        tickerSymbol = request.form.get('tickerSymbol')
        allotment = int(request.form.get('allotment'))
        finalPrice = int(request.form.get('finalPrice'))
        sellCommission = int(request.form.get('sellCommission'))
        initialPrice = int(request.form.get('initialPrice'))
        buyCommission = int(request.form.get('buyCommission'))
        capitalGainTaxRate = int(request.form.get('capitalGainTaxRate'))

        proceeds = allotment * finalPrice
        purchasePrice = (allotment * initialPrice)
        totalExpenditure = purchasePrice + sellCommission + buyCommission
        capitalGain = proceeds - totalExpenditure
        tax = 0
        if capitalGain > 0 :
            tax = capitalGain * (capitalGainTaxRate/100)
        cost = totalExpenditure + tax
        netProfit = proceeds - cost
        roi = (netProfit/cost)*100


        data = {
        'tickerSymbol' : tickerSymbol,
        'allotment' : allotment,
        'finalPrice' : finalPrice,
        'sellCommission' : sellCommission,
        'initialPrice' : initialPrice,
        'buyCommission' : buyCommission,
        'capitalGainTaxRate' : capitalGainTaxRate,
        'proceeds' : proceeds,
        'purchasePrice' : purchasePrice,
        'totalExpenditure' : totalExpenditure,
        'capitalGain' : capitalGain,
        'tax' : tax,
        'cost' : cost,
        'netProfit' : netProfit,
        'roi' : roi
        }

        return render_template('output.html', data = data)
    return render_template('form.html')


@app.route("/stocks", methods = ['GET','POST'])
def helloStocks():
    if request.method == 'POST':

        stockSymbol = request.form.get('stockSymbol');
        try :

            result = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+stockSymbol+'&apikey=C3UMGJ3EA980AWMZ')
            data = result.json();
            print('vishal', data)

            symbol = data['Global Quote']['01. symbol'];
            price = data['Global Quote']['05. price'];
            change = data['Global Quote']['09. change'];
            changePercent = data['Global Quote']['10. change percent'];

            stockName = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+stockSymbol+'&apikey=C3UMGJ3EA980AWMZ')
            name = stockName.json()['bestMatches'][0]['2. name']

            fmt = "%a %b %d %H:%M:%S %Z %Y"
            now_utc = datetime.datetime.now(timezone('US/Pacific'))
            print('\nOutput : \n')

            time = now_utc.strftime(fmt);


            data = {
            'symbol' : symbol,
            'price' : price,
            'change' : float(change),
            'changePercent' : changePercent,
            'stockName' : stockName,
            'name' : name,
            'time' : time
            }
            return render_template('searchStocks.html', data = data);
        except :

            try:
                note = data['Note'];
                return render_template('searchStocks.html', error = {'error' : 'Connection Limit, Please try again later!'});
            except:
                return render_template('searchStocks.html', error = {'error' : 'Invalid Symbol, Please try again!'});



    return render_template('searchStocks.html');

if __name__ == '__main__':
    app.run(port=8000)
