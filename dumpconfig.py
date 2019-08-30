"""1. Jaehrliche Statistik einer Serie mit Zahlen pro Episode (Brueckenkurs)"""

APP = {
    'limit': '1',
    'sleep': '1',
    'fileprefix': 'fall1',
    }
OPENCAST = {
    'host': 'localhost',
    'port': '8080',
    'user': 'admin',
    'password': 'opencast',
    'organization': 'mh_default_org',
    }
QUERY = {
    'resourceId': '1c760d9a-26ce-48ad-b93e-cdda15ac5a5d',
    'detailLevel': 'EPISODE',
    'from': '2010-01-01T00:00:00.000Z',
    'to': '2020-01-01T00:00:00.000Z',
    'dataResolution': 'YEARLY',
    'identifier': 'series.views.sum.influx',
    'resourceType': 'series',
    }
