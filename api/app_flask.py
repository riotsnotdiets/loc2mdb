from flask import Flask
from flask_cors import CORS, cross_origin

import ujson as json  # https://stackoverflow.com/questions/18517949/what-is-faster-loading-a-pickled-dictionary-object-or-loading-a-json-file-to

import os
from loc2mdb.config import Config
from loc2mdb.apis import constituency_by_wahlkreis_nr, mandates_by_constituency_id
from loc2mdb.geo import coordinates_by_address, wahlkreis_by_coordinates
from loc2mdb.utils import pimp_data_for_return
from pprint import pprint
import git

app = Flask(__name__)
#CORS(app)

# paths
root_dir = os.path.dirname(os.path.dirname(__file__))
json_path = os.path.join(root_dir, "loc2mdb", "data", "")

# load GeoJSON file containing Wahlkreise
jahr_btw = Config.get('JAHR_BTW')
filename_json = Config.get('BUNDESTAGSWAHL')[2021]['WAHLKREISE_GEOJSON_FILE']

with open(f'{json_path}{filename_json}') as f:
    wahlkreise_json = json.load(f)


@app.route("/")
@cross_origin()
def index():
    return {"checking": "basic api works"}


@app.route("/loc2mdb/adresse/<string:adresse>")
#@cross_origin()
def loc2mdb(adresse):
    debug = Config.get('DEBUG')
    ret = coordinates_by_address(adresse)
    if 'error' in ret:
        if debug:
            return {'error_debug':ret['error_msg_debug']}
        else:
            return {'error':'Adresse wahrscheinlich fehlerhaft'}
    else:
        coordinates = ret['coordinates']
        address = ret['address']

    wahlkreis = wahlkreis_by_coordinates(coordinates, wahlkreise_json)
    # print(wahlkreis)
    constituency = constituency_by_wahlkreis_nr(jahr_btw, wahlkreis['WKR_NR'])
    # print(constituency['data'])
    constituency_id = constituency['data'][0]['id']
    # print(constituency_id)
    mandates = mandates_by_constituency_id(constituency_id)
    ret = pimp_data_for_return(address, coordinates, wahlkreis, constituency['data'], mandates)
    return ret


# @app.route('/loc2mdb/update_server', methods=['POST'])
# def webhook():
#     # only allows POST-requests
#     repo = git.Repo('path/to/git_repo')
#     origin = repo.remotes.origin
#     origin.pull()
#     return 'Updated PythonAnywhere successfully'

#if __name__ == '__main__':

    #app.run()
    #adresse = 'Burgsteige 11, 72070 Tübingen'
    #x = loc2mdb(adresse)
    #pprint(x)


