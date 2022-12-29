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
    parser.add_argument("-l", "--log", metavar="LEVEL", default="WARNING",
        help="logging verbosity, e.g. DEBUG, INFO, WARNING (default)", type=str)
    args = parser.parse_args()

    # Update logging level and formatting
    loglevel = getattr(logging, args.log.upper(), None)
    if loglevel is None:
        raise ValueError('Invalid log level: %s' % args.log)
    logging.basicConfig(level=loglevel, format='[%(asctime)s] %(levelname)s: %(message)s')

    # Update once or continuously
    config = json.loads(args.config.read())
    if args.interval is None:
        update_once(config)
    else:
        seconds = args.interval
        update_every(config, seconds)

if __name__ == "__main__":
    main()
