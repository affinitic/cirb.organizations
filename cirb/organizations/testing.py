# -*- coding: utf-8 -*-
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting, FunctionalTesting
import cirb.organizations

from sqlalchemy.orm import clear_mappers
from plone.testing import zca

ORGA = PloneWithPackageLayer(
    zcml_filename="configure.zcml",
    zcml_package=cirb.organizations,
    additional_z2_products=(),
    gs_profile_id='cirb.organizations:default',
    name="ORGA")

ORGA_INTEGRATION = IntegrationTesting(
    bases=(ORGA,), name="ORGA_INTEGRATION")


ORGA_FUNCTIONAL = FunctionalTesting(
    bases=(ORGA,), name="ORGA_FUNCTIONAL")


class SQLAlchemyFixture(object):

    def __init__(self, bases=(), name='SQLALCHEMY_FIXTURE'):
        self.__name__ = name
        self.__bases__ = bases
    
    def setUp(self):
        pass

    def tearDown(self):
        clear_mappers()

ORGA_FIXTURE = zca.ZCMLSandbox(bases=(SQLAlchemyFixture(), zca.LAYER_CLEANUP), 
                               filename="configure.zcml",
                               package=cirb.organizations,
                               name="ORGA_FIXTURE")
