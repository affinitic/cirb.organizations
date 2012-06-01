# -*- coding: utf-8 -*-
import unittest2 as unittest
import tempfile
import os
import transaction

from  sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from cirb.organizations import ORMBase
from cirb.organizations.content.organization import Organization
from zope.component import provideUtility

from z3c.saconfig.utility import EngineFactory
from z3c.saconfig.utility import GloballyScopedSession

from z3c.saconfig import Session

class TestOrmbase(unittest.TestCase):

    def setUp(self):
        super(TestOrmbase, self).setUp()
        fileno, self.dbFileName = tempfile.mkstemp(suffix='.db')
        dbURI = 'sqlite:///{0}'.format(self.dbFileName)
        dbEngine = create_engine(dbURI)
        ORMBase.metadata.create_all(dbEngine)

        engine = EngineFactory(dbURI, echo=False, convert_unicode=False)
        provideUtility(engine, name=u"ftesting")

        session = GloballyScopedSession(engine=u"ftesting", twophase=False)
        provideUtility(session)

    def tearDown(self):
        super(TestOrmbase, self).tearDown()
        os.unlink(self.dbFileName)

    def test_add(self):
        session = Session()
        session.add(Organization(name="bsuttor"))
        self.assertEqual(len(session.query(Organization).all()), 1)

