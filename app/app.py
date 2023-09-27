

from flask import Flask, request, jsonify
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:/// restaurant.db"

db.init_app(app)

from models import Restaurant, Pizza, RestaurantPizza

with app.app_context():
    db.create_all()

@app.route('/')
def Home():
    return "This is my API home page"


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
    

@app.route("/restaurants/<int:id>", methods=['GET', 'DELETE'])
def restaurant_by_id(id):
    # Retrieve a restaurant by ID
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return "Restaurant not found", 404
    # retrieving the pizzas associated with the restaurant
    pizzas = restaurant.pizzas

    # creating a JSON reponse
    if request.method =='GET':
        restaurant_json = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "pizzas":[
                {
                    "id": pizza.id,
                    "name": pizza.name,
                    "ingredients": pizza.ingredients,
                }
                for pizza in pizzas
            ]
        }
        return jsonify(restaurant_json)
    elif request.method == "DELETE":
        db.session.delete(restaurant)
        db.session.commit()  
        return "Restaurant was successfully deleted"
    else:
        return "Invalid request method"

@app.route("/pizzas", methods=["POST", "GET"])
def pizzas():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']

        # Saving new pizza to the database
        new_pizza = Pizza(name=name, ingredients=ingredients)
        db.session.add(new_pizza)
        db.session.commit()
        return "Pizza details added successfully"
    elif request.method == "GET":
        # Retrieving a list of pizzas that have been added to the database
        pizza_list = Pizza.query.all()
        pizza_json = [
            {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients,
            }
            for pizza in pizza_list
        ]
        return jsonify(pizza_json)
    else:
        return "Invalid request method"
    
@app.route("/restaurant_pizzas", methods=["POST"])
def restaurantpizzas():
    # Parse form data
    price = request.form.get("price")
    pizza_id = request.form.get("pizza_id")
    restaurant_id = request.form.get("restaurant_id")

    if not all([price, pizza_id, restaurant_id]):
        return jsonify({"errors": ["Missing required fields"]}), 400

    price = int(price)
    pizza_id = int(pizza_id)
    restaurant_id = int(restaurant_id)

    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza:
        return jsonify({"errors": ["Pizza not found"]}), 404

    if not restaurant:
        return jsonify({"errors": ["Restaurant not found"]}), 404

    restaurant_pizza = RestaurantPizza(
        price=price, pizza_id=pizza_id, restaurant_id=restaurant_id
    )

    db.session.add(restaurant_pizza)
    db.session.commit()

    pizza_data = {
        "id": pizza.id,
        "name": pizza.name,
        "ingredients": pizza.ingredients,
    }

    return jsonify(pizza_data), 201


if __name__ == "__main__":
    app.run()