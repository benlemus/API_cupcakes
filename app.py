"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request
from models import db, connect_db, Cupcake


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'shhhh'

connect_db(app)

@app.route('/api/cupcakes')
def all_cupcakes():
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:id>')
def cupcake_details(id):
    data = Cupcake.query.get_or_404(id)
    cupcake = data.serialize()
    
    return jsonify(cupcake=cupcake)

@app.route('/api/cupcakes', methods=['POST'])
def add_cupcake():
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()),201)


