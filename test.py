import unittest
from pgadapter import PgAdapter


class CarMaker:
    def __init__(self, id=None, name='', **kwargs):
        self.id = id
        self.name = name


class TestPgAdapter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dsn = {
            'host': 'localhost',
            'dbname': 'pg_adapter',
            'user': 'root',
            'password': 'root',
            'port': 5432
        }

    def tearDown(self):
        self.__cleanup()

    def test_connect_success(self):
        db = PgAdapter(self.dsn)
        self.assertTrue(db.connected)

    def test_connect_with_context(self):
        with PgAdapter(self.dsn) as db:
            self.assertTrue(db.connected)

    def test_connect_failure_when_dsn_is_null(self):
        with self.assertRaises(Exception):
            db = PgAdapter(None)

    def test_run_commands_when_command_is_empty(self):
        db = PgAdapter(self.dsn)
        with self.assertRaises(ValueError):
            db.execute(None)
            db.execute('')
            db.execute_many(None)
            db.execute_many('')
            db.execute_proc(None)
            db.execute_proc('')
            db.fetch(None)
            db.fetch('')
            db.fetch_one(None)
            db.fetch_one('')
            db.fetch_proc(None)
            db.fetch_proc('')
            db.fetch_one_proc(None)
            db.fetch_one_proc('')

    def test_run_commands_when_command_is_invalid_type(self):
        db = PgAdapter(self.dsn)
        with self.assertRaises(TypeError):
            db.execute(1)
            db.execute_many(1)
            db.execute_proc(1)
            db.fetch(1)
            db.fetch_one(1)
            db.fetch_proc(1)
            db.fetch_one_proc(1)

    def test_execute_success(self):
        query = 'INSERT INTO car_makers (name) VALUES (%s);'
        affected = 0
        with PgAdapter(self.dsn) as tran:
            affected = tran.execute(query, ('toyota',))
        self.assertEqual(affected, 1)

    def test_fetch_success(self):
        self.__setup_car_makers()
        rows = None
        with PgAdapter(self.dsn) as tran:
            rows = tran.fetch('SELECT * FROM car_makers;')
        self.assertEqual(3, len(rows))

    def test_fetch_one(self):
        self.__setup_car_makers()
        row = None
        with PgAdapter(self.dsn) as tran:
            query = 'SELECT * FROM car_makers WHERE name like %s;'
            row = tran.fetch_one(query, ('%nis%',))
        self.assertIsNotNone(row)
        self.assertEqual(row['name'], 'nissan')

    def test_execute_proc(self):
        affected = 0
        with PgAdapter(self.dsn) as tran:
            affected = tran.execute_proc('save_car_maker', (None, 'toyota',))
        self.assertEqual(affected, 1)

    def test_fetch_proc(self):
        self.__setup_car_makers()
        rows = None
        with PgAdapter(self.dsn) as tran:
            rows = tran.fetch_proc('find_car_makers')
        self.assertEqual(3, len(rows))

    def test_fetch_one_proc(self):
        self.__setup_car_makers()
        row = None
        with PgAdapter(self.dsn) as tran:
            row = tran.fetch_one_proc('find_car_maker_by_id', (1,))
        self.assertIsNotNone(row)

    def test_fetch_one_proc_when_mapping_object(self):
        self.__setup_car_makers()
        car_maker = None
        with PgAdapter(self.dsn) as tran:
            row = tran.fetch_one_proc('find_car_maker_by_id', (1,))
            car_maker = CarMaker(**row)
        self.assertIsNotNone(car_maker)
        self.assertEqual('toyota', car_maker.name)

    def __setup_car_makers(self):
        query = 'INSERT INTO car_makers (name) VALUES (%s);'
        makers = [('toyota',), ('nissan',), ('honda',)]
        with PgAdapter(self.dsn) as tran:
            tran.execute_many(query, makers)

    def __cleanup(self):
        with PgAdapter(self.dsn) as tran:
            tables = ['car_makers', 'cars']
            for table in tables:
                query = 'TRUNCATE TABLE {} RESTART IDENTITY;'.format(table)
                tran.execute(query)


if __name__ == '__main__':
    unittest.main()
