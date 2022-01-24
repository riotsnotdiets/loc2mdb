from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import ujson as json  # https://stackoverflow.com/questions/18517949/what-is-faster-loading-a-pickled-dictionary-object-or-loading-a-json-file-to

import os
from loc2mdb.config import Config

from loc2mdb.apis import constituency_by_wahlkreis_nr, mandates_by_constituency_id
from loc2mdb.geo import coordinates_by_address, wahlkreis_by_coordinates
from loc2mdb.utils import pimp_data_for_return
from pprint import pprint

import git

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# paths
root_dir = os.path.dirname(os.path.dirname(__file__))
json_path = os.path.join(root_dir, "loc2mdb", "data", "")

# load GeoJSON file containing Wahlkreise
jahr_btw = Config.get('JAHR_BTW')
filename_json = Config.get('BUNDESTAGSWAHL')[2021]['WAHLKREISE_GEOJSON_FILE']

with open(f'{json_path}{filename_json}') as f:
    wahlkreise_json = json.load(f)


@app.get("/")
def index():
    return {"checking": "basic api works"}


@app.get("/loc2mdb")
def loc2mdb(adresse):
    debug = True
    ret = coordinates_by_address(adresse)
    if 'error' in ret and debug:
        print(ret['error_msg_debug'])
        quit()
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


@app.post("/loc2mdb/update_server")
def loc2mdb():
    # only allows POST-requests
    repo = git.Repo('path/to/git_repo')
    origin = repo.remotes.origin
    origin.pull()
    return 'Updated PythonAnywhere successfully'

if __name__ == '__main__':
    pass
    # adresse = 'hobrechtstr. 73, 12047 berlin'
    # x = loc2mdb(adresse)
    # print(x)


