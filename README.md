AKAMAI-CCU-PURGE
================

A Simple Script to Flush URL's (or) CP Code's in Akamai

#### INSTALL DEPENDENCIES
        python version: v3.6 (or) higher, tested with Python 3.8.5

        Install the dependencies from requirements.txt

        pip3 install -r requirements.txt

#### FLUSH URL's
        python3 ccu-purge.py --host_name <host_name> --access_token <access_token> --client_token <client_token> --client_secret <client_secret> -u url1,url2

        python3 ccu-purge.py -f </path/to/.edgerc> -u url1,url2

#### FLUSH CP-CODE's
	python3 ccu-purge.py --host_name <host_name> --access_token <access_token> --client_token <client_token> --client_secret <client_secret> -c cpcode1,cpcode2

        python3 ccu-purge.py -f </path/to/.edgerc> -c cpcode1,cpcode2

#### ARGS
        usage: ccu-purge.py [-h] [-u URL | -c CPCODE] [--host_name HOST_NAME] [--access_token ACCESS_TOKEN] [--client_token CLIENT_TOKEN]
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

#### KNOWN ISSUES
        1. System must meet Requirements.txt specs for the script to work properly.

        2. Failed to establish a new connection: '[Errno -2] Name or service not known' => This can be resolved by passing -p, --proxy input, format: user:pass@ip:port

        3. Caused by ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response' => Validate if the proxy credentails (or) EdgeAuth credentials are valid.

        look at usage for more info

#### REFERENCES

        https://developer.akamai.com/api/core_features/fast_purge/v3.html

        https://control.akamai.com/apps/api-definitions/#/

        https://developer.akamai.com/legacy/introduction/Conf_Client.html
