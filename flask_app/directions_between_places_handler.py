import openrouteservice
import folium
from openrouteservice_api_key import api_key
from distance_calculator import find_nearest_neighbors


def create_map_with_directions(source_latitude, source_longitude, destination_latitude, destination_longitude, df_stations):
    """
    Create and save a Folium map with markers and routes connecting the source location and destination location.

    Args:
        source_latitude: source location - latitude
        source_longitude: source location - longitude
        destination_latitude: destination location - latitude
        destination_longitude: destination location - longitude
        df_stations: Pandas Dataframe containing the stations' information and status

    """
    folium_map = folium.Map(width='70%', height='60%', location=[source_latitude, source_longitude], zoom_start=15)

    nearest_station_with_bike, nearest_station_with_dock = find_key_locations(source_latitude, source_longitude,
                                                                              destination_latitude, destination_longitude,
                                                                              df_stations)

    add_routes_connecting_key_locations_to_map(source_latitude, source_longitude,
                                               destination_latitude, destination_longitude,
                                               folium_map, nearest_station_with_bike, nearest_station_with_dock)

    add_markers_with_key_locations_to_map(source_latitude, source_longitude,
                                          destination_latitude, destination_longitude,
                                          folium_map, nearest_station_with_bike, nearest_station_with_dock)

    folium_map.save('templates/directions_map.html')


def add_markers_with_key_locations_to_map(source_latitude, source_longitude,
                                          destination_latitude, destination_longitude,
                                          folium_map, nearest_station_with_bike, nearest_station_with_dock):
    """
    Add markers representing the 4 key locations to the Folium map.

    Args:
        source_latitude: source location - latitude
        source_longitude: source location - longitude
        destination_latitude: destination location - latitude
        destination_longitude: destination location - longitude
        folium_map: Folium map with routes and markers
        nearest_station_with_bike: the nearest station from the source location with at least one bike available
        nearest_station_with_dock: the nearest station from the destination location with at least one dock available
    """

    # button triggers JavaScript functions on click event
    cycling_travel_mode = '1'
    directions_button = '<button onclick="show_directions({}, {}, {}, {}, {}, {}, {}, {}, {})">Show directions</button>' \
        .format(source_latitude, source_longitude,
                nearest_station_with_bike['lat'], nearest_station_with_bike['lon'],
                nearest_station_with_dock['lat'], nearest_station_with_dock['lon'],
                destination_latitude, destination_longitude,
                cycling_travel_mode)

    # add markers to Folium map
    folium.Marker(location=[source_latitude, source_longitude],
                  popup="Source location" + directions_button,
                  icon=folium.Icon(color='red', icon='crosshairs', prefix='fa')).add_to(folium_map)
    folium.Marker(location=[nearest_station_with_bike['lat'], nearest_station_with_bike['lon']],
                  popup="The nearest station with bike" + directions_button,
                  icon=folium.Icon(color='orange', icon='bicycle', prefix='fa')).add_to(folium_map)
    folium.Marker(location=[nearest_station_with_dock['lat'], nearest_station_with_dock['lon']],
                  popup="The nearest station with dock" + directions_button,
                  icon=folium.Icon(color='blue', icon='gas-pump', prefix='fa')).add_to(folium_map)
    folium.Marker(location=[destination_latitude, destination_longitude],
                  popup="Destination location" + directions_button,
                  icon=folium.Icon(color='green', icon='font-awesome', prefix='fa')).add_to(folium_map)


def add_routes_connecting_key_locations_to_map(source_latitude, source_longitude,
                                               destination_latitude, destination_longitude,
                                               folium_map, nearest_station_with_bike, nearest_station_with_dock):
    """
    Add routes connecting the 4 key locations to the Folium map.

    Args:
        source_latitude: source location - latitude
        source_longitude: source location - longitude
        destination_latitude: destination location - latitude
        destination_longitude: destination location - longitude
        folium_map: Folium map with routes and markers
        nearest_station_with_bike: the nearest station from the source location with at least one bike available
        nearest_station_with_dock: the nearest station from the destination location with at least one dock available
    """
    source_to_station = add_path_between_points(source_latitude, source_longitude,
                                                nearest_station_with_bike['lat'], nearest_station_with_bike['lon'],
                                                'foot-walking', 'red')
    station_to_dock = add_path_between_points(nearest_station_with_bike['lat'], nearest_station_with_bike['lon'],
                                              nearest_station_with_dock['lat'], nearest_station_with_dock['lon'],
                                              'cycling-regular', 'orange')
    dock_to_destination = add_path_between_points(nearest_station_with_dock['lat'], nearest_station_with_dock['lon'],
                                                  destination_latitude, destination_longitude,
                                                  'foot-walking', 'blue')
    source_to_station.add_to(folium_map)
    station_to_dock.add_to(folium_map)
    dock_to_destination.add_to(folium_map)


def find_key_locations(source_latitude, source_longitude, destination_latitude, destination_longitude, df_stations):
    """
    Find the key locations which will be used in the travel.

    Args:
        source_latitude: source location - latitude
        source_longitude: source location - longitude
        destination_latitude: destination location - latitude
        destination_longitude: destination location - longitude
        df_stations: Pandas Dataframe containing the stations' information and status

    Returns:
        nearest_station_with_bike: the nearest station from the source location with at least one bike available
        nearest_station_with_dock: the nearest station from the destination location with at least one dock available
    """
    # station nearest to source location
    nearest_station_with_bike = find_nearest_neighbors(source_latitude, source_longitude, df_stations, 1, 'bikes')[0]
    # station nearest to destination location
    nearest_station_with_dock = find_nearest_neighbors(destination_latitude, destination_longitude, df_stations, 1, 'docks')[0]
    return nearest_station_with_bike, nearest_station_with_dock


def add_path_between_points(source_latitude, source_longitude,
                            destination_latitude, destination_longitude, directions_profile, route_color):
    """

    Args:
        source_latitude: source location - latitude
        source_longitude: source location - longitude
        destination_latitude: destination location - latitude
        destination_longitude: destination location - longitude
        directions_profile: profile used by openrouteservice client during searching the route connecting source and destination location
        route_color: color of the route

    Returns:
        directions: route connecting source and destination location
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
                                                                                    destination_latitude,
                                                                                    destination_longitude,
                                                                                    directions_profile)
    directions = folium.PolyLine(locations=[list(reversed(coord))
                                            for coord in
                                            route['features'][0]['geometry']['coordinates']],
                                 color=route_color,
                                 weight=5,
                                 opacity=1,
                                 tooltip="Click for details",  # showed on hover
                                 popup=folium.Popup(popup_content, max_width=200)  # showed on click
                                 )
    return directions
