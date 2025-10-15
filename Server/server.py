from flask import Flask, request, jsonify
import util
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return "Welcome! Root path is working."

@app.route('/get_location_names') #if someone vists http://127.0.0.1:5000/get_location_names then below function will execute
def get_location_names():
    response = jsonify({ #we are jsonifying the location because fronend or client usually expects Json file as response to parse it hastle free
        'locations': util.get_location_names() #from util module we are importing get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin','*') #this will ensure that CORS effect does not happens. Similar we used experience while development This line of code ensures that Front apps like React, Angular or anyyone has access to this API
    return response

@app.route('/predict_home_price',methods=['POST'])
def predict_home_price():
    total_sqft = request.form['total_sqft'] #since we will use forms in frontend so whatever request coming from frontend we will extract the following details from request.form
    bath = request.form['bath']
    balcony = request.form['balcony']
    bhk = request.form['bhk']
    location = request.form['location']

    response = jsonify({
        'estimated_price': util.get_estimated_price(total_sqft,bath,balcony,bhk,location)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
if __name__ == "__main__":
    print("Starting Python flask server for house price prediction")
    app.run() #this will run my app on http://127.0.0.1:5000