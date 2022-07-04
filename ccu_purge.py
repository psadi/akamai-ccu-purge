#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
ccu-purge.py
a simple python script that purges url/cpcode cache in akamai layer
"""

import json
import argparse
import logging
import requests
import urllib3
from akamai.edgegrid import EdgeGridAuth, EdgeRc

# disable insecure warnings thrown by urllib3 module
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# standard logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s: %(message)s')

def parser():
    """ccu purge argument parser"""
    arg_parser = argparse.ArgumentParser()
    purge_content_by = arg_parser.add_mutually_exclusive_group()
    purge_content_by.add_argument("--url", type=str, metavar='',
                                  help="Url's to flush, ex: --url url1,url2")
    purge_content_by.add_argument("--cpcode", type=str, metavar='',
                                  help="CP code's to flush, ex: --cpcode 00,11")
    arg_parser.add_argument("--host_name", type=str, metavar='',
                            help="Akamai edgegrid Hostname")
    arg_parser.add_argument("--access_token", type=str, metavar='',
                            help="Akamai edge-grid access token")
    arg_parser.add_argument("--client_token", type=str, metavar='',
                            help="Akamai edge-grid client token")
    arg_parser.add_argument("--client_secret", type=str, metavar='',
                            help="Akamai edge-grid client secret")
    arg_parser.add_argument("--edge_file", type=str, metavar='',
                            help="Use .edgerc file", default=False)
    arg_parser.add_argument("--env", type=str.lower, metavar='',
                            help="Environment, staging/production", default="production")
    arg_parser.add_argument("--proxy", type=str, metavar='',
                            help="Proxy, ex: --proxy user:pass@ip:port", default=False)
    return arg_parser.parse_args()

def main():
    """ccu purge main func, Parses arguments, Creates edge session and purges url/cpcode"""
    args = parser()
    body, request_type = None, None

    try:

        if args.url:
            body = json.dumps({'objects': args.url.split(',')})
            request_type = 'url'

        elif args.cpcode:
            body = json.dumps({'type': 'cpcode', 'objects': args.cpcode.split(',')})
            request_type = 'cpcode'

        else:
            raise ValueError("No URL's (or) CP codes to flush")

        logging.info("Payload body: %s", body)
        headers = {'Content-Type': 'application/json'}

        edge_session = requests.Session()

        if args.edge_file:
            edgerc = EdgeRc(args.edge_file)
            section = 'default'
            host_name = edgerc.get(section, 'host')
            edge_session.auth = EdgeGridAuth.from_edgerc(edgerc, section)

        else:
            if (args.host_name and
                args.access_token and
                args.client_token and
                args.client_secret) == "":
                raise ValueError("EdgeGrid Credentials required")

            edge_session.auth = EdgeGridAuth(
                access_token=args.access_token,
                client_token=args.client_token,
                client_secret=args.client_secret
            )

            host_name = args.host_name

        akamai_url = f"https://{host_name}/ccu/v3/invalidate/{request_type}/{args.env}"

        if args.proxy:
            edge_session.proxies = {
                'http': f"http://{args.proxy}",
                'https': f"https://{args.proxy}"
            }

            logging.info("Proxying via : '%s'", args.proxy.split('@')[-1])

        response = edge_session.post(akamai_url, data=body, headers=headers, verify=False)
        content = json.loads(response.content)

        if content['httpStatus'] != 201:
            raise ValueError(content)

        logging.info('Purge Successful')
        logging.info("httpStatus: %s", content['httpStatus'])
        logging.info("estimatedSeconds: %s", content['estimatedSeconds'])

    except ValueError as ex:
        logging.error(ex)

if __name__ == "__main__":
    main()
