# -*- coding: utf-8 -*-
import unittest2 as unittest
import tempfile
import transaction

from sqlalchemy import create_engine
from cirb.organizations import ORMBase
#from cirb.organizations.browser.organizationsmanage import delete_orga
from cirb.organizations.content.organization import Organization
from zope.component import getGlobalSiteManager

from z3c.saconfig.utility import EngineFactory
from z3c.saconfig.utility import GloballyScopedSession
from z3c.saconfig.interfaces import IEngineFactory, IScopedSession
from z3c.saconfig import Session
from zope.interface import alsoProvides

from cirb.organizations.browser.interfaces import ISearch
from cirb.organizations.testing import ORGA_FUNCTIONAL

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing.z2 import Browser


class TestOrmbase(unittest.TestCase):
    layer = ORGA_FUNCTIONAL

    def setUp(self):
        super(TestOrmbase, self).setUp()
        gsm = getGlobalSiteManager()
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        fileno, self.dbFileName = tempfile.mkstemp(suffix='.db')
        dbURI = 'sqlite:///{0}'.format(self.dbFileName)
        dbEngine = create_engine(dbURI)
        ORMBase.metadata.create_all(dbEngine)
        self.engine = EngineFactory(dbURI, echo=False, convert_unicode=False)
        gsm.registerUtility(self.engine, name=u"ftesting", provided=IEngineFactory)
        self.session = GloballyScopedSession(engine=u"ftesting",
                                        twophase=False)
        gsm.registerUtility(self.session, provided=IScopedSession)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'folder_fr', title=u"Folder",
                                  langague="fr")
        self.folder_fr = self.portal["folder_fr"]
        alsoProvides(self.folder_fr, ISearch)

        self.portal.invokeFactory('Folder', 'folder_nl', title=u"Folder",
                                  langague="nl")
        self.folder_nl = self.portal["folder_nl"]
        alsoProvides(self.folder_nl, ISearch)
        #folder_nl.addTranslationReference(folder_fr)
        transaction.commit()

    def tearDown(self):
        super(TestOrmbase, self).tearDown()
        #import os
        #os.remove(self.dbFileName)
        #os.unlink(self.dbFileName)
        gsm = getGlobalSiteManager()
        gsm.unregisterUtility(self.engine, name=u"ftesting", provided=IEngineFactory)
        gsm.unregisterUtility(self.session, provided=IScopedSession)

    def test_empty_search(self):
        browser = Browser(self.app)

        testURL = self.folder_fr.absolute_url()
        browser.open(testURL)
        browser.getControl(name='form.widgets.search').value = u'A'
        browser.getControl(name='form.buttons.search').click()
        self.assertTrue('<dd>Pas d\'organisme trouv\xc3\xa9.</dd>' in  browser.contents)

    def test_not_empty_search(self):
        #session = Session()
        #session.add(Organization(name=u"Vin", language="fr"))
        #transaction.commit()

        browser = Browser(self.app)
        testURL = self.folder_fr.absolute_url()
        browser.open(testURL)
        browser.getControl(name='form.widgets.search').value = u'in'
        #browser.getControl(name='form.buttons.search').click()

        #self.assertFalse('<dd>Pas d\'organisme trouv\xc3\xa9.</dd>' in  browser.contents)
        #self.assertTrue('Organisme du vin de liege' in  browser.contents)
