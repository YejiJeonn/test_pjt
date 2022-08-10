from crypt import methods
from itertools import product
from flask import Flask, render_template, request, redirect
from flask.json import jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/local'
mongo = PyMongo(app)

@app.route('/detail') #어떤 부분에서 쓰이는 페이지인건지?
def detail():
    market_db = mongo.db.market
    products = market_db.find_one({"title": request.args.get('title')})

    return jsonify({
        'title': products.get('title'),
        'content': products.get('content')
    })

@app.route('/writepage')
def writepage():
    return render_template('/write.html')

@app.route('/write', methods=['POST'])
def write():
    market_db = mongo.db.market

    market_db.insert_one({
        'title': request.form.get('title'),
        'location': request.form.get('location'),
        'price': request.form.get('price'),
        'content': request.form.get('content')
    })
    return redirect('/')

@app.route('/')
def first_page():
    market_db = mongo.db.market
    products = market_db.find()

    return render_template('market_list.html', products=products)  #products=products가 정확히 어떤 동작은 하는건지?

if __name__ == '__main__':
    app.run()