# -*- coding: utf-8 -*-
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting, FunctionalTesting
import cirb.organizations

ORGA = PloneWithPackageLayer(
        zcml_filename="configure.zcml",
        zcml_package=cirb.ORGA,
        additional_z2_products=(),
        gs_profile_id='cirb.organizations:default',
        name="ORGA")

ORGA_INTEGRATION = IntegrationTesting(
        bases=(ORGA,), name="ORGA_INTEGRATION")


ORGA_FUNCTIONAL = FunctionalTesting(
        bases=(ORGA,), name="ORGA_FUNCTIONAL")
