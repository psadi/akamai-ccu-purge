#!/usr/bin/env python3

from akamai.edgegrid import EdgeGridAuth, EdgeRc
import requests
import json
import argparse
import logging
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
    usage: ccu-purge.py [-h] [-u URL | -c CPCODE] [--host_name HOST_NAME]
                    [--access_token ACCESS_TOKEN] [--client_token CLIENT_TOKEN]
                    [--client_secret CLIENT_SECRET] [-f FILE] [-e ENV] [-p PROXY] [-v]

    optional arguments:
    -h, --help            show this help message and exit
    -u URL, --url URL     URL's to flush, usage: -u url1,url2 (or) --url url1,url2
    -c CPCODE, --cpcode CPCODE
                            CP Codes to flush, usage: -c 0000,1111 (or) --cpcode 0000,1111
    --host_name HOST_NAME
                            Akamai EdgeGrid Hostname, refers .edgerc by default
    --access_token ACCESS_TOKEN
                            Akamai EdgeGrid Access Token
    --client_token CLIENT_TOKEN
                            Akamai EdgeGrid Client Token
    --client_secret CLIENT_SECRET
                            Akamai EdgeGrid Client Secret
    -f FILE, --file FILE  point to a .edgerc
    -e ENV, --env ENV     staging (or) production, default_value='production'
    -p PROXY, --proxy PROXY
                            Use Proxy, usage: -p user:pass@ip:port (or) --proxy user:pass@ip:port
    -v, --verbose         verbose output

"""

start = time.perf_counter()

parser = argparse.ArgumentParser()
purge_content_by = parser.add_mutually_exclusive_group()
purge_content_by.add_argument("-u", "--url", type=str, help="URL's to flush, usage: -u url1,url2 (or) --url url1,url2")
purge_content_by.add_argument("-c", "--cpcode", type=str,
                              help="CP Codes to flush, usage: -c 0000,1111 (or) --cpcode 0000,1111")
parser.add_argument("--host_name", type=str, help="Akamai EdgeGrid Hostname, refers .edgerc by default")
parser.add_argument("--access_token", type=str, help="Akamai EdgeGrid Access Token")
parser.add_argument("--client_token", type=str, help="Akamai EdgeGrid Client Token")
parser.add_argument("--client_secret", type=str, help="Akamai EdgeGrid Client Secret")
parser.add_argument("-f", "--file", type=str, help="point to a .edgerc", default=False)
parser.add_argument("-e", "--env", type=str, help="staging (or) production, default_value='production'",
                    default="production")
parser.add_argument("-p", "--proxy", type=str,
                    help="Use Proxy, usage: -p user:pass@ip:port (or) --proxy user:pass@ip:port", default=False)
parser.add_argument("-v", "--verbose", help="verbose output", action="store_true")
args = parser.parse_args()


def main():

    # noinspection PyGlobalUndefined
    global body
    global request_type

    try:

        if args.verbose:

            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s: %(levelname)s: %(message)s')

        else:

            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s: %(levelname)s: %(message)s')

        if args.url:

            body = json.dumps({'objects': args.url.split(',')})
            request_type = 'url'

            if args.verbose:

                logging.debug(f'Payload Body: {body}')

        elif args.cpcode:

            body = json.dumps({'type': 'cpcode', 'objects': args.cpcode.split(',')})
            request_type = 'cpcode'

            if args.verbose:

                logging.debug(f'Payload Body: {body}')
        else:

            if args.verbose:

                logging.debug("No URL's (or) CP codes to flush")

        headers = {'Content-Type': 'application/json'}

        edge_session = requests.Session()

        if not args.file:

            if args.host_name and args.access_token and args.client_token and args.client_secret != "":

                edge_session.auth = EdgeGridAuth(
                    access_token=args.access_token,
                    client_token=args.client_token,
                    client_secret=args.client_secret
                )

                host_name = args.host_name

            else:

                raise Exception("EdgeGrid Credentials required")

        else:

            edgerc = EdgeRc(f'{args.file}')
            section = 'default'
            host_name = '%s' % edgerc.get(section, 'host')
            edge_session.auth = EdgeGridAuth.from_edgerc(edgerc, section)

        akamai_url = f'https://{host_name}' + f'/ccu/v3/invalidate/{request_type}/{args.env}'

        if args.proxy:

            proxies = {
                'http': f'http://{args.proxy}',
                'https': f'https://{args.proxy}'
            }

            edge_session.proxies = proxies

            if args.verbose:
                logging.debug(f"proxying via : '{args.proxy.split('@')[-1]}'")

        response = edge_session.post(akamai_url, data=body, headers=headers, verify=False)

        if args.verbose:

            logging.debug(f'{json.loads(response.content)}')

            if json.loads(response.content)['httpStatus'] == 201:
                logging.debug(
                    f'PURGE SUCCESSFUL => httpStatus:\'{json.loads(response.content)["httpStatus"]}\','
                    f'estimatedSeconds:\'{json.loads(response.content)["estimatedSeconds"]}\'')

        else:

            logging.info(f'{json.loads(response.content)}')

            if json.loads(response.content)['httpStatus'] == 201:
                logging.info('PURGE SUCCESSFUL')

    except Exception as E:

        logging.basicConfig(filename='purge.log', level=logging.ERROR,
                            format='%(asctime)s: %(levelname)s: %(message)s')
        logging.error(E)

    finish = time.perf_counter()

    logging.info(f'Finished in {round(finish - start, 2)} second(s)')


if __name__ == "__main__":
    main()
