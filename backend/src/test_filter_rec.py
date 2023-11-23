"""
Use this to test the recommendation system in the backend.

"""

import pandas as pd
from flask import Flask, request, jsonify
from filter import filter_data
from poke_rec import get_recommendations
pokemon_data = pd.read_csv('pokemon.csv') # Your Pokemon data
filter_params = {
    'opponent_type': ['Water']
}

# Extract opponent type from filter_params
opponent_type = filter_params.get('opponent_type', None)

# Apply filtering
filteredData,filter_json = filter_data(pokemon_data, filter_params)
# Get recommendations using the opponent type (or all types if not specified)
recommendations = get_recommendations(filteredData, opponent_type)
print(recommendations)