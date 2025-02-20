import copy
import json
import random
import string
import logging
from threading import Thread
from flask import Flask, render_template, request

app = Flask(__name__)

OHLC = [
    { "date": "2024-11-10", "open": 0.3, "high": 0.5, "low": -0.1, "close": 0.2 },
    { "date": "2024-11-09", "open": 0.9, "high": 1.7, "low": -2.5, "close": 0.6 },
    { "date": "2024-11-08", "open": 0.1, "high": 0.8, "low": -0.8, "close": -0.8 }
]

@app.route('/')
def home():
    # name = request.args.get('name', "Quantum Dynamics Corp.")
    # ticker = request.args.get('ticker', "QDY")
    name = app.config['DEFAULT_NAME']
    ticker = app.config['DEFAULT_TICKER']
    ytd_return = app.config['DEFAULT_YTD_RETURN']
    price = app.config['DEFAULT_PRICE']

    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    template = '<tr id="{id_prefix}-'+random_suffix+'"><td>{name}</td><td class="price">{value}</td></tr>'
    metrics = [
        {
            "name": "YTD Return",
            "id_prefix": "ytd-return",
            "value": ytd_return
        },
        {
            "name": "Profit Margin",
            "id_prefix": "profit-margin",
            "value": "18.7%"
        },
        {
            "name": "Revenue",
            "id_prefix": "revenue",
            "value": "$10.5 Billion"
        },
    ]
    # Shuffle the order of the rows.
    metrics = random.sample(metrics, len(metrics))
    rows = "".join([
        template.format(**metric) for metric in metrics
    ])

    ohlc = copy.deepcopy(OHLC)
    #
    for row in ohlc:
        for key in row:
            if isinstance(row[key], (int, float)):
                row[key] = round(row[key] + price, 2)

    return render_template('index.html', name=name, ticker=ticker, ytd_return=ytd_return, financial_metrics=rows, ohlc=json.dumps(ohlc))

def run(port, name="Quantum Dynamics Corp.", ticker="QDY", ytd_return="12.3%", price=129):
    app.config['DEFAULT_NAME'] = name
    app.config['DEFAULT_TICKER'] = ticker
    app.config['DEFAULT_YTD_RETURN'] = ytd_return
    app.config['DEFAULT_PRICE'] = price

    app.run(host='0.0.0.0', port=port)

def start(port, name, ticker, ytd_return, price):
    t = Thread(target=run, args=[port, name, ticker, ytd_return, price])
    t.start()

if __name__ == '__main__':
    run(port=5001) # change the port to 5001 because in OSX, 5000 is already used 
