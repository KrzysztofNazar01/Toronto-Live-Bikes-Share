import folium
from jinja2 import Template
from folium.map import Marker


def create_popup_html(station):
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
    popup = folium.Popup(folium.Html(popup_html_code, script=True, width=350))
    return popup


def add_styles_to_map(html_string):
    style_string = """
        <style>

        .tableTitle{
            font-size:1.8em;
            text-align: center;
            font-weight: bolder;
        }

        .tableHeader{
            text-align: center;
            border: 1px solid;
            font-size: 1.3em;
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
    html_string = html_string.replace("<style>", style_string)

    return html_string


def create_popup_with_target_location(target_latitude, target_longitude):
    popup_html_code = """
    <h2>Target location</h2>
    <br>
        <h3>{}</h3>
    <br>
        <h3>{}</h3>
    """.format(target_latitude, target_longitude)
    popup_target_location = folium.Popup(folium.Html(popup_html_code, script=True, width=350))

    return popup_target_location


def add_marker_with_target_location(map_with_stations, target_latitude, target_longitude):
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
                          input_field_lat.value = value_lat.toFixed(4);

                          var value_lon = point['lng'];
                          var input_field_lon = document.getElementById("lon");
                          input_field_lon.value = value_lon.toFixed(4);

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
    map_with_stations = folium.Map(
        width='65%', height='65%',
        location=[target_latitude, target_longitude],  # 43.7, -79.4
        zoom_start=14)

    for index, station in df_stations.iterrows():
        popup = create_popup_html(station)

        latitude, longitude = station['lat'], station['lon']

        # if the station is nearby, set the color to green
        # otherwise set color to blue
        color = 'blue'
        for nearest_neighbor in nearest_neighbors:
            if nearest_neighbor['station_id'] == station['station_id']:
                color = 'green'

        folium.Marker(location=[latitude, longitude], popup=popup,
                      icon=folium.Icon(color=color, icon='university', prefix='fa')).add_to(map_with_stations)

    map_with_stations = add_marker_with_target_location(map_with_stations, target_latitude, target_longitude)

    map_with_stations.save('templates/folium_map.html')
    # map_with_stations.show_in_browser()
    map_as_html = map_with_stations.get_root().render()
    map_as_html = add_styles_to_map(map_as_html)
    return map_as_html
