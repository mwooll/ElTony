"""
Recommender for the ideal pokemon team

return recommendation as well as Key feature for recommendation

"""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

def get_recommendations(filtered_dataset, opponent_type):
    if opponent_type != "None":
        types = opponent_type
        print("opponentType")
        if types:
            # Read in csv with type interactions
            df_type = pd.read_csv('typing_chart.csv')

            # Initialize an empty list to store recommended types
            recommended_types = []

            # Iterate through each selected type
            for selected_type in types:
                # Look at the column corresponding to the selected type
                interaction_column = df_type[selected_type]

                # Find types where the column has a value of 2
                recommended_types.extend(df_type.loc[interaction_column == 2, 'Types'].tolist())

            # Remove duplicates from the recommended types list
            recommended_types = list(set(recommended_types))

            # Filter the data for the returned types
            filtered_dataset = filtered_dataset[filtered_dataset['Type_1'].isin(recommended_types)]
    print(filtered_dataset)

    pokemon_data = filtered_dataset

    selected_cols = ['HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed', 'Type_1', 'Type_2', 'Name']
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

    recommended_team_json = recommended_team.to_json(orient='records', default_handler=str)
    print(recommended_team_json)
    return recommended_team_json