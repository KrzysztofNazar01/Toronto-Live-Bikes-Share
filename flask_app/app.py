from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from map_handler import create_map_with_stations
from get_data import get_data
from distance_calculator import find_nearest_neighbors

app = Flask(__name__)  # reference to this file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # 3 slashes --> relative path
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Created task with id {}'.format(self.id)


@app.route('/', methods=['POST', 'GET'])
def index():
    df_stations = get_data()

    target_latitude, target_longitude = 43.633655, -79.398874
    k = 3  # Number of nearest neighbors to find
    nearest_neighbors = find_nearest_k_neighbours(df_stations, target_latitude, target_longitude, k)

    html = create_map_with_stations(df_stations, nearest_neighbors)

    return render_template('map_view.html', map_stations=html)


def find_nearest_k_neighbours(df_stations, target_latitude, target_longitude, k):
    nearest_neighbors = find_nearest_neighbors(target_latitude, target_longitude, df_stations, k)

    # Print the nearest neighbors
    for neighbor in nearest_neighbors:
        print(neighbor['station_id'], "(", neighbor['lat'], ",", neighbor['lon'], ")")

    return nearest_neighbors


if __name__ == "__main__":
    app.run(debug=True)
