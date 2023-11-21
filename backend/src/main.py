"""
Handle in and output to frontend
"""
import pandas as pd
from flask import Flask, request, jsonify
from filter import filter_data
from poke_rec import get_recommendations
import csv
import json
from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
from backend.src.model import Pokemon
from flask import request

app = Flask(__name__)

cors = CORS()
cors.init_app(app, resources={r"*": {"origins": "*"}})
api = Api(app)


pokemon_data = pd.read_csv('pokemon.csv')
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
        # Get filter parameters from the frontend
        params = request.json['params']
        print("Received filter parameters:", params)

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
        filtered_data = filter_data(pokemon_data,params)
        json_filtered_df = jsonify({'filtered_data': filtered_data.to_json(orient='records')})
        json_data = json.dumps(filtered_data, indent=2)
        print(json_data)
        return json_data

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

class PokemonList(Resource):
    def get(self):
        
        with open('pokemon.csv', newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)

        pokemons = [Pokemon(**{k: v if v != '' else None for k, v in item.items()}) for item in data]

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

api.add_resource(PokemonList, '/pokemons')
api.add_resource(PokemonResource, '/pokemons/<string:name>')



if __name__ == '__main__':
    app.run(debug=True)