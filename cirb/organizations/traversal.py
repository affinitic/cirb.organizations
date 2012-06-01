# -*- coding: utf-8 -*-
import re
from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.interface import implements
from zope.component import adapts
from five import grok
from z3c.saconfig import Session

from collective.shuttle.traversal import Traverser, TraversableItem
from OFS.interfaces import ITraversable
from Acquisition import Implicit
from .browser.interfaces import ISearch
from .interfaces import IOrganization
from cirb.organizations.content.organization import Organization

def isInt(name):
    m = re.compile(r'^\d+$')
    return bool(m.match(name))


class PloneTraverser(Traverser):
    grok.adapts(ISearch, IHTTPRequest)
    grok.provides(IPublishTraverse)
    

class OrganizationWrapper(Implicit):
    """ Traversable organization 
    """
    implements(IOrganization)
    def __init__(self, organization):
        self._organization = organization

    def __getattr__(self, name):
        try:
            return getattr(self._organization, name)
        except AttributeError:
            return Implicit.__getattr__(self, name)


class OrganizationTraversable(TraversableItem):
    
    def __getitem__(self, key):
        if isInt(key):
            session = Session()
            organization = session.query(Organization).get(int(key))
            if organization is not None:
                wrapper = OrganizationWrapper(organization)
                return  wrapper.__of__(self)
        raise KeyError

@grok.adapter(ISearch, name=u"editorga")
@grok.implementer(ITraversable)
def getOrganizationsTraversable(context):
    return OrganizationTraversable("editorga")

#from z3c.form.field import FieldWidgets 
#import zope.component
#import zope.interface
#import z3c.form
from collective.z3cform.wizard.interfaces import IWizard
#class WizardWidgets(FieldWidgets): #, grok.MultiAdapter):
#
#    zope.component.adapts(
#        IWizard, z3c.form.interfaces.IFormLayer, zope.interface.Interface)
#
#    def __init__(self, form, request, content):
#        print 'WizardWidgets'
#        super(WizardWidgets, self).__init__(form, request, content)
#        self.form = self.form.currentStep
#
from plone.z3cform.traversal import FormWidgetTraversal
from Acquisition import aq_base
class WizardWidgetTraversal(FormWidgetTraversal):
    adapts(IWizard, IBrowserRequest) 

    def _form_traverse(self, form, name):
        import pdb; pdb.set_trace()
        print '_form_traverse'
        if name in form.widgets:
            return form.widgets.get(name)
        # If there are no groups, give up now
        if getattr(aq_base(form), 'groups', None) is None:
            return None
        for group in form.groups:
            if group.widgets and name in group.widgets:
                return group.widgets.get(name)


