#/bin/bash
# generate self-signed certificates with 1-year validation period
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
