import openrouteservice
import folium
from openrouteservice_api_key import api_key


def get_color_based_on_iteration(iteration, max_iterations):
    """
    Calculate route color based on the index of station in the sorted list of the nearest stations.
    The greater the index of station in the list (iteration),
    the greater the distance from the source location (in comparison to other stations).

    Args:
        iteration: index of station in the sorted list of the nearest stations
        max_iterations: number of stations in the list of the nearest stations

    Returns:
        color: the calculated color in hex format
    """
    factor = float((iteration + 1) / max_iterations)
    r = 0 + int(200 * factor)
    g = 255 - int(200 * factor)
    b = 0
    color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    return color


def map_value_between_ranges(num, inMin, inMax, outMin, outMax):
    """
    Maps a number from one range to another range.

    Args:
        num: value to be mapped
        inMin: minimum possible value as input
        inMax: maximum possible value as input
        outMin: minimum possible value as output
        outMax: maximum possible value as output

    Returns:
        mapped_value: mapped value based on the two ranges (input and output)
    """
    mapped_value = outMin + (float(num - inMin) / float(inMax - inMin) * (outMax - outMin))
    return mapped_value


def get_weight_based_on_iteration(iteration, max_iterations):
    """
    Calculate route weight based on the index of station in the sorted list of the nearest stations.
    The greater the index of station in the list (iteration),
    the greater the distance from the source location (in comparison to other stations).

    Args:
        iteration: index of station in the sorted list of the nearest stations
        max_iterations: number of stations in the list of the nearest stations

    Returns:
        weight: value of weight based on the iteration
    """
    weight = map_value_between_ranges(max_iterations - iteration, 0, max_iterations, 2, 8)
    return weight


def get_opacity_based_on_iteration(iteration, max_iterations):
    """
    Calculate route opacity based on the index of station in the sorted list of the nearest stations.
    The greater the index of station in the list (iteration),
    the greater the distance from the source location (in comparison to other stations).

    Args:
        iteration: index of station in the sorted list of the nearest stations
        max_iterations: number of stations in the list of the nearest stations

    Returns:
        opacity: value of opacity based on the iteration
    """
    opacity = map_value_between_ranges(max_iterations - iteration, 1, max_iterations + 1, 0.4, 1)
    return opacity


def get_routes_between_source_location_and_station(source_latitude, source_longitude, station, iteration, max_iterations):
    """

    Args:
        source_latitude: source location - latitude
        source_longitude: source location - longitude
        station: row in the Pandas Dataframe containing information about stations' status and information
        iteration: index of station in the sorted list of the nearest stations
        max_iterations: number of stations in the list of the nearest stations

    Returns:
        directions: Folium Polyline containing the route between source and destination location
    """
    # get the API key from imported file
    openrouteservice_api_key = api_key
    client = openrouteservice.Client(key=openrouteservice_api_key)

    # specify the source and destination location
    coordinates = [[source_longitude, source_latitude], [station['lon'], station['lat']]]

    route = client.directions(
        coordinates=coordinates,
        profile='foot-walking',
        format='geojson',
        options={"avoid_features": ["steps"]},
        validate=False,
    )

    color = get_color_based_on_iteration(iteration, max_iterations)
    weight = get_weight_based_on_iteration(iteration, max_iterations)
    opacity = get_opacity_based_on_iteration(iteration, max_iterations)
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
