#Cloudflare-Backup

This Python script allows you to backup your Cloudflare configuration. This includes all Zones, DNS records and associated rules.


**NOTE:** This script uses the [python-cloudflare](https://github.com/cloudflare/python-cloudflare).

##Installation
### Pre-requisites
Ensure that the following items are installed on your machine which will execute this script. Also ensure you have permissions to clone the repositories.

`git`
`python 2.7`
`pip`

Clone the following python repositories 

`git clone git@github.com:f1gjam/cloudflare-backup.git`

Now you can install the cloudflare python module

`pip install cloudflare`

Create the Cloudflare configuration directory and file (This should be under the user who will execute the script)
**DO NOT CHANGE THE LOCATION OF THE FILE**

`mkdir ~/.cloudflare/`
`nano -w ~/.cloudflare/cloudflare.cfg` - you can use whichever editor you like

**Example contents for the file below**
```
[CloudFlare]
email = my_cloudflare_email@somewhere.com
token = jkhwj24h9812h12jkdwuykk2108721321asdl
certtoken = v1.0-...
```

##How to use

`python <path to script>/cloudflare_backup.py`

The script will read ALL dns zones and associated records and rules and create two file

`/tmp/cloudflare-backup-dns-records-data-<domain>.yml`
`/tmp/cloudflare-backup-rule-<domain>.yml`


##Known Issues

The API call for extracting rules is currently in BETA. There is no pagination available (although the cloudflare
documentation states the response contains this information). Contacted Cloudflare and they are looking into the issue.
