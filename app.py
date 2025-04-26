from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import numpy as np
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase Admin
cred = credentials.Certificate('firebase-credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app)

# Store the latest sensor data
sensor_data = {
    'accelerometer1': [],
    'accelerometer2': [],
    'accelerometer3': [],
    'accelerometer4': [],
    'timestamps': []
}

def fetch_latest_data():
    try:
        # Query the Firestore collection for the latest document
        docs = db.collection('sensor_data').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(100).stream()
        
        # Reset the sensor data
        sensor_data['accelerometer1'] = []
        sensor_data['accelerometer2'] = []
        sensor_data['accelerometer3'] = []
        sensor_data['accelerometer4'] = []
        sensor_data['timestamps'] = []
        
        # Process the documents in reverse order to maintain chronological order
        for doc in reversed(list(docs)):
            data = doc.to_dict()
            sensor_data['accelerometer1'].append(data.get('acc1', 0))
            sensor_data['accelerometer2'].append(data.get('acc2', 0))
            sensor_data['accelerometer3'].append(data.get('acc3', 0))
            sensor_data['accelerometer4'].append(data.get('acc4', 0))
            sensor_data['timestamps'].append(data.get('timestamp', ''))
            
    except Exception as e:
        print(f"Error fetching data from Firestore: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    fetch_latest_data()
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 