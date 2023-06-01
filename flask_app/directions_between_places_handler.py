import openrouteservice
import folium
from openrouteservice_api_key import api_key
from distance_calculator import find_nearest_neighbors
from get_data import get_data


def create_map_with_directions(source_latitude, source_longitude,
                               destination_latitude, destination_longitude, df_stations):
    """

    Args:
        source_latitude:
        source_longitude:
        destination_latitude:
        destination_longitude:
        df_stations:

    Returns:

    """
    m = folium.Map(width='70%', height='60%', location=[source_latitude, source_longitude], zoom_start=15)

    # nearest to source location
    nearest_station_with_bike = find_nearest_neighbors(source_latitude, source_longitude, df_stations, 1, 'bikes')[0]

    # nearest to destination location
    nearest_station_with_dock = find_nearest_neighbors(destination_latitude, destination_longitude, df_stations, 1, 'docks')[0]

    source_to_station = add_path_between_points(source_latitude, source_longitude,
                                                nearest_station_with_bike['lat'], nearest_station_with_bike['lon'],
                                                'foot-walking', 'red')

    station_to_dock = add_path_between_points(nearest_station_with_bike['lat'], nearest_station_with_bike['lon'],
                                              nearest_station_with_dock['lat'], nearest_station_with_dock['lon'],
                                              'cycling-regular', 'orange')

    dock_to_destination = add_path_between_points(nearest_station_with_dock['lat'], nearest_station_with_dock['lon'],
                                                  destination_latitude, destination_longitude,
                                                  'foot-walking', 'blue')

    source_to_station.add_to(m)
    station_to_dock.add_to(m)
    dock_to_destination.add_to(m)

    cycling_travel_mode = '1'
    directions_button = '<button onclick="show_directions({}, {}, {}, {}, {}, {}, {}, {}, {})">Show directions</button>'\
        .format(source_latitude, source_longitude,
                nearest_station_with_bike['lat'], nearest_station_with_bike['lon'],
                nearest_station_with_dock['lat'], nearest_station_with_dock['lon'],
                destination_latitude, destination_longitude,
                cycling_travel_mode)

    folium.Marker(location=[source_latitude, source_longitude],
                  popup="Source location" + directions_button,
                  icon=folium.Icon(color='red', icon='crosshairs', prefix='fa')).add_to(m)

    folium.Marker(location=[nearest_station_with_bike['lat'], nearest_station_with_bike['lon']],
                  popup="The nearest station with bike" + directions_button,
                  icon=folium.Icon(color='orange', icon='bicycle', prefix='fa')).add_to(m)

    folium.Marker(location=[nearest_station_with_dock['lat'], nearest_station_with_dock['lon']],
                  popup="The nearest station with dock" + directions_button,
                  icon=folium.Icon(color='blue', icon='gas-pump', prefix='fa')).add_to(m)

    folium.Marker(location=[destination_latitude, destination_longitude],
                  popup="Destination location" + directions_button,
                  icon=folium.Icon(color='green', icon='font-awesome', prefix='fa')).add_to(m)

    m.save('templates/directions_map.html')


def add_path_between_points(source_latitude, source_longitude,
                            destination_latitude, destination_longitude, directions_profile, line_color):
    """

    Args:
        source_latitude:
        source_longitude:
        destination_latitude:
        destination_longitude:
        directions_profile:
        line_color:

    Returns:

    """
    openrouteservice_api_key = api_key
    client = openrouteservice.Client(key=openrouteservice_api_key)  # Specify your personal API key

    coordinates = [[source_longitude, source_latitude], [destination_longitude, destination_latitude]]

    route = client.directions(
        coordinates=coordinates,
        profile=directions_profile,
        format='geojson',
        options={"avoid_features": ["steps"]},
        validate=False,
    )

    popup_content = "Route from ({}, {}) <br> to ({}, {}). <br> Profile: {}".format(source_latitude, source_longitude,
                                                                  destination_latitude, destination_longitude, directions_profile)
    # print("###" + popup_content)
    directions = folium.PolyLine(locations=[list(reversed(coord))
                                            for coord in
                                            route['features'][0]['geometry']['coordinates']],
                                 color=line_color,
                                 weight=5,
                                 opacity=1,
                                 tooltip="Click for details",  # showed on hover
                                 popup=folium.Popup(popup_content, max_width=200)  # showed on click
                                 )
    return directions

