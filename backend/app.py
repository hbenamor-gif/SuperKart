
# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize Flask app with a name
superkart_api = Flask("SuperKart")

# Load the trained model
model = joblib.load("SuperKart.joblib")

# Define a route for the home page
@superkart_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Forecast System"

# Define an endpoint to predict sales for a single product
@superkart_api.post('/v1/predict')
def predict_sales():

    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing Product details and returns
    the predicted Sales  as a JSON response.
    """
    # Get JSON data from the request
    data = request.get_json()
    
    # Extract relevant features from the input data
    sample = {
    'Product_Weight': data['Product_Weight'],
    'Product_Sugar_Content': data['Product_Sugar_Content'],
    'Product_Allocated_Area': data['Product_Allocated_Area'],
    'Product_MRP': data['Product_MRP'],
    'Store_Size': data['Store_Size'],
    'Store_Location_City_Type': data['Store_Location_City_Type'],
    'Store_Type': data['Store_Type'],
    'Product_Id_char': data['Product_Id_char'],
    'Store_Age_Years': data['Store_Age_Years'],
    'Product_Type_Category': data['Product_Type_Category']
}

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])
    
    # Make a prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]
    
    # Return the prediction as a JSON response
    return jsonify({'Sales': prediction})

# Define an endpoint to predict sales for a batch of products
@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It expects a CSV file containing Product details and returns
    the predicted Sales for all rows as a JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']
    
    # Read the file into a DataFrame
    input_data = pd.read_csv(file)
    
    # Make predictions for the batch data
    predictions = model.predict(input_data).tolist()
    
    # Append predictions to the dataframe
    output_data = input_data.copy()
    output_data['Predicted_Sales'] = np.round(predictions, 2)
    
    # Return the data as JSON to be displayed and downloaded by the frontend
    return output_data.to_json(orient="records")

# Run the Flask app in debug mode
if __name__ == '__main__':
    superkart_api.run(debug=True)
