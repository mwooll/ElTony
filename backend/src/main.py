"""
Handle in and output to frontend
"""
import pandas as pd
from flask import Flask, request, jsonify
from filter import filter_data
from poke_rec import get_recommendations


app = Flask(__name__)

# Mock data (replace this with your actual data)
pokemon_data = pd.read_csv('pokemon.csv') # Your Pokemon data

@app.route('/api/filter', methods=['POST'])
def filter_endpoint():
    try:
        # Get filter parameters from the frontend
        params = request.json['params']

        # Filter data based on received parameters
        """
        params for Filter data should look like this
        filter_params = {
            'type': ['Fire', 'Water'],
            'legendary': True,
            'generation': 3,
            'color': ['Red', 'Blue']
        }
        """
        filtered_data = filter_data(params)

        return jsonify({'filtered_data': filtered_data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend_endpoint():
    try:
        # Get optimization parameters from the frontend
        optims = request.json['optims']

        # Get recommendations based on received parameters
        recommendations = get_recommendations(optims)

        return jsonify({'recommendations': recommendations})

    except Exception as e:
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)