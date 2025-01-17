from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


#init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# init masrshmallow
ma = Marshmallow(app)


# Product Class model
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True)
	description = db.Column(db.String(200))
	price = db.Column(db.Float)
	qty = db.Column(db.Integer)


	# constructor
	def __init__(self, name, description, price, qty):
		self.name = name
		self.description = description
		self.price = price
		self.qty = qty


# product schema
class ProductSchema(ma.Schema):
	class Meta:
		fields = ('id', 'name', 'description', 'price', 'qty')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# create a product
@app.route('/product', methods=['POST'])
def add_product():
	name = request.json['name']
	description = request.json['description']
	price = request.json['price']
	qty = request.json['qty']


	new_product = Product(name, description, price, qty)
	db.session.add(new_product)
	db.session.commit()

	return product_schema.jsonify(new_product)



# get all prdoucts
@app.route('/product', methods=['GET'])
def get_products():
	all_products = Product.query.all()
	result = products_schema.dump(all_products)
	return jsonify(result)



# single product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
	product = Product.query.get(int(id))
	return product_schema.jsonify(product)



# create a product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
	product = Product.query.get(id)

	name = request.json['name']
	description = request.json['description']
	price = request.json['price']
	qty = request.json['qty']

	product.name = name
	product.description = description
	product.price = price
	product.qty = qty

	db.session.commit()

	return product_schema.jsonify(product)

@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
	product = Product.query.get(id)
	db.session.delete(product)
	db.session.commit()

	return product_schema.jsonify(product)


# runserver
if __name__ == '__main__':
	app.run(debug=True)