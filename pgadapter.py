# -*- coding: utf-8 -*-
import os
import psycopg2
import psycopg2.extras

"""
Todos
Query logging.
Passing multiple composite type when exec callproc
"""
class PgAdapter():
    """
        PostgreSQL database adapter
        (This module is psycopg2 wrapper)
        See: http://initd.org/psycopg/docs/
    """
    __cashed_query = {} # Cashing loaded query.

    def __init__(self, dsn):
        self.__con = None
        self.__dsn = dsn

    def __build_cursor(self):
        if not self.connected():
            self.__con.close()
        self.__con = psycopg2.connect(self.__dsn)
        self.__con.autocommit = False
        return self.__con.curosor(psycopg2.extras.DictCursor)

    @property
    def auto_commit(self):
        return self.__con.autocommit

    @auto_commit.setter
    def auto_commit(self, value):
        self.__con.autocommit = value

    @property
    def connected(self):
        if self.__con is None:
            return False
        return True if self.__con.closed == 0 else False

    @property
    def current_db(self):
        return self.__dsn

    def query(self, query):
        with self.__build_cursor() as cur:
            cur.execute(query)

    def save(self, query, args):
        saved = False
        with self.__build_cursor() as cur:
            cur.callproc(query, args)
            print(cur.query)
           saved =True if cur.rowcount > 0 else False
        return saved

    def delete(self, query, args):
        return self.save(query, args)

    def find(self, query, args):
        rows = []
        with self.__build_cursor() as cur:
            cur.callproc(query, args)
            print(cur.query)
            rows = cur.fetchall()
        return rows

    def find_one(self, query, args):
        row = ()
        with self.__build_cursor() as cur:
            cur.callproc(query, args)
            print(cur.query)
            row = cur.fetchone()
        return row

    def commit(self):
        if self.__con is not None:
            self.__con.commit()
            self.__con.close()

    def rollback(self):
        if self.__con is not None:
            self.__con.rollback()
            self.__con.close()

    def swich_db(self, dsn):
        if dsn is None:
            raise ValueError()
        if self.connected:
            self.__con.close()
            self.__con = None
        print ('switch {0} to {1}', self.__dsn['dbname'], dsn['dbname'])
        self.__dsn = dsn

    @classmethod
    def load_sqlfile(filepath):
        if not os.path.isfile(filepath):
            raise FileNotFoundError()
        filename = filepath.split('/')[-1]
        if not filename in PgAdapter.__cashed_query:
            with open(filepath, mode='r') as f:
                query = f.read()
                PgAdapter.__cashed_query[filename] = query
        return PgAdapter.__cashed_query[filename]
