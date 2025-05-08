"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake
from forms import CupcakeForm
import requests


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'shhhh'

connect_db(app)

@app.route('/api/cupcakes')
def get_cupcakes():
    cupcakes = Cupcake.get_all_cupcakes()
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:id>')
def cupcake_details(id):
    cupcake = Cupcake.query.get_or_404(id)
    
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def add_cupcake():
    new_cupcake = Cupcake(**request.json)

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()),201)

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.delete()    
    return jsonify(message='deleted')

@app.route('/api/cupcakes/search/<input>')
def search_cupcakes(input):
    cupcakes = Cupcake.query.filter(Cupcake.flavor.ilike(f'%{input}%')).order_by(Cupcake.flavor).all()

    return jsonify([cupcake.serialize() for cupcake in cupcakes])


# front-end

@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/cupcakes/add')
def add_cupcake_page():
    form = CupcakeForm()
    return render_template('add_cupcake.html', form=form)

@app.route('/cupcakes/<int:id>/update')
def update_cupcake_page(id):
    res = requests.get(f'http://localhost:5000/api/cupcakes/{id}')

    data = res.json()

    cupcake = data.get('cupcake')

    form = CupcakeForm(data=cupcake)
    return render_template('update_cupcake.html', form=form, cupcake=cupcake)
