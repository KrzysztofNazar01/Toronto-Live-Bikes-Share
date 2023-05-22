import pandas as pd
from get_data import get_data, format_data

if __name__ == "__main__":
    url_station_information = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"
    url_station_status = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status"
    df_information = get_data(url_station_information)
    df_status = get_data(url_station_status)

    df_stations = pd.merge(df_information, df_status, on="station_id")
    df_stations = format_data(df_stations)
