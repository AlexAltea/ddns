#!/usr/bin/env python3

import argparse
import json
import logging
import time

import routers
import dns

def update_once(config):
    try:
        ip = routers.get_public_ip(**config['router'])
        for provider in config['dns']:
            dns.set_dns_records(ip, **provider)
    except BaseException as error:
        print('An exception occurred: {}'.format(error))

def update_every(config, seconds):
    last = None
    while True:
        # Check current public IP address from router
        try:
            ip = routers.get_public_ip(**config['router'])
        except BaseException as error:
            print('An exception occurred: {}'.format(error))

        # If unchanged, sleep and repeat
        if last == ip:
            time.sleep(seconds)
            continue

        # Otherwise update all DNS providers, sleep and repeat
        logging.info(f"Update IP address from {last} to {ip} across all records")
        last = ip
        for provider in config['dns']:
            try:
                dns.set_dns_records(ip, **provider)
            except BaseException as error:
                print('An exception occurred: {}'.format(error))
        time.sleep(seconds)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interval", metavar="<seconds>",
        help="continuously monitor/update IP changes every N seconds", type=float)
    parser.add_argument("-c", "--config", metavar="<path/to/config.json>",
        help="configuration file", required=True, type=argparse.FileType('r'))
    args = parser.parse_args()

    # Update once or continuously
    config = json.loads(args.config.read())
    if args.interval is None:
        update_once(config)
    else:
        seconds = args.interval
        update_every(config, seconds)

if __name__ == "__main__":
    main()
