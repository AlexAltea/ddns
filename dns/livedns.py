import requests

def set_dns_records(ip, key, entries):
    """
    Update Gandi LiveDNS records of the specified domain.
    """
    base = 'https://api.gandi.net/v5'
    auth = { 'Authorization': 'Apikey ' + key }

    for e in entries:
        record = requests.utils.quote(e.record)
        response = requests.put(f'{base}/livedns/domains/{e.domain}/records/{record}/{e.type}', headers=auth,
            json={ "rrset_values": e.data, "rrset_ttl": 300 })
        if response.status_code != 201:
            raise Exception(f"Could not update {e.type} record {e.record}.{e.domain}.")
