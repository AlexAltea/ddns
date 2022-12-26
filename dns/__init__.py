import collections

from . import livedns

def set_dns_records(ip, type, key, domains):
    # Generate list of entries to update
    entries = []
    EntryType = collections.namedtuple('Entry', ['domain', 'record', 'type', 'data'])
    for domain in domains:
        for record in domain['records']:
            data = record.get('data', [])
            entry = EntryType(domain['name'], record['name'], record['type'], data + [ip])
            entries.append(entry)

    if type == "livedns":
        return livedns.set_dns_records(ip, key, entries)
    else:
        raise Exception("Unknown provider")
