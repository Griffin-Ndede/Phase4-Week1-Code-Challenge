# Restaurant and Pizza API

This is a Flask-Based API for managing restaurants and their associated pizzas. This API can be used to perfom CRUD operations on restaurants and pizzas as well as pizzas to restaurants with prices.

## Prerequisites

Before running the application, make sure you have the following installed

Python 3.x 

Flask

SQLAlchemy installed using the command below

pip install Flask SQLAlchemy

## Getting started

* Clone this repository to your local machine

* Navigate to the project directory

* Create a virtual environment

* Activate your virtual environment

* Install require packages

* Initialize the SQLite database using the commands below

*       flask db init

*       flask db migrate

*       flask db upgrade

* Start the application

The API should now be running locally at http://localhost:5000.

# API Endpoints
## GET /
Description: Home page of the API

Response: "This is my API home page"

## POST /restaurants
Description: Create a new restaurant
Request body:
* name (string, required): The name of the restaurant
* address (string, required): The address of the restaurant

Response: "Restaurant added successfully!"
## GET /restaurants
Description: Retrieve a list of all restaurants

Response: JSON array of restaurant objects
## GET /restaurants/<int:id>
Description: Retrieve a restaurant by ID

Response: JSON object with restaurant details, including associated pizzas
## DELETE /restaurants/<int:id>
Description: Delete a restaurant by ID

Response: "Restaurant was successfully deleted"
## POST /pizzas
Description: Create a new pizza
Request body:
* name (string, required): The name of the pizza
* ingredients (string, required): The ingredients of the pizza

Response: "Pizza details added successfully"
## POST /restaurant_pizzas
Description: Add a pizza to a restaurant with a price
Request body:
* price (integer, required): The price of the pizza at the restaurant
* pizza_id (integer, required): The ID of the pizza to add
* restaurant_id (integer, required): The ID of the restaurant to which the pizza is added

Response: JSON object with pizza details

# License
This project is licensed under the MIT License