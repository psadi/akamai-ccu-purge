AKAMAI-CCU-PURGE
================

A Simple Script to Flush URL's (or) CP Code's in Akamai

#### INSTALL
---
Download the latest download file from release page

`pip3 install --user akamai-ccu-purge-<version>.tar.gz`

#### FLUSH URL's
---
`ccu_purge --host_name <host_name> --access_token <access_token> --client_token <client_token> --client_secret <client_secret> -u url1,url2`


#### FLUSH CP-CODE's
---
`ccu_purge --host_name <host_name> --access_token <access_token> --client_token <client_token> --client_secret <client_secret> -c cpcode1,cpcode2`

#### KNOWN ISSUES
---
1. `Failed to establish a new connection: '[Errno -2] Name or service not known'` - This can be resolved by passing -p, --proxy input, format: user:pass@ip:port
1. `Caused by ProxyError('Cannot connect to proxy.', RemoteDisconnected('Remote end closed connection without response'` - Validate if the proxy credentails (or) EdgeAuth credentials are valid.

#### REFERENCES
---
* https://developer.akamai.com/api/core_features/fast_purge/v3.html
* https://control.akamai.com/apps/api-definitions/#/
* https://developer.akamai.com/legacy/introduction/Conf_Client.html
