# openssl-ca
Playing with root certificate authority and mtls


## Setup

```bash
% cd openssl
% sh 0_init.sh  # initialize the RootCA
% sh 1_client_csr.sh client   # create the client key and certificate signing request
% sh 2_client_auth.sh client  # certify the client
% sh 1_client_csr.sh server   # create the server key and certificate signing request
% sh 2_client_auth.sh server  # certify the server
```

Final keys and certificates are located in:

  * openssl/
    * cert/
      * myCA.key   # root CA key
      * myCA.pem   # root CA self-signed cert
    * mtls-client.domain.com/
      * mtls-client.domain.com.key   # client key
      * mtls-client.domain.com.crt   # client cert
    * mtls-server.domain.com/
      * mtls-server.domain.com.key   # server key
      * mtls-server.domain.com.crt   # server cert

The mutual TLS connection test is written using the Python 'urllib3' library on the client side, and the 'http.server' library on the server side.

The client verifies the specific server that it is talking to separately from the default SSL server validation by supplying a specific hostname to look for independent of the hostname used to set up the connection and that is certified by the trusted root certificate 'myCA.pem'.  This use simulates a use case where the messages are being forwarded over untrusted network load balancers or DNAT gateways to a server at a private IP address so the client's initial connection point will not match the eventual service, but the client still wants to confirm that they are talking to the correct final service without any man in the middle.

The server verifies the specific client by checking the distinguished name of the certificate explicitly after the TLS connection has been negotiated.  The
initial negotiation only verifies that the certificate was signed by the trusted root certificate 'myCA.pem', and that the certificate hasn't expired.   All
additional identity validation must be done by inspecting distinguished name.

### Shell 1
```bash
% sh mtls_server.py
```

### Shell 2
```bash
% sh mtls_client.py
```
