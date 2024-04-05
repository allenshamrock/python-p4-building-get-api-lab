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
    bakeries_data = {}

    for bakery in Bakery.query.all():
        bakery_dict = {
            "created_at": bakery.created_at,
            "id": bakery.id,
            "name": bakery.name,
            "updated_at": bakery.updated_at,
            "baked_goods": []  # List to hold baked goods
        }
        # Use bakery ID as key
        bakeries_data[bakery.id] = bakery_dict  

    for baked_good in BakedGood.query.all():
        baked_good_dict = {
            "bakery_id": baked_good.bakery_id,
            "created_at": baked_good.created_at,
            "id": baked_good.id,
            "name": baked_good.name,
            "price": baked_good.price,
            "updated_at": baked_good.updated_at
        }
        # Append baked good to respective bakery
        bakeries_data[baked_good.bakery_id]["baked_goods"].append(baked_good_dict)  

    # Convert dictionary values to list
    bakeries_list = list(bakeries_data.values())

    response = make_response(
        jsonify(bakeries_list),
        200
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakeries_data = {}
    
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
            bakery_dict = {
                "created_at": bakery.created_at,
                "id": bakery.id,
                "name": bakery.name,
                "updated_at": bakery.updated_at,
                "baked_goods": []
            }
            bakeries_data[bakery.id] = bakery_dict
    
            baked_goods = BakedGood.query.filter_by(bakery_id=id).all()
            for baked_good in baked_goods:
                baked_good_dict = {
                    "bakery_id": baked_good.bakery_id,
                    "created_at": baked_good.created_at,
                    "id": baked_good.id,
                    "name": baked_good.name,
                    "price": baked_good.price,
                    "updated_at": baked_good.updated_at
                }
                bakery_dict["baked_goods"].append(baked_good_dict)

    response = make_response(
        jsonify(bakeries_data),
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    res_data = []

    for baked_good in baked_goods:
        baked_good_data = {
            "id": baked_good.id,
            "name": baked_good.name,
            "price": baked_good.price,
            "created_at": baked_good.created_at,
            "updated_at": baked_good.updated_at,
            "bakery_id": baked_good.bakery_id
        }
        bakery = Bakery.query.get(baked_good.bakery_id)
        if bakery:
            bakery_data = {
                "id": bakery.id,
                "name": bakery.name,
                "created_at": bakery.created_at,
                "updated_at": bakery.updated_at
            }
            baked_good_data["bakery"] = bakery_data
            res_data.append(baked_good_data)
    response = make_response(
        jsonify(res_data),
        200
    )
    return response


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good_data = {}

    expensive_baked_good = BakedGood.query.order_by(
        BakedGood.price.desc()).first()
    if expensive_baked_good:
        baked_good_data = {
            "id": expensive_baked_good.id,
            "name": expensive_baked_good.name,
            "price": expensive_baked_good.price,
            "created_at": expensive_baked_good.created_at,
            "updated_at": expensive_baked_good.updated_at,
            "bakery_id": expensive_baked_good.bakery_id
        }

        bakery = Bakery.query.get(expensive_baked_good.bakery_id)
        if bakery:
            bakery_data = {
                "id": bakery.id,
                "name": bakery.name,
                "created_at": bakery.created_at,
                "updated_at": bakery.updated_at
            }
            baked_good_data["bakery"] = bakery_data

    # Return JSON response
    response = make_response(
        jsonify(baked_good_data),
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
