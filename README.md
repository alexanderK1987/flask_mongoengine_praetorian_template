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


### Edit Configuration Files
Copy `app.config.template` to `app.config`

    cp app.config.template app.config

Modify the files to match your app profile

- app.config
- mongoinit.js

### Generate Keys and Certificates for SSL Access
Run the following commands to generate the necessary key files (`certs\key.pem`, `certs\cert.pem`:

    cd certs
    bash keygen.sh
    cd ..

### Installation for native environment
Run the commands directly to install requirements:

    sudo pip3 install --upgrade pip
    sudo pip3 install -r requirements.txt
    mongo < mongoinit.js
    
Run the commands to start the service:

    export FLASK_APP=mainframe.py; flask run --certs=./certs/cert.pem --key=./certs/key.pem
    

### Installation for virtual enviroment
Run the commands directly to install requirements:

    sudo pip3 install virtualenv
    make install
    mongo < mongoinit.js

Run the commands to start the service:

    make run

## Reference
 - **structural design**
   - [codeburst: JWT authorization in Flask](https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb "codeburst: JWT authorization in Flask")

 - **flask-praetorian**
   - [readthedocs: flask-praetorian](https://flask-praetorian.readthedocs.io/en/latest/ "readthedocs: flask-praetorian")
   - [github: flask-praetorian](https://github.com/dusktreader/flask-praetorian "github")
  
 - **flask-marshmallow**
   - [readthedocs: flask-marshmallow example](https://flask-marshmallow.readthedocs.io/en/latest/ "readthedocs: flask-marshmallow example")
 
