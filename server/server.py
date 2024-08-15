# from flask import Flask, request, jsonify, render_template
# import util

# app = Flask(__name__)

# # Serve the HTML page
# @app.route('/')
# def index():
#     return render_template('app.html')

# @app.route('/get_location_names', methods=['GET'])
# def get_location_names():
#     response = jsonify({
#         'locations': util.get_location_names()
#     })
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

# @app.route('/predict_home_price', methods=['GET', 'POST'])
# def predict_home_price():
#     total_sqft = float(request.form['total_sqft'])
#     location = request.form['location']
#     bhk = int(request.form['bhk'])
#     bath = int(request.form['bath'])

#     response = jsonify({
#         'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
#     })
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

# if __name__ == "__main__":
#     print("Starting Python Flask Server For Home Price Prediction...")
#     util.load_saved_artifacts()
#     app.run(debug=True)

import pickle
import json
import numpy as np
import os
from flask import Flask, request, jsonify, render_template

# Global variables for model and data
__locations = None
__data_columns = None
__model = None

# Utility function to get the estimated price
def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

# Function to load saved artifacts (model and columns)
def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global __data_columns
    global __locations

    # Print current working directory for debugging
    print("Current Working Directory:", os.getcwd())

    try:
        with open("server/artifacts/columns.json", "r") as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[3:]  # First 3 columns are sqft, bath, bhk
    except FileNotFoundError:
        print("File not found: ./artifacts/columns.json")
        raise

    global __model
    if __model is None:
        try:
            with open('server/artifacts/banglore_home_prices_model.pickle', 'rb') as f:
                __model = pickle.load(f)
        except FileNotFoundError:
            print("File not found: ./artifacts/banglore_home_prices_model.pickle")
            raise

    print("Loading saved artifacts...done")

# Utility function to get the location names
def get_location_names():
    return __locations

# Utility function to get the data columns
def get_data_columns():
    return __data_columns

# Flask application setup
app = Flask(__name__)

# Serve the HTML page
@app.route('/')
def index():
    return render_template('app.html')

# API endpoint to get location names
@app.route('/get_location_names', methods=['GET'])
def get_location_names_route():
    response = jsonify({
        'locations': get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# API endpoint to predict home price
@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': get_estimated_price(location, total_sqft, bhk, bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Main entry point
if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    load_saved_artifacts()
    app.run(debug=True)
