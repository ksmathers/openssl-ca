set -x
. ./settings.sh

# initialize CA directory
rm -rf $CA_ROOT/certs
mkdir $CA_ROOT/certs
cd $CA_ROOT/certs

# generate root key
openssl genrsa -des3 -out myCA.key 2048

# self sign

MSYS_NO_PATHCONV=1 openssl req -x509 -new -nodes -key myCA.key -sha256 -days 1825 -out myCA.pem \
   -subj '/C=US/ST=California/L=Hayward/O=PG&E/OU=DA&I/CN=devops-root.pge.com'

