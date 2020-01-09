import numpy as np
import pandas as pd
import datetime
import folium
from folium.plugins import HeatMap

def create_heatmap_layer(df, base_map, layer_name):
    '''
    Create a heatmap layer onto the base map, with the lat/lon in the dataframe.

    ARGS:
        df (dataframe): Data to show in the heatmap layer, with 'latitude' and 'longitude' columns
        base_map (folium Map object): Base map to apply the layer to
        layer_name (str): Name of the layer.
    '''

    feature_map = folium.FeatureGroup(name = layer_name)
    feature_map.add_child(HeatMap(list(zip(df['latitude'].values, df['longitude'].values)), 
                            min_opacity=0.2,
                            max_val=30,
                            radius=4, blur=1, 
                            max_zoom=1
                        ))
    base_map.add_child(feature_map)


def create_multiple_dots_layers(df, base_map, layer_names, col_name):

    colors = ['red', 'orange', 'blue', 'purple', 'white', 'black', 'beige']
    
    for idx, layer in enumerate(layer_names):
        layer_df = df[df[col_name].str.contains(pat=layer)]
        color = colors[idx % 7]
        create_dots_layer(layer_df, base_map, layer, color=color)
        

def create_dots_layer(df, base_map, layer_name, color='black'):
    '''
    Create a dots layer onto the base map, with the lat/lon in the dataframe.
    Opacity of dot is the business star rating.

    ARGS:
        df (dataframe): Data to show in the layer, with 'latitude' and 'longitude' columns
        base_map (folium Map object): Base map to apply the layer to
        layer_name (str): Name of the layer.
        color (str): Color of the dots.
    '''

    feature_map = folium.FeatureGroup(name = layer_name)

    for idx, row in df.iterrows():
        opacity = row['stars'] / 5
        folium.CircleMarker(location=(row['latitude'], row['longitude']),
                                    radius=.75,
                                    color=color,
                                    opacity=opacity,
                                    popup=str(row['name'] \
                                              + '\nRating: ' + str(row['stars']) \
                                              + '\n# Reviews: '+ str(row['review_count']) \
                                             ),
                                    fill=True).add_to(feature_map)

    base_map.add_child(feature_map)


if __name__ == '__main__':

    #Load the pickeled dataframes
    businesses_df = pd.read_pickle('../data/pickled_businesses_df')
    category_counts = pd.read_pickle('../data/pickled_category_counts')
    top_4_cats = list(category_counts['elem'][0:4])

    # Set up city dataframes for mapping
    vegas_df = businesses_df[businesses_df['city']=='Las Vegas']
    charlotte_df = businesses_df[businesses_df['city']=='Charlotte']

    base_map = folium.Map(location=[39.73782,-104.971338],
                            zoom_start=4,
                            tiles="Cartodbpositron")


    vegas_map = folium.Map(location=[36.1699, -115.1398],
                            zoom_start=11,
                            tiles="Cartodbpositron")


    charlotte_map = folium.Map(location=[35.2271, -80.8431],
                            zoom_start=11,
                            tiles="Cartodbpositron")


    # Create overall heatmap for all businesses in dataset
    create_heatmap_layer(businesses_df, base_map, 'all businesses')

    # Create heatmap layers for Vegas
    create_heatmap_layer(vegas_df, vegas_map, 'all businesses')

    vegas_five_stars_df = vegas_df[vegas_df['stars']==5.0]
    create_heatmap_layer(vegas_five_stars_df, vegas_map, '5-star businesses')

    chinese_df = vegas_df[vegas_df['categories'].str.contains(pat='Chinese')]
    create_heatmap_layer(chinese_df, vegas_map, 'Chinese restaurants')


    # Create map layers for Charlotte
    create_multiple_dots_layers(charlotte_df, charlotte_map, top_4_cats, 'categories')

    # add toggle controls for the layers
    folium.LayerControl().add_to(vegas_map)
    folium.LayerControl().add_to(charlotte_map)

    base_map.save('../images/base_map.html')
    vegas_map.save('../images/vegas_map.html')
    charlotte_map.save('../images/charlotte_map.html')
