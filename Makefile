
all: install run

venv/bin/activate:
	if which virtualenv-2.7 >/dev/null; then virtualenv-2.7 venv; else virtualenv venv; fi
run: venv/bin/activate requirements.txt
	. venv/bin/activate; FLASK_APP=mainframe.py flask run --cert=adhoc 
install: venv/bin/activate requirements.txt
	. venv/bin/activate; pip3 install -r requirements.txt


