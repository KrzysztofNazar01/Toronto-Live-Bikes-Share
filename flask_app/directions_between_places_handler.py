import openrouteservice
import folium
from openrouteservice_api_key import api_key
from distance_calculator import find_nearest_neighbors
from get_data import get_data


def create_map_with_directions(source_latitude, source_longitude,
                               destination_latitude, destination_longitude, df_stations):
    m = folium.Map(width='65%', height='65%', location=[source_latitude, source_longitude], zoom_start=15)

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
                  icon=folium.Icon(color='red', icon='bicycle', prefix='fa')).add_to(m)

    folium.Marker(location=[nearest_station_with_bike['lat'], nearest_station_with_bike['lon']],
                  popup="nearest_station_with_bike" + directions_button,
                  icon=folium.Icon(color='orange', icon='bicycle', prefix='fa')).add_to(m)

    folium.Marker(location=[nearest_station_with_dock['lat'], nearest_station_with_dock['lon']],
                  popup="nearest_station_with_dock" + directions_button,
                  icon=folium.Icon(color='blue', icon='bicycle', prefix='fa')).add_to(m)

    folium.Marker(location=[destination_latitude, destination_longitude],
                  popup="Destination location" + directions_button,
                  icon=folium.Icon(color='green', icon='bicycle', prefix='fa')).add_to(m)

    m.save('templates/directions_map.html')
    # m.show_in_browser()


def add_path_between_points(source_latitude, source_longitude,
                            destination_latitude, destination_longitude, directions_profile, line_color):
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


# For debugging purpose:
if __name__ == "__main__":
    start_coords = [43.663340, -79.502842]  # longitude, latitude for start point
    end_coords = [43.660825, -79.497264]

    m = folium.Map(location=[start_coords[1], start_coords[0]], tiles='cartodbpositron', zoom_start=13)

    # get the data from JSON
    df_stations = get_data()

    create_map_with_directions(start_coords[0], start_coords[1], end_coords[0], end_coords[1], df_stations)


