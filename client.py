#!/usr/bin/env python2

import dumpconfig as cfg
import requests
import json
import csv
from StringIO import StringIO

URL = 'http://%s:%s/api/statistics/data/export.csv' % (cfg.opencast['host'], cfg.opencast['port'])
AUTH = (cfg.opencast['user'], cfg.opencast['password'])
DATA = {
        'limit': 0,
        'offset': 0,
        'filter': '',
        'data': json.dumps({
            'parameters': {
                'resourceId': cfg.opencast['organization'],
                'detailLevel': 'EPISODE',
                'from': cfg.query['from'],
                'to': cfg.query['to'],
                'dataResolution': 'MONTHLY'
                },
            'provider': {
                'identifier': 'organization.views.sum.influx',
                'resourceType': 'organization',
                },
            }),
        }

r = requests.post(URL, auth=AUTH, data=DATA)
#r.status_code
csvstring = json.loads(r.text)['csv']

f = StringIO(csvstring)
reader = csv.reader(f, delimiter=',')
for row in reader:
    print('\t'.join(row))
