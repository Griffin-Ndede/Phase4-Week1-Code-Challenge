from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(), nullable=False)
    
    @validates("name")
    def validate_name(self,key,value):
        if len(value) > 50:
            raise ValueError("Name must be less than 50 characters")
        return value
    
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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

