import pandas as pd
from fastapi import requests
from flask import Flask, request, jsonify
from filter import filter_data
from poke_rec import get_recommendations, swap_logic
import csv
from flask_cors import CORS
from flask_restx import Resource, Api
from model import Pokemon

app = Flask(__name__)
cors = CORS()
cors.init_app(app, resources={r"*": {"origins": "*"}})
api = Api(app)

pokemon_data = pd.read_csv('pokemon.csv')
clusterinfo = []  # Initialize clusterinfo to an empty list
teamStats = []
filtered_pokemon_data = pd.DataFrame()
swapped = False
@app.route('/api/filter', methods=['OPTIONS'])
def handle_options_request():
    response = jsonify({'status': 'OK'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/api/filter', methods=['POST'])
def filter_endpoint():
    try:
        global filtered_pokemon_data  # Use the global variable

        # Get filter parameters from the frontend
        params = request.json['params']
        print("Received filter parameters:", params)

        if params:
            # Filter the data
            filtered_pokemon_data, json_data = filter_data(pokemon_data, params)
            return json_data
        else:
            # If no filter applied, use the entire pokemon_data
            filtered_pokemon_data = pd.DataFrame()  # Set the dataframe to empty
            return jsonify({'message': 'No filter applied. Using all data.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/recomputeRecommendations', methods=['GET'])
def recompute_recommendations_endpoint():
    try:
        global swapped

        # Check if re-computation of recommendations is necessary
        if swapped:
            # Call the recommend_endpoint logic
            updated_recommendations = recommend_endpoint()
            swapped = False  # Reset the swapped flag

            return updated_recommendations

        # If no re-computation is needed, return a message or appropriate response
        return jsonify({'message': 'No re-computation needed'})

    except Exception as e:
        print("Error in recompute_recommendations_endpoint:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend', methods=['POST'])
def recommend_endpoint():
    try:
        # Get opponentTeamType from the filter params as opponent type
        opponentType = request.json['opponentType']
        print(opponentType)

        # Use filtered_pokemon_data if not empty, otherwise use the entire pokemon_data
        data_to_recommend = filtered_pokemon_data if not filtered_pokemon_data.empty else pokemon_data

        # Assuming you have a function get_recommendations in poke_rec.py
        global clusterinfo  # Use the global variable
        global teamStats
        global othersinCluster
        global recommendations
        global swapped

        if swapped == True:
            print("SWAPPED RECS ")
            recommendations = new_recommendations
            othersinCluster = new_othersinCluster
            teamStats = new_teamStat
            print("TEAM STATS")
            swapped = False
        else:
            recommendations, clusterinfo, teamStats, othersinCluster = get_recommendations(data_to_recommend, opponentType)

        return recommendations

    except Exception as e:
        return jsonify({'error': str(e)}), 500

class PokemonList(Resource):
    def get(self):
        global filtered_pokemon_data  # Use the global variable

        if not filtered_pokemon_data.empty:  # Check if the DataFrame is not empty
            # If filtered data is available, use it
            data = filtered_pokemon_data
        else:
            # If filtered data is empty, use the entire pokemon_data
            data = pokemon_data

        pokemons = [Pokemon(**{k: str(v) if pd.notna(v) and v != '' else None for k, v in item.items()}) for item in
                    data.to_dict(orient='records')]

        return [pokemon.to_json() for pokemon in pokemons]

class PokemonResource(Resource):
    def get(self, name):
        with open('pokemon.csv', newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)

        pokemons = [Pokemon(**item) for item in data]

        for pokemon in pokemons:
            if pokemon.Name == name:
                return pokemon.to_json()

        return {"error": "Pokémon not found"}, 404
@app.route('/api/swapPokemon', methods=['POST'])
def swap_pokemon_endpoint():
    global new_recommendations
    global new_othersinCluster
    global new_teamStat
    try:
        # Get data from the frontend
        data = request.json
        print("Received swap data:", data)

        # Ensure required data is present
        pokemon_to_swap_out = data.get('pokemonToSwapOut')
        selected_other_pokemon = data.get('selectedOtherPokemon')

        if not (pokemon_to_swap_out and selected_other_pokemon):
            raise ValueError("Missing required data for swap operation.")

        # Call swap_logic function
        updated_recommendations, updated_othersinCluster, updated_teamStat= swap_logic(
            pokemon_to_swap_out, selected_other_pokemon, recommendations, othersinCluster
        )

        # Update global variables
        new_recommendations = updated_recommendations
        new_othersinCluster = updated_othersinCluster
        new_teamStat = updated_teamStat
        print("Updated othersinCluster:", new_othersinCluster)

        global swapped
        swapped = True

        # Call recommend_endpoint
        return new_recommendations

    except Exception as e:
        print("Error in swap_pokemon_endpoint:", e)
        return jsonify({'error': str(e)}), 500
@app.route('/cluster-info', methods=['GET'])
def serve_cluster_info():
    # Return the global clusterinfo variable as JSON
    return clusterinfo

@app.route('/teamstats', methods=['GET'])
def serve_team_stats():
    # Return the global clusterinfo variable as JSON
    return teamStats

@app.route('/othersInCluster', methods=['GET'])
def serve_otherCluster():
    # Return the global clusterinfo variable as JSON
    return othersinCluster

api.add_resource(PokemonList, '/pokemons')
api.add_resource(PokemonResource, '/pokemons/<string:name>')

if __name__ == '__main__':
    app.run(debug=True)