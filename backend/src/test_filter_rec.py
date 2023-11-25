"""
Use this to test the recommendation system in the backend.

"""
import json
import pandas as pd
from flask import Flask, request, jsonify
from filter import filter_data
from poke_rec import get_recommendations
pokemon_data = pd.read_csv('pokemon.csv') # Your Pokemon data
filter_params = {
    'opponent_type': ['Water']
}

team_json = [{"HP":60,"Attack":60,"Defense":50,"Sp_Atk":40,"Sp_Def":50,"Speed":75,"Type_1":"Normal","Type_2":"Grass","Name":"Deerling","Types":"Normal,Grass","Cluster":0,"Key_Feature":"Speed"},{"HP":50,"Attack":47,"Defense":50,"Sp_Atk":57,"Sp_Def":50,"Speed":65,"Type_1":"Bug","Type_2":"Electric","Name":"Joltik","Types":"Bug,Electric","Cluster":0,"Key_Feature":"Speed"},{"HP":60,"Attack":40,"Defense":80,"Sp_Atk":60,"Sp_Def":45,"Speed":40,"Type_1":"Grass","Type_2":"Psychic","Name":"Exeggcute","Types":"Grass,Psychic","Cluster":0,"Key_Feature":"Defense"},{"HP":125,"Attack":58,"Defense":58,"Sp_Atk":76,"Sp_Def":76,"Speed":67,"Type_1":"Water","Type_2":"Electric","Name":"Lanturn","Types":"Water,Electric","Cluster":1,"Key_Feature":"HP"},{"HP":60,"Attack":40,"Defense":60,"Sp_Atk":40,"Sp_Def":60,"Speed":35,"Type_1":"Grass","Type_2":"None","Name":"Shroomish","Types":"Grass,nan","Cluster":0,"Key_Feature":"HP"},{"HP":90,"Attack":75,"Defense":85,"Sp_Atk":115,"Sp_Def":90,"Speed":55,"Type_1":"Electric","Type_2":"None","Name":"Ampharos","Types":"Electric,nan","Cluster":1,"Key_Feature":"Sp_Atk"}]
def calc_avg_teamstats(recommended_team_json):
    num_pokemon = len(recommended_team_json)
    average_stats = {}

    # Iterate through each stat and calculate the average
    for pokemon in recommended_team_json:
        for stat, value in pokemon.items():
            # Exclude Type_1 and Type_2 from averaging
            if stat not in ["Type_1", "Type_2", "Name", "Types", "Cluster", "Key_Feature"]:
                average_stats[stat] = average_stats.get(stat, 0) + value / num_pokemon

    # Convert the average stats to JSON
    average_stats_json = json.dumps(average_stats, indent=2)

    return average_stats_json

avgst = calc_avg_teamstats(team_json)
print(avgst)