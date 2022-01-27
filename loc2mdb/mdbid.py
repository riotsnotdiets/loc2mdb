from loc2mdb.config import Config

def get_mdbid(person):
    abgwatch_id = person['abgwatch_id']
    vorname = person['vorname']
    nachname = person['nachname']

    # check database
