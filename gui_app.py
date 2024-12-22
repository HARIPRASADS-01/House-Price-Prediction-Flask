from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the saved model
best_model = joblib.load('house_price_predictor_model.pkl')

# Define the function to predict the price based on input data
def predict_price(location, condition, garage, area, bedrooms, bathrooms, floors, year_built):
    location_values = ['Downtown', 'Suburban', 'Urban', 'Rural']
    condition_values = ['Excellent', 'Good', 'Fair', 'Poor']
    garage_values = ['No', 'Yes']

    # Convert the input categorical values into indices
    location_idx = location_values.index(location)
    condition_idx = condition_values.index(condition)
    garage_idx = garage_values.index(garage)

    # Prepare the input data in the correct feature order for the model
    input_data = pd.DataFrame({
        'Area': [area],
        'Bedrooms': [bedrooms],
        'Bathrooms': [bathrooms],
        'Floors': [floors],
        'YearBuilt': [year_built],
        'Location': [location_idx],
        'Condition': [condition_idx],
        'Garage': [garage_idx]
    })

    # Predict the price using the model
    predicted_price = best_model.predict(input_data)[0]
    return predicted_price

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get input data from the form
        location = request.form['location']
        condition = request.form['condition']
        garage = request.form['garage']
        area = int(request.form['area'])
        bedrooms = int(request.form['bedrooms'])
        bathrooms = int(request.form['bathrooms'])
        floors = int(request.form['floors'])
        year_built = int(request.form['year_built'])

        # Predict the price using the provided inputs
        predicted_price = predict_price(location, condition, garage, area, bedrooms, bathrooms, floors, year_built)
        
        # Return the prediction as JSON
        return jsonify({
            'status': 'success',
            'predicted_price': f"${predicted_price:,.2f}"
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)