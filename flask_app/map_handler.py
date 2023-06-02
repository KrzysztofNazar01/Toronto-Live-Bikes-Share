import folium
from jinja2 import Template
from folium.map import Marker
from directions_to_stations_handler import get_routes_between_source_location_and_station


def create_popup_for_station(station, source_latitude, source_longitude):
    """
    Create a popup information to the marker representing one station.

    Args:
        station: row in the Dataframe containing information and status of one station
        source_latitude: source location - latitude
        source_longitude: source location - longitude

    Returns:
         popup: html popup code
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
    values = ['address', 'num_bikes_available',
              'num_bikes_available_types_mechanical', 'num_bikes_available_types_ebike',
              'num_docks_available']
    values_names = ['Address', 'Bikes available',
                    'Bikes available - mechanical', 'Bikes available - ebike',
                    'Docks available']
    for index, value in enumerate(values):
        row = "<tr>"
        row += '<td class="popupRow" style="background-color: {};"><span>{}</span></td>'.format(color, values_names[index])
        row += '<td class="popupRow" style="background-color: {};"><span>{}</span></td>'.format(color, station[value])
        row += "</tr>"
        table_html += row

    table_html = add_buttons_with_directions(source_latitude, source_longitude, station, table_html)

    table_html += """ </tbody> </table>"""

    popup_html_code = """<!DOCTYPE html>
        <html>
        <head>
        </head>
        <body>
            <h1 class="tableTitle"> Station: """ + str(station['station_id']) + """</h1>""" + table_html + """
        </body>
        </html>
        """
    popup = folium.Popup(folium.Html(popup_html_code, script=True, width=400))
    return popup


def add_buttons_with_directions(source_latitude, source_longitude, station, table_html):
    """
    Add buttons which redirect to Google Maps and show the directions from source location to destination location.
    Two buttons are added - Walking and Cycling button.
    Args:
        source_latitude: source location - latitude
        source_longitude: source location - longitude
        station: row in the Dataframe containing information and status of one station
        table_html: code representing HTML table with station's details

    Returns:
        table_html: updated HTML code of table with station's details
    """
    dest_latitude, dest_longitude = station['lat'], station['lon']

    # create html code for buttons
    cycling_travel_mode = '1'
    cycling_button = '<button onclick="redirect_to_directions({}, {}, {}, {}, {})">Cycling</button>' \
        .format(dest_latitude, dest_longitude, source_latitude, source_longitude, cycling_travel_mode)

    walk_travel_mode = '2'
    walk_button = '<button onclick="redirect_to_directions({}, {}, {}, {}, {})">Walking</button>' \
        .format(dest_latitude, dest_longitude, source_latitude, source_longitude, walk_travel_mode)

    # add new row in table
    row = "<tr>"
    row += '<td class="popupRow" style="background-color: #4ce8fd;"><span>Directions</span></button></td>'
    row += '<td class="popupRow" style="background-color: #4ce8fd;"><span>{} {}</span></td>'.format(cycling_button, walk_button)
    row += "</tr>"

    table_html += row
    return table_html


def add_styles_to_map(folium_map):
    """
    Inject styles into the map. The style tag is replaced with styles information.

    Args:
        folium_map: Folium map converted to string

    Returns:
        folium_map: Folium map as string with styles
    """
    styles = """
        <style>

        .tableTitle{
            font-size:2em;
            text-align: center;
            font-weight: bold;
        }

        .tableHeader{
            text-align: center;
            border: 1px solid;
            font-size: 1.4em;
            font-weight: bolder;
        }

        .popupRow{
            border: 1px solid;
            padding: 0.3em;
            font-size: 1.3em;
        }

        #popupTable{
            text-align: center;
            margin: auto;
        }
        """
    folium_map = folium_map.replace("<style>", styles)

    return folium_map


def add_marker_with_source_location(map_with_stations, source_latitude, source_longitude):
    """
    Add marker with source location to the Folium map which contains the information about stations.

    Args:
        map_with_stations: Folium map displaying the information about stations
        source_latitude: source location - latitude
        source_longitude: source location - longitude

    Returns:
        map_with_stations: Folium map with marker of the source location
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
                      
                    function redirect_to_directions(dest_latitude, dest_longitude, source_latitude, source_longitude, travel_mode) {                
                        url= 'https://www.google.com/maps/dir/' + dest_latitude + ',' + dest_longitude + '/' + source_latitude + ',' + source_longitude + '/data=!3m1!4b1!4m2!4m1!3e' + travel_mode + '?entry=ttu';
                        window.open(url, '_blank');
                    }                   
                    """

    e = folium.Element(click_js)
    html = map_with_stations.get_root()
    html.script.get_root().render()
    html.script._children[e.get_name()] = e

    popup_html_code = """
                        <p id="marker_source_location"
                        style="font-size:1.3em; text-align:center;font-weight: bolder;margin-left: auto; margin-right: auto;">
                        User location set!
                        </p>
                      """
    popup = folium.Popup(folium.Html(popup_html_code, script=True, width=130))

    # Add marker (click on map an alert will display with latlng values)
    folium.Marker(location=[source_latitude, source_longitude],
                  popup=popup,
                  icon=folium.Icon(color="red", icon='crosshairs', prefix='fa'),
                  draggable=True).add_to(map_with_stations)

    return map_with_stations


def create_map_with_stations(df_stations, nearest_neighbors, source_latitude, source_longitude):
    """
    Create a map with stations and the marker of user.
    The K nearest stations to the user's position are in a different color than other stations.

    Args:
        df_stations: Pandas Dataframe containing the stations' information and status
        nearest_neighbors: list of station which are the nearest to the source location
        source_latitude: source location - latitude
        source_longitude: source location - longitude
    """
    map_with_stations = folium.Map(
        width='70%', height='60%',
        location=[source_latitude, source_longitude],  # 43.7, -79.4
        zoom_start=14)

    for index, station in df_stations.iterrows():
        popup = create_popup_for_station(station, source_latitude, source_longitude)

        latitude, longitude = station['lat'], station['lon']

        # if the station is nearby, set the color to green
        # otherwise set color to blue
        color = 'blue'
        for iteration, nearest_neighbor in enumerate(nearest_neighbors):
            if nearest_neighbor['station_id'] == station['station_id']:
                color = 'green'
                path_visualisation = get_routes_between_source_location_and_station(source_latitude, source_longitude, station, iteration,
                                                                                    len(nearest_neighbors))
                path_visualisation.add_to(map_with_stations)

        folium.Marker(location=[latitude, longitude], popup=popup,
                      icon=folium.Icon(color=color, icon='bicycle', prefix='fa')).add_to(map_with_stations)

    map_with_stations = add_marker_with_source_location(map_with_stations, source_latitude, source_longitude)

    # TODO: add filters to select specific types of markers and routes that are visible
    # map_with_stations.add_child(folium.LayerControl())

    map_as_html = map_with_stations.get_root().render()
    map_as_html = add_styles_to_map(map_as_html)

    # save the map in file
    with open('templates/stations_map.html', "w", encoding='utf-8') as file:
        file.write(map_as_html)
