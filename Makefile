
all: install run

venv/bin/activate:
	if which virtualenv-2.7 >/dev/null; then virtualenv-2.7 venv; else virtualenv venv; fi

run: venv/bin/activate requirements.txt
ifeq ( "","$(wildcard .certs/cert.pem)" ) 
	. venv/bin/activate; FLASK_APP=mainframe.py flask run --cert=adhoc 
else
	. venv/bin/activate; FLASK_APP=mainframe.py flask run --cert=./certs/cert.pem --key=./certs/key.pem 
endif

install: venv/bin/activate requirements.txt
	. venv/bin/activate; pip3 install -r requirements.txt


