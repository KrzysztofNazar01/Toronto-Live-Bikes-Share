from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

from directions_between_places_handler import create_map_with_directions
from distance_calculator import find_nearest_neighbors
from get_data import get_data
from map_handler import create_map_with_stations

app = Flask(__name__)  # reference to this file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Use a local SQLite database file
db = SQLAlchemy(app)


class Station(db.Model):
    id_db = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    is_charging_station_x = db.Column(db.Boolean)
    nearby_distance = db.Column(db.Integer)
    num_bikes_available = db.Column(db.Integer)
    num_bikes_disabled = db.Column(db.Integer)
    num_docks_available = db.Column(db.Integer)
    num_docks_disabled = db.Column(db.Integer)
    is_charging_station_y = db.Column(db.Boolean)
    is_renting = db.Column(db.Boolean)
    is_returning = db.Column(db.Boolean)
    num_bikes_available_types_mechanical = db.Column(db.Integer)
    num_bikes_available_types_ebike = db.Column(db.Integer)

    def __repr__(self):
        return '<Station >'.format(self.station_id)


@app.errorhandler(404)
def invalid_route(e):
    return render_template('error_404.html')


@app.route('/')
def index():
    model_object = Station(station_id=1,
                           latitude=123.123,
                           longitude=123.123,
                           address="address",
                           capacity=1
                           )

    # Add the object to the session
    db.session.add(model_object)

    # Commit the session to the database
    db.session.commit()

    return redirect('/search_available')


@app.route('/about_author')
def about_author():
    return render_template('about_author_view.html')


@app.route('/about_project')
def about_project():
    return render_template('about_project_view.html')


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
