from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl


def certIsValid(cert):
    kv = cert['subjectAltName'][0]
    #print(kv)
    key,val = kv
    if key != 'DNS' or val != 'mtls-client.domain.com':
        return False
    kv = cert['issuer'][5][0]
    key,val = kv
    if key != 'commonName' or val != 'devops-root.pge.com':
        return False
    return True

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        cert = self.connection.getpeercert()
        if cert is None or not certIsValid(cert):
            self.send_response(403)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes('Hello World\n', 'UTF-8'))
        self.wfile.write(bytes('You have requested '+self.path+'\n', 'UTF-8'))
        self.wfile.write(bytes(str(cert), 'UTF-8'))


def certpath(name, ext):
    return f"./openssl/{name}/{name}.{ext}"

def certpair(name):
    return (certpath(name, "crt"), certpath(name, "key"))

httpd = HTTPServer(('localhost', 4443), MyHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile=certpath("mtls-server.domain.com", "key"),
        certfile=certpath("mtls-server.domain.com", "crt"),
        ca_certs="./openssl/certs/myCA.pem", server_side=True, cert_reqs=ssl.CERT_REQUIRED)


print("listening at localhost:4443")
httpd.serve_forever()