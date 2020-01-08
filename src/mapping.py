import numpy as np
import pandas as pd
import datetime
import folium
from folium.plugins import HeatMap

#Load the pickeled dataframe
businesses_df = pd.read_pickle('../data/pickled_businesses_df')

# Set up variables for Vegas map
vegas_df = businesses_df[businesses_df['city']=='Las Vegas']
num_vegas_businesses = len(vegas_df)
default_max_val = 30  # default value to use as maximum point intensity in the heatmap


# Set up Charlotte map data
charlotte_df = businesses_df[businesses_df['city']=='Charlotte']

# base_map = folium.Map(location=[39.73782,-104.971338],
#                         zoom_start=4,
#                         tiles="Cartodbpositron")


vegas_map = folium.Map(location=[36.1699, -115.1398],
                        zoom_start=11,
                        tiles="Cartodbpositron")


charlotte_map = folium.Map(location=[35.2271, -80.8431],
                        zoom_start=11,
                        tiles="Cartodbpositron")


def create_heatmap_layer(df, base_map, layer_name, max_val=default_max_val):
    '''
    Create a heatmap layer onto the base map, with the lat/lon in the dataframe.

    ARGS:
        df (dataframe): Data to show in the heatmap layer, with 'latitude' and 'longitude' columns
        base_map (folium Map object): Base map to apply the layer to
        layer_name (str): Name of the layer.
        max_val (double): Will be passed into HeatMap for the maximum point intensity, used to increase intensity
            in df's with few number of rows.
    '''

    feature_map = folium.FeatureGroup(name = layer_name)
    max_amount = float(max_val)
    feature_map.add_child(HeatMap(list(zip(df['latitude'].values, df['longitude'].values)), 
                            min_opacity=0.2,
                            max_val=max_amount,
                            radius=4, blur=1, 
                            max_zoom=1
                        ))
    base_map.add_child(feature_map)


def create_dots_layer(df, base_map, layer_name, color):
    '''
    Create a dots layer onto the base map, with the lat/lon in the dataframe.

    ARGS:
        df (dataframe): Data to show in the layer, with 'latitude' and 'longitude' columns
        base_map (folium Map object): Base map to apply the layer to
        layer_name (str): Name of the layer.
        color (str): Color of the dots.
    '''

    feature_map = folium.FeatureGroup(name = layer_name)

    for idx, row in df.iterrows():
        folium.CircleMarker(location=(row['latitude'], row['longitude']),
                                    radius=.75,
                                    color=color,
                                    popup=str(row['name'] \
                                              + '\nRating: ' + str(row['stars']) \
                                              + '\n# Reviews: '+ str(row['review_count']) \
                                             ),
                                    fill=True).add_to(feature_map)

    base_map.add_child(feature_map)


### Create map layers for Vegas

create_heatmap_layer(vegas_df, vegas_map, 'all businesses')

vegas_five_stars_df = vegas_df[vegas_df['stars']==5.0]
#max_val = (len(five_stars_df) / len(vegas_df)) * default_max_val * 2
create_heatmap_layer(vegas_five_stars_df, vegas_map, '5-star businesses')

chinese_df = vegas_df[vegas_df['categories'].str.contains(pat='Chinese')]
#max_val = (len(chinese_df) / num_vegas_businesses) * default_max_val * 2
create_heatmap_layer(chinese_df, vegas_map, 'Chinese restaurants')


### Create map layers for Charlotte
create_dots_layer(charlotte_df, charlotte_map, 'all businesses', 'black')

charlotte_five_stars_df = charlotte_df[charlotte_df['stars']==5.0]
create_dots_layer(charlotte_five_stars_df, charlotte_map, '5-star businesses', 'red')


# add toggle controls for the layers
folium.LayerControl().add_to(vegas_map)
folium.LayerControl().add_to(charlotte_map)

vegas_map.save('../images/vegas_map.html')
charlotte_map.save('../images/charlotte_map.html')
