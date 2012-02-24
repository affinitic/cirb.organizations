# -*- coding: utf-8 -*-
import re
from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.interfaces import IPublishTraverse
from five import grok
from z3c.saconfig import Session

from collective.shuttle.traversal import Traverser

from .browser.interfaces import ISearch
from cirb.organizations.content.organization import Organization


def isInt(name):
    m = re.compile(r'^\d+$')
    return bool(m.match(name))


class OrganizationTraverser(Traverser):
    grok.adapts(ISearch, IHTTPRequest)
    grok.provides(IPublishTraverse)

    def publishTraverse(self, request, name):
        if isInt(name):
            session = Session()
            organization = session.query(Organization).get(int(name))
            if organization is not None:
                organization.__parent__ = self.context
                return organization
                #XXX we need
                #return organization.__of__(self.context)
        return super(OrganizationTraverser, self).publishTraverse(request, name)
