import pandas as pd
from flask import Flask, request, jsonify
from filter import filter_data
from poke_rec import get_recommendations
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

@app.route('/api/recommend', methods=['POST'])
def recommend_endpoint():
    try:
        print("Recommend")

        # Get opponentTeamType from the filter params as opponent type
        opponentType = request.json['opponentType']
        print(opponentType)

        # Use filtered_pokemon_data if not empty, otherwise use the entire pokemon_data
        data_to_recommend = filtered_pokemon_data if not filtered_pokemon_data.empty else pokemon_data

        # Assuming you have a function get_recommendations in poke_rec.py
        global clusterinfo  # Use the global variable
        global teamStats
        global othersinCluster
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