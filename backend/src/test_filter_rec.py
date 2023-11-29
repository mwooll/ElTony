"""
Use this to test the recommendation system in the backend.

"""
import json
import pandas as pd
from flask import Flask, request, jsonify
from filter import filter_data
from poke_rec import get_recommendations

pokemon_data = pd.read_csv('pokemon.csv')  # Your Pokemon data
filter_params = {}  # Add your filter parameters if needed
opponent_type = 'Grass'

filtered_pokemon_data, json_data = filter_data(pokemon_data, filter_params)

preselected_pokemons = ['Bulbasaur','Beedrill']

recommended_team_json, cluster_info_json, team_stats_json = get_recommendations(filtered_pokemon_data, opponent_type,preselected_pokemons)
print("Recommended Team ")
print(recommended_team_json)


