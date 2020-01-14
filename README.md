## Flask Praetorian JWT Template
This is a RESTful service template based on Python3, flask, flask-praetorian, flask-mongoengine.
- Provide basic authentication functions, including:
 - https service
 - user registration
 - email validation
 - login/logout
 - role-based permission handling
 

- Provide admin function, including:
 - user activation/deactivation
 - user deletion

## Base Package Requirement
This template requires Python3 development environments. Virtual environment is recommended but not required.

### Installation for native environment
Run the command directly:

    sudo pip3 install --upgrade pip; sudo pip3 install -r requirements.txt
    bash certs/keygen.sh
    export FLASK_APP=mainframe.py; flask run --certs=./certs/cert.pem --key=./certs/key.pem

### Installation for virtual enviroment
    sudo pip3 install virtualenv
    make install
    make run

## Reference
 - **structural design**
  - [codeburst: JWT authorization in Flask](http://https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb "codeburst: JWT authorization in Flask")

 - **flask-praetorian**
  - [readthedocs: flask-praetorian](https://flask-praetorian.readthedocs.io/en/latest/ "readthedocs: flask-praetorian")
  - [github: flask-praetorian](http://https://github.com/dusktreader/flask-praetorian "github")
  
 - **flask-marshmallow**
  - [readthedocs: flask-marshmallow example](http://https://flask-marshmallow.readthedocs.io/en/latest/ "readthedocs: flask-marshmallow example")
 
