# Cloudflare DDNS
Dynamic DNS service for Cloudflare

## Origin

This script was written for a Raspberry Pi 3 B+ residing on the Spectrum ISP. On run, the script assesses the values for IPv4 and IPv6 and creates/updated DNS records for them in cloudflare.

## Config

Duplicate config-example.json and name it config.json.

Values explained:

```
"api_key": "Your cloudflare API Key",
"account_email": "The email address you use to sign in to cloudflare",
"zone_id": "The ID of the zone that will get the records. From your dashboard click into the zone. Under the overview tab, scroll down and the zone ID is listed in the right rail",
"subdomain": "The full subdomain you want to assign the IP(s) to (e.g. pi.example.com)",
"proxied": false (defaults to false. Make it true if you want CDN/SSL benefits from cloudflare. This usually disables SSH)
```

## Running

This script requires Python 3.5+, which comes available on the latest version of the Raspberry Pi. Download/clone this repo and execute `./sync`, which will set up a virtualenv pull in any dependencies and fire the script.

## Scheduling

This script was written with the intention of cron managing it.
