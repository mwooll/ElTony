"""
Use this to test the recommendation system in the backend.

"""

import pandas as pd
from flask import Flask, request, jsonify
from filter import filter_data
from poke_rec import get_recommendations

pokemon_data = pd.read_csv('pokemon.csv') # Your Pokemon data
filter_params = {
            'type': ['Rock'],
            'color': ['Red', 'Blue']
}

filteredData = filter_data(pokemon_data,filter_params)
recommendations = get_recommendations(filteredData)

print(recommendations[['Name', 'Total', 'Type_1', 'Type_2', 'Key_Feature']])
