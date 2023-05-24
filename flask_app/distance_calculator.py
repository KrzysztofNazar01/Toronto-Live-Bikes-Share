from math import radians, sin, cos, sqrt, atan2


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the haversine distance between two points given their latitude and longitude.

    :param lat1: Latitude of user location (source)
    :param lon1: Longitude of user location (source)
    :param lat2: Latitude of user location (destination)
    :param lon2: Longitude of user location (destination)
    :return: Haversine distance between two points

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
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def filter_stations(df, search_for_type):
    if search_for_type == 'bikes':
        df = df.drop(df[df.num_bikes_available == 0].index)
        df = df.drop(df[df.is_renting == 0].index)

    elif search_for_type == 'docks':
        df = df.drop(df[df.num_docks_available == 0].index)
        df = df.drop(df[df.is_returning == 0].index)

    return df


def find_nearest_neighbors(target_lat, target_lon, df_stations, k, search_for_type):
    """
    Find the K nearest neighbors to a target location (latitude and longitude) from a list of locations.

    :param target_lat: Latitude of user location (source)
    :param target_lon: Longitude of user location (source)
    :param df_stations: Pandas Dataframe containing the information about the stations
    :param k: Number of nearest neighbours to find

    :return: K nearest neighbours to the target location

    """

    stations_to_analyse = filter_stations(df_stations, search_for_type)

    distances = []
    for index, location in stations_to_analyse.iterrows():
        lat, lon = location['lat'], location['lon']
        distance = haversine_distance(target_lat, target_lon, lat, lon)
        distances.append((location, distance))

    distances.sort(key=lambda x: x[1])  # Sort distances in ascending order

    neighbors = []
    for i in range(k):
        neighbors.append(distances[i][0])

    return neighbors
