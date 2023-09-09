. ./settings.sh
if [ "$1" = "client" ] ; then
   SERVER_NAME=$CLIENT_NAME
elif [ "$1" = "server" ] ; then
   SERVER_NAME=$SERVER_NAME
else
   echo "Usage: $0 [client|server]"
   exit 1
fi

# Init client 
rm -rf $CA_ROOT/$SERVER_NAME
mkdir $CA_ROOT/$SERVER_NAME
cd $CA_ROOT/$SERVER_NAME

# generate client private key
openssl genrsa -out $SERVER_NAME.key 2048

# generate CSR
MSYS_NO_PATHCONV=1 openssl req -new -key $SERVER_NAME.key -out $SERVER_NAME.csr \
  -subj "/C=US/ST=California/L=Hayward/O=PG&E/OU=DA&I/CN=$SERVER_NAME"

# send CSR to CA
cp $SERVER_NAME.csr ..

