from math import radians, sin, cos, sqrt, atan2


def haversine_distance(source_latitude, source_longitude, destination_latitude, destination_longitude):
    """
    Calculate the haversine distance between two points given their latitude and longitude.

    Args:
        source_latitude: source location - latitude
        source_longitude: source location - longitude
        destination_latitude: destination location - latitude
        destination_longitude: destination location - longitude

    Returns:
         distance: Haversine distance between two points

    Haversine formula:
        a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
                        _   ____
        c = 2 ⋅ atan2( √a, √(1−a) )
        d = R ⋅ c

    where:
        φ is latitude,
        λ is longitude,
        R is earth’s radius (mean radius = 6,371km)

    note that angles need to be in radians to pass to trig functions!

    References:
        - https://community.esri.com/t5/coordinate-reference-systems-blog/distance-on-a-sphere-the-haversine-formula/ba-p/902128
        - https://stackoverflow.com/questions/37324332/how-to-find-the-nearest-neighbors-for-latitude-and-longitude-point-on-python
    """
    R = 6371  # radius of the Earth in kilometers
    dlat = radians(destination_latitude - source_latitude)
    dlon = radians(destination_longitude - source_longitude)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(source_latitude)) * cos(radians(destination_latitude)) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def filter_stations(df_stations, search_for_type):
    """
    Filter the Pandas Dataframe with stations' status and information to get stations that fit the search parameters.

    Args:
        df_stations: Pandas Dataframe containing the stations' information and status
        search_for_type: type of search - only "Bikes" or "Docks" are possible

    Returns:
        df_stations: filtered Pandas Dataframe containing the stations' information and status
    """
    if search_for_type == 'Bikes':
        df_stations = df_stations.drop(df_stations[df_stations.num_bikes_available == 0].index)
        df_stations = df_stations.drop(df_stations[df_stations.is_renting == 0].index)

    elif search_for_type == 'Docks':
        df_stations = df_stations.drop(df_stations[df_stations.num_docks_available == 0].index)
        df_stations = df_stations.drop(df_stations[df_stations.is_returning == 0].index)

    return df_stations


def find_nearest_neighbors(source_latitude, source_longitude, df_stations, k, search_for_type):
    """
    Find the K nearest neighbors to the source location (latitude and longitude) from a list of locations.

    Args:
        source_latitude: Latitude of user location (source)
        source_longitude: Longitude of user location (source)
        df_stations: Pandas Dataframe containing the information about the stations
        k: Number of nearest neighbours to find
        search_for_type: type of search - only "Bikes" or "Docks" are possible

    Returns:
         nearest_stations: K nearest neighbours to the source location
    """
    stations_to_analyse = filter_stations(df_stations, search_for_type)

    distances = []
    for index, location in stations_to_analyse.iterrows():
        lat, lon = location['lat'], location['lon']
        distance = haversine_distance(source_latitude, source_longitude, lat, lon)
        distances.append((location, distance))

    distances.sort(key=lambda x: x[1])  # Sort distances in ascending order

    nearest_stations = []
    for i in range(k):
        nearest_stations.append(distances[i][0])

    return nearest_stations
