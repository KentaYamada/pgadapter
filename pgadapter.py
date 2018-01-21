# -*- coding: utf-8 -*-
import os
# import logging
import psycopg2
import psycopg2.extras

"""
Todos
Logging query.
Clear query when error occuored.
Passing array data and multiple composite type when exec callproc
"""
class PgAdapter():
    """
        PostgreSQL database adapter
        Using PL/PgSQL
        (This module is psycopg2 wrapper)
        See: http://initd.org/psycopg/docs/
    """
    __cashed_query = {}  # Cashing loaded query.

    def __init__(self, dsn, commit=False):
        self.__con = None
        self.__dsn = dsn
        self.__auto_commit = commit
        # logger = logging.getLogger(__name__)

    def __build_cursor(self):
        if self.__con is not None:
            self.__con.close()
        self.__con = psycopg2.connect(**self.__dsn)
        self.__con.autocommit = self.__auto_commit
        return self.__con.cursor(cursor_factory=psycopg2.extras.DictCursor)

    @property
    def auto_commit(self):
        return self.__.auto_commit

    @auto_commit.setter
    def auto_commit(self, value):
        self.__auto_commit = value

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
            saved = True if cur.rowcount >= 0 else False
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

    def switch_db(self, dsn):
        if dsn is None:
            raise ValueError()
        for key in ['host', 'dbname', 'username', 'password']:
            if key not in dsn:
                raise KeyError()
        if self.connected:
            self.__con.close()
            self.__con = None
        print('switch {0} to {1}'.format(self.__dsn['dbname'], dsn['dbname']))
        self.__dsn = dsn

    @classmethod
    def load_sqlfile(cls, filepath):
        if not os.path.isfile(filepath):
            raise FileNotFoundError()

        filename = filepath.split('/')[-1]
        if not filename in PgAdapter.__cashed_query:
            with open(filepath, mode='r') as f:
                query = f.read()
                PgAdapter.__cashed_query[filename] = query

        return PgAdapter.__cashed_query[filename]
