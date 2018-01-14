# -*- coding: utf-8 -*-

import unittest
from pgadapter import PgAdapter


class TestPgAdapter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        print("Setup start.")
        self.__db = PgAdapter("host=localhost dbname=pgadapter_dev user=kenta password=kenta")

    def tearDown(self):
        print("Teardown start.")
        self.__db.remove("delete_person(%s)", ("test",))
        self.__db.commit()

    def test_save(self):
        saved = self.__db.save("save_person(%s, %s)", ("test", 20))
        if saved:
            self.__db.commit()
        else:
            self.__db.rollback()
        self.assertEqual(True, saved)

    def test_remove(self):
        removed = self.__db.remove("delete_person(%s)", ("test",))
        if removed:
            self.__db.commit()
        else:
            self.__db.rollback()
        self.assertEqual(True, removed)

    def test_find(self):
        persons = self.__db.find("find_persons()")
        print ("Connected:{0}".format(self.__db.connected))
        self.assertNotEqual(0, len(persons))

    def test_find_one(self):
        person = self.__db.find_one("find_persons_by(%s)", ("aaa",))
        print(person)
        self.assertEqual("aaa", person[0])


if __name__ == "__main__":
    unittest.main()
