"""
Recommender for the ideal pokemon team
Use clustering
Give Key feature for recommendation

"""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

pokemon_data = pd.read_csv('data/pokemon.csv')

# Select relevant columns for clustering
selected_cols = ['Total', 'HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed', 'Type_1', 'Type_2', 'Name']
pokemon_data = pokemon_data[selected_cols]

# Drop rows with missing types
pokemon_data = pokemon_data.dropna(subset=['Type_1'])

# Combine 'Type_1' and 'Type_2' columns to create 'Types' column
pokemon_data['Types'] = pokemon_data[['Type_1', 'Type_2']].astype(str).agg(','.join, axis=1)

# Select features for clustering
features = ['Total', 'HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed']

# Standardize the features
scaler = StandardScaler()
pokemon_data[features] = scaler.fit_transform(pokemon_data[features])

# Number of clusters (adjust as needed)
n_clusters = 18

# K-Means clustering
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
pokemon_data['Cluster'] = kmeans.fit_predict(pokemon_data[features])

# Sort Pokémon within each cluster by total stats
pokemon_data = pokemon_data.sort_values(by=['Cluster', 'Total'], ascending=[True, False])

team_size = 6
selected_types = set()
recommended_team = []

# Iterate through clusters and select Pokémon with diverse types
for cluster in pokemon_data['Cluster'].unique():
    cluster_data = pokemon_data[pokemon_data['Cluster'] == cluster]

    # Select the Pokémon with the highest stats and a new type
    for _, pokemon in cluster_data.iterrows():
        if pokemon['Type_1'] not in selected_types and pokemon['Type_2'] not in selected_types:
            # Add a column indicating the key feature
            key_feature = features[pokemon[features].argmax()]
            pokemon['Key_Feature'] = key_feature

            recommended_team.append(pd.DataFrame([pokemon]))
            selected_types.add(pokemon['Type_1'])
            if pd.notna(pokemon['Type_2']):
                selected_types.add(pokemon['Type_2'])
            break

    if len(recommended_team) == team_size:
        break

# Concatenate the DataFrames in the recommended_team list
recommended_team = pd.concat(recommended_team, ignore_index=True)

# Display the recommended team with key features
print("Recommended Team:")
print(recommended_team[['Name', 'Total', 'Type_1', 'Type_2', 'Key_Feature']])
