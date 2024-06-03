import json
from flask import abort

import requests
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main_db'  # for connecting to the database
CORS(app)
#
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'image': self.image
        }


class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint("user_id", "product_id", name="uniq_product_unique")


@app.route('/api/products')
def index():
    # return "Hello World"
    # return jsonify(Product.query.all())
    products = Product.query.all()
    products_dict = [product.to_dict() for product in products]
    return jsonify(products_dict)


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    try:
        response = requests.get("http://docker.for.mac.localhost:8002/api/user")
        response.raise_for_status()  # Raise an HTTPError for bad responses
        request_data = response.json()  # Extract JSON data
        try:
            productUser = ProductUser(user_id=request_data['id'], product_id=id)
            db.session.add(productUser)
            db.session.commit()


            publish('Product liked', id)
        except:
            abort(400, 'You already liked this product')

        return jsonify({
            'message': 'success'
        })  # Return the JSON data
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8001)
