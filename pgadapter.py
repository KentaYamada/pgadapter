import psycopg2
import psycopg2.extras


class PgAdapter:
    """
        This module is psycopg2 wrapper
        See psycopg2 (http://initd.org/psycopg/docs/)
    """
    def __init__(self, dsn):
        self.__con = None
        self.__cur = None
        self.__dsn = dsn
        self.connect()

    def __enter__(self):
        if self.connected:
            self.disconnect()
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        self.disconnect()
        return False

    @property
    def connected(self):
        if self.__con is None:
            return False
        return self.__con.closed == 0

    def connect(self):
        self.__con = psycopg2.connect(
            **self.__dsn,
            cursor_factory=psycopg2.extras.DictCursor
        )
        self.__cur = self.__con.cursor()

    def disconnect(self):
        self.__con.close()
        self.__cur = None
        self.__con = None

    def execute(self, command, args=None):
        if not command:
            raise ValueError()
        if not isinstance(command, str):
            raise TypeError()
        self.__cur.execute(command, args)
        return self.__cur.rowcount

    def execute_many(self, command, var_list):
        if not command:
            raise ValueError()
        if not isinstance(var_list, (set, list)):
            raise TypeError()
        self.__cur.executemany(command, var_list)
        return self.__cur.rowcount

    def execute_proc(self, command, args=None):
        if not command:
            raise ValueError()
        if not isinstance(command, str):
            raise TypeError()
        self.__cur.callproc(command, args)
        return self.__cur.rowcount

    def fetch(self, command, args=None):
        if not command:
            raise ValueError()
        if not isinstance(command, str):
            raise TypeError()
        self.__cur.execute(command, args)
        return self.__cur.fetchall()

    def fetch_one(self, command, args):
        if not command:
            raise ValueError()
        if not isinstance(command, str):
            raise TypeError()
        self.__cur.execute(command, args)
        return self.__cur.fetchone()

    def fetch_proc(self, command, args=None):
        if not command:
            raise ValueError()
        if not isinstance(command, str):
            raise TypeError()
        self.__cur.callproc(command, args)
        return self.__cur.fetchall()

    def fetch_one_proc(self, command, args):
        if not command:
            raise ValueError()
        if not isinstance(command, str):
            raise TypeError()
        self.__cur.callproc(command, args)
        return self.__cur.fetchone()

    def commit(self):
        if self.__con is not None:
            self.__con.commit()
            self.__con.close()

    def rollback(self):
        if self.__con is not None:
            self.__con.rollback()
            self.__con.close()
