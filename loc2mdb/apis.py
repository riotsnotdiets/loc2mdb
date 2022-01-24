import requests
import re
from loc2mdb.config import Config

def constituency_by_wahlkreis_nr(jahr_btw, wahlkreis_nr):
    # remove everything but numbers and int it
    wahlkreis_nr = int(re.sub("[^0-9]", "", str(wahlkreis_nr)))
    if wahlkreis_nr <= 0:
        return {'error': True, 'error_msg_debug': 'wahlkreis_nr has to be positive'}

    if wahlkreis_nr==100000: # todo: in db ..
        pass
    else:
        parliament_period = Config.get('BUNDESTAGSWAHL')[jahr_btw]['PARLIAMENT_PERIOD']
        url = f'https://www.abgeordnetenwatch.de/api/v2/constituencies?parliament_period={parliament_period}&number={wahlkreis_nr}'
        response = requests.get(url)
        if response.status_code != 200:
            return {'error': True, 'error_msg_debug': 'requesting from abgeordnetenwatch yielded html status code '+str(response.status_code)}
        else:
            # check if request has payload
            data = response.json()
            if data['meta']:
                if data['meta']['status'] == 'ok' and data['meta']['result']['count'] == 1:
                    return data
                else:
                    return {'error': True, 'error_msg_debug': 'payload from abgeordnetenwatch is either empty or the count is too big'}
            else:
                return {'error': True, 'error_msg_debug': 'response from abgeordnetenwatch has no metadata'}


def mandates_by_constituency_id(constituency_id):
    # omitted the testing for now
    url = f'https://www.abgeordnetenwatch.de/api/v2/candidacies-mandates?electoral_data[entity.constituency]={constituency_id}'
    response = requests.get(url)
    if response.status_code != 200:
        return {'error': True, 'error_msg_debug': 'requesting from abgeordnetenwatch/candidacies-mandates yielded html status code ' + str(response.status_code)}
    else:
        # check if request has payload
        data = response.json()
        if data['meta']:
            if data['meta']['status'] == 'ok' and data['meta']['result']['count'] >= 1:
                return data['data']
            else:
                return {'error': True, 'error_msg_debug': 'payload from abgeordnetenwatch/candidacies-mandates is either empty or the count is too big'}
        else:
            return {'error': True, 'error_msg_debug': 'response from abgeordnetenwatch/candidacies-mandates has no metadata'}


if __name__ == '__main__':
    pass