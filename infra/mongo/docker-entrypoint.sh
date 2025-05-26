#!/bin/bash
set -e

# Копируем keyfile в защищённое место и задаём права
cp /mongo-keyfile/mongo-keyfile /tmp/mongo-keyfile
chmod 400 /tmp/mongo-keyfile
chown mongodb:mongodb /tmp/mongo-keyfile

# Запускаем mongod в фоне без auth, чтобы выполнить инициализацию
mongod --replSet rs0 --keyFile /tmp/mongo-keyfile --bind_ip_all --fork --logpath /var/log/mongod.log

# Ждём запуска
sleep 5

# Инициализируем реплику, если ещё не инициализирована
if ! mongosh --quiet --eval "rs.status().ok" | grep -q 1; then
  mongosh --quiet --eval "rs.initiate({_id: 'rs0', members: [{_id: 0, host: 'mongo:27017'}]})"
  sleep 3
fi

# Проверяем, существует ли пользователь
USER_EXISTS=$(mongosh admin --quiet --eval "db.system.users.find({user: '${MONGO_INITDB_ROOT_USERNAME}'}).count()" || echo 0)

if [ "$USER_EXISTS" -eq 0 ]; then
  mongosh admin --quiet --eval "
    db.createUser({
      user: '${MONGO_INITDB_ROOT_USERNAME}',
      pwd: '${MONGO_INITDB_ROOT_PASSWORD}',
      roles: [ { role: 'root', db: 'admin' } ]
    });
  "
fi

# Останавливаем временный mongod
mongod --shutdown

# Запускаем mongod с авторизацией
exec mongod --auth --replSet rs0 --keyFile /tmp/mongo-keyfile --bind_ip_all
