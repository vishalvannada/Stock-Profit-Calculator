from flask import Flask, request, render_template
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



if __name__ == '__main__':
    app.run(debug=True)
