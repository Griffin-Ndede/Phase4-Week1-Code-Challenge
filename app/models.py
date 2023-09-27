from sqlalchemy.orm import validates
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define your models in singular form (Restaurant, Pizza, not Restaurants, Pizzas).
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(), nullable=False)
    
    # Define many-to-many relationship between Pizza and Restaurant through Restaurant_pizza.
    # restaurant = db.relationship('Restaurant', back_populates='restaurant_pizza')
    # pizza = db.relationship('Pizza', back_populates='restaurants_pizza')
    pizzas = db.relationship('Pizza', secondary='restaurant_pizza', back_populates='restaurants')

    # Validation for the name column.
    @validates("name")
    def validate_name(self, key, value):
        if len(value) > 50:
            raise ValueError("Name must be less than 50 characters")
        return value
    
class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    ingredients = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Define the many-to-many relationship between Restaurant and Pizza through Restaurant_pizza.
    # restaurants_pizza = db.relationship("RestaurantPizza", back_populates="pizza")
    restaurants = db.relationship('Restaurant', secondary='restaurant_pizza', back_populates='pizzas')

class RestaurantPizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Define relationships for the RestaurantPizza model.
    # restaurant = db.relationship('Restaurant', back_populates='pizzas')
    # pizza = db.relationship('Pizza', back_populates='restaurants')

    # Validation for the price column.
    @validates("price")
    def validate_price(self, key, value):
        if value < 1 or value > 30:
            raise ValueError("Price must be between 1 and 30")
        return value
    
