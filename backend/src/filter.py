"""
Filter Dataset according to params set by user

"""

def filter_data(dataset,filters):
    filtered_data = dataset.copy()

    # Filter based on type
    if 'type' in filters:
        types = filters['type']
        if types:
            filtered_data = filtered_data[(filtered_data['Type_1'].isin(types)) | (filtered_data['Type_2'].isin(types))]

    # Filter based on legendary status
    if 'legendary' in filters:
        legendary = filters['legendary']
        if legendary is not None:
            filtered_data = filtered_data[filtered_data['isLegendary'] == legendary]

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

    # Add more filters based on your dataset columns

    return filtered_data
