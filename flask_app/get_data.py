import requests
import pandas as pd
import json


def get_data_from_url(url):
    """
    Parse JSON data from url.

    :param url: Link containing the JSON data
    :return: Dataframe containing the data from JSON
    """
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data
        json_data = json.loads(response.text)
        dataframe = pd.json_normalize(json_data, record_path=['data', 'stations'])
        return dataframe

    else:
        print("Failed to fetch data. Error:", response.status_code)
        return None


def format_data(df):
    """
    Prepare the data for further analysis.

    :param df: Pandas dataframe with stations' information and status
    :return: Pandas dataframe with formatted data
    """
    # drop rows with stations out of service
    df.drop(df[df.status == 'END_OF_LIFE'].index, inplace=True)

    # drop unneeded columns
    columns_to_drop = ['altitude', 'rental_methods', 'obcn', 'is_valet_station', 'cross_street',
                       '_ride_code_support',
                       'physical_configuration', 'groups', 'post_code', 'name',
                       'is_renting', 'is_returning', 'last_reported', 'last_reported',
                       'traffic', 'is_installed', 'status']
    df.drop(columns_to_drop, axis=1, inplace=True)

    # rename columns with available bikes
    df.rename(columns={'num_bikes_available_types.mechanical': 'num_bikes_available_types_mechanical',
                       'num_bikes_available_types.ebike': 'num_bikes_available_types_ebike'}, inplace=True)

    df.reset_index(drop=True, inplace=True)
    return df


def get_data():
    """
    Get data about the current station information and station status.
    The data is in JSON format.

    :return: Pandas dataframe with stations' information and status
    """
    # url with json data
    url_station_information = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"
    url_station_status = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status"

    # parse the json data
    df_information = get_data_from_url(url_station_information)
    df_status = get_data_from_url(url_station_status)

    # prepare data for further analysis
    df_stations = pd.merge(df_information, df_status, on="station_id")
    df_stations = format_data(df_stations)

    # print(df_stations.columns.values)

    return df_stations
