. ./settings.sh

if [ "$1" = "client" ] ; then
   SERVER_NAME=$CLIENT_NAME
elif [ "$1" = "server" ] ; then
   SERVER_NAME=$SERVER_NAME
else
   echo "Usage: $0 [client|server]"
   exit 1
fi

# Generate certificate extension for server
cd $CA_ROOT
cat >.$SERVER_NAME.ext <<!
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = $SERVER_NAME
!

# Generate signed certificate
openssl x509 -req -in $SERVER_NAME.csr -CA certs/myCA.pem -CAkey certs/myCA.key \
  -CAcreateserial -out $SERVER_NAME.crt -days 825 -sha256 -extfile .$SERVER_NAME.ext

# Deliver cert to server
cp $SERVER_NAME.crt $CA_ROOT/$SERVER_NAME/$SERVER_NAME.crt

