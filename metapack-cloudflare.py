import CloudFlare

def main():
    cf = CloudFlare.CloudFlare()
    response = cf.zones.get(params = {'per_page':50})
    zones = response['result']
    for zone in zones:
        zone_name = zone['name']
        zone_id = zone['id']
        response = cf.zones.settings.ipv6.get(zone_id)
        settings_ipv6 = response['result']
        ipv6_status = settings_ipv6['value']
        response = cf.zones.settings.ssl.get(zone_id)
        settings_ssl = response['result']
        ssl_status = settings_ssl['value']
        print zone_id, ssl_status, ipv6_status, zone_name

if __name__ == '__main__':
    main()
