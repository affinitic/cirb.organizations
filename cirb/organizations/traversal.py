# -*- coding: utf-8 -*-
import re
from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.interfaces import IPublishTraverse
#from zope.publisher.interfaces.browser import IBrowserRequest
from zope.interface import implements
#from zope.component import adapts
from five import grok
from z3c.saconfig import Session

from collective.shuttle.traversal import Traverser, TraversableItem
from OFS.interfaces import ITraversable
from Acquisition import Implicit
from .browser.interfaces import ISearch
from .interfaces import IOrganization
from cirb.organizations.content.organization import Organization, Association
from plone.namedfile import file
from plone.namedfile.interfaces import IImageScaleTraversable
from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs
from Products.LinguaPlone.interfaces import ITranslatable


def isInt(name):
    m = re.compile(r'^\d+$')
    return bool(m.match(name))


class PloneTraverser(Traverser):
    grok.adapts(ISearch, IHTTPRequest)
    grok.provides(IPublishTraverse)


class OrganizationWrapper(Implicit):
    """ Traversable organization
    """
    implements(IOrganization, IImageScaleTraversable, ITranslatable)
    security = ClassSecurityInfo()

    def __init__(self, organization):
        self._organization = organization
        initlogo = self._organization.logo
        if not initlogo:
            self._logo = file.NamedImage()
        else:
            self._logo = file.NamedImage(data=initlogo)
        initpicture = self._organization.picture
        if not initpicture:
            self._picture = file.NamedImage()
        else:
            self._picture = file.NamedImage(data=initpicture)

    security.declarePublic('logo')
    @property
    def logo(self):
        """ logo """
        return self._logo

    security.declarePublic('picture')
    @property
    def picture(self):
        """ picture """
        return self._picture

    def __getattr__(self, name):
        try:
            return getattr(self._organization, name)
        except AttributeError:
            return Implicit.__getattr__(self, name)

    def getId(self):
        return str(self._organization.organization_id)

    def Title(self):
        return self._organization.name

    def absolute_url(self):
        return "{0}/{1}".format(self.__parent__.absolute_url(), self.getId())

    def getPhysicalPath(self):
        return self.__parent__.getPhysicalPath() + (self.getId(),)

    def getTranslation(self):
        """ return id of the transalted organization or None """
        import pdb; pdb.set_trace()
        session = Session()
        query1 = session.query(Association).filter(Association.canonical_id == self.organization_id).filter(Association.association_type == 'lang')
        query2 = session.query(Association).filter(Association.translated_id == self.organization_id).filter(Association.association_type == 'lang')
        query = query1.union(query2)
        assoc = query.all()
        if len(assoc) > 1:
            raise IndexError # to many translation for this organization
        if len(assoc) == 0:
            return None

        organization_ids = [assoc[0].canonical_id, assoc[0].translated_id]
        organization_ids.remove(self.organization_id)
        return organization_ids.pop()

from AccessControl.class_init import InitializeClass
InitializeClass(OrganizationWrapper)


class OrganizationTraversable(TraversableItem):
    implements(IHideFromBreadcrumbs)

    def __getitem__(self, key):
        if isInt(key):
            session = Session()
            organization = session.query(Organization).get(int(key))
            if organization is not None:
                wrapper = OrganizationWrapper(organization)
                return  wrapper.__of__(self)
        raise KeyError


@grok.adapter(ISearch, name=u"org")
@grok.implementer(ITraversable)
def getOrganizationsTraversable(context):
    return OrganizationTraversable("org")


#from z3c.form.field import FieldWidgets
#import zope.component
#import zope.interface
#import z3c.form
#from collective.z3cform.wizard.interfaces import IWizard
#class WizardWidgets(FieldWidgets): #, grok.MultiAdapter):
#
#    zope.component.adapts(
#        IWizard, z3c.form.interfaces.IFormLayer, zope.interface.Interface)
#
#    def __init__(self, form, request, content):
#        print 'WizardWidgets'
#        super(WizardWidgets, self).__init__(form, request, content)
#        self.form = self.form.currentStep


#from plone.z3cform.traversal import FormWidgetTraversal
#from Acquisition import aq_base
#
#
#class WizardWidgetTraversal(FormWidgetTraversal):
#    adapts(IWizard, IBrowserRequest)
#
#    def _form_traverse(self, form, name):
#        print '_form_traverse'
#        if name in form.widgets:
#            return form.widgets.get(name)
#        # If there are no groups, give up now
#        if getattr(aq_base(form), 'groups', None) is None:
#            return None
#        for group in form.groups:
#            if group.widgets and name in group.widgets:
#                return group.widgets.get(name)
