import CloudFlare

def main():
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get(params = {'per_page':50})
    for zone in zones:
        zone_name = zone['name']
        zone_id = zone['id']
        settings_ipv6 = cf.zones.settings.ipv6.get(zone_id)
        ipv6_status = settings_ipv6['value']
        settings_ssl = cf.zones.settings.ssl.get(zone_id)
        ssl_status = settings_ssl['value']
        print zone_id, ssl_status, ipv6_status, zone_name

if __name__ == '__main__':
    main()
