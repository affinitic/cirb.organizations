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
from cirb.organizations.content.organization import Organization, Category, Address, Contact, InCharge, AdditionalInformation, Association
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
        container = self.aq_parent.aq_parent
        translatedContainer = container.getTranslation(self.language)
        return "/".join((translatedContainer.absolute_url(),
                         'org',
                         self.getId()))

    def getPhysicalPath(self):
        return self.__parent__.getPhysicalPath() + (self.getId(),)

    # ITranslatable

    def Language(self):
        return self._organization.language

    def _wrapOrganization(self, organization):
        parent = self.aq_parent
        return OrganizationWrapper(organization).__of__(parent)

    def getTranslation(self, language):
        """ return id of the transalted organization or None """
        translation = self._organization.get_translation()
        if translation.language == language:
            return self._wrapOrganization(translation)

    def getTranslations(self, include_canonical=True, review_state=True,
                          _is_canonical=None):
        """Returns a dict of {lang : [object, wf_state]}.
          If review_state is False, returns a dict of {lang : object}
        """
        trans = self._organization.get_translation()
        if trans:
            translation = self._wrapOrganization(trans)
            if review_state:
                return {translation.language: [translation, None]}
            else:
                return {translation.language: translation}
        return {self.Language: self}

    def hasTranslation(self, language):
        return bool(self._organization.get_translation())

    def addTranslation(self, language):
        organization = Organization(address=Address(), category=Category(),
                                    person_incharge=InCharge(), person_contact=Contact(),
                                    additionalinfo=AdditionalInformation())
        organization.name = self._organization.name
        organization.language = language
        session = Session()
        session.add(organization)
        session.flush()
        canonical_id = self.getId()
        assoc = Association(association_type="lang")
        assoc.translated_id = organization.organization_id
        assoc.canonical_id = canonical_id
        session.add(assoc)
        session.flush()


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


from plone.z3cform.traversal import FormWidgetTraversal, WrapperWidgetTraversal
from Acquisition import aq_base
from cirb.organizations.browser.organizationsform import WizardView

class WizardWidgetTraversal(FormWidgetTraversal):
    adapts(WizardView, IBrowserRequest)

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

class WizardWrapperWidgetTraversal(WrapperFormWidgetTraversal):
    adapts(OrganizationWrapper, IBrowserRequest)

    def _prepareForm(self):
        form = self.context.form_instance
        z2.switch_on(self.context, request_layer=self.context.request_layer)
        return form


    def _form_traverse(self, form, name):
        import pdb; pdb.set_trace()
        super(WizardWrapperWidgetTraversal, self)._form_traverse(self, form, name)
        #form = self.context.form_instance
        #z2.switch_on(self.context, request_layer=self.context.request_layer)
        #return form

