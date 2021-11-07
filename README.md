# Python honeypot

## Installation
## Byl jsem zde Alex
### SSH

You need the ssh-key which malitous user will see and try to connect to it.
`ssh-keygen -t rsa -f ~/.ssh/honeypot.key`

Get your IP address with command
`ip a`
so you know to which IP you should connect to.

### HTTPS

`openssl req -x509 -nodes -subj '/CN=localhost'  -newkey rsa:4096 -keyout /etc/pki/tls/private/key.pem -out /etc/pki/tls/certs/cert.pem -days 365`

## Run

By default the honepot runs on proper ports in dev version it run with prefix of 80
so for example the ssh honeypot is opened on port 8022.

`python3 honeypot.py --prod`

For server on which you have configured ports you can run:

`python3 honeypot.py`

## Dev testing

### HTTPS Test

`curl -d "param1=value1" -X POST https://localhost:8043 -k`

### HTTP Test

`curl -d "param1=value1" -X POST http://localhost:8080`

### SSH/SFTP Test

`ssh root@localhost -p 8022`

`sftp -P 8022 root@localhost`
