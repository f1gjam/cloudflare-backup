# Metapack Cloudflare

This Python script allows Metapack to configure a single or multiple records and backup the configuration.
It will also allow the restoration of a backup.

Master Branch = Current stable release
Develop Branch = Latest development snapshot

*NOTE: This script uses the [python-cloudflare](https://github.com/f1gjam/python-cloudflare) - This is the modified version of the original.
[The original repo](https://github.com/cloudflare/python-cloudflare)
A simple change was made to the original to ensure a full response was returned.

## How to use ##

Create a credentials file under: ~/.cloudflare/cloudflare.cfg (This should be under the user who will execute the script)

`python <path to script>/cloudflare-backup.py`

The script will read ALL dns zones and extract all records to a file under /tmp/cloud