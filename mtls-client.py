import requests
import ssl
import urllib3


def certpath(name, ext):
    return f"c:/Users/Kevin/git/openssl-ca/openssl/{name}/{name}.{ext}"

def certpair(name):
    return (certpath(name, "crt"), certpath(name, "key"))

def match_hostname(cert, hostname):
    print("cert=",cert)
    print("host=",hostname)
    return True

def get(host, path):
    pool = urllib3.HTTPSConnectionPool(
        "localhost",
        port=4443,
        assert_hostname=host,
        cert_file=certpath("mtls-client.domain.com", "crt"),
        key_file=certpath("mtls-client.domain.com", "key"),
        cert_reqs="CERT_REQUIRED",
        ca_certs="./openssl/certs/myCA.pem"
    )
    return pool.request("GET", path)


r = get("mtls-server.domain.com", "/")
print(r.status)
print(r.reason)
print(r.data.decode('utf-8'))
#requests.get("https://localhost:4443", cert=certpair("mtls-client.domain.com"), verify="./openssl/certs/myCA.pem", )
