# -*- coding: utf-8 -*-
import unittest
import psycopg2
from pgadapter import PgAdapter


TEST_CASES = {
    'error_message': 'Failed {0}, no. {1}. except: {2}, result: {3}',
    'test_save_ok': [
        {'no': 1, 'expect': True, 'data': ('test', 100)}
    ],
    'test_save_invalid_value': [
        {'no': 1, 'data': (None, 100)},
        {'no': 2, 'data': ('test', None)},
        {'no': 3, 'data': (None, None)},
        {'no': 4, 'data': (100, 'test')}
    ]
}

SETUP_DATA = [
    {'name': 'Taro', 'age': 26},
    {'name': 'Taro', 'age': 24},
    {'name': 'Hanako', 'age': 24},
    {'name': 'Tom', 'age': 22}
]

DSN = {
    'host': '192.168.56.101',
    'dbname': 'pgadapter_db',
    'user': 'kenta',
    'password': 'kenta'
}


class TestPgAdapter(unittest.TestCase):
    def setUp(self):
        self.db = PgAdapter(DSN)
        for d in SETUP_DATA:
            args = (d['name'], d['age'])
            self.db.save('save_person', args)
            self.db.commit()

    def tearDown(self):
        self.db = PgAdapter(DSN, commit=True)
        self.db.query('DELETE FROM  persons;')

    def test_save_ok(self):
        data = TEST_CASES['test_save_ok'][0]
        saved = self.db.save('save_person', data['data'])
        self.db.commit()
        self.assertEqual(saved, data['expect'])

    def test_save_invalid_value(self):
        data = TEST_CASES['test_save_invalid_value']
        with self.assertRaises(psycopg2.IntegrityError):
            for d in data:
                self.db.save('save_person', d['data'])
        self.db.rollback()

    def test_delete_ok(self):
        deleted = self.db.delete('delete_person', ('test',))
        self.db.commit()
        self.assertEqual(deleted, True)

    def test_find_ok(self):
        self.db.auto_commit = True
        rows = self.db.find('find_persons', ('Taro',))
        self.assertEqual(2, len(rows))

    def test_find_one_ok(self):
        self.db.auto_commit = True
        row = self.db.find_one('find_persons', ('Hanako',))
        self.assertEqual('Hanako', row['name'])

    def test_invalid_connection(self):
        dsn = DSN.copy()
        dsn['host'] = 'invalid host'
        self.db = PgAdapter(dsn)
        with self.assertRaises(psycopg2.OperationalError):
            self.db.query('SELECT * FROM persons;')
            self.db.save('save_person', ('test', 100))
            self.db.delete('save_person', ('test',))
        self.db.rollback()

    def test_invalid_dsn(self):
        with self.assertRaises(ValueError):
            self.db.switch_db(None)
        with self.assertRaises(KeyError):
            self.db.switch_db({})

    def test_load_invalid_filepath(self):
        filepath = 'notfound'
        with self.assertRaises(FileNotFoundError):
            PgAdapter.load_sqlfile(filepath)


if __name__ == '__main__':
    unittest.main()
