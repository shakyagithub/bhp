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

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from . import util

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

# Serve the HTML page
@app.route('/')
def index():
    return render_template('app.html')

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        locations = util.get_location_names()
        response = jsonify({'locations': locations})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])
        
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({'estimated_price': estimated_price})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except (KeyError, ValueError) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)
