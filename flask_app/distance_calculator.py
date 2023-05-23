from math import radians, sin, cos, sqrt, atan2


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the haversine distance between two points given their latitude and longitude.
    """
    R = 6371  # radius of the Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def find_nearest_neighbors(target_lat, target_lon, df_stations, k):
    """
    Find the K nearest neighbors to a target location (latitude and longitude) from a list of locations.
    """
    distances = []
    for index, location in df_stations.iterrows():
        lat, lon = location['lat'], location['lon']
        distance = haversine_distance(target_lat, target_lon, lat, lon)
        distances.append((location, distance))

    distances.sort(key=lambda x: x[1])  # Sort distances in ascending order

    neighbors = []
    for i in range(k):
        neighbors.append(distances[i][0])

    return neighbors


