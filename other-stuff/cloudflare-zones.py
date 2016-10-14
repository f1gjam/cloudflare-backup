#!/usr/bin/env python
"""CloudFlare API code - example"""

import os
import sys
import re

sys.path.insert(0, os.path.abspath('..'))
import CloudFlare

def main():

    # Grab the first argument, if there is one
    try:
        zone_name = sys.argv[1]
        params = {'name':zone_name, 'per_page':1}
    except IndexError:
        params = {'per_page':50}

    cf = CloudFlare.CloudFlare()

    # grab the zone identifier
    try:
        response = cf.zones.get(params = {'per_page':50})
        total_pages = response['result_info']['total_pages']
        page = 0
        zones = []
        while page <= total_pages:
            page += 1
            response = cf.zones.get(params={'page': page, 'per_page': 50})
            zones.extend(response['result'])
    except CloudFlare.CloudFlareAPIError as e:
        exit('/zones %d %s - api call failed' % (e, e))
    except Exception as e:
        exit('/zones.get - %s - api call failed' % (e))


    for zone in sorted(zones, key=lambda v: v['name']):
        zone_name = zone['name']
        zone_id = zone['id']
        if 'email' in zone['owner']:
            zone_owner = zone['owner']['email']
        else:
            zone_owner = '"' + zone['owner']['name'] + '"'
        zone_plan = zone['plan']['name']

        try:
            response = cf.zones.dns_records.get(zone_id)
            dns_records = response['result']
        except CloudFlare.CloudFlareAPIError as e:
            exit('/zones/dns_records %d %s - api call failed' % (e, e))

        print zone_id, zone_name, zone_owner, zone_plan

        prog = re.compile('\.*'+zone_name+'$')
        dns_records = sorted(dns_records, key=lambda v: prog.sub('', v['name']) + '_' + v['type'])
        for dns_record in dns_records:
            r_name = dns_record['name']
            r_type = dns_record['type']
            r_value = dns_record['content']
            r_ttl = dns_record['ttl']
            r_id = dns_record['id']
            print '\t%s %60s %6d %-5s %s' % (r_id, r_name, r_ttl, r_type, r_value)

        print ''

    exit(0)

if __name__ == '__main__':
    main()