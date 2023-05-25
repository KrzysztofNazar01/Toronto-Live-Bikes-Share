import openrouteservice
import folium
from openrouteservice_api_key import api_key


def calculate_color_based_on_distance(iteration, max_iterations):
    factor = float((iteration + 1) / max_iterations)
    r = 0 + int(200 * factor)
    g = 255 - int(200 * factor)
    b = 0
    color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    return color


def num_to_range(num, inMin, inMax, outMin, outMax):
    return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax - outMin))


def calculate_weight_based_on_distance(iteration, max_iterations):
    """
    it can be float
    Args:
        iteration:
        max_iterations:

    Returns:

    """
    factor = float((iteration + 1) / max_iterations)
    return num_to_range(factor, 1, float(1 / max_iterations), 2, 7)  # weight = 2/factor


def calculate_opacity_based_on_distance(iteration, max_iterations):
    """
    it can be float
    Args:
        iteration:
        max_iterations:

    Returns:

    """
    factor = float((iteration + 1) / max_iterations)
    return num_to_range(factor, 1, float(1 / max_iterations), 0.2, 1)  # weight = 2/factor


def add_paths_to_station(target_latitude, target_longitude, station, iteration, max_iterations):
    openrouteservice_api_key = api_key
    client = openrouteservice.Client(key=openrouteservice_api_key)  # Specify your personal API key
    station_latitude, station_longitude = station['lat'], station['lon']

    coordinates = [[target_longitude, target_latitude], [station_longitude, station_latitude]]

    route = client.directions(
        coordinates=coordinates,
        profile='foot-walking',
        format='geojson',
        options={"avoid_features": ["steps"]},
        validate=False,
    )

    color = calculate_color_based_on_distance(iteration, max_iterations)
    weight = calculate_weight_based_on_distance(iteration, max_iterations)
    opacity = calculate_opacity_based_on_distance(iteration, max_iterations)
    directions = folium.PolyLine(locations=[list(reversed(coord))
                                            for coord in
                                            route['features'][0]['geometry']['coordinates']],
                                 color=color,
                                 weight=weight,
                                 opacity=opacity,
                                 tooltip="Click for details",  # showed on hover
                                 popup="Route to station: {}".format(station['station_id'])  # showed on click
                                 )
    return directions


if __name__ == "__main__":
    openrouteservice_api_key = '5b3ce3597851110001cf6248407589fa9dd24009974cdd09d4f6fd7f'

    client = openrouteservice.Client(key=openrouteservice_api_key)  # Specify your personal API key

    m = folium.Map(location=[52.521861, 13.40744], tiles='cartodbpositron', zoom_start=13)

    # Some coordinates in Berlin
    coordinates = [[13.42731, 52.51088], [13.384116, 52.533558]]

    route = client.directions(
        coordinates=coordinates,
        profile='foot-walking',
        format='geojson',
        options={"avoid_features": ["steps"]},
        validate=False,
    )

    folium.PolyLine(locations=[list(reversed(coord))
                               for coord in
                               route['features'][0]['geometry']['coordinates']],
                    color="orange",
                    weight=3,
                    opacity=1,
                    tooltip="tooltip text",
                    popup="popup text"
                    ).add_to(m)
    m.show_in_browser()
