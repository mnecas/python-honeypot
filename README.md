# Python honeypot

## Installation

### SSH

You need the ssh-key which malitous user will see and try to connect to it.
`ssh-keygen -t rsa -f ssh.key`

Get your IP address with command
`ip a`
so you know to which IP you should connect to.

## Run

By default the honepot runs on proper ports in dev version it run with prefix of 80
so for example the ssh honeypot is opened on port 8022.

`python3 main.py --dev`

For server on which you have configured ports you can run:

`python3 main.py`
