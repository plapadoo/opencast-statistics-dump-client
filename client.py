#!/usr/bin/env python2

"""Fetches a opencast statistics dump in a robust way and saves result as csv file."""

import sys
import json
import os.path
import requests
import dumpconfig as cfg

URL = 'http://%s:%s/api/statistics/data/export.csv' % (cfg.OPENCAST['host'], cfg.OPENCAST['port'])
AUTH = (cfg.OPENCAST['user'], cfg.OPENCAST['password'])

def get_csv_data(offset):
    """Return one page of csv data fetched from opencast csv statistics dump."""
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
    return json.loads(response.text)['csv']

def write_page(page, offset):
    """Write page of csv data to file."""
    path = 'part-%s-limit-%d-offset-%d.csv' % (cfg.APP['fileprefix'], int(cfg.APP['limit']), offset)
    os.path.exists
    print 'Writing to %s.' % (path)
    part_file = open(path, "w")
    part_file.write(page)
    part_file.close()

def main():
    """Reads pages from endpoint until no more data is received."""
    reading = True
    offset = 0
    while reading:
        page = get_csv_data(offset)
        if not page:
            print 'End of dump.'
            reading = False
        else:
            write_page(page, offset)
            offset = offset + 1

if __name__ == "__main__":
    main()
