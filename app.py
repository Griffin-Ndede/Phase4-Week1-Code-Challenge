from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates, relationship
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(), nullable=False)
    
    # defining many to many relationship btn pizza through restaurantpizza
    pizzas = relationship('Pizzas', secondary="restaurant_pizza", back_populates= "pizzas")
    
    # validation for the name column
    @validates("name")
    def validate_name(self,key,value):
        if len(value) > 50:
            raise ValueError("Name must be less than 50 characters")
        return value

class Pizzas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    ingredients = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# defining the many to many relationship btn Restaurant through Restaurantpizza
    restaurants = relationship("Restaurant", secondary="restaurant_pizza", back_populates= "pizzas")
@app.route("/")
def Home():
    return "This is my restaurant API"

@app.route("/restaurants", methods=["POST", "GET"])
def restaurants():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        # Saving restaurant details to the database
        new_restaurant = Restaurant(name=name, address=address)
        db.session.add(new_restaurant)
        db.session.commit()
        return "Restaurant added successfully!"
    
    elif request.method == "GET":
        # Retrieving a list of restaurants that have been added
        restaurant_list = Restaurant.query.all()
        restaurant_json = [
            {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
            }
            for restaurant in restaurant_list
        ]
        return jsonify(restaurant_json)
    else:
        return "Invalid request method"
    
@app.route("/restaurants/<int:id>", methods=['GET'])
def restaurant_by_id(id):
    # Retrieve a restaurant by ID
    restaurant = Restaurant.query.get(id)
    if restaurant:
        restaurant_json = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
        }
        return jsonify(restaurant_json)
    else:
        return "Restaurant not found", 404
    
# @app.route("/pizzas", methods =["POST", "GET"])
# def pizzas():
#     if request.method == 'POST':
#         name = request.form['name']
#         ingredients = request.form['ingredients']

#         # saving new pizza to the database
#         new_pizza = Pizzas(name=name, ingredients=ingredients)
#         db.session.add(new_pizza)
#         db.session.commit()
#         return "Pizza details added successfully"
#     # retrieving a list of pizza that has been added to the database
#     elif request.method == "GET":
#         pizza_list = Pizzas.query.all()
#         pizza_json = [
#             {
#                 "id": pizzas.id,
#                 "name": pizzas.name,
#                 "ingredients": pizzas.ingredients,

#             }
#             for pizzas in pizza_list
#         ]
#         return jsonify(pizza_json)
#     else:
#         return "Invalid request method"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

