import folium
from jinja2 import Template
from folium.map import Marker
from directions_to_stations_handler import add_paths_to_station

def create_popup_for_station(station):
    """
    Create a popup information to the marker representing one station.

    :param station: row in the Dataframe containing information and status of one station
    :return: html popup code
    """
    table_html = """
    <table id="popupTable">
            <thead>
                  <tr>
                    <th id="RefNoHeader" class="tableHeader">Information</th>
                    <th id="OfferTypeHeader" class="tableHeader">Value</th>
                  </tr>
            </thead>
                <tbody>               
    """
    color = '#4ce8fd'
    values = ['station_id', 'address', 'capacity', 'num_bikes_available', 'num_bikes_disabled',
              'num_bikes_available_types_mechanical', 'num_bikes_available_types_ebike',
              'num_docks_available', 'num_docks_disabled']
    for value in values:
        row = "<tr>"
        row += '<td class="popupRow" style="background-color: {};"><span>{}</span></td>'.format(color, value)
        row += '<td class="popupRow" style="background-color: {};"><span>{}</span></td>'.format(color, station[value])
        row += "</tr>"
        table_html += row

    table_html += """ </tbody>
            </table>"""

    popup_html_code = """<!DOCTYPE html>
        <html>
        <head>

        </head>
            <h1 class="tableTitle"> Station: """ + str(station['station_id']) + """</h1>""" + table_html + """
        </html>
        """
    popup = folium.Popup(folium.Html(popup_html_code, script=True, width=400))
    return popup


def add_styles_to_map(folium_map_as_string):
    """
    Inject styles into the map. The style tag is replaced with styles infromation.

    :param folium_map_as_string: Folium map converted to string
    :return: Folium map as string with styles
    """
    style_string = """
        <style>

        .tableTitle{
            font-size:2em;
            text-align: center;
            font-weight: bolder;
        }

        .tableHeader{
            text-align: center;
            border: 1px solid;
            font-size: 1em;
        }

        .popupRow{
            border: 1px solid;
            padding: 0.3em;
            font-size: 1em;
        }

        #popupTable{
            text-align: center;
            margin: auto;
        }
        """
    folium_map_as_string = folium_map_as_string.replace("<style>", style_string)

    return folium_map_as_string


def add_marker_with_target_location(map_with_stations, target_latitude, target_longitude):
    """
    Add marker with target location to the Folium map which contains the information about stations.

    :param map_with_stations: Folium map displaying the information about stations
    :param target_latitude: user location - latitude
    :param target_longitude: user location - longitude
    :return: Folium map with marker of the target location (user location)
    """
    # Modify Marker template to include the onClick event
    click_template = """{% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.marker(
                {{ this.location|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }}).on('click', copy_location_to_form_fields);
        {% endmacro %}"""

    # Change template to custom template
    Marker._template = Template(click_template)

    # Create the onClick listener function as a branca element and add to the map html
    click_js = """
                    function copy_location_to_form_fields(e) {
                          var point = e.latlng; 

                          var value_lat = point['lat'];
                          var input_field_lat = document.getElementById("lat");
                          input_field_lat.value = value_lat.toFixed(6);

                          var value_lon = point['lng'];
                          var input_field_lon = document.getElementById("lon");
                          input_field_lon.value = value_lon.toFixed(6);

                      }                     
                    """

    e = folium.Element(click_js)
    html = map_with_stations.get_root()
    html.script.get_root().render()
    html.script._children[e.get_name()] = e

    popup_html_code = """
                        <p id="marker_target_location"
                        style="font-size:1.3em; text-align:center;font-weight: bolder;margin-left: auto; margin-right: auto;">
                        Target location set!
                        </p>
                      """
    popup = folium.Popup(folium.Html(popup_html_code, script=True, width=130))

    # Add marker (click on map an alert will display with latlng values)
    folium.Marker(location=[target_latitude, target_longitude],  # target location
                  popup=popup,
                  icon=folium.Icon(color="red", icon='crosshairs', prefix='fa'),
                  draggable=True).add_to(map_with_stations)

    return map_with_stations


def create_map_with_stations(df_stations, nearest_neighbors, target_latitude, target_longitude):
    """
    Create a map with stations and the marker of user. The K nearest stations to the user's position are
    in a different color than other stations.

    :param df_stations: Pandas Dataframe containing the stations' information and status
    :param nearest_neighbors: list of station which are the nearest to the target location
    :param target_latitude: user location - latitude
    :param target_longitude: user location - longitude
    """
    map_with_stations = folium.Map(
        width='65%', height='65%',
        location=[target_latitude, target_longitude],  # 43.7, -79.4
        zoom_start=14)

    for index, station in df_stations.iterrows():
        popup = create_popup_for_station(station)

        latitude, longitude = station['lat'], station['lon']

        # if the station is nearby, set the color to green
        # otherwise set color to blue
        color = 'blue'
        for iteration, nearest_neighbor in enumerate(nearest_neighbors):
            if nearest_neighbor['station_id'] == station['station_id']:
                color = 'green'
                path_visualisation = add_paths_to_station(target_latitude, target_longitude, station, iteration, len(nearest_neighbors))
                path_visualisation.add_to(map_with_stations)

        folium.Marker(location=[latitude, longitude], popup=popup,
                      icon=folium.Icon(color=color, icon='bicycle', prefix='fa')).add_to(map_with_stations)

    map_with_stations = add_marker_with_target_location(map_with_stations, target_latitude, target_longitude)

    # map_with_stations.save('templates/folium_map.html')

    map_as_html = map_with_stations.get_root().render()
    map_as_html = add_styles_to_map(map_as_html)

    # save the map in file
    with open('templates/folium_map.html', "w", encoding='utf-8') as file:
        file.write(map_as_html)


