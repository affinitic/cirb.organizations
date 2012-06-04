# -*- coding: utf-8 -*-
import unittest2 as unittest
import tempfile

from sqlalchemy import create_engine
from cirb.organizations import ORMBase
from cirb.organizations.browser.organizationsmanage import delete_orga
from cirb.organizations.content.organization import Organization, Association
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
        #os.unlink(self.dbFileName)

    def test_add(self):
        session = Session()
        session.add(Organization(name=u"Vin", language="fr"))
        self.assertEqual(len(session.query(Organization).all()), 1)

        orga = session.query(Organization).first()
        self.assertEqual(orga.name, u"Vin")

    def test_translation(self):
        session = Session()
        session.add(Organization(name=u"Wijn", language="nl"))
        self.assertEqual(len(session.query(Organization).all()), 2)

        assoc = Association(association_type="lang")
        [orgafr, organl] = [orga for orga in session.query(Organization).all()]
        assoc.translated_id = organl.organization_id
        assoc.canonical_id = orgafr.organization_id
        session.add(assoc)
        self.assertEqual(orgafr, organl.get_translation())
        self.assertEqual(orgafr.get_translation().name, u"Wijn")
        self.assertEqual(organl.get_translation().name, u"Vin")

    def test_zdelete(self):
        session = Session()
        del_orga_id = session.query(Organization).all()[0].organization_id
        result = delete_orga(session, del_orga_id)
        self.assertTrue(result)
        self.assertEqual(len(session.query(Organization).all()), 0)

        result = delete_orga(session, del_orga_id)
        self.assertFalse(result)
