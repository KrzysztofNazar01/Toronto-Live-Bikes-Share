import folium
# from flask_app import get_data
from math import radians, cos, sin, asin, sqrt, degrees, atan2




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


def create_map_with_stations(df_stations, nearest_neighbors):
    map_with_stations = folium.Map([43.7, -79.4], zoom_start=11, )

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

    # map_with_stations.show_in_browser()
    map_as_html = map_with_stations.get_root().render()
    map_as_html = add_styles_to_map(map_as_html)
    return map_as_html

# if __name__ == "__main__":
#     df_stations = get_data.get_data()
#     html = create_map_with_stations(df_stations)
