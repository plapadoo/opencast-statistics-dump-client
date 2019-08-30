#!/usr/bin/env python2

"""Fetches a opencast statistics dump in a robust way and saves result as csv file."""

import sys
import csv
import json
from StringIO import StringIO
import requests
import dumpconfig as cfg

URL = 'http://%s:%s/api/statistics/data/export.csv' % (cfg.OPENCAST['host'], cfg.OPENCAST['port'])
AUTH = (cfg.OPENCAST['user'], cfg.OPENCAST['password'])

def get_csv_reader(offset):
    """Return a csv reader object which will iterate over lines in the fetched
    opencast csv statistics dump."""
    data = {
        'offset': offset,
        'filter': '',
        'limit': cfg.APP['limit'],
        'data': json.dumps({
            'parameters': {
                'resourceId': cfg.QUERY['resourceId'],
                'detailLevel': cfg.QUERY['detailLevel'],
                'from': cfg.QUERY['from'],
                'to': cfg.QUERY['to'],
                'dataResolution': cfg.QUERY['dataResolution'],
                },
            'provider': {
                'identifier': cfg.QUERY['identifier'],
                'resourceType': cfg.QUERY['resourceType'],
                },
            }),
        }
    response = requests.post(URL, auth=AUTH, data=data)
    if int(response.status_code) != 200:
        print 'HTTP response was %s.' % (response.status_code)
        print response.text
        if int(response.status_code) == 401:
            print 'This can mean your credentials are incorrect.'
            print 'This can mean the resourceID configured could not be found.'
        sys.exit(1)
    csvstring = json.loads(response.text)['csv']
    return csv.reader(StringIO(csvstring), delimiter=',')

def main():
    """Reads pages from endpoint until no more data is received."""
    reading = True
    offset = 0
    while reading:
        reader = get_csv_reader(offset)
        for row in reader:
            '\t'.join(row)
        print '%d lines read while parsing.' % (reader.line_num)
        if reader.line_num == 0:
            print 'End of dump.'
            reading = False
        else:
            offset = offset + 1

if __name__ == "__main__":
    main()
