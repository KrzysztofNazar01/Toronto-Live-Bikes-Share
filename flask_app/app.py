from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from map_handler import create_map_with_stations
from get_data import get_data
from distance_calculator import find_nearest_neighbors

app = Flask(__name__)  # reference to this file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # 3 slashes --> relative path
db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def index():

    # generate new map
    if request.method == 'POST':
        # get values from html form using id of each field
        target_latitude = float(request.form['lat'])
        target_longitude = float(request.form['lon'])
        k_value = int(request.form['k_value'])  # Number of nearest neighbors to find

        # get the data from JSON
        df_stations = get_data()

        # get the K nearest neighbours from the target location
        nearest_neighbors = find_nearest_neighbors(target_latitude, target_longitude, df_stations, k_value)

        # create and save the map
        create_map_with_stations(df_stations, nearest_neighbors, target_latitude, target_longitude)

        return redirect('/')

    # use the already generated map
    else:
        return render_template('map_view.html')


if __name__ == "__main__":
    app.run(debug=True)
