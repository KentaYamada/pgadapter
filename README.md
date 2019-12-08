# pgadapter
PostgreSQL database adapter  
This module execute PL/PgSQL.  

### DB Server
```
Start
cd ./docker
> docker-compose -d

Stop
cd ./docker
> docker-compose stop
```

```

# Connection info.
dsn = {
    'dbname': 'example',
    'host': 'localhost',
    'user': 'ham',
    'password': 'spam'
}

# Init db
db = PgAdapter(dsn)

# Insert or Update(Call stored procedure)
try:
    saved = db.save('save_hoge', ('a': 'a', 'b', 'b'))
    db.commit()
except psycopg2.DatabaseError as e:
    db.rollback()

# Fetch(Call stored procedure)
db.auto_commit = True  # If single query, set auto commit.
rows = db.find('find_hoges')  # fetch all data.
rows = db.find('find_hoges_by', ('fuga', 11111))  # fetch with condition.
row = db.find_one('find_hoge', ('id', 12345)) # fetch row.

```
