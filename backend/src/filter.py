"""
Filter Dataset according to params set by user

"""
import pandas as pd

def filter_data(dataset, filters):
    # Make a copy of the original dataset
    filtered_data = dataset.copy()

    # Filter based on type
    if 'type' in filters:
        types_to_filter = filters['type']
        if types_to_filter is not None and isinstance(types_to_filter, list):
            # Initialize a mask of False values
            type_mask = pd.Series(False, index=filtered_data.index)

            # Loop through each type and update the mask
            for pokemon_type in types_to_filter:
                type_mask = type_mask | (filtered_data['Type_1'] == pokemon_type) | (
                            filtered_data['Type_2'] == pokemon_type)

            # Apply the final type filter
            filtered_data = filtered_data[type_mask]

    # Filter based on legendary status
    if 'legendary' in filters:
        legendary = filters['legendary']
        if legendary is not None:

            if legendary == "FALSE":
                # Use only non-legendary Pokemon when legendary is False
                filtered_data = filtered_data[filtered_data['isLegendary'] == False]

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

    json_data = filtered_data.to_json(orient='records')

    return filtered_data,json_data
