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
opponent_type = 'Normal'

filtered_pokemon_data, json_data = filter_data(pokemon_data, filter_params)


recommended_team_json,cluster_info_json, team_stats_json,others_in_cluster_json= get_recommendations(filtered_pokemon_data, opponent_type)
print("cluster_info_json ")
cluster_info_data = json.loads(cluster_info_json)

for pokemon_info in cluster_info_data:
    print(pokemon_info["Name"])

print("recTeam")
team_json = json.loads(recommended_team_json)
for pokemon_info in team_json:
    print(pokemon_info["Name"])

