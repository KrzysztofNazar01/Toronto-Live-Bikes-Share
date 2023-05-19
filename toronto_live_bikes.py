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


def get_stations_information():
    url = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"
    # Send a GET request to the URL and fetch the JSON data
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data
        json_data = json.loads(response.text)

        # df = pd.read_json(url)
        df_stations = pd.json_normalize(json_data, record_path=['data', 'stations'])
        return df_stations
    else:
        print("Failed to fetch data. Error:", response.status_code)
        return None


def get_stations_status():
    url = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"
    # Send a GET request to the URL and fetch the JSON data
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data
        json_data = json.loads(response.text)

        # df = pd.read_json(url)
        df_stations = pd.json_normalize(json_data, record_path=['data', 'stations'])
        return df_stations
    else:
        print("Failed to fetch data. Error:", response.status_code)
        return None


if __name__ == "__main__":
    get_live_data_links()
