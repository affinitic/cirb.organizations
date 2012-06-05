# -*- coding: utf-8 -*-
import unittest2 as unittest
import tempfile

from sqlalchemy import create_engine
from cirb.organizations import ORMBase
from cirb.organizations.browser.organizationsmanage import delete_orga
from cirb.organizations.content.organization import Organization, Association
from zope.component import getGlobalSiteManager

from z3c.saconfig.utility import EngineFactory
from z3c.saconfig.utility import GloballyScopedSession
from z3c.saconfig.interfaces import IEngineFactory, IScopedSession

from z3c.saconfig import Session


class TestOrmbase(unittest.TestCase):

    def setUp(self):
        super(TestOrmbase, self).setUp()
        gsm = getGlobalSiteManager()
        fileno, self.dbFileName = tempfile.mkstemp(suffix='.db')
        dbURI = 'sqlite:///{0}'.format(self.dbFileName)
        dbEngine = create_engine(dbURI)
        ORMBase.metadata.create_all(dbEngine)
        self.engine = EngineFactory(dbURI, echo=False, convert_unicode=False)
        gsm.registerUtility(self.engine, name=u"ftesting", provided=IEngineFactory)
        self.session = GloballyScopedSession(engine=u"ftesting",
                                        twophase=False)
        gsm.registerUtility(self.session, provided=IScopedSession)

    def tearDown(self):
        super(TestOrmbase, self).tearDown()
        #import os
        #os.remove(self.dbFileName)
        gsm = getGlobalSiteManager()
        gsm.unregisterUtility(self.engine, name=u"ftesting", provided=IEngineFactory)
        gsm.unregisterUtility(self.session, provided=IScopedSession)

    def test_add(self):
        session = Session()
        session.add(Organization(name=u"Vin", language="fr"))
        self.assertEqual(len(session.query(Organization).all()), 1)

        orga = session.query(Organization).first()
        self.assertEqual(orga.name, u"Vin")

    def test_translation_and_delete(self):
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

        del_orga_id = orgafr.organization_id
        result = delete_orga(session, del_orga_id)
        self.assertTrue(result)
        self.assertEqual(len(session.query(Organization).all()), 0)

        result = delete_orga(session, del_orga_id)
        self.assertFalse(result)
