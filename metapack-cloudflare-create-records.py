import CloudFlare
from threading import Thread

import random, string

def main():
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get(params = {'per_page':50})
    for zone in zones:
        zone_name = zone['name']
        zone_id = zone['id']

        print 'Using zone %s ...' % (zone_name)
        #try:
        #    zone_info = cf.zones.post(data={'jump_start':False, 'name': zone_name})
        #except Exception as e:
        #    exit('/zones.post %s - %s' % (zone_name, e))

        dns_records = [
            {'name':'ding', 'type':'A', 'content':'216.58.194.206'},
            {'name':'foo', 'type':'AAAA', 'content':'2001:d8b::1'},
            {'name':'foo', 'type':'A', 'content':'192.168.0.1'},
            {'name':'duh', 'type':'A', 'content':'10.0.0.1', 'ttl':'120'},
            {'name':'shakespeare', 'type':'TXT', 'content':"What's in a name? That which we call a rose by any other name would smell as sweet."}
        ]

        def randomword(length):
            return ''.join(random.choice(string.lowercase) for i in range(length))


        for i in range(1,300):
            randomthing = str(randomword(10))
            r_name = ''.join([randomthing, str(i)])
            print(r_name)
            #dns_records.append({'name': r_name, 'type': 'CNAME', 'content': 'metapack.co'})
            dns_records.append({'name': r_name, 'type': 'A', 'content': '1.2.3.4'})


        print ''


        for i in dns_records:
           # t = Thread(target=createDNSrecords(cf, zone_name, zone_id, i, dns_records))
           # t.daemon = True
           # t.start()
           # t.join()
           createDNSrecords(cf, zone_name, zone_id, i, dns_records)


            # Now read back all the DNS records
        print 'Read back DNS records ...'
        try:
            dns_records = cf.zones.dns_records.get(zone_id)
        except Exception as e:
            exit('/zones.dns_records.get %s - %d %s' % (zone_name, e, e))

        for dns_record in sorted(dns_records, key=lambda v: v['name']):
            print '\t%s %30s %6d %-5s %s ; proxied=%s proxiable=%s' % (
                dns_record['id'],
                dns_record['name'],
                dns_record['ttl'],
                dns_record['type'],
                dns_record['content'],
                dns_record['proxied'],
                dns_record['proxiable']
            )

        print ''


def createDNSrecords(cf_auth, z_name, z_id, record, d_records):
    dns_record = record
    dns_records = d_records
    zone_id = z_id
    zone_name = z_name
    cf = cf_auth

    print 'Create DNS records ...'
    try:
        r = cf.zones.dns_records.post(zone_id, data=dns_record)
    except CloudFlare.CloudFlareAPIError as e:
        exit('/zones.dns_records.post %s %s - %d %s' % (zone_name, dns_record['name'], e, e))
    # Print respose info - they should be the same
    dns_record = r
    print '\t%s %30s %6d %-5s %s ; proxied=%s proxiable=%s' % (
        dns_record['id'],
        dns_record['name'],
        dns_record['ttl'],
        dns_record['type'],
        dns_record['content'],
        dns_record['proxied'],
        dns_record['proxiable']
    )

    dns_record_id = dns_record['id']

    new_dns_record = {
        # Must have type/name/content (even if they don't change)
        'type':dns_record['type'],
        'name':dns_record['name'],
        'content':dns_record['content'],
        # now add new values you want to change
        'proxied':False
    }

    try:
        dns_record = cf.zones.dns_records.put(zone_id, dns_record_id, data=new_dns_record)
    except Exception as e:
        exit('/zones/dns_records.put %d %s - api call failed' % (e, e))



if __name__ == '__main__':
    main()

