db=db.getSiblingDB('admin')
db=db.getSiblingDB('<YOUR_APP_NAME>')
db.createUser({ user: "<YOUR_APP_NAME>_admin", pwd: "<YOUR_APP_NAME>", roles: [{role: "readWrite", db: "<YOUR_APP_NAME>" }]});

db.createCollection('users');
db.createCOllection('revoked_tokens');
db.createCollection('roles');

db.roles.insert({'role': 'root'});
db.roles.insert({'role': 'admin'});
db.roles.insert({'role': 'operator'});
db.roles.insert({'role': 'guest'});
