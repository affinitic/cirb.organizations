# -*- coding: utf-8 -*-
import unittest2 as unittest
from  sqlalchemy import create_engine, Table, Column, Integer, String, MetaData


class TestOracle(unittest.TestCase):

    def setUp(self):
        super(TestOracle, self).setUp()
        self.dbURI = 'oracle://etterbeek_culture:etterbeek_culture753@192.168.13.190/ORASTA01'
        self.engine = create_engine(self.dbURI)
        self.metadata = MetaData()
        
        self.test_table = Table('test_table', self.metadata,
                           Column('test_table_id', Integer, primary_key=True),
                           Column('test_string',  String(255), nullable = False)
                          )

        self.test_table.create(self.engine, checkfirst=True)

    def tearDown(self):
        super(TestOracle, self).tearDown()
        self.test_table.drop(self.engine, checkfirst=False)

    def test_add_without_accent(self):
        insert = self.test_table.insert().values(test_table_id=1, test_string=u'insert without accent')
        conn = self.engine.connect()
        result = conn.execute(insert)
        self.assertTrue(result.is_insert)

        select = self.test_table.select()
        result = conn.execute(select).fetchall()
        self.assertEqual(result.pop(), (1, u'insert without accent'))

    def test_add_with_accent(self):
        insert = self.test_table.insert().values(test_table_id=2, test_string=u'insert with accent : é')
        conn = self.engine.connect()
        result = conn.execute(insert)
        self.assertTrue(result.is_insert)

        select = self.test_table.select()
        result = conn.execute(select).fetchall()
        self.assertEqual(result.pop(), (2, u'insert with accent : é'))
