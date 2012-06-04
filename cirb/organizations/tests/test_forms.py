# -*- coding: utf-8 -*-
import unittest2 as unittest
import tempfile

from sqlalchemy import create_engine
from cirb.organizations import ORMBase
#from cirb.organizations.browser.organizationsmanage import delete_orga
#from cirb.organizations.content.organization import Organization, Association
from zope.component import provideUtility

from z3c.saconfig.utility import EngineFactory
from z3c.saconfig.utility import GloballyScopedSession
from z3c.saconfig.interfaces import IEngineFactory

from cirb.organizations.testing import ORGA_FUNCTIONAL


class TestOrmbase(unittest.TestCase):
    layer = ORGA_FUNCTIONAL

    def setUp(self):
        super(TestOrmbase, self).setUp()
        self.portal = self.layer['portal']
        fileno, self.dbFileName = tempfile.mkstemp(suffix='.db')
        dbURI = 'sqlite:///{0}'.format(self.dbFileName)
        dbEngine = create_engine(dbURI)
        ORMBase.metadata.create_all(dbEngine)

        engine = EngineFactory(dbURI, echo=False, convert_unicode=False)
        provideUtility(engine, name=u"gscetterbeek", provides=IEngineFactory)

        session = GloballyScopedSession(engine=u"gscetterbeek",
                                        twophase=False,
                                        provides=IEngineFactory)
        provideUtility(session)

    def tearDown(self):
        super(TestOrmbase, self).tearDown()
        #os.unlink(self.dbFileName)

    def test_add(self):
        #layout = "organizations_form"
        self.portal.REQUEST["form.widgets.name"] = ['Test organizsation name']
        self.portal.REQUEST["form-buttons-continue"] = u"continue"

        #import pdb; pdb.set_trace()
        #view = self.portal.restrictedTraverse(layout)
        # Call update() for form
        #view.process_form()
        #print view.form.render()
        #errors = view.errors
        #self.assertEqual(len(errors), 0, "Got errors:" + str(errors))
