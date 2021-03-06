def pimp_data_for_return(address, coordinates, wahlkreis, constituency, mandates):
    ret = {}
    ret['anfrage'] = {}
    ret['anfrage']['longitude'] = coordinates['lon']
    ret['anfrage']['latitude'] = coordinates['lat']
    ret['anfrage']['adresse'] = address
    ret['wahlkreis'] = {}
    ret['wahlkreis']['id_btw'] = wahlkreis['WKR_NR']
    ret['wahlkreis']['id_abgwatch'] = constituency[0]['id']
    ret['wahlkreis']['name'] = constituency[0]['name']
    ret['wahlkreis']['land_id'] = wahlkreis['LAND_NR']
    ret['wahlkreis']['land_name'] = wahlkreis['LAND_NAME']
    ret['wahlkreis']['label'] = constituency[0]['label']
    ret['mdbs'] = []
    for mandate in mandates:
        m = {}
        m['mensch_id_abgwatch'] = mandate['politician']['id']
        m['mensch_name'] = mandate['politician']['label']
        m['mensch_abgwatch_api'] = mandate['politician']['api_url']
        m['mensch_abgwatch_url'] = mandate['politician']['abgeordnetenwatch_url']
        tmp = mandate['electoral_data']['electoral_list']
        if tmp:
            m['einzug_ueber'] = tmp['label']
        else:
            m['einzug_ueber'] = 'unbekannt'
        m['partei_name'] = mandate['fraction_membership'][0]['label']
        m['partei_fraktion'] = mandate['fraction_membership'][0]['fraction']['label']

        ret['mdbs'].append(m)

    return ret
