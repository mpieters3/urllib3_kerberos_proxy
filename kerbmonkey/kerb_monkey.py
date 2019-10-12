import urllib3
import os

from requests_kerberos import HTTPKerberosAuth

try:
    import botocore
except ImportError:
    botocore = None
    pass

try:
    import requests
except ImportError:
    requests = None
    pass

def patch_urllib3_kerb():
    '''
    This will patch urllib3 to inject a kerberos authentication header into the proxies.
    If the auth details are left blank (IE: https://:@proxy_url/) then it will use kerberos

    it does this at the ConnectionPool level, so will work for most libraries we can't directly
    integrate with
    '''

    old_proxy_from_url = urllib3.poolmanager.proxy_from_url

    def proxy_from_url(proxy_url, **kw):
        if(not proxy_url.startswith("http://:@") and not proxy_url.startswith("https://:@")):
            return old_proxy_from_url(proxy_url, **kw)

        if(not 'proxy_headers' in kw):
            kw['proxy_headers'] = {}

        proxy_headers = kw['proxy_headers']
        if(not 'Proxy-Authorization' in proxy_headers):
            if isinstance(proxy_url, urllib3.connectionpool.HTTPConnectionPool):
                proxy_url = '%s://%s:%i' % (proxy_url.scheme, proxy_url.host,
                                            proxy_url.port)
            proxy = urllib3.util.url.parse_url(proxy_url)            
            kerb_auth = HTTPKerberosAuth(force_preemptive=True)
            auth_header = kerb_auth.generate_request_header(None, proxy.host, True)
            proxy_headers['Proxy-Authorization'] = auth_header
        return urllib3.poolmanager.ProxyManager(proxy_url=proxy_url, **kw)

    urllib3.poolmanager.proxy_from_url = proxy_from_url

    ##Because requests statically import proxy_from_url, we're going to do this here
    if(requests):
        requests.adapters.proxy_from_url = proxy_from_url

    ##Because boto statically import proxy_from_url, we're going to do this here
    if(botocore):
        botocore.httpsession.proxy_from_url = proxy_from_url

def _create_auth_header(proxy_host, proxy_headers):
    if(not 'Proxy-Authorization' in proxy_headers):
        kerb_auth = HTTPKerberosAuth(force_preemptive=True)
        auth_header = kerb_auth.generate_request_header(None, proxy_host, True)
        proxy_headers['Proxy-Authorization'] = auth_header