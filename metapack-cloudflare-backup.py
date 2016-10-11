import CloudFlare
import yaml
import datetime


def connect():
    cf = CloudFlare.CloudFlare()
    return cf


def get_zones(cf):
    zones = cf.zones.get(params = {'per_page':50})
    return zones


def get_records_per_zone(cf, zones):
    for zone in zones:
        zone_name = zone['name']
        zone_id = zone['id']

        print 'Getting DNS records for zone: %s' % zone
        try:
            dns_records = cf.zones.dns_records.get(zone_id)
        except Exception as e:
            exit('/zones.dns_records.get %s - %d %s' % (zone_name, e, e))

        record_list = []
        for dns_record in sorted(dns_records, key=lambda v: v['name']):
            single_record = {dns_record['name']: {
                'id': dns_record['id'],
                'type': dns_record['type'],
                'ttl': dns_record['ttl'],
                'content': dns_record['content'],
                'proxied': dns_record['proxied'],
                'proxiable': dns_record['proxiable']
                }
            }

            record_list.append(single_record)

        sorted_dns_records = {zone_name: record_list}

        return sorted_dns_records


def convert_to_yaml(dns_records):

    filename = '/tmp/cloudflare-backup-data-' + str(datetime.datetime.utcnow()) + '.yml'
    with open(filename, 'w') as outfile:
        yaml.safe_dump(dns_records, outfile, default_flow_style=False)
    #print(yaml.safe_dump(dns_records, default_flow_style=False))

def main():
    cf = connect()
    zones = get_zones(cf)
    sorted_dns_records = get_records_per_zone(cf, zones)
    convert_to_yaml(sorted_dns_records)

if __name__ == '__main__':
    main()

