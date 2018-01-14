# pgadapter
PostgreSQL database adapter  
This module execute PL/PgSQL.  

```

# Connection info.
dsn = {
    'dbname': 'example',
    'host': 'localhost',
    'user': 'taro',
    'password': 'taro'
}

# Init db
db = PgAdapter(dsn)

# Call Defined PL/PgSQL procedure.
try:
    saved = db.save('save_hoge', ('a': 'a', 'b', 'b')
    db.commit()
except psycopg2.DatabaseError as e:
    db.rollback()

```
