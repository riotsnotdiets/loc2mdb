from shapely.geometry import shape, Point
import ujson as json  # https://stackoverflow.com/questions/18517949/what-is-faster-loading-a-pickled-dictionary-object-or-loading-a-json-file-to
import requests

from pprint import pprint

# constants
# long 5.8 - 15.1  west ost
# lat 55.1 - 47.3 nord-süd
germany_lat_min = 47.3
germany_lat_max = 55.1
germany_lon_min = 5.8
germany_lon_max = 15.1

wahlkreise_available = [2021]
bundestag2parliament_period = {2021:132}  # BTW 2021 gilt als Wahlperiode 132

# load GeoJSON file containing sectors
with open('data/Geometrie_Wahlkreise_20DBT_geo.geojson') as f:
    wahlkreise_json = json.load(f)


def wahlkreis_by_coordinates(jahr_btw,longitude,latitude):
    """
    returns Wahlkreis data based on coordinates

    input:
        jahr_btw: year of the Bundestagswahl, defines which geojson-file has to be used,
                  the Wahlkreise might change every election
        longitude: ...
        latitude: ...

    output:
            {'LAND_NAME': 'Berlin',
            'LAND_NR': '11',
            'WKR_NAME': 'Berlin-Neukölln',
            'WKR_NR': 82}
        or
            {'error': True,
            'error_msg_debug':'...'}
    """
    # check input
    if not isinstance(longitude, (int, float)) or not isinstance(latitude, (int, float)):
        return {'error': True, 'error_msg_debug':'coordinates are not in a numerical form'}
    else:
        if not germany_lon_min < longitude < germany_lon_max:
            return {'error': True, 'error_msg_debug':'longitude not within Germany'}
        if not germany_lat_min < latitude < germany_lat_max:
            return {'error': True, 'error_msg_debug':'latitude not within Germany'}
    if not isinstance(jahr_btw, int):
        return {'error': True, 'error_msg_debug':'jahr_btw has to be integer'}
    else:
        if jahr_btw not in wahlkreise_available:
            return {'error': True, 'error_msg_debug': 'unfortunately there is no data for the selected year'}

    # todo: check db first
    # construct point based on lon/lat returned by forward geocoder
    point = Point(longitude, latitude)
    # check each polygon to see if it contains the point
    for feature in wahlkreise_json['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature['properties']


def constituency_id_by_wahlkreis_nr(jahr_btw, wahlkreis_nr):
    if not isinstance(wahlkreis_nr, int):
        return {'error': True, 'error_msg_debug':'wahlkreis_nr has to be integer'}
    else:
        if wahlkreis_nr <= 0:
            return {'error': True, 'error_msg_debug': 'wahlkreis_nr has to be positive'}
    if not isinstance(jahr_btw, int):
        return {'error': True, 'error_msg_debug':'jahr_btw has to be integer'}
    else:
        if jahr_btw not in wahlkreise_available:
            return {'error': True, 'error_msg_debug': 'unfortunately there is no data for the selected year'}

    if wahlkreis_nr==100000: # todo: in db ..
        pass
    else:
        parliament_period = bundestag2parliament_period[jahr_btw]
        url = f'https://www.abgeordnetenwatch.de/api/v2/constituencies?parliament_period={parliament_period}&number={wahlkreis_nr}'
        response = requests.get(url)
        if response.status_code != 200:
            return {'error': True, 'error_msg_debug': 'requesting from abgeordnetenwatch yielded html status code '+str(response.status_code)}
        else:
            # check if it has payload
            data = response.json()
            if data['meta']:
                if data['meta']['status'] == 'ok' and data['meta']['result']['count'] == 1:
                    constituency_id = response['data'][0]['id']
                else:
                    return {'error': True, 'error_msg_debug': 'payload from abgeordnetenwatch is either empty or the count is too big'}
            else:
                return {'error': True, 'error_msg_debug': 'response from abgeordnetenwatch has no metadata'}

    






x = wahlkreis_by_coordinates(2021, 11.094837, 51.094080)
print(x)
wkr_nr = x['WKR_NR']
print(wkr_nr)
y = constituency_id_by_wahlkreis_nr(2021,wkr_nr)
pprint(y)