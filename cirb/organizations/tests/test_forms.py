# -*- coding: utf-8 -*-
import unittest2 as unittest
import tempfile
import transaction

from sqlalchemy import create_engine
from cirb.organizations import ORMBase
#from cirb.organizations.browser.organizationsmanage import delete_orga
from cirb.organizations.content.organization import Organization

from z3c.saconfig.utility import EngineFactory
from z3c.saconfig.utility import GloballyScopedSession
from z3c.saconfig import Session
from zope.interface import alsoProvides

from zope.component import provideUtility
from cirb.organizations.browser.interfaces import ISearch
from cirb.organizations.testing import ORGA_FUNCTIONAL

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing.z2 import Browser


class TestForms(unittest.TestCase):
    layer = ORGA_FUNCTIONAL

    def setUp(self):
        super(TestForms, self).setUp()
        self.portal = self.layer['portal']
        self.app = self.layer['app']

        fileno, self.dbFileName = tempfile.mkstemp(suffix='.db')
        dbURI = 'sqlite:///{0}'.format(self.dbFileName)
        dbEngine = create_engine(dbURI)
        ORMBase.metadata.create_all(dbEngine)
        engine = EngineFactory(dbURI, echo=False, convert_unicode=False)
        provideUtility(engine, name=u"ftesting")
        session = GloballyScopedSession(engine=u"ftesting",
                                        twophase=False)
        provideUtility(session)

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

    def tearDown(self):
        super(TestForms, self).tearDown()
        Session().close_all()

    def test_empty_search(self):
        browser = Browser(self.app)

        #testURL = self.folder_fr.absolute_url()
        testURL = self.portal.absolute_url()
        browser.open(testURL)
        #browser.getControl(name='form.widgets.search').value = u'A'
        #browser.getControl(name='form.buttons.search').click()
        #self.assertTrue('<dl class="portalMessage info">' in browser.contents)
        self.assertTrue('content-core' in browser.contents)


    def test_not_empty_search(self):
        session = Session()
        session.add(Organization(name=u"Vin sur vin", language="fr"))
        session.flush()

        browser = Browser(self.app)
        #testURL = self.folder_fr.absolute_url()
        testURL = self.portal.absolute_url()
        browser.open(testURL)
        #browser.getControl(name='form.widgets.search').value = u'in'
        #browser.getControl(name='form.buttons.search').click()

        #self.assertFalse('<dd>Pas d\'organisme trouv\xc3\xa9.</dd>' in  browser.contents)
        #self.assertTrue('Vin sur vin' in  browser.contents)
