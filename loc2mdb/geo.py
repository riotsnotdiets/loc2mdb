from shapely.geometry import shape, Point
import re
import requests
from loc2mdb.config import Config
from dotenv import load_dotenv, find_dotenv
import os

# todo: check bbox parameter, maybe reduce to germany
# https://docs.mapbox.com/help/tutorials/local-search-geocoding-api/
# minLon,minLat,maxLon,maxLat
# bbox=-77.083056,38.908611,-76.997778,38.959167

# docs:
# https://docs.mapbox.com/api/search/geocoding/#forward-geocoding


def coordinates_by_address(adresse):
    # cleaning the address and remove ; (needed for mapbox)
    address = " ".join(re.findall("[a-zA-Z\x7f-\xff0-9_.\-,]+", adresse))
    mapbox_types = Config.get('MAPBOX_TYPES')
    mapbox_country = Config.get('MAPBOX_COUNTRY')
    mapbox_language = Config.get('MAPBOX_LANGUAGE')
    #env_path = find_dotenv()  # automatic find, does NOT work on python anywhere
    #load_dotenv(env_path)
    load_dotenv(os.path.join(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0], '.env'))  # works on PA
    mapbox_token = os.getenv('MAPBOX_TOKEN')
    if not mapbox_token:
        return {'error': True, 'error_msg_debug': 'mapbox_token is empty, did you set up the .env?'}

    url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json?country={mapbox_country}&types={mapbox_types}&language={mapbox_language}&access_token={mapbox_token}'

    response = requests.get(url)
    if response.status_code != 200:
        return {'error': True, 'error_msg_debug': 'request from mapbox yielded html status code ' + str(int(response.status_code))}
    else:
        # check if request has payload
        data = response.json()
        if data:
            if data['features']:
                coordinates = {'lon': data['features'][0]['center'][0], 'lat': data['features'][0]['center'][1]}
            else:
                return {'error': True, 'error_msg_debug': 'response from mapbox has no payload/coordinates'}
        else:
            return {'error': True, 'error_msg_debug': 'response from mapbox has no payload/at all'}

    return {'coordinates':coordinates, 'address': address}


def wahlkreis_by_coordinates(coordinates, wahlkreise_json):
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
    longitude = coordinates['lon']
    latitude = coordinates['lat']
    borders = Config.get('BORDERS_GERMANY')

    if not isinstance(longitude, (int, float)) or not isinstance(latitude, (int, float)):
        return {'error': True, 'error_msg_debug':'coordinates to get wahlkreis are not in a numerical form'}
    else:
        if not borders['LON_MIN'] < longitude < borders['LON_MAX']:
            return {'error': True, 'error_msg_debug':'longitude not within borders'}
        if not borders['LAT_MIN'] < latitude < borders['LAT_MAX']:
            return {'error': True, 'error_msg_debug':'latitude not within borders'}

    # todo: check db first
    # construct point based on lon/lat returned by forward geocoder
    point = Point(longitude, latitude)
    # check each polygon to see if it contains the point
    for feature in wahlkreise_json['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature['properties']
