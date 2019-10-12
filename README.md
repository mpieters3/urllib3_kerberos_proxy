# urllib3_kerberos_proxy
Monkey patches urllib3 with kerberos authentication for proxies

## How to use
Simple code that monkey patches in kerberos authentication for proxies in urllib3 

Once added, any proxy that starts with http://@: or https://@: will have a kerb authentication token pre-emptively created targeting the proxy address.
Any proxy with username/password still as part of the proxy address will continue to work normally, as will anything else that alread added proxy authenticaiton

## Future items
Finish adding tests, add proxy tests without standing infrastructure
Make it into a custom Pool instead, then we can integrate PAC based proxy selection 

## Disclaimers
This comes with all the major caveats of monkey patches in Python in general. Generally, don't rely on this too heavily for production code, it may end up being brittle,
but until urllib3 gives better ways to insert custom proxy providers, this will be the best way at present. 

Requirements are frozen against the specifically compatible version of urllib3 and requests; it's possible it may not work against other versions

