import openrouteservice
import folium
from openrouteservice_api_key import api_key


def create_map_with_directions(source_latitude, source_longitude,
                               destination_latitude, destination_longitude):
    m = folium.Map(location=[source_latitude, source_longitude], zoom_start=15)

    direct = add_path_between_points(source_latitude, source_longitude,
                                     destination_latitude, destination_longitude)
    direct.add_to(m)

    m.save('templates/folium_map_directions.html')


def add_path_between_points(source_latitude, source_longitude,
                            destination_latitude, destination_longitude):
    openrouteservice_api_key = api_key
    client = openrouteservice.Client(key=openrouteservice_api_key)  # Specify your personal API key

    coordinates = [[source_longitude, source_latitude], [destination_longitude, destination_latitude]]

    route = client.directions(
        coordinates=coordinates,
        profile='cycling-regular',
        format='geojson',
        options={"avoid_features": ["steps"]},
        validate=False,
    )

    popup_content = "Route from ({}, {}) <br> to ({}, {})".format(source_latitude, source_longitude,
                                                                  destination_latitude, destination_longitude)
    directions = folium.PolyLine(locations=[list(reversed(coord))
                                            for coord in
                                            route['features'][0]['geometry']['coordinates']],
                                 color="blue",
                                 weight=5,
                                 opacity=1,
                                 tooltip="Click for details",  # showed on hover
                                 popup=folium.Popup(popup_content, max_width=200)  # showed on click
                                 )
    return directions


# For debugging purpose:
if __name__ == "__main__":
    start_coords = [8.681495, 49.41461]  # longitude, latitude for start point
    end_coords = [8.687872, 49.420318]

    m = folium.Map(location=[start_coords[1], start_coords[0]], tiles='cartodbpositron', zoom_start=13)

    direct = add_path_between_points(start_coords[0], start_coords[1], end_coords[0], end_coords[1])
    direct.add_to(m)
    m.show_in_browser()
