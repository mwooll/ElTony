"""
Filter Dataset according to params set by user

"""
import pandas as pd


def filter_data(dataset, filters):
    # Make a copy of the original dataset
    filtered_data = dataset.copy()

    # Filter based on type
    if 'type' in filters:
        types = filters['type']
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
            filtered_data = filtered_data[filtered_data['Type_1'].isin(recommended_types)]

    # Filter based on legendary status
    if 'legendary' in filters:
        legendary = filters['legendary']
        if legendary is not None and len(legendary) == 1:
            filtered_data = filtered_data[filtered_data['isLegendary'] == (legendary[0] == 'TRUE')]

    # Filter based on generation
    if 'generation' in filters:
        generation = filters['generation']
        if generation is not None:
            filtered_data = filtered_data[filtered_data['Generation'] == generation]

    # Filter based on color
    if 'color' in filters:
        color = filters['color']
        if color:
            filtered_data = filtered_data[filtered_data['Color'].isin(color)]

    print("filtered")
    json_data = filtered_data.to_json(orient='records')
    return filtered_data,json_data
