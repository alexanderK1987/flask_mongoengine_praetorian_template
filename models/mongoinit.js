db=db.getSiblingDB('admin')
db=db.getSiblingDB('memphis')
db.createUser({ user: "memphis_admin",pwd: "memphis",roles: [ { role: "readWrite", db: "memphis" } ]});

db.createCollection('users');
db.createCollection('power_users');
db.power_users.insert({'email': 'k_101@live.com', 'password': 'k_101@live.com'});

