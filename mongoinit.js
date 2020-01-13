db=db.getSiblingDB('admin')
db=db.getSiblingDB('memphis')
db.createUser({ user: "memphis_admin", pwd: "memphis", roles: [{role: "readWrite", db: "memphis" }]});

db.createCollection('users');
db.createCOllection('revoked_tokens');
db.createCollection('roles');

db.roles.insert({'role': 'root'});
db.roles.insert({'role': 'admin'});
db.roles.insert({'role': 'operator'});
db.roles.insert({'role': 'guest'});
