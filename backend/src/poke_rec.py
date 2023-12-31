import os
import json

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA

def get_recommendations(filtered_dataset, opponent_type):
    cluster_info_path = 'cluster_info.csv'

    # Check if the file exists, and if so, remove it
    if os.path.exists(cluster_info_path):
        os.remove(cluster_info_path)

    if opponent_type != "No specific opponent":
        df_type = pd.read_csv('typing_chart.csv')

        recommended_types = df_type.loc[df_type[opponent_type] == 2, 'Types'].tolist()

        # Filter the data for the returned types
        rec_dataset = filtered_dataset[
            filtered_dataset['Type_1'].isin(recommended_types) | filtered_dataset['Type_2'].isin(recommended_types)]

        if len(rec_dataset) > 6:
            # Use the original dataset
            filtered_dataset = rec_dataset

    pokemon_data = filtered_dataset
    if len(pokemon_data) < 6:
        pokemon_data = pd.read_csv('pokemon.csv')
    selected_cols = ['HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed', 'Type_1', 'Type_2', 'Name', 'image']
    pokemon_data = pokemon_data[selected_cols]

    # Drop rows with missing types
    pokemon_data = pokemon_data.dropna(subset=['Type_1'])

    pokemon_data['Types'] = pokemon_data[['Type_1', 'Type_2']].astype(str).agg(','.join, axis=1)

    # selected features
    features = ['HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed', 'Types']

    # Define transformers for numerical and categorical features
    numeric_features = ['HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed']
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    categorical_features = ['Types']
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder())
    ])

    # Use ColumnTransformer to apply different transformers to numerical and categorical features
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # K-Means clustering
    n_clusters = 10
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)

    # Create a pipeline with preprocessing and clustering steps
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('kmeans', kmeans)])

    # Fit and predict clusters
    pokemon_data['Cluster'] = pipeline.fit_predict(pokemon_data[features])

    # Sort Pokémon within each cluster by total stats
    pokemon_data = pokemon_data.sort_values(by=['Cluster'] + numeric_features, ascending=[True] + [False] * len(numeric_features))

    team_size = 6
    recommended_team = []

    # Keep track of counts for offensive and defensive Pokemon
    offensive_count = 0
    defensive_count = 0

    # Iterate through clusters and select Pokémon with diverse types
    while len(recommended_team) < team_size:
        selected_types = set()

        # Iterate through clusters and select Pokémon with diverse types
        for cluster in pokemon_data['Cluster'].unique():
            cluster_data = pokemon_data[pokemon_data['Cluster'] == cluster]

            # Select the Pokémon with the highest stats and a new type
            for _, pokemon in cluster_data.iterrows():
                if len(recommended_team) < team_size and \
                        pokemon['Type_1'] not in selected_types and \
                        pokemon['Type_2'] not in selected_types:
                    # Add a column indicating the key feature
                    key_feature = numeric_features[pokemon[numeric_features].argmax()]
                    pokemon['Key_Feature'] = key_feature

                    # Check if the Pokemon is offensive or defensive
                    if key_feature in ['Attack', 'Sp_Atk', 'Speed'] and offensive_count < team_size / 2:
                        recommended_team.append(pd.DataFrame([pokemon]))
                        offensive_count += 1
                    elif key_feature in ['Defense', 'Sp_Def', 'HP'] and defensive_count < team_size / 2:
                        recommended_team.append(pd.DataFrame([pokemon]))
                        defensive_count += 1

                    selected_types.add(pokemon['Type_1'])
                    if pd.notna(pokemon['Type_2']):
                        selected_types.add(pokemon['Type_2'])

                    # Drop the selected Pokemon from pokemon_data
                    pokemon_data = pokemon_data[pokemon_data.index != pokemon.name]


    # Concatenate the DataFrames in the recommended_team list
    recommended_team = pd.concat(recommended_team, ignore_index=True)

    recommended_team['Type_2'].fillna('None', inplace=True)

    recommended_team_json = recommended_team.to_json(orient='records', default_handler=str)

    cluster_info = pokemon_data[['Name', 'Cluster', 'HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed']]
    cluster_info = pd.concat([cluster_info, recommended_team], ignore_index=True)

    cluster_info['Cluster'] = pipeline.fit_predict(cluster_info[features])

    # Sort Pokémon within each cluster by total stats
    cluster_info = cluster_info.sort_values(by=['Cluster'] + numeric_features,
                                            ascending=[True] + [False] * len(numeric_features))

    # Perform PCA for visualization
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(cluster_info[numeric_features])

    # Add PCA components to the DataFrame
    cluster_info['PCA1'] = pca_result[:, 0]
    cluster_info['PCA2'] = pca_result[:, 1]

    # Save the cluster information to a CSV file

    # Add recommended team to the cluster information

    # Convert the cluster information to JSON format
    cluster_info_json = cluster_info.to_json(orient='records', default_handler=str, indent=2)
    num_pokemon = len(recommended_team_json)
    average_stats = {}
    recommended_team_names = []

    for _, pokemon in recommended_team.iterrows():
        for stat, value in pokemon.items():
            # Exclude Type_1 and Type_2 from averaging
            for stat in numeric_features:
                # Exclude Type_1 and Type_2 from averaging
                    average_stats[stat] = recommended_team[stat].mean()

    print("original rec stats")
    print(average_stats)
    othersInCluster = []
    for _, pokemon in recommended_team.iterrows():
        cluster_id = int(pokemon['Cluster'])

        # Get other Pokémon names in the same cluster
        other_pokemon_in_cluster = pokemon_data.loc[pokemon_data['Cluster'] == cluster_id, 'Name'].tolist()

        # Check if the recommended Pokémon's name is in the list before removing it
        if pokemon['Name'] in other_pokemon_in_cluster:
            other_pokemon_in_cluster.remove(pokemon['Name'])

        othersInCluster.append({
            'Recommended_Pokemon': pokemon['Name'],
            'Other_Pokemon_In_Cluster': other_pokemon_in_cluster
        })

    others_in_cluster_json = json.dumps(othersInCluster, indent=2)

    # Construct the team_stats_json manually
    team_stats_json = "{\n"
    for stat, value in average_stats.items():
        team_stats_json += f'  "{stat}": {value},\n'
    team_stats_json = team_stats_json.rstrip(',\n')  # Remove the trailing comma and newline
    team_stats_json += "\n}"

    print(recommended_team_json)
    print(team_stats_json)

    return recommended_team_json, cluster_info_json, team_stats_json,others_in_cluster_json


def swap_logic(pokemon_to_swap_out, selected_other_pokemon, recommendations, othersinCluster):
    pokemon_data = pd.read_csv('pokemon.csv')
    recommendations = json.loads(recommendations)
    othersinCluster = json.loads(othersinCluster)
    print("inside Swap logic")
    selected_columns = ['HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed', 'Type_1', 'Type_2', 'image']

    # Iterate through recommendations
    for rec in recommendations:
        if rec['Name'] == pokemon_to_swap_out:
            # Swap the Pokemon in recommendations
            rec['Name'] = selected_other_pokemon
            # Retrieve the stats of the selected other Pokemon from the CSV
            selected_other_pokemon_stats = \
            pokemon_data.loc[pokemon_data['Name'] == selected_other_pokemon, selected_columns].to_dict(
                orient='records')[0]

            rec.update(selected_other_pokemon_stats)
    # Iterate through othersinCluster
    for cluster in othersinCluster:
        if cluster['Recommended_Pokemon'] == pokemon_to_swap_out:
            cluster['Recommended_Pokemon'] = selected_other_pokemon

            for i, pokemon in enumerate(cluster['Other_Pokemon_In_Cluster']):
                if pokemon == selected_other_pokemon:
                    cluster['Other_Pokemon_In_Cluster'][i] = pokemon_to_swap_out
    average_stats = {}
    num_pokemon = len(recommendations)
    print("Recommendations")
    print(recommendations)
    for pokemon in recommendations:
        for stat, value in pokemon.items():
            # Exclude Type_1 and Type_2 from averaging
            if stat not in ["Type_1", "Type_2", "Name", "Types", "Cluster", "Key_Feature", "image"]:
                average_stats[stat] = average_stats.get(stat, 0) + int(value) / num_pokemon



    print(average_stats)
    recommendations = json.dumps(recommendations)
    othersinCluster = json.dumps(othersinCluster)

    return recommendations, othersinCluster,average_stats