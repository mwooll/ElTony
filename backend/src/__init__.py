import csv
import json
from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
from .model import Pokemon
from flask import request

# Configure Flask:
app = Flask(__name__)
# allow access from any frontend
cors = CORS()
cors.init_app(app, resources={r"*": {"origins": "*"}})
api = Api(app)

class PokemonList(Resource):
    def get(self):
        # Load Pokémon data from a local CSV file:
        with open('/Users/Matija_1/IVDA/Pokemon/services/data/pokemon.csv', newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)

        # Convert data to Pokemon objects:
        pokemons = [Pokemon(**{k: v if v != '' else None for k, v in item.items()}) for item in data]

        return [pokemon.to_json() for pokemon in pokemons]

class PokemonResource(Resource):
    def get(self, name):
        # Load Pokémon data from a local CSV file:
        with open('your_file.csv', newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)

        # Convert data to Pokemon objects:
        pokemons = [Pokemon(**item) for item in data]

        # Find the Pokémon with the given name:
        for pokemon in pokemons:
            if pokemon.Name == name:
                return pokemon.to_json()

        # If no Pokémon with the given name was found, return an error:
        return {"error": "Pokémon not found"}, 404

api.add_resource(PokemonList, '/pokemons')
api.add_resource(PokemonResource, '/pokemons/<string:name>')

