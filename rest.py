"""
Primary restful api to handle requests to handle UI requests

User Interactions
- Buy/Sell Stickers
    - Type of Sticker (id or name?)
    - Number of stickers
    - Market or Limit(min, max) Order

Display Information
- Display User Information
    - Types and Count of stickers owned
    - Balance
    - Username
    - Avatar



"""

from flask import Flask, abort, jsonify, request, send_from_directory, render_template
from flask_restful import Resource, Api

import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse('postgres://gxspomxmufoybd:dskomEuwa9JYaxf8Jd7h8JYVKo@ec2-54-221-253-117.compute-1.amazonaws.com:5432/d62ndf8grb25cb')

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
cursor = conn.cursor()

app = Flask(__name__, static_url_path='')
api = Api(app)


@app.route('/entity/', methods=['GET'])
def get_entities():
    """
    :return: All Users
    """
    cursor.execute(
        'SELECT * FROM "entity"'
    )
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/inventory/<int:user_id>', methods=['GET'])
def get_inventory(user_id):
    cursor.execute(
        'SELECT * FROM "inventory" WHERE "userid" = %s' % user_id
    )
    return jsonify(cursor.fetchall())

@app.route('/order/', methods=['GET'])
def get_orders():
    cursor.execute(
        'SELECT * FROM "order"'
    )
    return jsonify(cursor.fetchall())

@app.route('/ledger/', methods=['GET'])
def get_ledgers():
    cursor.execute(
        'SELECT * FROM "ledger"'
    )
    return jsonify(cursor.fetchall())


@app.route('/price_history/<string:ticker>', methods=['GET'])
def get_price_history(ticker):
    cursor.execute(
        'SELECT * FROM "%s_price_history"' % ticker
    )
    return jsonify(cursor.fetchall())

@app.route('/buy/', methods=['POST'])
def buy():
    if not request.json or 'vol' not in request.json \
        or 'price' not in request.json or 'ticker' not in request.json \
        or 'isBuy' not in request.json or 'isMarket' not in request.json:
        abort(400)
    val = request.json['val']
    price = request.json['price']
    ticker = request.json['ticker']
    isBuy = request.json['isBuy']
    isMarket = request.json['isMarket']
    cursor.execute(
        'INSERT INTO "order"(val, price, ticker, isBuy, isMarket) VALUES '
        '( %s, %s, %s, %s, %s, %s)' % (val, price, ticker, isBuy, isMarket)
    )
    cursor.commit()
    return []

@app.route('/src/<path:path>')
def src(path):
    print path
    return send_from_directory('static/src', path)

# @app.route('/<path:path>')
# def static_proxy(path):
#   # send_static_file will guess the correct MIME type
#   return send_from_directory('static', path)

# @app.route('/')
# def root():
#     return send_from_directory('static', 'index.html')

    # return render_template('static/index.html')


if __name__ == '__main__':
    app.run(debug=True)