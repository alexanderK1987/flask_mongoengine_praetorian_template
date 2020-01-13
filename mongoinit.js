db=db.getSiblingDB('admin')
db=db.getSiblingDB('memphis')
db.createUser({ user: "memphis_admin",pwd: "memphis",roles: [{role: "readWrite", db: "memphis" }]});

db.createCollection('users');

