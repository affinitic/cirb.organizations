# -*- coding: utf-8 -*-
from Products.LinguaPlone.browser.translate import CreateTranslation


class CreateOrganizationTranslation(CreateTranslation):

    def nextUrl(self, trans):
        return "%s/organizations_form" % trans.absolute_url()
