#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakerie in Bakery.query.all():
        bakerie_dict = {
            "id": bakerie.id,
            "name": bakerie.name,
            "created_at":bakerie.created_at,
            "updated_at":bakerie.updated_at,
            }
        bakeries.append(bakerie_dict)

    response = make_response(
        bakeries, 
        200)
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakeries = Bakery.query.filter(Bakery.id == id).first()
    bakeries_dict = bakeries.to_dict()

    response = make_response(
        jsonify(bakeries_dict),
          200
          )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = []
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_dict = [good.to_dict() for good in baked_goods_by_price]

    response = make_response(
        jsonify(baked_goods_by_price_dict),
        200
        )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_baked_dict = most_expensive_baked_good.to_dict()
    
    response = make_response(
        jsonify(most_expensive_baked_dict), 
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=555, debug=True)
