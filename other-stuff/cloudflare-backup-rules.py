import CloudFlare
import yaml
import datetime


def connect():
    cf = CloudFlare.CloudFlare()
    return cf


def get_zones(cf):
    response = cf.zones.get(params={'per_page': 50})
    return response


def get_rules_per_zone(cf, response):
    total_pages = response['result_info']['total_pages']
    page = 0
    zones = []
    sorted_rules = {}

    while page <= total_pages:
        page += 1
        response = response = cf.zones.get(params={'page': page, 'per_page': 50})
        zones.extend(response['result'])

    for zone in zones:
        zone_name = zone['name']
        zone_id = zone['id']

        print 'Getting Rules for zone: %s' % zone_name
        response = cf.zones.pagerules.get(zone_id, params={'per_page': 50})

        pagerules = []
        pagerules.extend(response['result'])
        if len(pagerules) == 0:
            continue
        else:
            ### Commented out until API has pagination ###
            # total_pages = response['result_info']['total_pages']
            # page = 0
            # pagerules = []
            #
            # while page <= total_pages:
            #     page += 1
            #     response = cf.zones.pagerules.get(zone_id, params={'page': page, 'per_page': 50})
            #     pagerules.extend(response['result'])

            rules_list = []
            action_list = []
            for pagerules in sorted(pagerules, key=lambda v: v['targets']):

                for actions in pagerules['actions']:
                    action_list.append(actions)
                single_record = {pagerules['targets'][0]['constraint']['value']: {
                    'id': pagerules['id'],
                    'status': pagerules['status'],
                    'actions': action_list}
                }

                rules_list.append(single_record)
                sorted_rules[zone_name] = rules_list

    return sorted_rules


def convert_to_yaml(sorted_rules):
    for zone_name in sorted_rules:
        # format = "%d-%m-%Y.%H:%M:%S"
        # filename = '/tmp/cloudflare-backup-data-'  + zone_name + '-' + str(datetime.datetime.utcnow().strftime(format)) + '.yml'
        filename = '/tmp/cloudflare-backup-rule-' + zone_name + '.yml'
        with open(filename, 'w') as outfile:
            yaml.safe_dump(sorted_rules[zone_name], outfile, default_flow_style=False)
            print('created file for: ' + zone_name + ' : ' + filename)


def main():
    cf = connect()
    zones = get_zones(cf)
    sorted_rules = get_rules_per_zone(cf, zones)
    convert_to_yaml(sorted_rules)


if __name__ == '__main__':
    main()
