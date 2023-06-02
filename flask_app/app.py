from flask import Flask, request, redirect, render_template
from map_handler import create_map_with_stations
from get_data import get_data
from distance_calculator import find_nearest_neighbors
from directions_between_places_handler import create_map_with_directions

app = Flask(__name__)  # reference to this file


@app.route('/')
def index():
    return redirect('/search_available')


@app.route('/search_available', methods=['POST', 'GET'])
def search_available():
    """
    Load page responsible for handling search for available bikes and docks.
    """
    # generate new map
    if request.method == 'POST':
        # get values from html form using id of each field
        source_latitude = float(request.form['lat'])
        source_longitude = float(request.form['lon'])
        k_value = int(request.form['k_value'])  # Number of nearest neighbors to find
        search_for_type = request.form['search_for']

        # get the data from JSON
        df_stations = get_data()

        # get the K nearest neighbours from the source location
        nearest_neighbors = find_nearest_neighbors(source_latitude, source_longitude, df_stations, k_value, search_for_type)

        # create and save the map
        create_map_with_stations(df_stations, nearest_neighbors, source_latitude, source_longitude)

        return redirect('/search_available')
    # use the already generated map
    else:
        return render_template('stations_view.html')


@app.route('/search_directions', methods=['POST', 'GET'])
def search_directions():
    """
    Load page responsible for handling search for directions
    """
    # generate new map
    if request.method == 'POST':
        # get values from html form using id of each field
        source_latitude = float(request.form['source_lat'])
        source_longitude = float(request.form['source_lon'])
        destination_latitude = float(request.form['dest_lat'])
        destination_longitude = float(request.form['dest_lon'])

        # get the data from JSON
        df_stations = get_data()

        # create and save the map
        create_map_with_directions(source_latitude, source_longitude, destination_latitude, destination_longitude, df_stations)

        return redirect('/search_directions')
    # use the already generated map
    else:
        return render_template('directions_view.html')


if __name__ == "__main__":
    app.run(debug=True)
