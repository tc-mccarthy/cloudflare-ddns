import requests
import json
import sys

version = float(str(sys.version_info[0]) + "." + str(sys.version_info[1]))


if(version < 3.5):
    raise Exception("This script requires Python 3.5+")

with open("./config.json") as config_file:
    config = json.loads(config_file.read())


# Captures IPv4 and IPv6 IPs where applicable
def getIPs():
    a = requests.get("https://api.ipify.org?format=json").json().get("ip")
    aaaa = requests.get("https://api6.ipify.org?format=json").json().get("ip")
    ips = []

    if(a.find(".") > -1):
        ips.append({
            "type": "A",
            "ip": a
        })

    if(aaaa.find(":") > -1):
        ips.append({
            "type": "AAAA",
            "ip": aaaa
        })

    return ips


def commitRecord(ip):
    exists = False

    for c in config["cloudflare"]:
        record = {
            "type": ip["type"],
            "name": c["subdomain"],
            "content": ip["ip"],
            "proxied": c["proxied"]
        }

        list = cf_api("zones/" + c['zone_id'] + "/dns_records", "GET", c)

        for r in list["result"]:
            if (r["type"] == ip["type"] and r["name"] == c["subdomain"]):
                exists = r["id"]

        if(exists == False):
            response = cf_api(
                "zones/" + c['zone_id'] + "/dns_records", "POST", c, {}, record)
        else:
            response = cf_api(
                "zones/" + c['zone_id'] + "/dns_records/" + exists, "PUT", c, {}, record)
        print(response)

    return True


def cf_api(endpoint, method, config, headers={}, data=False):
    headers = {
        "X-Auth-Email": config['account_email'],
        "X-Auth-Key": config['api_key'],
        **headers
    }

    if(data == False):
        response = requests.request(
            method, "https://api.cloudflare.com/client/v4/" + endpoint, headers=headers)
    else:
        response = requests.request(
            method, "https://api.cloudflare.com/client/v4/" + endpoint, headers=headers, json=data)

    return response.json()


for ip in getIPs():
    commitRecord(ip)
