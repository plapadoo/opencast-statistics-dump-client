#!/usr/bin/env python2

"""Fetches a opencast statistics dump in a robust way and saves result as csv file."""

import sys
import json
import time
import os.path
import datetime
import requests


def get_csv_data(cfg, offset):
    """Return one page of csv data fetched from opencast csv statistics dump."""
    data = {
        'offset': offset,
        'filter': cfg['limit'],
        'limit': cfg['limit'],
        'data': json.dumps({
            'parameters': {
                'resourceId': cfg['resourceId'],
                'detailLevel': cfg['detailLevel'],
                'from': cfg['from'],
                'to': cfg['to'],
                'dataResolution': cfg['dataResolution'],
                },
            'provider': {
                'identifier': cfg['identifier'],
                'resourceType': cfg['resourceType'],
                },
            }),
        }
    response = requests.post(cfg['url'], auth=cfg['auth'], data=data)
    if int(response.status_code) != 200:
        print('HTTP response was %s.' % (response.status_code))
        print(response.text)
        if int(response.status_code) == 401:
            print('This can mean your credentials are incorrect.')
            print('This can mean the resourceID configured could not be found.')
        sys.exit(1)
    return json.loads(response.text)['csv']

def write_page(cfg, page, offset):
    """Write page of csv data to file."""
    path = 'part-%s-limit-%d-offset-%d.csv' % (cfg['fileprefix'], int(cfg['limit']), offset)
    if os.path.exists(path):
        print('File already exists: %s' % (path))
        sys.exit(1)
    print('Writing to %s.' % (path))
    part_file = open(path, "w")
    part_file.write(page)
    part_file.close()

def merge_pages(cfg):
    """Merge all found parts into one file."""
    path = '%s-%s.csv' % (cfg['fileprefix'], datetime.date.today())
    if os.path.exists(path):
        print('File already exists: %s' % (path))
        sys.exit(1)
    complete_file = open(path, "w")
    reading = True
    offset = 0
    while reading:
        path = 'part-%s-limit-%d-offset-%d.csv' % (cfg['fileprefix'],
                                                   int(cfg['limit']), offset)
        if os.path.exists(path):
            print('Found part file: %s' % (path))
            part_file = open(path, "r")
            complete_file.write(part_file.read())
            part_file.close()
            offset = offset + int(cfg['limit'])
        else:
            complete_file.close()
            reading = False
            print('End of merge.')

def main():
    """Reads pages from endpoint until no more data is received."""
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        print('Loading config from file: %s' % (sys.argv[1]))
        with open(sys.argv[1], "r") as read_file:
            cfg = json.load(read_file)
            cfg['url'] = 'http://%s:%s/api/statistics/data/export.csv' % (cfg['host'], cfg['port'])
            cfg['auth'] = (cfg['user'], cfg['password'])
    else:
        print('No config given. Run command as:')
        print('$ python2 %s config.json' % (sys.argv[0]))
        sys.exit(1)

    if int(cfg['limit']) == 0:
        print('Limit 0 is not allowed')
        sys.exit(1)

    reading = True
    offset = 0
    while reading:
        page = get_csv_data(cfg, offset)
        if not page:
            print('End of dump.')
            reading = False
        else:
            write_page(cfg, page, offset)
            offset = offset + int(cfg['limit'])
        time.sleep(float(cfg['sleep']))
    merge_pages(cfg)

if __name__ == "__main__":
    main()
