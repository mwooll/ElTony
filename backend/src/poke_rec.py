"""
Recommender for the ideal pokemon team

return recommendation as well as Key feature for recommendation

"""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

def get_recommendations(filtered_dataset):
    pokemon_data = filtered_dataset

    selected_cols = ['Total', 'HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed', 'Type_1', 'Type_2', 'Name']
    pokemon_data = pokemon_data[selected_cols]

    # Drop rows with missing types
    pokemon_data = pokemon_data.dropna(subset=['Type_1'])

    pokemon_data['Types'] = pokemon_data[['Type_1', 'Type_2']].astype(str).agg(','.join, axis=1)

    # selected features
    features = ['Total', 'HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed', 'Types']

    # Define transformers for numerical and categorical features
    numeric_features = ['Total', 'HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed']
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
    pokemon_data = pokemon_data.sort_values(by=['Cluster', 'Total'], ascending=[True, False])

    team_size = 6
    recommended_team = []

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
                    key_feature = features[pokemon[numeric_features].argmax()]
                    pokemon['Key_Feature'] = key_feature

                    recommended_team.append(pd.DataFrame([pokemon]))
                    selected_types.add(pokemon['Type_1'])
                    if pd.notna(pokemon['Type_2']):
                        selected_types.add(pokemon['Type_2'])

                    # Drop the selected Pokemon from pokemon_data
                    pokemon_data = pokemon_data[pokemon_data.index != pokemon.name]

    # Concatenate the DataFrames in the recommended_team list
    recommended_team = pd.concat(recommended_team, ignore_index=True)

    return recommended_team