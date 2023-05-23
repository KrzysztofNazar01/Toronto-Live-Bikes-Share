import requests
import pandas as pd
import json


def get_live_data_links():
    # all links with live data: https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/2b44db0d-eea9-442d-b038-79335368ad5a/resource/b69873a1-c180-4ccd-a970-514e434b4971/download/bike-share-gbfs-general-bikeshare-feed-specification.json

    # https://docs.ckan.org/en/latest/api/
    # Toronto Open Data is stored in a CKAN instance. It's APIs are documented here:

    base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    # To hit our API, you'll be making requests to:

    url = base_url + "/api/3/action/package_show"
    # Datasets are called "packages". Each package can contain many "resources"
    # To retrieve the metadata for this package and its resources, use the package name in this page's URL:
    params = {"id": "bike-share-toronto"}
    package = requests.get(url, params=params).json()

    # To get resource data:
    for idx, resource in enumerate(package["result"]["resources"]):

        # To get metadata for non datastore_active resources:
        if not resource["datastore_active"]:
            url = base_url + "/api/3/action/resource_show?id=" + resource["id"]
            resource_metadata = requests.get(url).json()
            print(resource_metadata)
            # From here, you can use the "url" attribute to download this file


def get_data_from_url(url):
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
