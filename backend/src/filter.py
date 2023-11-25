"""
Filter Dataset according to params set by user

"""
import pandas as pd

def filter_data(dataset, filters):
    # Make a copy of the original dataset

    filtered_data = dataset.copy()
    if 'color' in filters:
        colors_to_filter = filters['color']
        if colors_to_filter and isinstance(colors_to_filter, list):
            color_mask = filtered_data['Color'].isin(colors_to_filter)
            filtered_data = filtered_data[color_mask]
    # Filter based on type
    if 'type' in filters:
        types_to_filter = filters['type']
        if types_to_filter and isinstance(types_to_filter, list):
            type_mask = filtered_data['Type_1'].isin(types_to_filter) | filtered_data['Type_2'].isin(types_to_filter)
            filtered_data = filtered_data[type_mask]


    # Filter based on legendary status
    if 'legendary' in filters:
        legendary = filters['legendary']
        if legendary is not None and legendary == "FALSE":
            # Use only non-legendary Pokemon when legendary is False
            filtered_data = filtered_data[filtered_data['isLegendary'] == False]

    if 'generation' in filters:
        generation = filters['generation']
        if generation is not None:
            filtered_data = filtered_data[filtered_data['Generation'] == generation]

        # Convert filtered data to JSON
    json_data = filtered_data.to_json(orient='records')

    return filtered_data, json_data